"""Tests for compose_sources.py."""
from pathlib import Path
import json
import subprocess
import sys


SCRIPT = Path("scripts/compose_sources.py")


def setup_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    raw = tmp_path / "_raw"
    raw.mkdir()
    (raw / "alpha.md").write_text("# Repo: alpha\n## README.md\n```markdown\nALPHA-CONTENT\n```\n")
    (raw / "beta.md").write_text("# Repo: beta\n## README.md\n```markdown\nBETA-CONTENT\n```\n")
    (raw / "gamma.md").write_text("# Repo: gamma\n## README.md\n```markdown\nGAMMA-CONTENT\n```\n")
    mapping = tmp_path / "source_mapping.json"
    mapping.write_text(json.dumps({
        "source-foo": ["alpha", "beta"],
        "source-bar": ["*"],
    }))
    out_dir = tmp_path / "out"
    return raw, mapping, out_dir


def test_named_repos_are_concatenated(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    foo = (out / "source-foo.md").read_text()
    assert "ALPHA-CONTENT" in foo
    assert "BETA-CONTENT" in foo
    assert "GAMMA-CONTENT" not in foo  # not in source-foo's mapping


def test_wildcard_includes_all_repos(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    bar = (out / "source-bar.md").read_text()
    assert "ALPHA-CONTENT" in bar
    assert "BETA-CONTENT" in bar
    assert "GAMMA-CONTENT" in bar


def test_outputs_have_toc(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    foo = (out / "source-foo.md").read_text()
    assert "## Table of Contents" in foo
    assert "- alpha" in foo
    assert "- beta" in foo


def test_missing_repo_in_mapping_warns_but_succeeds(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    # add a mapping entry for a repo whose _raw file doesn't exist
    data = json.loads(mapping.read_text())
    data["source-foo"].append("nonexistent")
    mapping.write_text(json.dumps(data))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        capture_output=True, text=True, cwd=Path.cwd(),
    )
    assert result.returncode == 0  # graceful
    assert "WARNING" in result.stdout or "WARNING" in result.stderr


def test_max_bytes_per_repo_truncates(tmp_path):
    """Per-repo blocks are truncated to the max-bytes budget."""
    raw, mapping, out = setup_inputs(tmp_path)
    # alpha.md is 60 bytes; expand it to 5000 bytes so we can see truncation
    big_content = "# Repo: alpha\n## README.md\n```markdown\n" + ("X" * 5000) + "\n```\n"
    (raw / "alpha.md").write_text(big_content)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out),
         "--max-bytes-per-repo", "1000"],
        check=True, cwd=Path.cwd(),
    )
    foo = (out / "source-foo.md").read_text()
    # alpha's section should appear but be truncated
    assert "# Repo: alpha" in foo
    assert "[... truncated" in foo
    # the X's that exceeded the budget should NOT all be present
    assert foo.count("X") < 5000
    # beta should still be intact (only 60 bytes, well under 1000)
    assert "BETA-CONTENT" in foo


def test_default_budget_does_not_truncate_small_repos(tmp_path):
    """Default budget leaves small repos intact."""
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    foo = (out / "source-foo.md").read_text()
    # No truncation marker should appear since alpha and beta are tiny
    assert "[... truncated" not in foo
