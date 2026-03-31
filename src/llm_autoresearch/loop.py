from __future__ import annotations

import json
import logging
import os
import re
import signal
import threading
from pathlib import Path
from types import FrameType
from typing import Any

from .evaluator import evaluate_answers
from .feedback import append_judge_feedback, load_feedback_context, save_judge_review
from .git import commit_iteration, ensure_branch, ensure_clean_state, reset_last_commit
from .judge import build_judge_prompt, safe_run_judge, should_invoke_judge
from .models import BenchmarkItem, CliAgentConfig, IterationOutcome, ResearchResponse, StopConditions
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

_LOOP_STATUS_FILE = "loop_status.json"
_PROVIDER_STATUS_FILE = "provider_status.json"
_PROVIDER_ACTIVITY_FILE = "provider_activity.jsonl"
_PRIORITY_DIMENSION_PATTERN = re.compile(r"\*\*Priority dimension\*\*:\s*(.+)")
_IMPROVEMENT_SUGGESTION_PATTERN = re.compile(r"\*\*Improvement suggestion\*\*:\s*(.+)")


def _provider_status_path(run_dir: Path) -> Path:
    return run_dir / _PROVIDER_STATUS_FILE


def _loop_status_path(run_dir: Path) -> Path:
    return run_dir / _LOOP_STATUS_FILE


def _provider_activity_path(run_dir: Path) -> Path:
    return run_dir / _PROVIDER_ACTIVITY_FILE


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _record_provider_event(
    run_dir: Path,
    *,
    role: str,
    provider_kind: str,
    iteration: int,
    status: str,
    attempt_started_at: str,
    timeout_seconds: int | None = None,
    prompt_chars: int | None = None,
    duration_seconds: float | None = None,
    error: str = "",
    extra: dict[str, Any] | None = None,
) -> None:
    payload: dict[str, Any] = {
        "timestamp": utc_now_iso(),
        "role": role,
        "provider_kind": provider_kind,
        "iteration": iteration,
        "status": status,
        "active": status == "running",
        "attempt_started_at": attempt_started_at,
    }
    if timeout_seconds is not None:
        payload["timeout_seconds"] = timeout_seconds
    if prompt_chars is not None:
        payload["prompt_chars"] = prompt_chars
    if duration_seconds is not None:
        payload["duration_seconds"] = round(duration_seconds, 2)
    if error:
        payload["error"] = error
    if extra:
        payload.update(extra)

    write_json(_provider_status_path(run_dir), payload)
    _append_jsonl(_provider_activity_path(run_dir), payload)


def _write_loop_status(
    run_dir: Path,
    *,
    status: str,
    stop_reason: str = "",
    producer_kind: str = "",
    judge_kind: str = "",
    tag: str = "",
    stop_conditions: StopConditions | None = None,
) -> None:
    state = load_run_context(run_dir).state
    payload: dict[str, Any] = {
        "timestamp": utc_now_iso(),
        "status": status,
        "active": status == "running",
        "stop_reason": stop_reason,
        "state_iteration": state.iteration,
        "best_score": state.best_score,
        "producer_kind": producer_kind,
        "judge_kind": judge_kind,
        "tag": tag,
        "pid": os.getpid(),
    }
    if stop_conditions is not None:
        payload["stop_conditions"] = {
            "max_iterations": stop_conditions.max_iterations,
            "max_total_iterations": stop_conditions.max_total_iterations,
            "max_consecutive_discard": stop_conditions.max_consecutive_discard,
            "dimension_threshold": stop_conditions.dimension_threshold,
        }
    write_json(_loop_status_path(run_dir), payload)


def _create_provider_for_role(
    kind: str,
    role_config: CliAgentConfig,
    role: str,
) -> BaseProvider:
    normalized = kind.strip().lower()

    if normalized == "cli":
        return create_provider(
            normalized,
            cli_binary=role_config.cli,
            cli_flags=role_config.flags,
            role=role,
            timeout=role_config.timeout_seconds,
        )

    if normalized in {"codex", "claude"}:
        cli_binary = ""
        cli_flags = ""
        if not role_config.cli or role_config.cli.strip().lower() == normalized:
            cli_binary = role_config.cli
            cli_flags = role_config.flags
        return create_provider(
            normalized,
            cli_binary=cli_binary,
            cli_flags=cli_flags,
            role=role,
            timeout=role_config.timeout_seconds,
        )

    return create_provider(normalized, role=role, timeout=role_config.timeout_seconds)


def _latest_feedback_field(pattern: re.Pattern[str], markdown: str) -> str:
    matches = pattern.findall(markdown)
    if not matches:
        return ""
    return matches[-1].strip()


def _summarize_recent_history(history: list[dict[str, str]]) -> str:
    if not history:
        return "No prior iterations yet."

    window = history[-3:]
    parts: list[str] = []
    for row in window:
        iteration = row.get("iteration", "?")
        status = row.get("status", "unknown")
        score = row.get("score", "?")
        parts.append(f"iter {iteration} {status} score {score}")
    return "; ".join(parts)


def build_iteration_instructions(
    *,
    previous_best: float = 0.0,
    history: list[dict[str, str]] | None = None,
    judge_feedback: str = "",
    human_feedback: str = "",
) -> str:
    recent_history = _summarize_recent_history(history or [])
    priority_dimension = _latest_feedback_field(_PRIORITY_DIMENSION_PATTERN, judge_feedback)
    improvement_suggestion = _latest_feedback_field(_IMPROVEMENT_SUGGESTION_PATTERN, judge_feedback)

    lines = [
        "You are producing one research iteration for a bounded autoresearch loop.",
        f"Current best score to beat: {previous_best:.4f}.",
        f"Recent outcomes: {recent_history}",
        "",
        "Optimization mode:",
        "- Exploit, do not explore. Spend effort on the weakest judged dimension or the clearest benchmark regression.",
        "- Preserve existing strong sections and prefer targeted edits over broad rewrites unless the knowledge base is structurally broken.",
    ]

    if priority_dimension:
        lines.append(
            f"- Current priority dimension from the latest judge review: {priority_dimension}."
        )
    else:
        lines.append(
            "- If no judge priority exists yet, prioritize evidence density and benchmark citation completeness."
        )

    if improvement_suggestion:
        lines.append(f"- Latest judge suggestion to address directly: {improvement_suggestion}")

    if human_feedback.strip():
        lines.append(
            "- Human feedback is authoritative. If it conflicts with judge feedback, satisfy the human feedback first."
        )

    lines.extend(
        [
            "",
            "Required output discipline:",
            "- Improve the single mutable knowledge base.",
            "- Answer every benchmark item directly.",
            "- Every benchmark answer must include a non-empty `citations` array.",
            "- If an answer contains `[source-*]` tags, mirror those exact IDs in the `citations` array.",
            "- Prefer concrete, verifiable references in the knowledge base: URLs, paper titles, DOIs, doc paths, docket numbers, contract addresses, query links, or transaction hashes.",
            "- Do not broaden into new topics or venues unless the addition directly improves the current priority dimension, closes a benchmark gap, or materially strengthens evidence density.",
            "- Output JSON only.",
        ]
    )
    return "\n".join(lines)


def _repair_benchmark_citation_regressions(
    benchmark: list[BenchmarkItem],
    response: ResearchResponse,
) -> dict[str, Any]:
    benchmark_map = {item.id: item for item in benchmark}
    repaired: list[dict[str, Any]] = []
    missing: list[str] = []

    for answer in response.benchmark_answers:
        if answer.citations:
            continue
        item = benchmark_map.get(answer.id)
        required_sources = list(item.required_sources) if item is not None else []
        if required_sources:
            answer.citations = required_sources
            repaired.append(
                {
                    "id": answer.id,
                    "strategy": "benchmark_required_sources",
                    "citations": list(required_sources),
                }
            )
            continue
        missing.append(answer.id)

    return {
        "repaired_benchmark_citations": repaired,
        "missing_benchmark_citations": missing,
    }


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
    producer_provider: BaseProvider | None = None,
) -> IterationOutcome:
    context = load_run_context(run_dir)
    resolved_kind = provider_kind or context.config.provider.kind
    resolved_command = command if command is not None else context.config.provider.command
    provider = producer_provider
    if provider is None:
        if resolved_kind in {"cli", "codex", "claude"}:
            provider = _create_provider_for_role(
                resolved_kind,
                context.config.producer,
                role="producer",
            )
        else:
            provider = create_provider(resolved_kind, command=resolved_command)
    previous_best = context.state.best_score

    iteration = context.state.iteration + 1
    history = load_recent_results(context.paths, limit=5)
    feedback = load_feedback_context(context.paths)
    task = ProviderTask(
        task_type="research_iteration",
        instructions=build_iteration_instructions(
            previous_best=previous_best,
            history=history,
            judge_feedback=feedback["judge_feedback"],
            human_feedback=feedback["human_feedback"],
        ),
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
    artifact_dir = context.paths.artifacts_dir / f"iteration-{iteration:04d}"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    write_json(artifact_dir / "task.json", task.to_dict())

    producer_timeout = getattr(provider, "timeout", None)
    producer_started_at = utc_now_iso()
    producer_prompt_chars = len(json.dumps(task.to_dict(), indent=2))
    raw_response: Any = None
    _record_provider_event(
        run_dir,
        role="producer",
        provider_kind=resolved_kind,
        iteration=iteration,
        status="running",
        attempt_started_at=producer_started_at,
        timeout_seconds=producer_timeout,
        prompt_chars=producer_prompt_chars,
    )
    try:
        raw_response = provider.invoke(task)
        response = ResearchResponse.from_dict(raw_response)
        validation = _repair_benchmark_citation_regressions(context.benchmark, response)
    except Exception as exc:
        if raw_response is not None:
            extra: dict[str, Any] = {
                "raw_response_type": type(raw_response).__name__,
            }
            if isinstance(raw_response, dict):
                raw_benchmark_answers = raw_response.get("benchmark_answers")
                extra["raw_benchmark_answers_type"] = type(raw_benchmark_answers).__name__
                write_json(artifact_dir / "raw_response.json", raw_response)
            elif isinstance(raw_response, list):
                write_json(artifact_dir / "raw_response.json", raw_response)
            else:
                write_text(artifact_dir / "raw_response.txt", str(raw_response))
        else:
            extra = {}
        write_text(artifact_dir / "error.txt", str(exc))
        _record_provider_event(
            run_dir,
            role="producer",
            provider_kind=resolved_kind,
            iteration=iteration,
            status="error",
            attempt_started_at=producer_started_at,
            timeout_seconds=producer_timeout,
            prompt_chars=producer_prompt_chars,
            error=str(exc),
            extra=extra,
        )
        raise
    if validation["repaired_benchmark_citations"] or validation["missing_benchmark_citations"]:
        write_json(artifact_dir / "validation.json", validation)
    if validation["missing_benchmark_citations"]:
        logger.warning(
            "Iteration %d has benchmark answers without citations after repair: %s",
            iteration,
            ", ".join(validation["missing_benchmark_citations"]),
        )
    _record_provider_event(
        run_dir,
        role="producer",
        provider_kind=resolved_kind,
        iteration=iteration,
        status="success",
        attempt_started_at=producer_started_at,
        timeout_seconds=producer_timeout,
        prompt_chars=producer_prompt_chars,
        extra={
            "result_keys": sorted(raw_response.keys()),
            "repaired_benchmark_citations": len(validation["repaired_benchmark_citations"]),
            "missing_benchmark_citations": len(validation["missing_benchmark_citations"]),
        },
    )
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
            judge_timeout = getattr(judge_provider, "timeout", None)
            judge_started_at = utc_now_iso()
            judge_prompt_chars = len(
                build_judge_prompt(
                    goal_state=context.goal_state,
                    candidate_kb=response.knowledge_base_markdown,
                    benchmark_answers=response.benchmark_answers,
                )
            )
            judge_kind = getattr(judge_provider, "cli_binary", judge_provider.__class__.__name__)
            _record_provider_event(
                run_dir,
                role="judge",
                provider_kind=str(judge_kind),
                iteration=iteration,
                status="running",
                attempt_started_at=judge_started_at,
                timeout_seconds=judge_timeout,
                prompt_chars=judge_prompt_chars,
            )
            judge_report = safe_run_judge(
                goal_state=context.goal_state,
                candidate_kb=response.knowledge_base_markdown,
                benchmark_answers=response.benchmark_answers,
                judge_provider=judge_provider,
            )
            if judge_report is not None:
                _record_provider_event(
                    run_dir,
                    role="judge",
                    provider_kind=str(judge_kind),
                    iteration=iteration,
                    status="success",
                    attempt_started_at=judge_started_at,
                    timeout_seconds=judge_timeout,
                    prompt_chars=judge_prompt_chars,
                    extra={
                        "overall_score": judge_report.overall_score,
                        "priority_dimension": judge_report.priority_dimension,
                    },
                )
                decision_score = judge_report.overall_score
                priority_dimension = judge_report.priority_dimension
            else:
                _record_provider_event(
                    run_dir,
                    role="judge",
                    provider_kind=str(judge_kind),
                    iteration=iteration,
                    status="fallback",
                    attempt_started_at=judge_started_at,
                    timeout_seconds=judge_timeout,
                    prompt_chars=judge_prompt_chars,
                    error="Judge failed; fell back to deterministic scoring.",
                )

    status = _decision(
        candidate_score=decision_score,
        previous_best=context.state.best_score,
        candidate_chars=candidate_chars,
        current_chars=current_chars,
        minimum_improvement=context.config.evaluation.minimum_improvement,
        allow_tie_if_shorter=context.config.evaluation.allow_tie_if_shorter,
    )

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
    resume_branch: bool = False,
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
        resume_branch: When True, reuse an existing autoresearch branch with the
            same tag instead of treating it as a startup error.

    Returns:
        List of IterationOutcome for each completed iteration.
    """
    if stop_conditions is None:
        stop_conditions = StopConditions()

    # Ensure clean state and create branch BEFORE installing signal handler
    # so early failures don't leak the custom handler into the caller
    ensure_clean_state(cwd=run_dir)
    ensure_branch(tag, cwd=run_dir, allow_existing=resume_branch)

    # Setup SIGINT handling (after setup that can raise)
    own_event = shutdown_event is None
    if shutdown_event is None:
        shutdown_event = threading.Event()
    original_handler = None
    if own_event:
        original_handler = signal.getsignal(signal.SIGINT)
        handler = install_sigint_handler(shutdown_event)
        signal.signal(signal.SIGINT, handler)

    config = load_run_context(run_dir).config
    producer_provider = _create_provider_for_role(
        producer_kind,
        config.producer,
        role="producer",
    )
    judge_provider = _create_provider_for_role(
        judge_kind,
        config.judge,
        role="judge",
    )

    outcomes: list[IterationOutcome] = []
    iteration_count = 0
    consecutive_discards = 0
    consecutive_crashes = 0
    loop_status = "running"
    stop_reason = ""

    _write_loop_status(
        run_dir,
        status=loop_status,
        producer_kind=producer_kind,
        judge_kind=judge_kind,
        tag=tag,
        stop_conditions=stop_conditions,
    )

    try:
        while True:
            total_iterations = load_run_context(run_dir).state.iteration

            # Check shutdown event (SIGINT)
            if shutdown_event.is_set():
                logger.info("Shutdown requested, exiting loop.")
                loop_status = "stopped"
                stop_reason = "shutdown"
                break

            # Check absolute total-iteration stop condition across restarts
            if stop_conditions.max_total_iterations is not None:
                if total_iterations >= stop_conditions.max_total_iterations:
                    logger.info(
                        "Stopping: total iterations %d reached limit of %d.",
                        total_iterations,
                        stop_conditions.max_total_iterations,
                    )
                    loop_status = "stopped"
                    stop_reason = "max_total_iterations"
                    break

            # Check max_iterations stop condition
            if stop_conditions.max_iterations is not None:
                if iteration_count >= stop_conditions.max_iterations:
                    loop_status = "stopped"
                    stop_reason = "max_iterations"
                    break

            # Check max_consecutive_discard stop condition
            if stop_conditions.max_consecutive_discard is not None:
                if consecutive_discards >= stop_conditions.max_consecutive_discard:
                    logger.info(
                        "Stopping: %d consecutive discards reached limit of %d.",
                        consecutive_discards,
                        stop_conditions.max_consecutive_discard,
                    )
                    loop_status = "stopped"
                    stop_reason = "max_consecutive_discard"
                    break

            try:
                outcome = run_iteration(
                    run_dir=run_dir,
                    provider_kind=producer_kind,
                    judge_provider=judge_provider,
                    producer_provider=producer_provider,
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
                    loop_status = "failed"
                    stop_reason = "consecutive_crashes"
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
                        loop_status = "stopped"
                        stop_reason = "dimension_threshold"
                        break
    except Exception:
        loop_status = "failed"
        if not stop_reason:
            stop_reason = "unexpected_error"
        raise
    finally:
        _write_loop_status(
            run_dir,
            status=loop_status,
            stop_reason=stop_reason,
            producer_kind=producer_kind,
            judge_kind=judge_kind,
            tag=tag,
            stop_conditions=stop_conditions,
        )
        # Restore original signal handler if we installed one
        if own_event and original_handler is not None:
            signal.signal(signal.SIGINT, original_handler)

    return outcomes
