"""Goal-anchored LLM judge evaluation module.

Provides the JudgeReport dataclass, prompt construction, response parsing,
gate logic, and the run_judge orchestration function.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

from .models import BenchmarkAnswer, GoalState, QualityDimension
from .providers import BaseProvider, ProviderError, ProviderTask

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# JudgeReport dataclass
# ---------------------------------------------------------------------------

@dataclass
class JudgeReport:
    """Result of a judge evaluation.

    Attributes:
        dimension_scores: Normalized scores (0.0-1.0) per configured dimension.
        overall_score: Average of dimension_scores values.
        review_markdown: Free-form markdown review from the judge.
        priority_dimension: The dimension furthest from the goal.
        improvement_suggestion: One specific actionable suggestion.
        pairwise_verdict: Comparison verdict against the current retained best.
        pairwise_summary: Brief rationale for the pairwise verdict.
        mergeable_improvements: Local wins worth folding into the next retained best.
        regressions: Regressions or risks introduced relative to the current best.
    """

    dimension_scores: dict[str, float]
    overall_score: float
    review_markdown: str
    priority_dimension: str
    improvement_suggestion: str
    pairwise_verdict: str = "tie"
    pairwise_summary: str = ""
    mergeable_improvements: list[str] = field(default_factory=list)
    regressions: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Gate logic
# ---------------------------------------------------------------------------

def should_invoke_judge(deterministic_score: float, gate_threshold: float) -> bool:
    """Decide whether to invoke the LLM judge based on the deterministic evaluator score.

    The deterministic evaluator score acts as a boolean gate: if below the
    gate_threshold, the candidate is auto-discarded without invoking the
    (expensive) judge.

    Returns True if the judge should be invoked, False if auto-discard.
    """
    return deterministic_score >= gate_threshold


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def build_judge_prompt(
    goal_state: GoalState,
    candidate_kb: str,
    benchmark_answers: list[BenchmarkAnswer],
    current_best_kb: str = "",
    current_best_benchmark_answers: list[BenchmarkAnswer] | None = None,
) -> str:
    """Build the structured prompt sent to the judge CLI agent.

    The prompt includes:
    - Goal state (done_definition)
    - Quality dimensions with descriptions
    - Explicit scoring instructions (0-10 per dimension)
    - Instruction to identify the dimension furthest from goal
    - Instruction to provide one specific improvement suggestion
    - The candidate knowledge base
    - Benchmark answers
    """
    dimension_lines = []
    for dim in goal_state.dimensions:
        dimension_lines.append(f"  - {dim.name}: {dim.description}")
    dimensions_block = "\n".join(dimension_lines)

    answers_block = ""
    if benchmark_answers:
        answer_lines = []
        for ans in benchmark_answers:
            citations = ", ".join(ans.citations) if ans.citations else "none"
            answer_lines.append(
                f"  - [{ans.id}] Answer: {ans.answer}\n    Citations: {citations}"
            )
        answers_block = "\n".join(answer_lines)
    else:
        answers_block = "  (no benchmark answers provided)"

    expected_dims = ", ".join(f'"{dim.name}"' for dim in goal_state.dimensions)
    current_best_benchmark_answers = current_best_benchmark_answers or []

    if current_best_benchmark_answers:
        best_answer_lines = []
        for ans in current_best_benchmark_answers:
            citations = ", ".join(ans.citations) if ans.citations else "none"
            best_answer_lines.append(
                f"  - [{ans.id}] Answer: {ans.answer}\n    Citations: {citations}"
            )
        current_best_answers_block = "\n".join(best_answer_lines)
    else:
        current_best_answers_block = "  (no retained benchmark answers available)"

    current_best_kb_block = current_best_kb or "(no retained best yet; treat this as the initial baseline)"

    prompt = f"""\
You are an expert research quality judge. Evaluate the candidate knowledge base
against the goal state, the quality dimensions below, and the current retained best.

## Goal State

{goal_state.done_definition}

## Quality Dimensions

{dimensions_block}

## Instructions

1. Score each quality dimension on a scale of 0-10 (integer).
2. Compare the candidate against the current retained best and decide whether the candidate is better, the current retained best is better, or they are tied.
3. Identify the dimension that is furthest from the goal.
4. Provide one specific improvement suggestion for the next iteration.
5. If the candidate has any local wins that should be folded into the retained best even when the candidate should not replace it, list them under mergeable_improvements.
6. If the candidate introduces regressions relative to the current retained best, list them under regressions.

## Expected Output (JSON only)

Return a single JSON object with exactly these keys:
- "dimension_scores": object mapping dimension names to integer scores (0-10)
  Expected dimensions: {expected_dims}
- "review_markdown": string with a brief markdown review
- "pairwise_verdict": one of "candidate_better", "current_best_better", or "tie"
- "pairwise_summary": string explaining the pairwise verdict in 1-3 sentences
- "mergeable_improvements": array of concrete improvements worth absorbing into the retained best
- "regressions": array of concrete regressions or risks introduced by the candidate
- "priority_dimension": string naming the dimension furthest from goal
- "improvement_suggestion": string with one specific actionable improvement

When deciding the pairwise verdict, optimize for the retained artifact quality, not novelty.
If the candidate is roughly tied overall but clearly better in a meaningful way, prefer "candidate_better".

## Candidate Knowledge Base

{candidate_kb}

## Benchmark Answers

{answers_block}

## Current Retained Best Knowledge Base

{current_best_kb_block}

## Current Retained Best Benchmark Answers

{current_best_answers_block}
"""
    return prompt


# ---------------------------------------------------------------------------
# Response parsing and validation
# ---------------------------------------------------------------------------

_REQUIRED_KEYS = ("dimension_scores", "review_markdown", "priority_dimension", "improvement_suggestion")
_VALID_PAIRWISE_VERDICTS = {"candidate_better", "current_best_better", "tie"}


def _coerce_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple | set):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    return [str(value).strip()]


def parse_judge_response(
    raw: dict[str, Any],
    configured_dimensions: list[QualityDimension],
) -> JudgeReport:
    """Parse and validate a raw judge response dict into a JudgeReport.

    - Validates all required keys are present.
    - Clamps dimension scores to 0-10 range.
    - Normalizes scores by dividing by 10.
    - Logs warnings for unrecognized dimensions (excluded from report).
    - Computes overall_score as average of normalized configured dimension scores.

    Raises:
        ValueError: If any required key is missing from the raw response.
    """
    for key in _REQUIRED_KEYS:
        if key not in raw:
            raise ValueError(f"Judge response missing required key: '{key}'")

    raw_scores = raw["dimension_scores"]
    if not isinstance(raw_scores, dict):
        raise ValueError(
            f"Judge response 'dimension_scores' must be an object, got {type(raw_scores).__name__}"
        )
    configured_names = {dim.name for dim in configured_dimensions}

    # Warn about unrecognized dimensions
    for name in raw_scores:
        if name not in configured_names:
            logger.warning(
                "Judge returned unrecognized dimension '%s'; ignoring it.", name
            )

    # Build normalized scores for configured dimensions only
    # Missing configured dimensions default to 0.0 to prevent score inflation
    dimension_scores: dict[str, float] = {}
    for name in configured_names:
        if name in raw_scores:
            raw_val = float(raw_scores[name])
            clamped = max(0.0, min(10.0, raw_val))
            dimension_scores[name] = clamped / 10.0
        else:
            logger.warning(
                "Judge did not return score for configured dimension '%s'; defaulting to 0.0",
                name,
            )
            dimension_scores[name] = 0.0

    # Compute overall_score as average of normalized scores
    if dimension_scores:
        overall_score = sum(dimension_scores.values()) / len(dimension_scores)
    else:
        overall_score = 0.0

    return JudgeReport(
        dimension_scores=dimension_scores,
        overall_score=round(overall_score, 4),
        review_markdown=str(raw["review_markdown"]),
        priority_dimension=str(raw["priority_dimension"]),
        improvement_suggestion=str(raw["improvement_suggestion"]),
        pairwise_verdict=(
            str(raw.get("pairwise_verdict", "tie")).strip()
            if str(raw.get("pairwise_verdict", "tie")).strip() in _VALID_PAIRWISE_VERDICTS
            else "tie"
        ),
        pairwise_summary=str(raw.get("pairwise_summary", "")),
        mergeable_improvements=_coerce_string_list(raw.get("mergeable_improvements", [])),
        regressions=_coerce_string_list(raw.get("regressions", [])),
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_judge(
    goal_state: GoalState,
    candidate_kb: str,
    benchmark_answers: list[BenchmarkAnswer],
    judge_provider: BaseProvider,
    current_best_kb: str = "",
    current_best_benchmark_answers: list[BenchmarkAnswer] | None = None,
) -> JudgeReport:
    """Orchestrate a judge evaluation.

    1. Build the judge prompt from goal state, candidate KB, and benchmark answers.
    2. Create a ProviderTask with task_type="judge_evaluation".
    3. Invoke the judge provider.
    4. Parse and validate the response.
    5. Return a JudgeReport.

    Raises:
        ProviderError: If the judge provider fails (crash, timeout, etc.).
        ValueError: If the judge response is malformed.
    """
    prompt = build_judge_prompt(
        goal_state=goal_state,
        candidate_kb=candidate_kb,
        benchmark_answers=benchmark_answers,
        current_best_kb=current_best_kb,
        current_best_benchmark_answers=current_best_benchmark_answers,
    )

    task = ProviderTask(
        task_type="judge_evaluation",
        instructions=prompt,
        payload={
            "goal_state": {
                "done_definition": goal_state.done_definition,
                "dimensions": [
                    {"name": dim.name, "description": dim.description}
                    for dim in goal_state.dimensions
                ],
            },
            "candidate_kb": candidate_kb,
            "benchmark_answers": [ans.to_dict() for ans in benchmark_answers],
            "current_best_kb": current_best_kb,
            "current_best_benchmark_answers": [
                ans.to_dict() for ans in (current_best_benchmark_answers or [])
            ],
        },
    )

    raw_response = judge_provider.invoke(task)
    return parse_judge_response(raw_response, goal_state.dimensions)


def safe_run_judge(
    goal_state: GoalState,
    candidate_kb: str,
    benchmark_answers: list[BenchmarkAnswer],
    judge_provider: BaseProvider,
    current_best_kb: str = "",
    current_best_benchmark_answers: list[BenchmarkAnswer] | None = None,
) -> JudgeReport | None:
    """Graceful wrapper around run_judge for use in the loop.

    Returns None (instead of raising) when the judge CLI crashes or returns
    malformed output, allowing the caller to fall back to deterministic-only
    scoring.
    """
    try:
        return run_judge(
            goal_state,
            candidate_kb,
            benchmark_answers,
            judge_provider,
            current_best_kb=current_best_kb,
            current_best_benchmark_answers=current_best_benchmark_answers,
        )
    except (ProviderError, ValueError, TypeError, KeyError) as exc:
        logger.warning("Judge failed, falling back to deterministic scoring: %s", exc)
        return None
