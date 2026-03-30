from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.git import (
    COMMIT_PREFIX,
    commit_iteration,
    ensure_clean_state,
    get_current_sha,
    init_branch,
    reset_last_commit,
)


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


def _init_test_repo(tmp: Path) -> Path:
    """Create a minimal git repo with user config for CI compatibility."""
    repo = tmp / "repo"
    repo.mkdir()
    _run_git(["init"], cwd=repo)
    _run_git(["config", "user.email", "test@example.com"], cwd=repo)
    _run_git(["config", "user.name", "Test User"], cwd=repo)
    # Create initial commit so we have a branch
    (repo / "README.md").write_text("# Test\n")
    _run_git(["add", "README.md"], cwd=repo)
    _run_git(["commit", "-m", "Initial commit"], cwd=repo)
    return repo


class TestInitBranch(unittest.TestCase):
    def test_creates_branch_and_switches_to_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            init_branch("test-tag", cwd=repo)
            current = _run_git(["branch", "--show-current"], cwd=repo)
            self.assertEqual(current, "autoresearch/test-tag")

    def test_raises_if_branch_already_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            init_branch("duplicate", cwd=repo)
            # Switch back to main so we can try to create again
            _run_git(["checkout", "main"], cwd=repo)
            with self.assertRaises(ValueError) as ctx:
                init_branch("duplicate", cwd=repo)
            self.assertIn("already exists", str(ctx.exception))

    def test_tag_with_special_chars(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            init_branch("my-topic-2024", cwd=repo)
            current = _run_git(["branch", "--show-current"], cwd=repo)
            self.assertEqual(current, "autoresearch/my-topic-2024")


class TestCommitIteration(unittest.TestCase):
    def test_commits_tracked_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            # Create files that should be committed
            (repo / "knowledge_base.md").write_text("# KB\n")
            (repo / "state.json").write_text("{}\n")
            (repo / "results.tsv").write_text("header\n")

            sha = commit_iteration(
                iteration=1,
                experiment_title="test experiment",
                cwd=repo,
            )
            self.assertIsNotNone(sha)
            self.assertTrue(len(sha) >= 7)

            # Verify commit message
            log = _run_git(["log", "-1", "--pretty=%s"], cwd=repo)
            self.assertTrue(log.startswith(COMMIT_PREFIX))
            self.assertIn("test experiment", log)

    def test_commits_only_specified_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "knowledge_base.md").write_text("# KB\n")
            (repo / "state.json").write_text("{}\n")
            (repo / "results.tsv").write_text("header\n")
            (repo / "unrelated.txt").write_text("should not be committed\n")

            commit_iteration(iteration=1, experiment_title="test", cwd=repo)

            # unrelated.txt should still be untracked
            status = _run_git(["status", "--porcelain"], cwd=repo)
            self.assertIn("unrelated.txt", status)

    def test_returns_none_when_nothing_to_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            # No tracked files to commit
            sha = commit_iteration(
                iteration=1,
                experiment_title="empty",
                cwd=repo,
            )
            self.assertIsNone(sha)


class TestResetLastCommit(unittest.TestCase):
    def test_resets_autoresearch_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "knowledge_base.md").write_text("# KB iter 1\n")
            (repo / "state.json").write_text("{}\n")
            (repo / "results.tsv").write_text("header\n")

            sha_before = get_current_sha(cwd=repo)
            commit_iteration(iteration=1, experiment_title="to discard", cwd=repo)

            # Verify commit exists
            sha_after = get_current_sha(cwd=repo)
            self.assertNotEqual(sha_before, sha_after)

            # Reset it
            success = reset_last_commit(cwd=repo)
            self.assertTrue(success)

            sha_reset = get_current_sha(cwd=repo)
            self.assertEqual(sha_before, sha_reset)

    def test_refuses_to_reset_non_autoresearch_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            # The latest commit is "Initial commit" -- NOT an autoresearch commit
            sha_before = get_current_sha(cwd=repo)
            success = reset_last_commit(cwd=repo)
            self.assertFalse(success)
            sha_after = get_current_sha(cwd=repo)
            self.assertEqual(sha_before, sha_after)

    def test_reset_restores_files_to_working_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "knowledge_base.md").write_text("# KB\n")
            (repo / "state.json").write_text("{}\n")
            (repo / "results.tsv").write_text("header\n")

            commit_iteration(iteration=1, experiment_title="discard me", cwd=repo)

            # After reset, files should still exist in working tree (soft reset)
            reset_last_commit(cwd=repo)

            # Files should still exist on disk
            self.assertTrue((repo / "knowledge_base.md").exists())


class TestGetCurrentSha(unittest.TestCase):
    def test_returns_sha_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            sha = get_current_sha(cwd=repo)
            self.assertIsInstance(sha, str)
            self.assertEqual(len(sha), 40)  # Full SHA

    def test_sha_changes_after_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            sha1 = get_current_sha(cwd=repo)
            (repo / "knowledge_base.md").write_text("# KB\n")
            (repo / "state.json").write_text("{}\n")
            (repo / "results.tsv").write_text("header\n")
            commit_iteration(iteration=1, experiment_title="new", cwd=repo)
            sha2 = get_current_sha(cwd=repo)
            self.assertNotEqual(sha1, sha2)


class TestEnsureCleanState(unittest.TestCase):
    def test_clean_repo_does_not_raise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            # Should not raise
            ensure_clean_state(cwd=repo)

    def test_dirty_ratchet_file_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "knowledge_base.md").write_text("# KB\n")
            _run_git(["add", "knowledge_base.md"], cwd=repo)
            _run_git(["commit", "-m", "Add KB"], cwd=repo)
            (repo / "knowledge_base.md").write_text("# Modified\n")
            with self.assertRaises(RuntimeError) as ctx:
                ensure_clean_state(cwd=repo)
            self.assertIn("dirty", str(ctx.exception).lower())

    def test_staged_ratchet_changes_raise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "results.tsv").write_text("header\n")
            _run_git(["add", "results.tsv"], cwd=repo)
            _run_git(["commit", "-m", "Add results"], cwd=repo)
            (repo / "results.tsv").write_text("header\nrow1\n")
            _run_git(["add", "results.tsv"], cwd=repo)
            with self.assertRaises(RuntimeError) as ctx:
                ensure_clean_state(cwd=repo)
            self.assertIn("dirty", str(ctx.exception).lower())

    def test_untracked_files_are_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "some_new_file.txt").write_text("new\n")
            # Untracked files should NOT cause an error
            ensure_clean_state(cwd=repo)

    def test_unrelated_repo_changes_are_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            (repo / "README.md").write_text("# Modified outside ratchet\n")
            ensure_clean_state(cwd=repo)


class TestCommitResetIntegration(unittest.TestCase):
    """Integration test: commit then reset simulating keep/discard loop."""

    def test_keep_then_discard_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _init_test_repo(Path(tmp))
            init_branch("integration-test", cwd=repo)

            # Iteration 1: keep
            (repo / "knowledge_base.md").write_text("# KB v1\n")
            (repo / "state.json").write_text('{"iteration": 1}\n')
            (repo / "results.tsv").write_text("header\nrow1\n")
            sha1 = commit_iteration(iteration=1, experiment_title="kept iter", cwd=repo)
            self.assertIsNotNone(sha1)

            # Verify commit is in log
            log = _run_git(["log", "--oneline"], cwd=repo)
            self.assertIn("kept iter", log)

            # Iteration 2: discard
            (repo / "knowledge_base.md").write_text("# KB v2 bad\n")
            (repo / "state.json").write_text('{"iteration": 2}\n')
            (repo / "results.tsv").write_text("header\nrow1\nrow2\n")
            sha2 = commit_iteration(iteration=2, experiment_title="discarded iter", cwd=repo)
            self.assertIsNotNone(sha2)

            success = reset_last_commit(cwd=repo)
            self.assertTrue(success)

            # Discarded commit should not be in log
            log = _run_git(["log", "--oneline"], cwd=repo)
            self.assertNotIn("discarded iter", log)
            # But the kept commit should still be there
            self.assertIn("kept iter", log)


if __name__ == "__main__":
    unittest.main()
