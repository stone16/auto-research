from __future__ import annotations

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


def _snapshot(**overrides):
    base = {
        "timestamp": "2026-03-30 18:00:00 CST",
        "timestamp_iso": "2026-03-30T10:00:00+00:00",
        "main_session_alive": False,
        "main_session": "main-session",
        "sidecar_session": "sidecar-session",
        "stage": "idle",
        "stage_elapsed": "",
        "completed_iterations": 3,
        "state_iteration": 3,
        "best_score": 0.8,
        "provider_role": "producer",
        "provider_status": "error",
        "provider_iteration": 4,
        "provider_timeout_seconds": 3600,
        "provider_prompt_chars": 1234,
        "provider_elapsed": "00:30",
        "provider_error": "boom",
        "loop_status": "",
        "loop_stop_reason": "",
        "healthy": False,
    }
    base.update(overrides)
    return base


class TestSupervisor(unittest.TestCase):
    def test_build_loop_command_includes_resume_branch(self) -> None:
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.supervisor import build_loop_command

        command = build_loop_command(
            python_executable="/usr/bin/python3",
            run_dir=Path("/tmp/run"),
            producer="codex",
            judge="claude",
            tag="tag-1",
            stop_conditions=StopConditions(
                max_iterations=10,
                max_total_iterations=25,
                max_consecutive_discard=4,
                dimension_threshold=0.85,
            ),
            resume_branch=True,
        )

        self.assertIn("loop", command)
        self.assertIn("PYTHONPATH=", command)
        self.assertIn("--resume-branch", command)
        self.assertIn("--max-iterations 10", command)
        self.assertIn("--max-total-iterations 25", command)
        self.assertIn("--max-consecutive-discard 4", command)
        self.assertIn("--dimension-threshold 0.85", command)

    def test_supervise_once_restarts_dead_session(self) -> None:
        from llm_autoresearch.supervisor import supervise_once

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            log_file = run_dir / "supervisor.log"
            status_file = run_dir / "supervisor_status.json"
            loop_log = run_dir / "loop.log"

            with patch(
                "llm_autoresearch.supervisor.build_supervisor_snapshot",
                side_effect=[
                    _snapshot(),
                    _snapshot(main_session_alive=True, healthy=True, provider_status="running"),
                ],
            ), patch(
                "llm_autoresearch.supervisor.restart_main_session",
                return_value=(True, "restarted main session"),
            ) as restart:
                snapshot = supervise_once(
                    run_dir=run_dir,
                    main_session="main-session",
                    sidecar_session="sidecar-session",
                    cwd=run_dir,
                    loop_command="python -m llm_autoresearch.cli loop /tmp/run",
                    loop_log=loop_log,
                    log_file=log_file,
                    status_file=status_file,
                )

            self.assertTrue(restart.called)
            self.assertTrue(snapshot["healthy"])
            self.assertTrue(log_file.exists())
            self.assertTrue(status_file.exists())
            status_payload = json.loads(status_file.read_text(encoding="utf-8"))
            self.assertEqual(status_payload["last_action"], "restart-main-session")

    def test_supervise_once_marks_alive_error_as_degraded(self) -> None:
        from llm_autoresearch.supervisor import supervise_once

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            log_file = run_dir / "supervisor.log"
            status_file = run_dir / "supervisor_status.json"

            with patch(
                "llm_autoresearch.supervisor.build_supervisor_snapshot",
                return_value=_snapshot(main_session_alive=True),
            ), patch(
                "llm_autoresearch.supervisor.restart_main_session"
            ) as restart:
                supervise_once(
                    run_dir=run_dir,
                    main_session="main-session",
                    sidecar_session="sidecar-session",
                    cwd=run_dir,
                    loop_command="python -m llm_autoresearch.cli loop /tmp/run",
                    loop_log=run_dir / "loop.log",
                    log_file=log_file,
                    status_file=status_file,
                )

            self.assertFalse(restart.called)
            status_payload = json.loads(status_file.read_text(encoding="utf-8"))
            self.assertEqual(status_payload["last_action"], "degraded")

    def test_supervise_once_stops_restarting_after_total_cap(self) -> None:
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.supervisor import supervise_once

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            log_file = run_dir / "supervisor.log"
            status_file = run_dir / "supervisor_status.json"

            with patch(
                "llm_autoresearch.supervisor.build_supervisor_snapshot",
                return_value=_snapshot(
                    main_session_alive=False,
                    healthy=False,
                    completed_iterations=25,
                    state_iteration=25,
                ),
            ), patch(
                "llm_autoresearch.supervisor.restart_main_session"
            ) as restart:
                supervise_once(
                    run_dir=run_dir,
                    main_session="main-session",
                    sidecar_session="sidecar-session",
                    cwd=run_dir,
                    loop_command="python -m llm_autoresearch loop /tmp/run",
                    loop_log=run_dir / "loop.log",
                    log_file=log_file,
                    status_file=status_file,
                    stop_conditions=StopConditions(max_total_iterations=25),
                )

            self.assertFalse(restart.called)
            status_payload = json.loads(status_file.read_text(encoding="utf-8"))
            self.assertEqual(status_payload["last_action"], "loop-finished")
            self.assertEqual(status_payload["status"], "stopped")

    def test_supervise_once_does_not_restart_after_clean_terminal_stop(self) -> None:
        from llm_autoresearch.models import StopConditions
        from llm_autoresearch.supervisor import supervise_once

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            log_file = run_dir / "supervisor.log"
            status_file = run_dir / "supervisor_status.json"

            with patch(
                "llm_autoresearch.supervisor.build_supervisor_snapshot",
                return_value=_snapshot(
                    main_session_alive=False,
                    healthy=False,
                    loop_status="stopped",
                    loop_stop_reason="dimension_threshold",
                ),
            ), patch(
                "llm_autoresearch.supervisor.restart_main_session"
            ) as restart:
                supervise_once(
                    run_dir=run_dir,
                    main_session="main-session",
                    sidecar_session="sidecar-session",
                    cwd=run_dir,
                    loop_command="python -m llm_autoresearch loop /tmp/run",
                    loop_log=run_dir / "loop.log",
                    log_file=log_file,
                    status_file=status_file,
                    stop_conditions=StopConditions(dimension_threshold=0.9),
                )

            self.assertFalse(restart.called)
            status_payload = json.loads(status_file.read_text(encoding="utf-8"))
            self.assertEqual(status_payload["last_action"], "loop-finished")
            self.assertEqual(status_payload["status"], "stopped")
            self.assertIn("dimension_threshold", status_payload["note"])


if __name__ == "__main__":
    unittest.main()
