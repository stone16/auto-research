#!/usr/bin/env python3
"""Walk a getuai-like directory tree and emit per-repo raw markdown extracts.

Usage: python scripts/extract_sources.py <getuai_root> <output_dir>

For each subdirectory of <getuai_root> not starting with '.', extract:
- README.md (top level)
- CLAUDE.md / AGENTS.md / agents.md (top level)
- Every *.md under skills/, .claude/skills/, .cursor/skills/, .agents/skills/

Emit one markdown file per repo with structured sections.
"""
from __future__ import annotations

import sys
from pathlib import Path


SKILL_DIR_PATTERNS = [
    "skills",
    ".claude/skills",
    ".cursor/skills",
    ".agents/skills",
]
TOP_LEVEL_DOCS = ["README.md", "CLAUDE.md", "AGENTS.md", "agents.md"]
MAX_SKILL_BYTES = 8000  # truncate huge skill files to keep extracts manageable


def safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def extract_repo(repo_path: Path) -> str:
    """Return a markdown string for one repo."""
    sections: list[str] = [f"# Repo: {repo_path.name}\n"]

    for fname in TOP_LEVEL_DOCS:
        f = repo_path / fname
        if f.is_file():
            content = safe_read(f)
            if content is not None:
                sections.append(f"\n## {fname}\n```markdown\n{content}\n```\n")

    for pattern in SKILL_DIR_PATTERNS:
        skill_dir = repo_path / pattern
        if not skill_dir.is_dir():
            continue
        for skill_md in sorted(skill_dir.rglob("*.md")):
            try:
                rel = skill_md.relative_to(repo_path)
            except ValueError:
                continue
            content = safe_read(skill_md)
            if content is None:
                continue
            if len(content) > MAX_SKILL_BYTES:
                content = content[:MAX_SKILL_BYTES] + "\n\n[... truncated to 8KB ...]\n"
            sections.append(f"\n## {rel}\n```markdown\n{content}\n```\n")

    return "".join(sections)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_sources.py <getuai_root> <output_dir>", file=sys.stderr)
        return 2
    root = Path(argv[1])
    out_dir = Path(argv[2])
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        markdown = extract_repo(child)
        out = out_dir / f"{child.name}.md"
        out.write_text(markdown, encoding="utf-8")
        count += 1
        print(f"wrote {out}")

    print(f"\ntotal: {count} repos extracted")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
