"""Git operations for the autoresearch keep/discard loop.

All functions accept a ``cwd`` parameter so callers can point at the repo root
or run directory.  Git is invoked via ``subprocess.run`` -- no external
dependencies.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

COMMIT_PREFIX = "autoresearch:"
BRANCH_PREFIX = "autoresearch/"
TRACKED_FILES = ("knowledge_base.md", "state.json", "results.tsv")


def _git(
    args: list[str],
    cwd: Path,
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a git command, returning the CompletedProcess."""
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
    )


def init_branch(tag: str, *, cwd: Path) -> str:
    """Create and switch to ``autoresearch/<tag>``.

    Raises ``ValueError`` if the branch already exists so that callers never
    silently resume a previous run.

    Returns the branch name.
    """
    branch_name = f"{BRANCH_PREFIX}{tag}"

    # Check whether branch already exists (local)
    result = _git(["rev-parse", "--verify", branch_name], cwd=cwd, check=False)
    if result.returncode == 0:
        raise ValueError(
            f"Branch '{branch_name}' already exists. "
            "Delete it manually or choose a different tag to avoid silent resume."
        )

    _git(["checkout", "-b", branch_name], cwd=cwd)
    logger.info("Created and switched to branch %s", branch_name)
    return branch_name


def commit_iteration(
    iteration: int,
    experiment_title: str,
    *,
    cwd: Path,
) -> str | None:
    """Stage tracked files and create a prefixed commit.

    Only stages ``knowledge_base.md``, ``state.json``, and ``results.tsv``.
    Artifact directories are intentionally NOT committed.

    Returns the commit SHA on success, or ``None`` if there was nothing to
    commit (all tracked files are unchanged or missing).
    """
    # Stage only the files we care about (ignoring those that don't exist)
    staged_any = False
    for filename in TRACKED_FILES:
        filepath = cwd / filename
        if filepath.exists():
            result = _git(["add", filename], cwd=cwd, check=False)
            if result.returncode == 0:
                staged_any = True

    if not staged_any:
        logger.warning("commit_iteration: no tracked files found to stage")
        return None

    # Check if there are actually staged changes
    diff_result = _git(["diff", "--cached", "--quiet"], cwd=cwd, check=False)
    if diff_result.returncode == 0:
        # No staged changes -- nothing to commit
        logger.info("commit_iteration: no changes to commit for iteration %d", iteration)
        return None

    message = f"{COMMIT_PREFIX} [{iteration:04d}] {experiment_title}"
    _git(["commit", "-m", message], cwd=cwd)

    sha = _git(["rev-parse", "HEAD"], cwd=cwd).stdout.strip()
    logger.info("Committed iteration %d: %s (%s)", iteration, experiment_title, sha[:8])
    return sha


def reset_last_commit(*, cwd: Path) -> bool:
    """Undo the most recent commit if it is an autoresearch iteration commit.

    Uses ``git reset HEAD~1`` (mixed reset) so the changes go back to the
    working tree.

    Returns ``True`` if the reset was performed, ``False`` if the safety check
    blocked it (commit message does not start with the expected prefix).
    """
    result = _git(["log", "-1", "--pretty=%s"], cwd=cwd, check=False)
    if result.returncode != 0:
        logger.error("reset_last_commit: could not read last commit message")
        return False

    last_message = result.stdout.strip()
    if not last_message.startswith(COMMIT_PREFIX):
        logger.error(
            "reset_last_commit: refusing to reset -- last commit message "
            "'%s' does not start with '%s'",
            last_message,
            COMMIT_PREFIX,
        )
        return False

    _git(["reset", "HEAD~1"], cwd=cwd)
    logger.info("Reset last commit: %s", last_message)
    return True


def get_current_sha(*, cwd: Path) -> str:
    """Return the full 40-character SHA of HEAD."""
    return _git(["rev-parse", "HEAD"], cwd=cwd).stdout.strip()


def ensure_clean_state(*, cwd: Path) -> None:
    """Raise ``RuntimeError`` if the current run has staged or unstaged changes
    to ratchet-managed files.

    Untracked files and unrelated repo changes are allowed -- the loop only
    needs a clean state for the files it commits itself.
    """
    pathspec = ["--", *TRACKED_FILES]
    staged = _git(["diff", "--cached", "--quiet", *pathspec], cwd=cwd, check=False)
    unstaged = _git(["diff", "--quiet", *pathspec], cwd=cwd, check=False)

    if staged.returncode != 0 or unstaged.returncode != 0:
        status_output = _git(
            ["status", "--short", *pathspec],
            cwd=cwd,
            check=False,
        ).stdout.strip()
        raise RuntimeError(
            "Working tree is dirty -- staged or unstaged changes detected. "
            "Commit or reset the run files before running the autoresearch loop.\n"
            f"git status:\n{status_output}"
        )
