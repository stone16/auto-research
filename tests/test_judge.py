from __future__ import annotations

import json
import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.models import (
    BenchmarkAnswer,
    EvaluationConfig,
    GoalState,
    QualityDimension,
)
from llm_autoresearch.providers import ProviderError, ProviderTask


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sample_dimensions() -> list[QualityDimension]:
    return [
        QualityDimension(name="causal_completeness", description="All causal links covered"),
        QualityDimension(name="evidence_density", description="Claims backed by sources"),
    ]


def _sample_goal_state() -> GoalState:
    return GoalState(
        done_definition="Thorough understanding of causal mechanisms.",
        dimensions=_sample_dimensions(),
    )


def _valid_judge_response() -> dict:
    """A valid judge response JSON matching the expected schema."""
    return {
        "dimension_scores": {"causal_completeness": 7, "evidence_density": 4},
        "review_markdown": "Good coverage but weak evidence.",
        "priority_dimension": "evidence_density",
        "improvement_suggestion": "Add more source citations.",
    }


# ---------------------------------------------------------------------------
# Test: JudgeReport dataclass
# ---------------------------------------------------------------------------

class TestJudgeReportDataclass(unittest.TestCase):
    """Test that JudgeReport has the required fields and computes overall_score."""

    def test_judge_report_fields(self) -> None:
        from llm_autoresearch.judge import JudgeReport

        report = JudgeReport(
            dimension_scores={"causal_completeness": 0.7, "evidence_density": 0.4},
            overall_score=0.55,
            review_markdown="Good coverage but weak evidence.",
            priority_dimension="evidence_density",
            improvement_suggestion="Add more source citations.",
        )
        self.assertEqual(report.dimension_scores, {"causal_completeness": 0.7, "evidence_density": 0.4})
        self.assertAlmostEqual(report.overall_score, 0.55)
        self.assertEqual(report.review_markdown, "Good coverage but weak evidence.")
        self.assertEqual(report.priority_dimension, "evidence_density")
        self.assertEqual(report.improvement_suggestion, "Add more source citations.")


# ---------------------------------------------------------------------------
# Test: parse_judge_response
# ---------------------------------------------------------------------------

class TestParseJudgeResponse(unittest.TestCase):
    """Test parsing and validation of raw judge JSON responses."""

    def test_parse_valid_response(self) -> None:
        """Valid response with matching dimensions should parse correctly."""
        from llm_autoresearch.judge import parse_judge_response

        raw = _valid_judge_response()
        configured_dims = _sample_dimensions()
        report = parse_judge_response(raw, configured_dims)

        self.assertAlmostEqual(report.dimension_scores["causal_completeness"], 0.7)
        self.assertAlmostEqual(report.dimension_scores["evidence_density"], 0.4)
        # overall_score = average of normalized scores = (0.7 + 0.4) / 2 = 0.55
        self.assertAlmostEqual(report.overall_score, 0.55)
        self.assertEqual(report.review_markdown, "Good coverage but weak evidence.")
        self.assertEqual(report.priority_dimension, "evidence_density")
        self.assertEqual(report.improvement_suggestion, "Add more source citations.")

    def test_score_clamping_above_10(self) -> None:
        """Scores above 10 should be clamped to 10 (normalized to 1.0)."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {"causal_completeness": 15, "evidence_density": 4},
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        report = parse_judge_response(raw, _sample_dimensions())
        self.assertAlmostEqual(report.dimension_scores["causal_completeness"], 1.0)
        self.assertAlmostEqual(report.dimension_scores["evidence_density"], 0.4)

    def test_score_clamping_below_0(self) -> None:
        """Scores below 0 should be clamped to 0 (normalized to 0.0)."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {"causal_completeness": -3, "evidence_density": 4},
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        report = parse_judge_response(raw, _sample_dimensions())
        self.assertAlmostEqual(report.dimension_scores["causal_completeness"], 0.0)
        self.assertAlmostEqual(report.dimension_scores["evidence_density"], 0.4)

    def test_unrecognized_dimensions_logged_not_fatal(self) -> None:
        """Unrecognized dimension names should be logged as warnings but not cause failures."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {
                "causal_completeness": 7,
                "evidence_density": 4,
                "unknown_dimension": 5,
            },
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        with self.assertLogs("llm_autoresearch.judge", level="WARNING") as cm:
            report = parse_judge_response(raw, _sample_dimensions())

        # Unrecognized dimension should be excluded from the report
        self.assertNotIn("unknown_dimension", report.dimension_scores)
        # Known dimensions still parsed
        self.assertAlmostEqual(report.dimension_scores["causal_completeness"], 0.7)
        self.assertAlmostEqual(report.dimension_scores["evidence_density"], 0.4)
        # Warning was logged
        self.assertTrue(any("unknown_dimension" in msg for msg in cm.output))

    def test_missing_dimension_scores_raises(self) -> None:
        """Missing 'dimension_scores' key should raise ValueError."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        with self.assertRaises(ValueError):
            parse_judge_response(raw, _sample_dimensions())

    def test_missing_review_markdown_raises(self) -> None:
        """Missing 'review_markdown' key should raise ValueError."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {"causal_completeness": 7, "evidence_density": 4},
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        with self.assertRaises(ValueError):
            parse_judge_response(raw, _sample_dimensions())

    def test_missing_priority_dimension_raises(self) -> None:
        """Missing 'priority_dimension' key should raise ValueError."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {"causal_completeness": 7, "evidence_density": 4},
            "review_markdown": "Review.",
            "improvement_suggestion": "Improve.",
        }
        with self.assertRaises(ValueError):
            parse_judge_response(raw, _sample_dimensions())

    def test_missing_improvement_suggestion_raises(self) -> None:
        """Missing 'improvement_suggestion' key should raise ValueError."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {"causal_completeness": 7, "evidence_density": 4},
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
        }
        with self.assertRaises(ValueError):
            parse_judge_response(raw, _sample_dimensions())

    def test_overall_score_computation(self) -> None:
        """overall_score should be the average of dimension_scores / 10."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {"causal_completeness": 10, "evidence_density": 6},
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        report = parse_judge_response(raw, _sample_dimensions())
        # (10/10 + 6/10) / 2 = (1.0 + 0.6) / 2 = 0.8
        self.assertAlmostEqual(report.overall_score, 0.8)

    def test_overall_score_with_single_dimension(self) -> None:
        """overall_score with one dimension = that dimension's normalized score."""
        from llm_autoresearch.judge import parse_judge_response

        dims = [QualityDimension(name="accuracy", description="Correct facts")]
        raw = {
            "dimension_scores": {"accuracy": 8},
            "review_markdown": "Review.",
            "priority_dimension": "accuracy",
            "improvement_suggestion": "Improve.",
        }
        report = parse_judge_response(raw, dims)
        self.assertAlmostEqual(report.overall_score, 0.8)

    def test_only_configured_dimensions_counted(self) -> None:
        """Only scores for configured dimensions should contribute to overall_score."""
        from llm_autoresearch.judge import parse_judge_response

        raw = {
            "dimension_scores": {
                "causal_completeness": 10,
                "evidence_density": 6,
                "extra_dim": 2,
            },
            "review_markdown": "Review.",
            "priority_dimension": "evidence_density",
            "improvement_suggestion": "Improve.",
        }
        with self.assertLogs("llm_autoresearch.judge", level="WARNING"):
            report = parse_judge_response(raw, _sample_dimensions())
        # Only configured dimensions: (1.0 + 0.6) / 2 = 0.8
        self.assertAlmostEqual(report.overall_score, 0.8)


# ---------------------------------------------------------------------------
# Test: build_judge_prompt
# ---------------------------------------------------------------------------

class TestBuildJudgePrompt(unittest.TestCase):
    """Test that the judge prompt includes required context."""

    def test_prompt_includes_goal_state(self) -> None:
        from llm_autoresearch.judge import build_judge_prompt

        goal_state = _sample_goal_state()
        prompt = build_judge_prompt(
            goal_state=goal_state,
            candidate_kb="# Knowledge Base\nContent here.",
            benchmark_answers=[],
        )
        self.assertIn("causal mechanisms", prompt)

    def test_prompt_includes_quality_dimensions(self) -> None:
        from llm_autoresearch.judge import build_judge_prompt

        goal_state = _sample_goal_state()
        prompt = build_judge_prompt(
            goal_state=goal_state,
            candidate_kb="# Knowledge Base\nContent here.",
            benchmark_answers=[],
        )
        self.assertIn("causal_completeness", prompt)
        self.assertIn("evidence_density", prompt)

    def test_prompt_includes_scoring_instructions(self) -> None:
        from llm_autoresearch.judge import build_judge_prompt

        goal_state = _sample_goal_state()
        prompt = build_judge_prompt(
            goal_state=goal_state,
            candidate_kb="# Knowledge Base\nContent here.",
            benchmark_answers=[],
        )
        # Must instruct to score 0-10
        self.assertIn("0-10", prompt)
        # Must instruct to identify furthest-from-goal dimension
        self.assertIn("furthest", prompt.lower())
        # Must instruct to provide one improvement suggestion
        self.assertIn("improvement", prompt.lower())

    def test_prompt_includes_candidate_kb(self) -> None:
        from llm_autoresearch.judge import build_judge_prompt

        goal_state = _sample_goal_state()
        prompt = build_judge_prompt(
            goal_state=goal_state,
            candidate_kb="# Knowledge Base\nSpecific candidate content.",
            benchmark_answers=[],
        )
        self.assertIn("Specific candidate content", prompt)

    def test_prompt_includes_benchmark_answers(self) -> None:
        from llm_autoresearch.judge import build_judge_prompt

        goal_state = _sample_goal_state()
        answers = [BenchmarkAnswer(id="q1", answer="The answer is X", citations=["src1"])]
        prompt = build_judge_prompt(
            goal_state=goal_state,
            candidate_kb="# KB",
            benchmark_answers=answers,
        )
        self.assertIn("The answer is X", prompt)


# ---------------------------------------------------------------------------
# Test: run_judge (orchestration)
# ---------------------------------------------------------------------------

class TestRunJudge(unittest.TestCase):
    """Test the run_judge orchestration function."""

    def test_run_judge_returns_report(self) -> None:
        """run_judge should build task, invoke provider, parse response, return JudgeReport."""
        from llm_autoresearch.judge import JudgeReport, run_judge

        mock_provider = MagicMock()
        mock_provider.invoke.return_value = _valid_judge_response()

        report = run_judge(
            goal_state=_sample_goal_state(),
            candidate_kb="# KB\nContent.",
            benchmark_answers=[],
            judge_provider=mock_provider,
        )

        self.assertIsInstance(report, JudgeReport)
        self.assertAlmostEqual(report.overall_score, 0.55)
        # Provider was invoked with a ProviderTask
        mock_provider.invoke.assert_called_once()
        task = mock_provider.invoke.call_args[0][0]
        self.assertIsInstance(task, ProviderTask)
        self.assertEqual(task.task_type, "judge_evaluation")

    def test_run_judge_provider_crash_raises_provider_error(self) -> None:
        """When the provider crashes, run_judge should propagate ProviderError."""
        from llm_autoresearch.judge import run_judge

        mock_provider = MagicMock()
        mock_provider.invoke.side_effect = ProviderError("CLI crashed")

        with self.assertRaises(ProviderError):
            run_judge(
                goal_state=_sample_goal_state(),
                candidate_kb="# KB",
                benchmark_answers=[],
                judge_provider=mock_provider,
            )


# ---------------------------------------------------------------------------
# Test: EvaluationConfig.gate_threshold
# ---------------------------------------------------------------------------

class TestGateThreshold(unittest.TestCase):
    """Test that EvaluationConfig has a gate_threshold field."""

    def test_gate_threshold_default(self) -> None:
        config = EvaluationConfig()
        self.assertAlmostEqual(config.gate_threshold, 0.0)

    def test_gate_threshold_from_dict(self) -> None:
        config = EvaluationConfig.from_dict({"gate_threshold": 0.3})
        self.assertAlmostEqual(config.gate_threshold, 0.3)

    def test_gate_threshold_to_dict(self) -> None:
        config = EvaluationConfig(gate_threshold=0.5)
        d = config.to_dict()
        self.assertIn("gate_threshold", d)
        self.assertAlmostEqual(d["gate_threshold"], 0.5)

    def test_gate_threshold_roundtrip(self) -> None:
        original = EvaluationConfig(minimum_improvement=0.02, gate_threshold=0.25)
        restored = EvaluationConfig.from_dict(original.to_dict())
        self.assertAlmostEqual(restored.gate_threshold, 0.25)
        self.assertAlmostEqual(restored.minimum_improvement, 0.02)


# ---------------------------------------------------------------------------
# Test: Scoring flow (gate logic)
# ---------------------------------------------------------------------------

class TestScoringFlow(unittest.TestCase):
    """Test the deterministic gate + judge scoring flow."""

    def test_gate_auto_discards_below_threshold(self) -> None:
        """If deterministic score < gate_threshold, should_invoke_judge returns False."""
        from llm_autoresearch.judge import should_invoke_judge

        # deterministic_score=0.1, gate_threshold=0.3 => below threshold => no judge
        result = should_invoke_judge(deterministic_score=0.1, gate_threshold=0.3)
        self.assertFalse(result)

    def test_gate_passes_above_threshold(self) -> None:
        """If deterministic score >= gate_threshold, should_invoke_judge returns True."""
        from llm_autoresearch.judge import should_invoke_judge

        result = should_invoke_judge(deterministic_score=0.5, gate_threshold=0.3)
        self.assertTrue(result)

    def test_gate_passes_at_exact_threshold(self) -> None:
        """If deterministic score == gate_threshold, should_invoke_judge returns True."""
        from llm_autoresearch.judge import should_invoke_judge

        result = should_invoke_judge(deterministic_score=0.3, gate_threshold=0.3)
        self.assertTrue(result)

    def test_gate_with_default_threshold_always_passes(self) -> None:
        """Default gate_threshold=0.0 means the gate always passes (even score=0.0)."""
        from llm_autoresearch.judge import should_invoke_judge

        result = should_invoke_judge(deterministic_score=0.0, gate_threshold=0.0)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
