from __future__ import annotations

import logging
from pathlib import Path

from .evaluator import evaluate_answers
from .git import commit_iteration, reset_last_commit
from .models import IterationOutcome, ResearchResponse
from .providers import ProviderTask, create_provider
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
) -> IterationOutcome:
    context = load_run_context(run_dir)
    resolved_kind = provider_kind or context.config.provider.kind
    resolved_command = command if command is not None else context.config.provider.command
    provider = create_provider(resolved_kind, command=resolved_command)
    previous_best = context.state.best_score

    iteration = context.state.iteration + 1
    history = load_recent_results(context.paths, limit=5)
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
        },
    )

    response = ResearchResponse.from_dict(provider.invoke(task))
    evaluation = evaluate_answers(context.benchmark, response.benchmark_answers)
    candidate_chars = len(response.knowledge_base_markdown)
    current_chars = context.state.current_knowledge_chars or len(context.knowledge_base_markdown)
    status = _decision(
        candidate_score=evaluation.total_score,
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

    if status == "keep":
        write_text(context.paths.knowledge_path, response.knowledge_base_markdown)
        context.state.best_score = evaluation.total_score
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
            "score": f"{evaluation.total_score:.4f}",
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

    return IterationOutcome(
        iteration=iteration,
        status=status,
        candidate_score=evaluation.total_score,
        previous_best=previous_best,
        knowledge_chars=candidate_chars,
        artifact_dir=str(artifact_dir),
        experiment_title=response.experiment_title,
        change_summary=response.change_summary,
    )
