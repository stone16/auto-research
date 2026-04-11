from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.judge import JudgeReport
from llm_autoresearch.judge_invariants import (
    check_all,
    check_dismissal_includes_mergeables,
    check_priority_matches_lowest_dimension,
    check_regressions_acknowledged_in_summary,
    check_verdict_matches_score_direction,
    verdict_is_compromised,
)


def _clean_report(
    *,
    dimension_scores: dict[str, float] | None = None,
    overall_score: float = 0.7,
    review_markdown: str = "ok",
    priority_dimension: str = "architecture",
    improvement_suggestion: str = "strengthen the weakest section",
    pairwise_verdict: str = "tie",
    pairwise_summary: str = "the candidate and retained best are equivalent",
    mergeable_improvements: list[str] | None = None,
    regressions: list[str] | None = None,
) -> JudgeReport:
    """Build a JudgeReport that passes every invariant by default."""
    return JudgeReport(
        dimension_scores=dimension_scores
        if dimension_scores is not None
        else {"evidence": 0.9, "architecture": 0.5},
        overall_score=overall_score,
        review_markdown=review_markdown,
        priority_dimension=priority_dimension,
        improvement_suggestion=improvement_suggestion,
        pairwise_verdict=pairwise_verdict,
        pairwise_summary=pairwise_summary,
        mergeable_improvements=mergeable_improvements
        if mergeable_improvements is not None
        else [],
        regressions=regressions if regressions is not None else [],
    )


class PriorityLowestInvariantTests(unittest.TestCase):
    def test_clean_report_passes(self) -> None:
        report = _clean_report()
        self.assertIsNone(check_priority_matches_lowest_dimension(report))

    def test_priority_points_at_highest_dimension_fails(self) -> None:
        report = _clean_report(
            dimension_scores={"evidence": 0.9, "architecture": 0.5},
            priority_dimension="evidence",
        )
        violation = check_priority_matches_lowest_dimension(report)
        self.assertIsNotNone(violation)
        assert violation is not None
        self.assertEqual(violation.code, "priority_not_lowest")

    def test_tie_at_lowest_is_allowed(self) -> None:
        report = _clean_report(
            dimension_scores={"a": 0.5, "b": 0.5, "c": 0.9},
            priority_dimension="a",
        )
        self.assertIsNone(check_priority_matches_lowest_dimension(report))

    def test_missing_scores_or_priority_skips_check(self) -> None:
        self.assertIsNone(
            check_priority_matches_lowest_dimension(
                _clean_report(dimension_scores={}, priority_dimension="x")
            )
        )
        self.assertIsNone(
            check_priority_matches_lowest_dimension(
                _clean_report(priority_dimension="")
            )
        )


class VerdictScoreDirectionInvariantTests(unittest.TestCase):
    def test_candidate_better_with_higher_score_passes(self) -> None:
        report = _clean_report(pairwise_verdict="candidate_better", overall_score=0.9)
        self.assertIsNone(check_verdict_matches_score_direction(report, previous_best=0.8))

    def test_candidate_better_with_lower_score_fails(self) -> None:
        report = _clean_report(pairwise_verdict="candidate_better", overall_score=0.82)
        violation = check_verdict_matches_score_direction(report, previous_best=0.88)
        self.assertIsNotNone(violation)
        assert violation is not None
        self.assertEqual(violation.code, "verdict_score_mismatch")

    def test_current_best_better_with_higher_score_fails(self) -> None:
        report = _clean_report(pairwise_verdict="current_best_better", overall_score=0.91)
        violation = check_verdict_matches_score_direction(report, previous_best=0.85)
        self.assertIsNotNone(violation)
        assert violation is not None
        self.assertEqual(violation.code, "verdict_score_mismatch")

    def test_tie_verdict_has_no_direction_constraint(self) -> None:
        report = _clean_report(pairwise_verdict="tie", overall_score=0.70)
        self.assertIsNone(
            check_verdict_matches_score_direction(report, previous_best=0.90)
        )

    def test_equal_scores_are_not_a_contradiction(self) -> None:
        report = _clean_report(pairwise_verdict="candidate_better", overall_score=0.88)
        self.assertIsNone(
            check_verdict_matches_score_direction(report, previous_best=0.88)
        )


class RegressionAcknowledgmentInvariantTests(unittest.TestCase):
    def test_candidate_better_without_regressions_passes(self) -> None:
        report = _clean_report(pairwise_verdict="candidate_better", regressions=[])
        self.assertIsNone(check_regressions_acknowledged_in_summary(report))

    def test_candidate_better_with_acknowledged_tradeoff_passes(self) -> None:
        report = _clean_report(
            pairwise_verdict="candidate_better",
            regressions=["lost some inline citations"],
            pairwise_summary="net better despite a small regression on citation density",
        )
        self.assertIsNone(check_regressions_acknowledged_in_summary(report))

    def test_candidate_better_with_silent_regressions_fails(self) -> None:
        report = _clean_report(
            pairwise_verdict="candidate_better",
            regressions=["r1", "r2", "r3"],
            pairwise_summary="the candidate is clearly stronger than the retained best",
        )
        violation = check_regressions_acknowledged_in_summary(report)
        self.assertIsNotNone(violation)
        assert violation is not None
        self.assertEqual(violation.code, "unacknowledged_regressions")

    def test_non_candidate_better_verdict_is_ignored(self) -> None:
        report = _clean_report(
            pairwise_verdict="current_best_better",
            regressions=["r1"],
            pairwise_summary="retained best is ahead",
        )
        self.assertIsNone(check_regressions_acknowledged_in_summary(report))


class DismissalWithoutMergeablesInvariantTests(unittest.TestCase):
    def test_current_best_better_with_mergeables_passes(self) -> None:
        report = _clean_report(
            pairwise_verdict="current_best_better",
            mergeable_improvements=["absorb the new failure matrix rows"],
        )
        self.assertIsNone(check_dismissal_includes_mergeables(report))

    def test_current_best_better_without_mergeables_fails(self) -> None:
        report = _clean_report(
            pairwise_verdict="current_best_better",
            mergeable_improvements=[],
        )
        violation = check_dismissal_includes_mergeables(report)
        self.assertIsNotNone(violation)
        assert violation is not None
        self.assertEqual(violation.code, "dismissal_without_mergeables")

    def test_candidate_better_without_mergeables_is_ignored(self) -> None:
        report = _clean_report(
            pairwise_verdict="candidate_better", mergeable_improvements=[]
        )
        self.assertIsNone(check_dismissal_includes_mergeables(report))


class CheckAllAggregationTests(unittest.TestCase):
    def test_clean_report_produces_no_violations(self) -> None:
        report = _clean_report()
        self.assertEqual(check_all(report, previous_best=0.5), [])

    def test_multiple_violations_reported_in_definition_order(self) -> None:
        # priority_not_lowest + verdict_score_mismatch + unacknowledged_regressions
        report = _clean_report(
            dimension_scores={"evidence": 0.9, "architecture": 0.5},
            priority_dimension="evidence",  # I1
            pairwise_verdict="candidate_better",
            overall_score=0.70,  # triggers I2 against previous_best 0.90
            regressions=["dropped inline example"],
            pairwise_summary="candidate is flatly stronger",  # no tradeoff word → I3
        )
        violations = check_all(report, previous_best=0.90)
        codes = [v.code for v in violations]
        self.assertEqual(
            codes,
            [
                "priority_not_lowest",
                "verdict_score_mismatch",
                "unacknowledged_regressions",
            ],
        )


class VerdictCompromisedTests(unittest.TestCase):
    def test_empty_violations_is_not_compromised(self) -> None:
        self.assertFalse(verdict_is_compromised([]))

    def test_score_mismatch_compromises_verdict(self) -> None:
        report = _clean_report(pairwise_verdict="candidate_better", overall_score=0.8)
        violations = check_all(report, previous_best=0.9)
        self.assertTrue(verdict_is_compromised(violations))

    def test_unacknowledged_regressions_compromises_verdict(self) -> None:
        report = _clean_report(
            pairwise_verdict="candidate_better",
            overall_score=0.9,
            regressions=["r1"],
            pairwise_summary="clearly stronger overall",
        )
        violations = check_all(report, previous_best=0.85)
        self.assertTrue(verdict_is_compromised(violations))

    def test_priority_violation_alone_does_not_compromise_verdict(self) -> None:
        report = _clean_report(
            dimension_scores={"a": 0.9, "b": 0.5},
            priority_dimension="a",  # I1 fires
            pairwise_verdict="tie",
        )
        violations = check_all(report, previous_best=0.7)
        self.assertEqual([v.code for v in violations], ["priority_not_lowest"])
        self.assertFalse(verdict_is_compromised(violations))

    def test_dismissal_laziness_alone_does_not_compromise_verdict(self) -> None:
        report = _clean_report(
            pairwise_verdict="current_best_better",
            overall_score=0.8,
            mergeable_improvements=[],
        )
        violations = check_all(report, previous_best=0.85)
        self.assertEqual(
            [v.code for v in violations], ["dismissal_without_mergeables"]
        )
        self.assertFalse(verdict_is_compromised(violations))


class V5RegressionCasesTests(unittest.TestCase):
    """Real v5 run incidents that Tier 1 should catch."""

    def test_iter_23_candidate_better_but_score_dropped(self) -> None:
        # iter 23: verdict=candidate_better, score=0.82, prev_best=0.88
        report = _clean_report(
            pairwise_verdict="candidate_better",
            overall_score=0.82,
            pairwise_summary="modest improvement",
        )
        violations = check_all(report, previous_best=0.88)
        codes = [v.code for v in violations]
        self.assertIn("verdict_score_mismatch", codes)
        self.assertTrue(verdict_is_compromised(violations))

    def test_iter_25_silent_regressions_with_tied_score(self) -> None:
        # iter 25: verdict=candidate_better, 3 regressions, summary has no tradeoff word
        report = _clean_report(
            pairwise_verdict="candidate_better",
            overall_score=0.88,
            regressions=["r1", "r2", "r3"],
            pairwise_summary="the candidate is a clearer, stronger artifact",
        )
        violations = check_all(report, previous_best=0.88)
        codes = [v.code for v in violations]
        self.assertIn("unacknowledged_regressions", codes)
        self.assertTrue(verdict_is_compromised(violations))

    def test_iter_29_wholesale_dismissal(self) -> None:
        # iter 29: verdict=current_best_better, mergeable_improvements=[]
        report = _clean_report(
            pairwise_verdict="current_best_better",
            overall_score=0.78,
            mergeable_improvements=[],
        )
        violations = check_all(report, previous_best=0.89)
        codes = [v.code for v in violations]
        self.assertIn("dismissal_without_mergeables", codes)
        # dismissal laziness alone is logged but should not demote the verdict
        self.assertFalse(verdict_is_compromised(violations))


if __name__ == "__main__":
    unittest.main()
