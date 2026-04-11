"""Deterministic invariant checks on JudgeReport output.

Each invariant is a pure function that takes a JudgeReport plus minimal
context (previous_best when needed) and returns None if the report is
internally consistent, or an InvariantViolation describing the
contradiction.

These checks are cheap, LLM-free, and catch cases where the judge
contradicts itself (e.g. a priority_dimension that is not actually the
lowest-scoring dimension, or a "candidate_better" verdict when the
overall score went down). They are meant to sit between the judge and
the keep/discard decision so that self-contradictory judge output
cannot silently drive control flow.

Invariant catalog:

- I1 priority_not_lowest: priority_dimension must point at the dimension
  whose score is the minimum in dimension_scores.
- I2 verdict_score_mismatch: pairwise_verdict must agree with the sign
  of (overall_score - previous_best).
- I3 unacknowledged_regressions: if pairwise_verdict is candidate_better
  and regressions is non-empty, pairwise_summary must acknowledge the
  tradeoff using at least one recognizable keyword.
- I4 dismissal_without_mergeables: current_best_better with empty
  mergeable_improvements is almost always judge laziness and should be
  flagged.

Violation codes in _DECISION_CORRUPTING_CODES are the subset that
compromises pairwise_verdict enough that the verdict should be demoted
to "tie" before being fed into the keep/discard decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .judge import JudgeReport

_REGRESSION_ACKNOWLEDGMENT_KEYWORDS: Final[tuple[str, ...]] = (
    "regress",
    "trade",
    "lose",
    "lost",
    "drop",
    "weaker",
    "worse",
    "sacrific",
    "tension",
    "cost",
)

_DECISION_CORRUPTING_CODES: Final[frozenset[str]] = frozenset(
    {
        "verdict_score_mismatch",
        "unacknowledged_regressions",
    }
)


@dataclass(frozen=True)
class InvariantViolation:
    code: str
    message: str


def check_priority_matches_lowest_dimension(
    report: JudgeReport,
) -> InvariantViolation | None:
    """I1: priority_dimension must be the dimension with the lowest score."""
    if not report.dimension_scores or not report.priority_dimension:
        return None

    lowest_score = min(report.dimension_scores.values())
    lowest_dims = {
        name
        for name, score in report.dimension_scores.items()
        if score == lowest_score
    }
    if report.priority_dimension in lowest_dims:
        return None

    claimed_score = report.dimension_scores.get(report.priority_dimension)
    return InvariantViolation(
        code="priority_not_lowest",
        message=(
            f"priority_dimension={report.priority_dimension!r} has score="
            f"{claimed_score} but the actual minimum is {lowest_score} at "
            f"{sorted(lowest_dims)}"
        ),
    )


def check_verdict_matches_score_direction(
    report: JudgeReport,
    previous_best: float,
    tolerance: float = 1e-3,
) -> InvariantViolation | None:
    """I2: pairwise_verdict must agree with the score direction."""
    if report.pairwise_verdict == "candidate_better":
        if report.overall_score < previous_best - tolerance:
            return InvariantViolation(
                code="verdict_score_mismatch",
                message=(
                    f"verdict=candidate_better but overall_score="
                    f"{report.overall_score:.4f} < previous_best="
                    f"{previous_best:.4f}"
                ),
            )
    elif report.pairwise_verdict == "current_best_better":
        if report.overall_score > previous_best + tolerance:
            return InvariantViolation(
                code="verdict_score_mismatch",
                message=(
                    f"verdict=current_best_better but overall_score="
                    f"{report.overall_score:.4f} > previous_best="
                    f"{previous_best:.4f}"
                ),
            )
    return None


def check_regressions_acknowledged_in_summary(
    report: JudgeReport,
) -> InvariantViolation | None:
    """I3: candidate_better with regressions must acknowledge the tradeoff."""
    if report.pairwise_verdict != "candidate_better":
        return None
    if not report.regressions:
        return None

    summary_lower = report.pairwise_summary.lower()
    if any(kw in summary_lower for kw in _REGRESSION_ACKNOWLEDGMENT_KEYWORDS):
        return None

    return InvariantViolation(
        code="unacknowledged_regressions",
        message=(
            f"verdict=candidate_better with {len(report.regressions)} "
            f"regressions but pairwise_summary does not acknowledge any tradeoff"
        ),
    )


def check_dismissal_includes_mergeables(
    report: JudgeReport,
) -> InvariantViolation | None:
    """I4: current_best_better must salvage at least one mergeable improvement."""
    if (
        report.pairwise_verdict == "current_best_better"
        and not report.mergeable_improvements
    ):
        return InvariantViolation(
            code="dismissal_without_mergeables",
            message=(
                "verdict=current_best_better with no mergeable_improvements; "
                "a wholesale dismissal is almost always a sign of judge laziness"
            ),
        )
    return None


def check_all(
    report: JudgeReport,
    previous_best: float,
) -> list[InvariantViolation]:
    """Run every deterministic invariant on a JudgeReport.

    Returns a (possibly empty) list of InvariantViolation instances in
    definition order so callers can report the most significant issue first.
    """
    violations: list[InvariantViolation] = []

    v = check_priority_matches_lowest_dimension(report)
    if v is not None:
        violations.append(v)

    v = check_verdict_matches_score_direction(report, previous_best)
    if v is not None:
        violations.append(v)

    v = check_regressions_acknowledged_in_summary(report)
    if v is not None:
        violations.append(v)

    v = check_dismissal_includes_mergeables(report)
    if v is not None:
        violations.append(v)

    return violations


def verdict_is_compromised(violations: list[InvariantViolation]) -> bool:
    """Return True if any violation compromises pairwise_verdict enough that it
    should be demoted to "tie" before driving the keep/discard decision.
    """
    return any(v.code in _DECISION_CORRUPTING_CODES for v in violations)
