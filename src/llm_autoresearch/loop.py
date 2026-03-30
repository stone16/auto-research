from __future__ import annotations

import logging
import signal
import threading
from pathlib import Path
from types import FrameType

from .evaluator import evaluate_answers
from .feedback import append_judge_feedback, load_feedback_context, save_judge_review
from .git import commit_iteration, ensure_clean_state, init_branch, reset_last_commit
from .judge import safe_run_judge, should_invoke_judge
from .models import IterationOutcome, ResearchResponse, StopConditions
from .providers import BaseProvider, ProviderTask, create_provider
from .run_files import (
    append_results_row,
    load_recent_results,
    load_run_context,
    utc_now_iso,
    write_json,
    write_text,
)

logger = logging.getLogger(__name__)


def build_iteration_instructions() -> str:
    return (
        "You are producing one research iteration. Improve the single mutable knowledge base, "
        "answer every benchmark item directly, and cite source IDs. Output JSON only."
    )


def _decision(
    candidate_score: float,
    previous_best: float,
    candidate_chars: int,
    current_chars: int,
    minimum_improvement: float,
    allow_tie_if_shorter: bool,
) -> str:
    if candidate_score > previous_best + minimum_improvement:
        return "keep"
    if previous_best == 0.0 and candidate_score > 0.0:
        return "keep"
    if (
        allow_tie_if_shorter
        and candidate_score >= previous_best
        and candidate_chars < current_chars
    ):
        return "keep"
    return "discard"


def run_iteration(
    run_dir: Path,
    provider_kind: str | None = None,
    command: str | None = None,
    judge_provider: BaseProvider | None = None,
) -> IterationOutcome:
    context = load_run_context(run_dir)
    resolved_kind = provider_kind or context.config.provider.kind
    resolved_command = command if command is not None else context.config.provider.command
    provider = create_provider(resolved_kind, command=resolved_command)
    previous_best = context.state.best_score

    iteration = context.state.iteration + 1
    history = load_recent_results(context.paths, limit=5)
    feedback = load_feedback_context(context.paths)
    task = ProviderTask(
        task_type="research_iteration",
        instructions=build_iteration_instructions(),
        payload={
            "topic": context.config.topic,
            "topic_markdown": context.topic_markdown,
            "program": context.program_markdown,
            "knowledge_base_markdown": context.knowledge_base_markdown,
            "benchmark": [item.to_dict() for item in context.benchmark],
            "sources": [source.to_dict() for source in context.sources],
            "history": history,
            "state": context.state.to_dict(),
            "judge_feedback": feedback["judge_feedback"],
            "human_feedback": feedback["human_feedback"],
        },
    )

    response = ResearchResponse.from_dict(provider.invoke(task))
    evaluation = evaluate_answers(context.benchmark, response.benchmark_answers)
    candidate_chars = len(response.knowledge_base_markdown)
    current_chars = context.state.current_knowledge_chars or len(context.knowledge_base_markdown)

    # Determine the score used for the keep/discard decision.
    # If a judge_provider is supplied and the deterministic gate passes,
    # invoke the judge and use its overall_score instead.
    decision_score = evaluation.total_score
    judge_report = None
    priority_dimension = ""

    if judge_provider is not None and context.goal_state.dimensions:
        gate_threshold = context.config.evaluation.gate_threshold
        if should_invoke_judge(evaluation.total_score, gate_threshold):
            judge_report = safe_run_judge(
                goal_state=context.goal_state,
                candidate_kb=response.knowledge_base_markdown,
                benchmark_answers=response.benchmark_answers,
                judge_provider=judge_provider,
            )
            if judge_report is not None:
                decision_score = judge_report.overall_score
                priority_dimension = judge_report.priority_dimension

    status = _decision(
        candidate_score=decision_score,
        previous_best=context.state.best_score,
        candidate_chars=candidate_chars,
        current_chars=current_chars,
        minimum_improvement=context.config.evaluation.minimum_improvement,
        allow_tie_if_shorter=context.config.evaluation.allow_tie_if_shorter,
    )

    artifact_dir = context.paths.artifacts_dir / f"iteration-{iteration:04d}"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    write_json(artifact_dir / "task.json", task.to_dict())
    write_json(artifact_dir / "candidate.json", response.to_dict())
    write_text(artifact_dir / "candidate_knowledge_base.md", response.knowledge_base_markdown)
    write_json(artifact_dir / "evaluation.json", evaluation.to_dict())

    # Save judge feedback and review if judge was invoked
    if judge_report is not None:
        append_judge_feedback(context.paths, judge_report, iteration)
        save_judge_review(artifact_dir, judge_report)

    if status == "keep":
        write_text(context.paths.knowledge_path, response.knowledge_base_markdown)
        context.state.best_score = decision_score
        context.state.best_iteration = iteration
        context.state.current_knowledge_chars = candidate_chars
        context.state.last_kept_experiment = response.experiment_title

    context.state.iteration = iteration
    write_json(context.paths.state_path, context.state.to_dict())

    append_results_row(
        context.paths,
        {
            "iteration": iteration,
            "timestamp": utc_now_iso(),
            "score": f"{decision_score:.4f}",
            "prev_best": f"{previous_best:.4f}",
            "status": status,
            "knowledge_chars": candidate_chars,
            "provider": resolved_kind,
            "experiment": response.experiment_title,
            "change_summary": response.change_summary,
        },
    )

    # -- Git integration: commit the iteration, then reset on discard --
    commit_sha = commit_iteration(
        iteration=iteration,
        experiment_title=response.experiment_title,
        cwd=run_dir,
    )
    if status == "discard" and commit_sha is not None:
        reset_ok = reset_last_commit(cwd=run_dir)
        if not reset_ok:
            logger.error(
                "Failed to reset commit %s for discarded iteration %d",
                commit_sha,
                iteration,
            )

    # Extract dimension scores from judge report for use by stop conditions
    dimension_scores: dict[str, float] | None = None
    if judge_report is not None:
        dimension_scores = judge_report.dimension_scores

    return IterationOutcome(
        iteration=iteration,
        status=status,
        candidate_score=decision_score,
        previous_best=previous_best,
        knowledge_chars=candidate_chars,
        artifact_dir=str(artifact_dir),
        experiment_title=response.experiment_title,
        change_summary=response.change_summary,
        priority_dimension=priority_dimension,
        dimension_scores=dimension_scores,
    )


def install_sigint_handler(
    shutdown_event: threading.Event,
) -> signal.Handlers:
    """Create and return a SIGINT handler that sets the shutdown event.

    The returned callable can also be used directly for testing without
    actually registering it as a signal handler.

    Args:
        shutdown_event: Event to set when SIGINT is received.

    Returns:
        The handler callable (compatible with signal.signal).
    """

    def _handler(signum: int, frame: FrameType | None) -> None:
        logger.info("SIGINT received, finishing current iteration before exiting...")
        shutdown_event.set()

    return _handler


_MAX_CONSECUTIVE_CRASHES = 3


def run_loop(
    run_dir: Path,
    producer_kind: str,
    judge_kind: str,
    tag: str,
    stop_conditions: StopConditions | None = None,
    shutdown_event: threading.Event | None = None,
) -> list[IterationOutcome]:
    """Run iterations continuously with the full produce-evaluate-judge-feedback cycle.

    Creates an ``autoresearch/<tag>`` branch on start, then loops calling
    ``run_iteration()`` until the stop conditions are met.

    Args:
        run_dir: Path to the initialized run directory.
        producer_kind: Provider kind for the producer (mock, codex, claude).
        judge_kind: Provider kind for the judge (mock, codex, claude).
        tag: Tag for the autoresearch branch name.
        stop_conditions: When to stop iterating. None means unlimited.
        shutdown_event: Optional threading.Event for graceful SIGINT shutdown.
            If not provided, one is created and a SIGINT handler is installed.

    Returns:
        List of IterationOutcome for each completed iteration.
    """
    if stop_conditions is None:
        stop_conditions = StopConditions()

    # Ensure clean state and create branch BEFORE installing signal handler
    # so early failures don't leak the custom handler into the caller
    ensure_clean_state(cwd=run_dir)
    init_branch(tag, cwd=run_dir)

    # Setup SIGINT handling (after setup that can raise)
    own_event = shutdown_event is None
    if shutdown_event is None:
        shutdown_event = threading.Event()
    original_handler = None
    if own_event:
        original_handler = signal.getsignal(signal.SIGINT)
        handler = install_sigint_handler(shutdown_event)
        signal.signal(signal.SIGINT, handler)

    # Create the judge provider
    judge_provider = create_provider(judge_kind)

    outcomes: list[IterationOutcome] = []
    iteration_count = 0
    consecutive_discards = 0
    consecutive_crashes = 0

    try:
        while True:
            # Check shutdown event (SIGINT)
            if shutdown_event.is_set():
                logger.info("Shutdown requested, exiting loop.")
                break

            # Check max_iterations stop condition
            if stop_conditions.max_iterations is not None:
                if iteration_count >= stop_conditions.max_iterations:
                    break

            # Check max_consecutive_discard stop condition
            if stop_conditions.max_consecutive_discard is not None:
                if consecutive_discards >= stop_conditions.max_consecutive_discard:
                    logger.info(
                        "Stopping: %d consecutive discards reached limit of %d.",
                        consecutive_discards,
                        stop_conditions.max_consecutive_discard,
                    )
                    break

            try:
                outcome = run_iteration(
                    run_dir=run_dir,
                    provider_kind=producer_kind,
                    judge_provider=judge_provider,
                )
            except Exception:
                consecutive_crashes += 1
                logger.warning(
                    "Iteration crashed (%d consecutive). Skipping.",
                    consecutive_crashes,
                    exc_info=True,
                )
                if consecutive_crashes >= _MAX_CONSECUTIVE_CRASHES:
                    logger.error(
                        "Halting: %d consecutive crashes detected. "
                        "Check provider configuration and logs for diagnostics.",
                        consecutive_crashes,
                    )
                    break
                # Crashes don't consume the iteration budget
                continue

            # Successful iteration: reset crash counter
            consecutive_crashes = 0

            outcomes.append(outcome)
            iteration_count += 1

            # Track consecutive discards
            if outcome.status == "discard":
                consecutive_discards += 1
            else:
                consecutive_discards = 0

            # Print one-line summary
            dim_info = (
                f"dimension: {outcome.priority_dimension}"
                if outcome.priority_dimension
                else "dimension: n/a"
            )
            print(
                f"iteration {outcome.iteration} | "
                f"score {outcome.candidate_score:.2f} | "
                f"status {outcome.status} | "
                f"{dim_info}"
            )

            # Check dimension_threshold stop condition (after iteration)
            if stop_conditions.dimension_threshold is not None:
                if outcome.dimension_scores is not None and outcome.dimension_scores:
                    threshold = stop_conditions.dimension_threshold
                    if all(
                        score >= threshold
                        for score in outcome.dimension_scores.values()
                    ):
                        logger.info(
                            "Stopping: all dimension scores above threshold %.2f.",
                            threshold,
                        )
                        break
    finally:
        # Restore original signal handler if we installed one
        if own_event and original_handler is not None:
            signal.signal(signal.SIGINT, original_handler)

    return outcomes
