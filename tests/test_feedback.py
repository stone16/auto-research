"""Tests for the feedback engine module (Checkpoint 05).

Tests cover:
- append_judge_feedback: single and multiple entries, file accumulation
- load_feedback_context: recent_n filtering, character cap, cold-start
- human_feedback hot-reload
- save_judge_review: artifact file creation
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import tempfile

from llm_autoresearch.judge import JudgeReport
from llm_autoresearch.run_files import RunPaths, build_paths


def _make_paths(tmp: Path) -> RunPaths:
    """Build RunPaths pointing at a temp directory."""
    paths = build_paths(tmp)
    paths.run_dir.mkdir(parents=True, exist_ok=True)
    paths.artifacts_dir.mkdir(parents=True, exist_ok=True)
    return paths


def _sample_report(
    review: str = "Good coverage but weak evidence.",
    priority: str = "evidence_density",
    suggestion: str = "Add more citations from source-3.",
) -> JudgeReport:
    return JudgeReport(
        dimension_scores={"causal_completeness": 0.7, "evidence_density": 0.4},
        overall_score=0.55,
        review_markdown=review,
        priority_dimension=priority,
        improvement_suggestion=suggestion,
    )


# ---------------------------------------------------------------------------
# Test: append_judge_feedback
# ---------------------------------------------------------------------------

class TestAppendJudgeFeedback(unittest.TestCase):
    """Test that judge feedback is appended correctly to judge_feedback.md."""

    def test_append_single_entry(self) -> None:
        """Appending one entry creates judge_feedback.md with an Iteration section."""
        from llm_autoresearch.feedback import append_judge_feedback

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            report = _sample_report()
            append_judge_feedback(paths, report, iteration=1)

            fb_path = paths.judge_feedback_path
            self.assertTrue(fb_path.exists())
            content = fb_path.read_text(encoding="utf-8")
            self.assertIn("## Iteration 1", content)
            self.assertIn("**Priority dimension**: evidence_density", content)
            self.assertIn("**Improvement suggestion**: Add more citations from source-3.", content)
            self.assertIn("### Review", content)
            self.assertIn("Good coverage but weak evidence.", content)

    def test_append_multiple_entries_accumulate(self) -> None:
        """Appending multiple entries grows the file with multiple sections."""
        from llm_autoresearch.feedback import append_judge_feedback

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            for i in range(1, 4):
                report = _sample_report(review=f"Review for iteration {i}")
                append_judge_feedback(paths, report, iteration=i)

            content = paths.judge_feedback_path.read_text(encoding="utf-8")
            self.assertIn("## Iteration 1", content)
            self.assertIn("## Iteration 2", content)
            self.assertIn("## Iteration 3", content)
            self.assertIn("Review for iteration 1", content)
            self.assertIn("Review for iteration 3", content)


# ---------------------------------------------------------------------------
# Test: load_feedback_context
# ---------------------------------------------------------------------------

class TestLoadFeedbackContext(unittest.TestCase):
    """Test loading feedback context with recent_n and character cap."""

    def test_cold_start_returns_empty(self) -> None:
        """When no feedback files exist, both keys are empty strings."""
        from llm_autoresearch.feedback import load_feedback_context

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            result = load_feedback_context(paths)

            self.assertIsInstance(result, dict)
            self.assertEqual(result["judge_feedback"], "")
            self.assertEqual(result["human_feedback"], "")

    def test_recent_n_filters_entries(self) -> None:
        """load_feedback_context with recent_n=2 returns only last 2 iteration sections."""
        from llm_autoresearch.feedback import append_judge_feedback, load_feedback_context

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            for i in range(1, 6):
                report = _sample_report(review=f"Review-{i}")
                append_judge_feedback(paths, report, iteration=i)

            result = load_feedback_context(paths, recent_n=2)
            judge_fb = result["judge_feedback"]

            # Should contain iterations 4 and 5
            self.assertIn("## Iteration 4", judge_fb)
            self.assertIn("## Iteration 5", judge_fb)
            self.assertIn("Review-4", judge_fb)
            self.assertIn("Review-5", judge_fb)
            # Should NOT contain iterations 1, 2, 3
            self.assertNotIn("## Iteration 1", judge_fb)
            self.assertNotIn("## Iteration 2", judge_fb)
            self.assertNotIn("## Iteration 3", judge_fb)

    def test_character_cap_truncation(self) -> None:
        """Total returned text is capped at 4000 characters, oldest entries trimmed first."""
        from llm_autoresearch.feedback import append_judge_feedback, load_feedback_context

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            # Create entries with large review text to exceed cap
            for i in range(1, 20):
                report = _sample_report(review="X" * 500 + f" iter-{i}")
                append_judge_feedback(paths, report, iteration=i)

            result = load_feedback_context(paths, recent_n=19)
            total_len = len(result["judge_feedback"]) + len(result["human_feedback"])
            self.assertLessEqual(total_len, 4000)
            # Most recent entry should still be present
            self.assertIn("iter-19", result["judge_feedback"])

    def test_character_cap_with_human_feedback(self) -> None:
        """Character cap accounts for human_feedback length too."""
        from llm_autoresearch.feedback import append_judge_feedback, load_feedback_context

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            # Write large human feedback
            paths.human_feedback_path.write_text("H" * 3000, encoding="utf-8")
            # Add judge entries
            for i in range(1, 10):
                report = _sample_report(review="Y" * 500 + f" iter-{i}")
                append_judge_feedback(paths, report, iteration=i)

            result = load_feedback_context(paths, recent_n=9)
            total_len = len(result["judge_feedback"]) + len(result["human_feedback"])
            self.assertLessEqual(total_len, 4000)
            # Human feedback should be fully included
            self.assertEqual(result["human_feedback"], "H" * 3000)

    def test_human_feedback_hot_reload(self) -> None:
        """human_feedback.md is read fresh each time (hot-reload)."""
        from llm_autoresearch.feedback import load_feedback_context

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))

            # First: no file
            result1 = load_feedback_context(paths)
            self.assertEqual(result1["human_feedback"], "")

            # Write file
            paths.human_feedback_path.write_text("Focus on citations.", encoding="utf-8")
            result2 = load_feedback_context(paths)
            self.assertEqual(result2["human_feedback"], "Focus on citations.")

            # Modify file
            paths.human_feedback_path.write_text("Now focus on clarity.", encoding="utf-8")
            result3 = load_feedback_context(paths)
            self.assertEqual(result3["human_feedback"], "Now focus on clarity.")

    def test_missing_human_feedback_returns_empty(self) -> None:
        """If human_feedback.md does not exist, returns empty string."""
        from llm_autoresearch.feedback import load_feedback_context

        with tempfile.TemporaryDirectory() as tmp:
            paths = _make_paths(Path(tmp))
            result = load_feedback_context(paths)
            self.assertEqual(result["human_feedback"], "")


# ---------------------------------------------------------------------------
# Test: save_judge_review
# ---------------------------------------------------------------------------

class TestSaveJudgeReview(unittest.TestCase):
    """Test that judge_review.md is saved correctly to artifact dir."""

    def test_saves_review_file(self) -> None:
        """save_judge_review writes judge_review.md with the review_markdown content."""
        from llm_autoresearch.feedback import save_judge_review

        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifacts" / "iteration-0001"
            artifact_dir.mkdir(parents=True, exist_ok=True)

            report = _sample_report(review="Detailed review of iteration 1.")
            save_judge_review(artifact_dir, report)

            review_path = artifact_dir / "judge_review.md"
            self.assertTrue(review_path.exists())
            content = review_path.read_text(encoding="utf-8")
            self.assertIn("Detailed review of iteration 1.", content)


# ---------------------------------------------------------------------------
# Test: RunPaths has feedback path attributes
# ---------------------------------------------------------------------------

class TestRunPathsFeedbackAttributes(unittest.TestCase):
    """Test that RunPaths exposes judge_feedback_path and human_feedback_path."""

    def test_judge_feedback_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_paths(Path(tmp))
            self.assertEqual(paths.judge_feedback_path, Path(tmp) / "judge_feedback.md")

    def test_human_feedback_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_paths(Path(tmp))
            self.assertEqual(paths.human_feedback_path, Path(tmp) / "human_feedback.md")


# ---------------------------------------------------------------------------
# Test: loop.py integration - payload includes feedback keys
# ---------------------------------------------------------------------------

class TestLoopFeedbackIntegration(unittest.TestCase):
    """Test that run_iteration includes feedback keys in the producer payload."""

    def test_payload_contains_feedback_keys(self) -> None:
        """run_iteration should add judge_feedback and human_feedback to the payload."""
        from unittest.mock import patch, MagicMock
        from llm_autoresearch.loop import run_iteration
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)

            # Write human feedback so we can verify it's picked up
            paths = build_paths(run_dir)
            paths.human_feedback_path.write_text("Focus on citations.", encoding="utf-8")

            # Patch the provider to capture the ProviderTask
            captured_tasks: list = []

            original_create_provider = None
            from llm_autoresearch import providers as providers_mod
            original_create = providers_mod.create_provider

            class SpyProvider:
                def __init__(self, real_provider):
                    self._real = real_provider

                def invoke(self, task):
                    captured_tasks.append(task)
                    return self._real.invoke(task)

            def spy_create_provider(kind, **kwargs):
                real = original_create(kind, **kwargs)
                return SpyProvider(real)

            with patch("llm_autoresearch.loop.create_provider", side_effect=spy_create_provider):
                run_iteration(run_dir, provider_kind="mock")

            self.assertEqual(len(captured_tasks), 1)
            payload = captured_tasks[0].payload
            self.assertIn("judge_feedback", payload)
            self.assertIn("human_feedback", payload)
            self.assertEqual(payload["human_feedback"], "Focus on citations.")
            # On first iteration with no judge feedback file, should be empty
            self.assertEqual(payload["judge_feedback"], "")


if __name__ == "__main__":
    unittest.main()
