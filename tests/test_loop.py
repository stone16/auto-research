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
from unittest.mock import patch

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


class TestRoleProviderResolution(unittest.TestCase):
    """Test provider resolution for producer/judge role configs."""

    def test_matching_role_cli_config_is_applied(self) -> None:
        from llm_autoresearch.loop import _create_provider_for_role
        from llm_autoresearch.models import CliAgentConfig

        role_config = CliAgentConfig(cli="codex", flags="exec --foo")

        with patch("llm_autoresearch.loop.create_provider") as mock_create:
            sentinel = object()
            mock_create.return_value = sentinel

            result = _create_provider_for_role("codex", role_config, role="producer")

        self.assertIs(result, sentinel)
        mock_create.assert_called_once_with(
            "codex",
            cli_binary="codex",
            cli_flags="exec --foo",
            role="producer",
        )

    def test_mismatched_role_cli_config_is_ignored(self) -> None:
        from llm_autoresearch.loop import _create_provider_for_role
        from llm_autoresearch.models import CliAgentConfig

        role_config = CliAgentConfig(
            cli="claude",
            flags="-p --dangerously-skip-permissions",
        )

        with patch("llm_autoresearch.loop.create_provider") as mock_create:
            sentinel = object()
            mock_create.return_value = sentinel

            result = _create_provider_for_role("codex", role_config, role="producer")

        self.assertIs(result, sentinel)
        mock_create.assert_called_once_with(
            "codex",
            cli_binary="",
            cli_flags="",
            role="producer",
        )


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


# ---------------------------------------------------------------------------
# Test: StopConditions new fields (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestStopConditionsExtended(unittest.TestCase):
    """Test that StopConditions has the new fields for 06b."""

    def test_max_consecutive_discard_default_none(self) -> None:
        from llm_autoresearch.models import StopConditions

        sc = StopConditions()
        self.assertIsNone(sc.max_consecutive_discard)

    def test_max_consecutive_discard_set(self) -> None:
        from llm_autoresearch.models import StopConditions

        sc = StopConditions(max_consecutive_discard=3)
        self.assertEqual(sc.max_consecutive_discard, 3)

    def test_dimension_threshold_default_none(self) -> None:
        from llm_autoresearch.models import StopConditions

        sc = StopConditions()
        self.assertIsNone(sc.dimension_threshold)

    def test_dimension_threshold_set(self) -> None:
        from llm_autoresearch.models import StopConditions

        sc = StopConditions(dimension_threshold=0.8)
        self.assertAlmostEqual(sc.dimension_threshold, 0.8)


# ---------------------------------------------------------------------------
# Test: IterationOutcome new field dimension_scores (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestIterationOutcomeDimensionScores(unittest.TestCase):
    """Test that IterationOutcome has a dimension_scores field."""

    def test_dimension_scores_default_none(self) -> None:
        from llm_autoresearch.models import IterationOutcome

        outcome = IterationOutcome(
            iteration=1,
            status="keep",
            candidate_score=0.5,
            previous_best=0.0,
            knowledge_chars=100,
            artifact_dir="/tmp/test",
            experiment_title="test",
            change_summary="test",
        )
        self.assertIsNone(outcome.dimension_scores)

    def test_dimension_scores_set(self) -> None:
        from llm_autoresearch.models import IterationOutcome

        scores = {"accuracy": 0.8, "coverage": 0.6}
        outcome = IterationOutcome(
            iteration=1,
            status="keep",
            candidate_score=0.7,
            previous_best=0.0,
            knowledge_chars=100,
            artifact_dir="/tmp/test",
            experiment_title="test",
            change_summary="test",
            dimension_scores=scores,
        )
        self.assertEqual(outcome.dimension_scores, scores)


# ---------------------------------------------------------------------------
# Test: max_consecutive_discard stop condition (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestMaxConsecutiveDiscard(unittest.TestCase):
    """Test that run_loop stops after N consecutive discards."""

    def test_stops_after_consecutive_discards(self) -> None:
        """run_loop should stop when max_consecutive_discard is exceeded.

        The mock provider produces deterministic results. We run enough
        iterations that all will be discards (after the first keep) and
        verify the loop stops at the right point.
        """
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "discard-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            # Make run_iteration always return "discard" outcomes
            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                return IterationOutcome(
                    iteration=call_count,
                    status="discard",
                    candidate_score=0.1,
                    previous_best=0.5,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="accuracy",
                )

            stop = StopConditions(max_consecutive_discard=3, max_iterations=100)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="discard-test",
                    stop_conditions=stop,
                )

            # Should have stopped after 3 consecutive discards
            self.assertEqual(len(outcomes), 3)

    def test_discard_counter_resets_on_keep(self) -> None:
        """If a 'keep' occurs, consecutive discard counter resets."""
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "reset-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            # Pattern: discard, discard, keep, discard, discard, discard (stop at 6)
            call_count = 0
            statuses = ["discard", "discard", "keep", "discard", "discard", "discard"]

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                idx = min(call_count - 1, len(statuses) - 1)
                return IterationOutcome(
                    iteration=call_count,
                    status=statuses[idx],
                    candidate_score=0.5 if statuses[idx] == "keep" else 0.1,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="accuracy",
                )

            stop = StopConditions(max_consecutive_discard=3, max_iterations=100)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="reset-test",
                    stop_conditions=stop,
                )

            # 6 iterations: 2 discards, 1 keep (resets), then 3 discards (triggers stop)
            self.assertEqual(len(outcomes), 6)


# ---------------------------------------------------------------------------
# Test: dimension_threshold stop condition (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestDimensionThreshold(unittest.TestCase):
    """Test that run_loop stops when all dimension scores exceed the threshold."""

    def test_stops_when_all_dimensions_above_threshold(self) -> None:
        """If all dimension scores are above threshold, loop should stop."""
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "threshold-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                # All dimension scores above 0.8 threshold
                return IterationOutcome(
                    iteration=call_count,
                    status="keep",
                    candidate_score=0.9,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="accuracy",
                    dimension_scores={"accuracy": 0.9, "coverage": 0.85},
                )

            stop = StopConditions(dimension_threshold=0.8, max_iterations=100)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="threshold-test",
                    stop_conditions=stop,
                )

            # Should stop after 1 iteration since all scores are above threshold
            self.assertEqual(len(outcomes), 1)

    def test_continues_when_some_dimensions_below_threshold(self) -> None:
        """If some dimension scores are below threshold, loop continues."""
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "below-threshold-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                # First 2 iterations: coverage below threshold; 3rd: all above
                if call_count < 3:
                    scores = {"accuracy": 0.9, "coverage": 0.5}
                else:
                    scores = {"accuracy": 0.9, "coverage": 0.85}
                return IterationOutcome(
                    iteration=call_count,
                    status="keep",
                    candidate_score=0.7,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="coverage",
                    dimension_scores=scores,
                )

            stop = StopConditions(dimension_threshold=0.8, max_iterations=100)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="below-test",
                    stop_conditions=stop,
                )

            # Should run 3 iterations (first 2 below threshold, 3rd triggers stop)
            self.assertEqual(len(outcomes), 3)

    def test_skips_threshold_check_when_no_dimension_scores(self) -> None:
        """If dimension_scores is None, threshold check is skipped."""
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "no-scores-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                return IterationOutcome(
                    iteration=call_count,
                    status="keep",
                    candidate_score=0.9,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="",
                    dimension_scores=None,  # No scores available
                )

            stop = StopConditions(dimension_threshold=0.8, max_iterations=3)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="no-scores-test",
                    stop_conditions=stop,
                )

            # Should run all 3 iterations (threshold check skipped without scores)
            self.assertEqual(len(outcomes), 3)


# ---------------------------------------------------------------------------
# Test: Crash recovery (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestCrashRecovery(unittest.TestCase):
    """Test that a crash in one iteration does not kill the loop."""

    def test_single_crash_does_not_kill_loop(self) -> None:
        """If run_iteration raises on one iteration, loop continues."""
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "crash-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                if call_count == 2:
                    raise RuntimeError("Simulated crash on iteration 2")
                return IterationOutcome(
                    iteration=call_count,
                    status="keep",
                    candidate_score=0.5,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="accuracy",
                )

            stop = StopConditions(max_iterations=3)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="crash-test",
                    stop_conditions=stop,
                )

            # Crashes don't consume iteration budget — 3 successful outcomes total
            self.assertEqual(len(outcomes), 3)

    def test_three_consecutive_crashes_halt_loop(self) -> None:
        """After 3 consecutive crashes, loop halts with diagnostic message."""
        import logging
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "multi-crash-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                raise RuntimeError(f"Simulated crash on iteration {call_count}")

            stop = StopConditions(max_iterations=10)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                with self.assertLogs("llm_autoresearch.loop", level=logging.ERROR) as cm:
                    outcomes = run_loop(
                        run_dir=run_dir,
                        producer_kind="mock",
                        judge_kind="mock",
                        tag="multi-crash-test",
                        stop_conditions=stop,
                    )

            # Should have 0 successful outcomes (all crashed)
            self.assertEqual(len(outcomes), 0)
            # Should have exactly 3 calls (halted after 3 consecutive crashes)
            self.assertEqual(call_count, 3)
            # Should log an error about consecutive crashes
            error_messages = [r for r in cm.output if "consecutive crash" in r.lower()]
            self.assertTrue(len(error_messages) > 0, "Should log consecutive crash halt message")

    def test_crash_counter_resets_on_success(self) -> None:
        """Consecutive crash counter resets after a successful iteration."""
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "crash-reset-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            call_count = 0
            # Pattern: crash, crash, success, crash, crash, crash (halt at 6)
            crash_pattern = [True, True, False, True, True, True]

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                idx = min(call_count - 1, len(crash_pattern) - 1)
                if crash_pattern[idx]:
                    raise RuntimeError(f"Simulated crash on call {call_count}")
                return IterationOutcome(
                    iteration=call_count,
                    status="keep",
                    candidate_score=0.5,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="accuracy",
                )

            stop = StopConditions(max_iterations=100)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="crash-reset-test",
                    stop_conditions=stop,
                )

            # Should have 1 successful outcome (call 3), then halt at call 6 (3 consecutive)
            self.assertEqual(len(outcomes), 1)
            self.assertEqual(call_count, 6)


# ---------------------------------------------------------------------------
# Test: SIGINT handling (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestSIGINTHandling(unittest.TestCase):
    """Test that SIGINT sets a shutdown event and the loop checks it."""

    def test_shutdown_event_stops_loop_immediately(self) -> None:
        """If shutdown event is set before loop runs, loop exits with 0 iterations."""
        import threading
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "sigint-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            # Pre-set the shutdown event
            shutdown = threading.Event()
            shutdown.set()

            stop = StopConditions(max_iterations=100)
            outcomes = run_loop(
                run_dir=run_dir,
                producer_kind="mock",
                judge_kind="mock",
                tag="sigint-test",
                stop_conditions=stop,
                shutdown_event=shutdown,
            )

            # Should exit immediately with no iterations
            self.assertEqual(len(outcomes), 0)

    def test_shutdown_event_after_first_iteration(self) -> None:
        """If shutdown event is set during first iteration, loop exits after that iteration."""
        import threading
        from unittest.mock import patch

        from llm_autoresearch.loop import run_loop
        from llm_autoresearch.models import IterationOutcome, StopConditions
        from llm_autoresearch.run_files import init_run

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "sigint-after-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            _init_test_repo(run_dir)

            shutdown = threading.Event()
            call_count = 0

            def mock_run_iteration(**kwargs):
                nonlocal call_count
                call_count += 1
                # Set shutdown after first iteration completes
                shutdown.set()
                return IterationOutcome(
                    iteration=call_count,
                    status="keep",
                    candidate_score=0.5,
                    previous_best=0.0,
                    knowledge_chars=100,
                    artifact_dir=str(run_dir / f"artifacts/iteration-{call_count:04d}"),
                    experiment_title=f"mock-{call_count}",
                    change_summary="test",
                    priority_dimension="accuracy",
                )

            stop = StopConditions(max_iterations=100)
            with patch("llm_autoresearch.loop.run_iteration", side_effect=mock_run_iteration):
                outcomes = run_loop(
                    run_dir=run_dir,
                    producer_kind="mock",
                    judge_kind="mock",
                    tag="sigint-after-test",
                    stop_conditions=stop,
                    shutdown_event=shutdown,
                )

            # Should have exactly 1 iteration (shutdown set after first)
            self.assertEqual(len(outcomes), 1)

    def test_sigint_handler_sets_event(self) -> None:
        """The install_sigint_handler function should set the event on simulated call."""
        import threading

        from llm_autoresearch.loop import install_sigint_handler

        shutdown = threading.Event()
        handler = install_sigint_handler(shutdown)

        # Verify event is not set initially
        self.assertFalse(shutdown.is_set())

        # Simulate calling the handler (signal number and frame are irrelevant)
        handler(2, None)  # SIGINT = signal 2

        # Event should now be set
        self.assertTrue(shutdown.is_set())


# ---------------------------------------------------------------------------
# Test: CLI flags for new stop conditions (Checkpoint 06b)
# ---------------------------------------------------------------------------


class TestLoopCLIExtended(unittest.TestCase):
    """Test new CLI flags --max-consecutive-discard and --dimension-threshold."""

    def test_max_consecutive_discard_flag(self) -> None:
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "loop", "/tmp/t", "--tag", "x", "--max-consecutive-discard", "5",
        ])
        self.assertEqual(args.max_consecutive_discard, 5)

    def test_max_consecutive_discard_default_none(self) -> None:
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x"])
        self.assertIsNone(args.max_consecutive_discard)

    def test_dimension_threshold_flag(self) -> None:
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "loop", "/tmp/t", "--tag", "x", "--dimension-threshold", "0.85",
        ])
        self.assertAlmostEqual(args.dimension_threshold, 0.85)

    def test_dimension_threshold_default_none(self) -> None:
        from llm_autoresearch.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["loop", "/tmp/t", "--tag", "x"])
        self.assertIsNone(args.dimension_threshold)

    def test_cmd_loop_passes_new_stop_conditions(self) -> None:
        """cmd_loop should pass new stop conditions to run_loop."""
        from unittest.mock import patch

        from llm_autoresearch.cli import cmd_loop

        # Create a namespace that simulates parsed args
        import argparse

        args = argparse.Namespace(
            run_dir="/tmp/test",
            tag="test",
            producer="mock",
            judge="mock",
            max_iterations=10,
            max_consecutive_discard=5,
            dimension_threshold=0.9,
        )

        with patch("llm_autoresearch.cli.run_loop", return_value=[]) as mock_loop:
            cmd_loop(args)
            call_kwargs = mock_loop.call_args
            stop = call_kwargs[1]["stop_conditions"] if "stop_conditions" in call_kwargs[1] else call_kwargs[0][4] if len(call_kwargs[0]) > 4 else None
            # Access via keyword args
            stop = mock_loop.call_args.kwargs.get("stop_conditions") or mock_loop.call_args[1].get("stop_conditions")
            self.assertIsNotNone(stop)
            self.assertEqual(stop.max_iterations, 10)
            self.assertEqual(stop.max_consecutive_discard, 5)
            self.assertAlmostEqual(stop.dimension_threshold, 0.9)


if __name__ == "__main__":
    unittest.main()
