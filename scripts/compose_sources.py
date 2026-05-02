#!/usr/bin/env python3
"""Compose 10 source-*.md digests from per-repo raw extracts and a mapping.

Usage: python scripts/compose_sources.py <raw_dir> <mapping.json> <out_dir> [--max-bytes-per-repo N]

Reads source_mapping.json. For each named source file, concatenates the relevant
per-repo extracts under <raw_dir>/<repo>.md with a TOC and per-repo section
headings. The wildcard mapping value ["*"] expands to all repos found under
<raw_dir>.

--max-bytes-per-repo N (default 2500)
    Truncate each per-repo block to at most N bytes before appending.  Content
    beyond the budget is dropped and replaced with a marker line so downstream
    tools know where to find the full text.

    Budget math / justification:
      - Worst case: 64 wildcard repos × 2500 B = 160 KB per wildcard source
      - Typical:    14 repos × 2500 B = 35 KB per source
      - 10 sources × ~50 KB average = ~500 KB total
      → comfortably under the 700 KB target (300 KB headroom below codex's 1 MB limit)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Default per-repo byte budget.
# See module docstring for the budget-math justification.
DEFAULT_MAX_BYTES_PER_REPO = 2500


def list_all_repos(raw_dir: Path) -> list[str]:
    return sorted(p.stem for p in raw_dir.glob("*.md"))


def compose_one(
    source_name: str,
    repos: list[str],
    raw_dir: Path,
    *,
    max_bytes_per_repo: int = DEFAULT_MAX_BYTES_PER_REPO,
) -> str:
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
        content_bytes = raw_file.read_bytes()
        if len(content_bytes) > max_bytes_per_repo:
            # Truncate at the byte budget and append a clear marker so readers
            # know the content is incomplete and where to find the full text.
            content = content_bytes[:max_bytes_per_repo].decode("utf-8", errors="replace")
            content += (
                f"\n\n[... truncated to {max_bytes_per_repo} bytes;"
                f" full extract at sources/_raw/{repo}.md ...]\n"
            )
        else:
            content = content_bytes.decode("utf-8")
        sections.append(f"\n{content}\n")

    return "".join(sections)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="compose_sources.py",
        description="Compose source-*.md digests from per-repo raw extracts.",
    )
    parser.add_argument("raw_dir", help="Directory containing per-repo _raw/*.md files")
    parser.add_argument("mapping", help="Path to source_mapping.json")
    parser.add_argument("out_dir", help="Output directory for composed source-*.md files")
    parser.add_argument(
        "--max-bytes-per-repo",
        type=int,
        default=DEFAULT_MAX_BYTES_PER_REPO,
        metavar="N",
        help=(
            f"Truncate each per-repo block to at most N bytes (default: {DEFAULT_MAX_BYTES_PER_REPO}). "
            "Content beyond the budget is replaced with a truncation marker."
        ),
    )
    args = parser.parse_args(argv[1:])

    raw_dir = Path(args.raw_dir)
    mapping_path = Path(args.mapping)
    out_dir = Path(args.out_dir)

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
        out.write_text(
            compose_one(source_name, repos, raw_dir, max_bytes_per_repo=args.max_bytes_per_repo),
            encoding="utf-8",
        )
        print(f"wrote {out} ({len(repos)} repos)")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
