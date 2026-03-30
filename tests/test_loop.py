"""Tests for the loop CLI subcommand and run_loop orchestration (Checkpoint 06a).

Tests cover:
- StopConditions dataclass in models.py
- MockProvider handling judge_evaluation task type
- run_iteration with optional judge_provider parameter
- run_loop continuous iteration with mock producer and mock judge
- loop CLI subcommand argument parsing
- Integration: 3 iterations with results.tsv, git log, and knowledge_base.md assertions
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _run_git(args: list[str], cwd: Path) -> str:
    """Helper to run git commands in tests."""
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _init_test_repo(run_dir: Path) -> None:
    """Initialize a git repo in the run_dir's parent (or run_dir itself)."""
    _run_git(["init"], cwd=run_dir)
    _run_git(["config", "user.email", "test@example.com"], cwd=run_dir)
    _run_git(["config", "user.name", "Test User"], cwd=run_dir)
    # Create initial commit so we have a branch
    (run_dir / "README.md").write_text("# Test\n")
    _run_git(["add", "README.md"], cwd=run_dir)
    _run_git(["commit", "-m", "Initial commit"], cwd=run_dir)


# ---------------------------------------------------------------------------
# Test: StopConditions dataclass
# ---------------------------------------------------------------------------


class TestStopConditions(unittest.TestCase):
    """Test that StopConditions dataclass exists with the right fields."""

    def test_stop_conditions_default(self) -> None:
        """StopConditions with no args should have max_iterations=None."""
        from llm_autoresearch.models import StopConditions

        sc = StopConditions()
        self.assertIsNone(sc.max_iterations)

    def test_stop_conditions_with_max_iterations(self) -> None:
        """StopConditions should accept max_iterations."""
        from llm_autoresearch.models import StopConditions

        sc = StopConditions(max_iterations=5)
        self.assertEqual(sc.max_iterations, 5)


# ---------------------------------------------------------------------------
# Test: MockProvider handles judge_evaluation
# ---------------------------------------------------------------------------


class TestMockProviderJudge(unittest.TestCase):
    """Test that MockProvider can handle judge_evaluation task type."""

    def test_mock_provider_judge_evaluation_returns_valid_response(self) -> None:
        """MockProvider should return a valid judge response for judge_evaluation tasks."""
        from llm_autoresearch.providers import MockProvider, ProviderTask

        provider = MockProvider()
        task = ProviderTask(
            task_type="judge_evaluation",
            instructions="Evaluate the candidate.",
            payload={
                "goal_state": {
                    "done_definition": "Complete understanding.",
                    "dimensions": [
                        {"name": "causal_completeness", "description": "All causal links"},
                        {"name": "evidence_density", "description": "Claims backed by sources"},
                    ],
                },
                "candidate_kb": "# Knowledge Base\nContent.",
                "benchmark_answers": [],
            },
        )
        result = provider.invoke(task)

        # Must have all required judge response keys
        self.assertIn("dimension_scores", result)
        self.assertIn("review_markdown", result)
        self.assertIn("priority_dimension", result)
        self.assertIn("improvement_suggestion", result)

        # dimension_scores should have entries for the configured dimensions
        scores = result["dimension_scores"]
        self.assertIn("causal_completeness", scores)
        self.assertIn("evidence_density", scores)

        # Scores should be integers 0-10
        for name, score in scores.items():
            self.assertIsInstance(score, int)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 10)


# ---------------------------------------------------------------------------
# Test: run_iteration with judge_provider
# ---------------------------------------------------------------------------


class TestRunIterationWithJudge(unittest.TestCase):
    """Test that run_iteration accepts an optional judge_provider."""

    def test_run_iteration_without_judge_still_works(self) -> None:
        """Backward compat: run_iteration without judge_provider should work."""
        from llm_autoresearch.loop import run_iteration
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            outcome = run_iteration(run_dir, provider_kind="mock")
            self.assertEqual(outcome.iteration, 1)
            self.assertIn(outcome.status, ("keep", "discard"))

    def test_run_iteration_with_mock_judge(self) -> None:
        """run_iteration with a mock judge_provider should work and return an outcome."""
        from llm_autoresearch.loop import run_iteration
        from llm_autoresearch.providers import MockProvider
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            judge = MockProvider()
            outcome = run_iteration(run_dir, provider_kind="mock", judge_provider=judge)
            self.assertEqual(outcome.iteration, 1)
            self.assertIn(outcome.status, ("keep", "discard"))


# ---------------------------------------------------------------------------
# Test: run_loop function
# ---------------------------------------------------------------------------


class TestRunLoop(unittest.TestCase):
    """Test the run_loop orchestration function."""

    def test_run_loop_exists(self) -> None:
        """run_loop should be importable from loop module."""
        from llm_autoresearch.loop import run_loop

        self.assertTrue(callable(run_loop))

    def test_run_loop_3_iterations_returns_outcomes(self) -> None:
        """run_loop with max_iterations=3 should return 3 outcomes."""
        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            stop = StopConditions(max_iterations=3)
            outcomes = run_loop(
                run_dir=run_dir,
                producer_kind="mock",
                judge_kind="mock",
                tag="test-loop",
                stop_conditions=stop,
            )
            self.assertEqual(len(outcomes), 3)
            for i, outcome in enumerate(outcomes, start=1):
                self.assertEqual(outcome.iteration, i)


# ---------------------------------------------------------------------------
# Test: loop CLI subcommand argument parsing
# ---------------------------------------------------------------------------


class TestLoopCLI(unittest.TestCase):
    """Test that the loop CLI subcommand parses arguments correctly."""

    def test_loop_subcommand_exists(self) -> None:
        """build_parser should have a 'loop' subcommand."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/test", "--tag", "t1"])
        self.assertEqual(args.subcommand, "loop")
        self.assertEqual(args.run_dir, "/tmp/test")
        self.assertEqual(args.tag, "t1")

    def test_loop_producer_flag(self) -> None:
        """--producer flag should accept mock, codex, claude."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x", "--producer", "codex"])
        self.assertEqual(args.producer, "codex")

    def test_loop_judge_flag(self) -> None:
        """--judge flag should accept mock, codex, claude."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x", "--judge", "claude"])
        self.assertEqual(args.judge, "claude")

    def test_loop_max_iterations_flag(self) -> None:
        """--max-iterations flag should be parsed as int."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x", "--max-iterations", "5"])
        self.assertEqual(args.max_iterations, 5)

    def test_loop_max_iterations_default_none(self) -> None:
        """--max-iterations should default to None."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x"])
        self.assertIsNone(args.max_iterations)

    def test_loop_producer_default_mock(self) -> None:
        """--producer should default to mock."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x"])
        self.assertEqual(args.producer, "mock")

    def test_loop_judge_default_mock(self) -> None:
        """--judge should default to mock."""
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x"])
        self.assertEqual(args.judge, "mock")


# ---------------------------------------------------------------------------
# Test: Integration - 3 iterations, results.tsv, git log, knowledge_base
# ---------------------------------------------------------------------------


class TestLoopIntegration(unittest.TestCase):
    """Integration test: run 3 iterations with mock producer and mock judge.

    Asserts:
    (a) 3 entries in results.tsv
    (b) git log shows only "keep" commits (no discarded commits remain)
    (c) knowledge_base.md reflects the latest kept version
    """

    def test_full_loop_integration(self) -> None:
        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "integration-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            stop = StopConditions(max_iterations=3)
            outcomes = run_loop(
                run_dir=run_dir,
                producer_kind="mock",
                judge_kind="mock",
                tag="integration",
                stop_conditions=stop,
            )

            # (a) 3 entries in results.tsv (excluding header)
            results_path = run_dir / "results.tsv"
            self.assertTrue(results_path.exists())
            with results_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f, delimiter="\t")
                rows = list(reader)
            self.assertEqual(len(rows), 3, f"Expected 3 result rows, got {len(rows)}")

            # (b) git log should show only "keep" commits
            # All autoresearch commits in git log should be for "keep" iterations
            # (discarded iterations should have been reset)
            log_output = _run_git(["log", "--oneline"], cwd=run_dir)
            kept_iterations = [o for o in outcomes if o.status == "keep"]
            discarded_iterations = [o for o in outcomes if o.status == "discard"]

            for kept in kept_iterations:
                self.assertIn(
                    kept.experiment_title,
                    log_output,
                    f"Kept iteration '{kept.experiment_title}' should be in git log",
                )

            for discarded in discarded_iterations:
                self.assertNotIn(
                    discarded.experiment_title,
                    log_output,
                    f"Discarded iteration '{discarded.experiment_title}' should NOT be in git log",
                )

            # (c) knowledge_base.md should reflect the latest kept version
            kb_content = (run_dir / "knowledge_base.md").read_text(encoding="utf-8")
            # The mock provider generates KB with iteration number,
            # so the latest kept version should reference the highest kept iteration
            if kept_iterations:
                last_kept = max(kept_iterations, key=lambda o: o.iteration)
                # Mock provider generates "Iteration: N" in the KB
                self.assertIn(
                    f"Iteration: {last_kept.iteration}",
                    kb_content,
                    "knowledge_base.md should reflect the latest kept iteration",
                )

    def test_iterate_subcommand_still_works(self) -> None:
        """After adding the loop subcommand, iterate should still work for single-step runs."""
        from llm_autoresearch.cli import main
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "single-step"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)

            code = main(["iterate", str(run_dir), "--provider", "mock"])
            self.assertEqual(code, 0)


# ---------------------------------------------------------------------------
# Test: One-line summary output
# ---------------------------------------------------------------------------


class TestLoopSummaryOutput(unittest.TestCase):
    """Test that each iteration prints a one-line summary."""

    def test_loop_prints_iteration_summaries(self) -> None:
        """run_loop should print one-line summaries; we verify via capsys-like approach."""
        import io
        from contextlib import redirect_stdout

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "summary-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            stop = StopConditions(max_iterations=2)
            buf = io.StringIO()
            with redirect_stdout(buf):
                run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="summary-test",
                    stop_conditions=stop,
                )

            output = buf.getvalue()
            # Each iteration should produce a one-line summary matching the format:
            # iteration N | score X.XX | status keep/discard | dimension: <priority>
            self.assertIn("iteration 1", output.lower())
            self.assertIn("iteration 2", output.lower())
            self.assertIn("score", output.lower())
            self.assertIn("status", output.lower())


if __name__ == "__main__":
    unittest.main()
