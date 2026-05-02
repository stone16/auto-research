#!/usr/bin/env python3
"""Compose 10 source-*.md digests from per-repo raw extracts and a mapping.

Usage: python scripts/compose_sources.py <raw_dir> <mapping.json> <out_dir>

Reads source_mapping.json. For each named source file, concatenates the relevant
per-repo extracts under <raw_dir>/<repo>.md with a TOC and per-repo section
headings. The wildcard mapping value ["*"] expands to all repos found under
<raw_dir>.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def list_all_repos(raw_dir: Path) -> list[str]:
    return sorted(p.stem for p in raw_dir.glob("*.md"))


def compose_one(source_name: str, repos: list[str], raw_dir: Path) -> str:
    sections: list[str] = []
    sections.append(f"# {source_name}\n")
    sections.append(
        f"\nSource digest auto-composed from {len(repos)} per-repo raw extracts under "
        f"`runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections "
        f"using `source-*.md§Repo: <name>` per §6.3.\n"
    )
    sections.append("\n## Table of Contents\n")
    for r in repos:
        sections.append(f"- {r}\n")

    sections.append("\n---\n")

    for repo in repos:
        raw_file = raw_dir / f"{repo}.md"
        if not raw_file.exists():
            print(f"WARNING: {raw_file} missing for {source_name}", file=sys.stderr)
            sections.append(f"\n## Repo: {repo}\n\n*Raw extract not found.*\n")
            continue
        sections.append(f"\n{raw_file.read_text(encoding='utf-8')}\n")

    return "".join(sections)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: compose_sources.py <raw_dir> <mapping.json> <out_dir>", file=sys.stderr)
        return 2
    raw_dir = Path(argv[1])
    mapping_path = Path(argv[2])
    out_dir = Path(argv[3])

    if not raw_dir.is_dir():
        print(f"ERROR: {raw_dir} not a directory", file=sys.stderr)
        return 1

    mapping = json.loads(mapping_path.read_text())
    out_dir.mkdir(parents=True, exist_ok=True)

    all_repos = list_all_repos(raw_dir)

    for source_name, repos in mapping.items():
        if repos == ["*"]:
            repos = all_repos
        out = out_dir / f"{source_name}.md"
        out.write_text(compose_one(source_name, repos, raw_dir), encoding="utf-8")
        print(f"wrote {out} ({len(repos)} repos)")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
