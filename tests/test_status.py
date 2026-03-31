from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _write_results(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "iteration",
                "timestamp",
                "score",
                "prev_best",
                "status",
                "knowledge_chars",
                "provider",
                "experiment",
                "change_summary",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class TestStatusSummary(unittest.TestCase):
    def test_build_status_summary_reads_runtime_files(self) -> None:
        from llm_autoresearch.status import build_status_summary

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            (run_dir / "artifacts" / "iteration-0001").mkdir(parents=True)
            (run_dir / "state.json").write_text(
                json.dumps(
                    {
                        "iteration": 1,
                        "best_score": 0.75,
                        "last_kept_experiment": "iter-1",
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "provider_status.json").write_text(
                json.dumps(
                    {
                        "role": "producer",
                        "provider_kind": "codex",
                        "status": "running",
                        "iteration": 2,
                        "timeout_seconds": 1800,
                        "prompt_chars": 12345,
                        "attempt_started_at": "2026-03-30T09:00:00+00:00",
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "loop_status.json").write_text(
                json.dumps(
                    {
                        "status": "stopped",
                        "stop_reason": "dimension_threshold",
                    }
                ),
                encoding="utf-8",
            )
            _write_results(
                run_dir / "results.tsv",
                [
                    {
                        "iteration": "1",
                        "timestamp": "2026-03-30T09:10:00+00:00",
                        "score": "0.7500",
                        "prev_best": "0.0000",
                        "status": "keep",
                        "knowledge_chars": "100",
                        "provider": "codex",
                        "experiment": "iter-1",
                        "change_summary": "summary",
                    }
                ],
            )

            with patch("llm_autoresearch.status.session_alive", return_value=True), patch(
                "llm_autoresearch.status.load_processes",
                return_value=[],
            ):
                summary = build_status_summary(run_dir, session="main-session")

            self.assertTrue(summary["session_alive"])
            self.assertEqual(summary["completed_iterations"], 1)
            self.assertEqual(summary["best_score"], 0.75)
            self.assertEqual(summary["provider_status"], "running")
            self.assertEqual(summary["provider_iteration"], 2)
            self.assertEqual(summary["last_result_experiment"], "iter-1")
            self.assertEqual(summary["loop_status"], "stopped")
            self.assertEqual(summary["loop_stop_reason"], "dimension_threshold")

    def test_format_status_summary_includes_provider_fields(self) -> None:
        from llm_autoresearch.status import format_status_summary

        line = format_status_summary(
            {
                "timestamp": "2026-03-30 18:00:00 CST",
                "session_alive": True,
                "stage": "producer:codex",
                "stage_elapsed": "00:15",
                "completed_iterations": 4,
                "state_iteration": 4,
                "best_score": 0.8,
                "artifact_iterations": 4,
                "provider_role": "producer",
                "provider_status": "running",
                "provider_iteration": 5,
                "provider_timeout_seconds": 3600,
                "provider_prompt_chars": 200000,
                "provider_elapsed": "00:15",
                "provider_error": "",
                "loop_status": "stopped",
                "loop_stop_reason": "dimension_threshold",
                "last_result_experiment": "iter-4",
                "last_result_status": "keep",
            }
        )
        self.assertIn("provider=producer:running#5", line)
        self.assertIn("timeout=3600s", line)
        self.assertIn("loop=stopped:dimension_threshold", line)


if __name__ == "__main__":
    unittest.main()
