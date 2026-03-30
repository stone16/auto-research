"""Feedback engine for managing judge and human feedback across iterations.

Manages two feedback files:
- judge_feedback.md: cumulative, appended after each judge evaluation
- human_feedback.md: manually edited by the user, hot-reloaded each iteration

Both are included in the producer's prompt context to guide research improvements.
"""

from __future__ import annotations

import re
from pathlib import Path

from .judge import JudgeReport
from .run_files import RunPaths, write_text

# Maximum total characters for feedback context returned to the producer LLM.
_CHAR_CAP = 4000


def append_judge_feedback(
    paths: RunPaths,
    judge_report: JudgeReport,
    iteration: int,
) -> None:
    """Append a judge's feedback entry to judge_feedback.md.

    Each entry is formatted as a ## Iteration N section containing the
    priority dimension, improvement suggestion, and full review markdown.
    """
    entry = (
        f"## Iteration {iteration}\n"
        f"\n"
        f"**Priority dimension**: {judge_report.priority_dimension}\n"
        f"**Improvement suggestion**: {judge_report.improvement_suggestion}\n"
        f"\n"
        f"### Review\n"
        f"{judge_report.review_markdown}\n"
    )

    fb_path = paths.judge_feedback_path
    if fb_path.exists():
        existing = fb_path.read_text(encoding="utf-8")
        combined = existing.rstrip() + "\n\n" + entry
    else:
        combined = entry

    write_text(fb_path, combined)


def _parse_iteration_sections(content: str) -> list[str]:
    """Split judge_feedback.md content into individual iteration sections.

    Each section starts with '## Iteration N' and runs until the next
    '## Iteration' header or end of file.

    Returns a list of section strings, preserving their headers.
    """
    pattern = re.compile(r"^## Iteration \d+", re.MULTILINE)
    matches = list(pattern.finditer(content))
    if not matches:
        return []

    sections: list[str] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections.append(content[start:end].strip())

    return sections


def load_feedback_context(
    paths: RunPaths,
    recent_n: int = 3,
) -> dict[str, str]:
    """Load feedback context for the producer's prompt.

    Returns a dict with:
    - "judge_feedback": last recent_n entries from judge_feedback.md
    - "human_feedback": full content of human_feedback.md (hot-reloaded)

    Total returned text is capped at _CHAR_CAP characters. When over the cap,
    judge feedback entries are trimmed oldest-first until under the limit.
    Human feedback is always included in full (it is written by the user and
    assumed to be concise).

    Cold-start behavior: if judge_feedback.md does not exist, returns empty
    string for judge_feedback. Same for human_feedback.md.
    """
    # Hot-reload human feedback
    human_fb = ""
    if paths.human_feedback_path.exists():
        human_fb = paths.human_feedback_path.read_text(encoding="utf-8")

    # Load judge feedback sections
    judge_sections: list[str] = []
    if paths.judge_feedback_path.exists():
        content = paths.judge_feedback_path.read_text(encoding="utf-8")
        all_sections = _parse_iteration_sections(content)
        # Take only the most recent recent_n sections
        judge_sections = all_sections[-recent_n:]

    # Apply character cap: trim oldest judge sections first
    human_len = len(human_fb)
    budget = _CHAR_CAP - human_len

    if budget <= 0:
        # Human feedback alone exceeds cap; return it all, no judge feedback
        return {"judge_feedback": "", "human_feedback": human_fb}

    # Build judge feedback string, trimming oldest sections if needed
    while judge_sections:
        candidate = "\n\n".join(judge_sections)
        if len(candidate) <= budget:
            break
        # Remove the oldest section (first in list) to make room
        judge_sections.pop(0)

    judge_fb = "\n\n".join(judge_sections) if judge_sections else ""

    return {"judge_feedback": judge_fb, "human_feedback": human_fb}


def save_judge_review(
    artifact_dir: Path,
    judge_report: JudgeReport,
) -> None:
    """Write the judge's review_markdown to judge_review.md in the artifact directory."""
    write_text(artifact_dir / "judge_review.md", judge_report.review_markdown)
