#!/usr/bin/env python3
"""Example command-provider wrapper.

This script demonstrates the stdin/stdout contract used by the `command`
provider. It simply delegates to the built-in mock provider so you can verify
the wiring end-to-end before connecting a real model backend.
"""

from __future__ import annotations

import json
import sys

ROOT_TASK_ERROR = {
    "experiment_title": "invalid-task",
    "change_summary": "The wrapper received an invalid task payload.",
    "knowledge_base_markdown": "# Knowledge Base\n\nThe provider wrapper received invalid input.\n",
    "benchmark_answers": [],
    "notes": ["Invalid input passed to example command provider."],
}


def main() -> int:
    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError:
        json.dump(ROOT_TASK_ERROR, sys.stdout)
        sys.stdout.write("\n")
        return 0

    task_type = raw.get("task_type")
    payload = raw.get("payload", {})
    if task_type != "research_iteration":
        json.dump(ROOT_TASK_ERROR, sys.stdout)
        sys.stdout.write("\n")
        return 0

    topic = payload.get("topic", "Unknown topic")
    iteration = int(payload.get("state", {}).get("iteration", 0)) + 1
    benchmark = payload.get("benchmark", [])
    sources = payload.get("sources", [])

    benchmark_answers = []
    for item in benchmark:
        citations = item.get("required_sources", []) or ([sources[0]["id"]] if sources else [])
        benchmark_answers.append(
            {
                "id": item["id"],
                "answer": (
                    f"Example command provider answer for {item['id']} on {topic}. "
                    f"Required details: {', '.join(item.get('must_include', [])) or 'none'}."
                ),
                "citations": citations,
            }
        )

    response = {
        "experiment_title": f"iteration-{iteration}-example-command-provider",
        "change_summary": "Demonstrate the command-provider contract with a local wrapper script.",
        "knowledge_base_markdown": (
            "# Knowledge Base\n\n"
            f"Topic: {topic}\n\n"
            f"Iteration: {iteration}\n\n"
            "This file was produced by the example command-provider wrapper.\n"
        ),
        "benchmark_answers": benchmark_answers,
        "notes": ["Replace this script with a real model-backed wrapper later."],
    }
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
