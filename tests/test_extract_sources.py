"""Tests for extract_sources.py."""
from pathlib import Path
import subprocess
import sys


SCRIPT = Path("scripts/extract_sources.py")
FIXTURES = Path("tests/fixtures/fake_getuai")


def test_script_exists():
    assert SCRIPT.exists()


def test_extracts_readme_and_claude_and_skill(tmp_path):
    """Running extract on the fixture tree produces one markdown file per repo containing all relevant content."""
    out_dir = tmp_path / "_raw"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES), str(out_dir)],
        check=True,
        cwd=Path.cwd(),
    )
    # one .md per repo
    files = sorted(out_dir.glob("*.md"))
    assert {p.stem for p in files} == {"repo-a", "repo-b"}, [p.stem for p in files]

    # repo-a content checks
    repo_a = (out_dir / "repo-a.md").read_text()
    assert "# Repo: repo-a" in repo_a
    assert "## README.md" in repo_a
    assert "This is repo-a's README" in repo_a
    assert "## CLAUDE.md" in repo_a
    assert "address the user as Tester" in repo_a
    assert "## skills/skill-1/SKILL.md" in repo_a
    assert "name: skill-1" in repo_a

    # repo-b minimal content
    repo_b = (out_dir / "repo-b.md").read_text()
    assert "# Repo: repo-b" in repo_b
    assert "Repo-b is similar but different" in repo_b


def test_skips_dotfile_repos(tmp_path):
    """A directory starting with '.' is not treated as a repo."""
    fake = tmp_path / "fake_getuai"
    (fake / ".cache" / "skills").mkdir(parents=True)
    (fake / ".cache" / "skills" / "S.md").write_text("not a repo")
    (fake / "real-repo").mkdir()
    (fake / "real-repo" / "README.md").write_text("# real")
    out = tmp_path / "out"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(fake), str(out)],
        check=True,
        cwd=Path.cwd(),
    )
    assert (out / "real-repo.md").exists()
    assert not (out / ".cache.md").exists()
