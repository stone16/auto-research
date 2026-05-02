#!/usr/bin/env python3
"""Parse the design spec and emit benchmark.json.

Usage: python scripts/extract_benchmark.py <spec.md> <output.json>

Reads ```json``` blocks from the spec, keeps those that look like benchmark
question objects (have id/question/rubric), validates them, and writes a
JSON array.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


JSON_BLOCK_RE = re.compile(r"```json\n(\{[^`]+?\})\n```", re.DOTALL)


def extract_questions(spec_text: str) -> list[dict]:
    """Return all JSON blocks in the spec that look like benchmark questions."""
    questions: list[dict] = []
    for match in JSON_BLOCK_RE.finditer(spec_text):
        try:
            obj = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and {"id", "question", "rubric"}.issubset(obj.keys()):
            questions.append(obj)
    return questions


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_benchmark.py <spec.md> <output.json>", file=sys.stderr)
        return 2
    spec_path = Path(argv[1])
    out_path = Path(argv[2])
    if not spec_path.is_file():
        print(f"ERROR: spec not found: {spec_path}", file=sys.stderr)
        return 2
    # Normalize CRLF so the JSON-block regex matches on Windows-saved specs.
    spec_text = spec_path.read_text().replace("\r\n", "\n")
    questions = extract_questions(spec_text)
    if len(questions) != 15:
        print(f"ERROR: expected 15 questions, found {len(questions)}", file=sys.stderr)
        return 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(questions, indent=2))
    print(f"wrote {len(questions)} questions to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
