from __future__ import annotations

import shlex
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import StopConditions
from .status import append_log, build_status_summary, run_command, write_status


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def now_label() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def tail_text(path: Path, limit: int = 20) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[-limit:])


def latest_loop_log(run_dir: Path) -> Path | None:
    loop_logs = sorted(run_dir.glob("loop-*.log"))
    return loop_logs[-1] if loop_logs else None


def build_supervisor_snapshot(
    run_dir: Path,
    *,
    main_session: str,
    sidecar_session: str = "",
) -> dict[str, Any]:
    status = build_status_summary(run_dir, session=main_session)
    loop_log = latest_loop_log(run_dir)
    provider_state = str(status.get("provider_status", ""))
    main_alive = bool(status.get("session_alive", False))
    healthy = main_alive and provider_state != "error"

    if not main_alive and int(status.get("state_iteration", 0) or 0) < int(
        status.get("completed_iterations", 0) or 0
    ):
        healthy = False

    snapshot: dict[str, Any] = dict(status)
    snapshot.update(
        {
            "timestamp_iso": now_iso(),
            "sidecar_session": sidecar_session,
            "main_session": main_session,
            "main_session_alive": main_alive,
            "healthy": healthy,
            "latest_loop_log": str(loop_log) if loop_log else "",
            "recent_loop_log": tail_text(loop_log, 12) if loop_log else "",
        }
    )
    return snapshot


def stop_limit_reached(
    snapshot: dict[str, Any],
    stop_conditions: StopConditions | None,
) -> tuple[bool, str]:
    loop_status = str(snapshot.get("loop_status", ""))
    loop_stop_reason = str(snapshot.get("loop_stop_reason", ""))
    if loop_status == "stopped" and loop_stop_reason in {
        "shutdown",
        "max_iterations",
        "max_total_iterations",
        "max_consecutive_discard",
        "dimension_threshold",
    }:
        return True, f"loop stopped cleanly: {loop_stop_reason}"
    if loop_status == "failed" and loop_stop_reason == "consecutive_crashes":
        return True, "loop halted after consecutive crashes"

    if stop_conditions is None:
        return False, ""

    max_total_iterations = stop_conditions.max_total_iterations
    if max_total_iterations is None:
        return False, ""

    completed_iterations = int(snapshot.get("completed_iterations", 0) or 0)
    state_iteration = int(snapshot.get("state_iteration", 0) or 0)
    total_iterations = max(completed_iterations, state_iteration)
    if total_iterations < max_total_iterations:
        return False, ""

    return True, f"max total iterations {max_total_iterations} reached"


def build_loop_command(
    *,
    python_executable: str,
    run_dir: Path,
    producer: str,
    judge: str,
    tag: str,
    stop_conditions: StopConditions,
    resume_branch: bool = True,
    src_path: Path | None = None,
) -> str:
    resolved_src = src_path or Path(__file__).resolve().parents[1]
    command = [
        "env",
        f"PYTHONPATH={resolved_src}",
        python_executable,
        "-m",
        "llm_autoresearch",
        "loop",
        str(run_dir),
        "--tag",
        tag,
        "--producer",
        producer,
        "--judge",
        judge,
    ]
    if stop_conditions.max_iterations is not None:
        command.extend(["--max-iterations", str(stop_conditions.max_iterations)])
    if stop_conditions.max_total_iterations is not None:
        command.extend(["--max-total-iterations", str(stop_conditions.max_total_iterations)])
    if stop_conditions.max_consecutive_discard is not None:
        command.extend(
            [
                "--max-consecutive-discard",
                str(stop_conditions.max_consecutive_discard),
            ]
        )
    if stop_conditions.dimension_threshold is not None:
        command.extend(
            ["--dimension-threshold", str(stop_conditions.dimension_threshold)]
        )
    if resume_branch:
        command.append("--resume-branch")
    return shlex.join(command)


def restart_main_session(
    *,
    main_session: str,
    cwd: Path,
    loop_command: str,
    loop_log: Path,
) -> tuple[bool, str]:
    if not loop_command.strip():
        return False, "restart command missing"

    loop_log.parent.mkdir(parents=True, exist_ok=True)
    shell_command = f"{loop_command} > {shlex.quote(str(loop_log))} 2>&1"
    result = run_command(
        [
            "tmux",
            "new-session",
            "-d",
            "-s",
            main_session,
            "-c",
            str(cwd),
            "sh",
            "-lc",
            shell_command,
        ]
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or "failed to start tmux session"
    return True, "restarted main session"


def write_supervisor_heartbeat(
    *,
    snapshot: dict[str, Any],
    action: str,
    note: str = "",
    status_label: str | None = None,
    log_file: Path,
    status_file: Path,
) -> None:
    line = (
        f"{snapshot['timestamp']} | action={action} | "
        f"main={'up' if snapshot['main_session_alive'] else 'down'} | "
        f"stage={snapshot['stage']}"
        + (f" ({snapshot['stage_elapsed']})" if snapshot["stage_elapsed"] else "")
        + f" | completed={snapshot['completed_iterations']} | "
        f"state.iteration={snapshot['state_iteration']} | "
        f"best={float(snapshot['best_score']):.4f}"
        + (
            f" | provider={snapshot['provider_role']}:{snapshot['provider_status']}"
            f"#{snapshot['provider_iteration']}"
            if snapshot["provider_role"]
            else ""
        )
        + (
            f" timeout={snapshot['provider_timeout_seconds']}s"
            if snapshot["provider_timeout_seconds"]
            else ""
        )
        + (
            f" prompt={snapshot['provider_prompt_chars']}"
            if snapshot["provider_prompt_chars"]
            else ""
        )
        + (f" elapsed={snapshot['provider_elapsed']}" if snapshot["provider_elapsed"] else "")
        + (f" error={snapshot['provider_error'][:120]}" if snapshot["provider_error"] else "")
        + (f" note={note}" if note else "")
    )
    append_log(log_file, line)

    status_payload = dict(snapshot)
    status_payload["last_action"] = action
    status_payload["last_check_at"] = snapshot["timestamp_iso"]
    status_payload["status"] = status_label or ("healthy" if snapshot["healthy"] else "degraded")
    status_payload["note"] = note
    write_status(status_file, status_payload)


def supervise_once(
    *,
    run_dir: Path,
    main_session: str,
    sidecar_session: str = "",
    cwd: Path,
    loop_command: str,
    loop_log: Path,
    log_file: Path,
    status_file: Path,
    stop_conditions: StopConditions | None = None,
) -> dict[str, Any]:
    snapshot = build_supervisor_snapshot(
        run_dir,
        main_session=main_session,
        sidecar_session=sidecar_session,
    )
    action = "heartbeat"
    note = "main loop healthy"
    status_label: str | None = None

    reached_limit, limit_note = stop_limit_reached(snapshot, stop_conditions)
    if reached_limit:
        action = "loop-finished"
        note = limit_note
        status_label = "failed" if snapshot.get("loop_status") == "failed" else "stopped"

    if not reached_limit and not snapshot["healthy"]:
        if bool(snapshot.get("main_session_alive", False)):
            action = "degraded"
            note = "main loop session alive but provider is unhealthy"
        else:
            restarted, restart_note = restart_main_session(
                main_session=main_session,
                cwd=cwd,
                loop_command=loop_command,
                loop_log=loop_log,
            )
            action = "restart-main-session" if restarted else "degraded"
            note = restart_note
            snapshot = build_supervisor_snapshot(
                run_dir,
                main_session=main_session,
                sidecar_session=sidecar_session,
            )

    write_supervisor_heartbeat(
        snapshot=snapshot,
        action=action,
        note=note,
        status_label=status_label,
        log_file=log_file,
        status_file=status_file,
    )
    return snapshot


def supervise(
    *,
    run_dir: Path,
    main_session: str,
    sidecar_session: str = "",
    cwd: Path | None = None,
    loop_command: str,
    loop_log: Path,
    log_file: Path,
    status_file: Path,
    stop_conditions: StopConditions | None = None,
    interval: int = 600,
    once: bool = False,
) -> int:
    if cwd is None:
        cwd = Path.cwd()

    while True:
        supervise_once(
            run_dir=run_dir,
            main_session=main_session,
            sidecar_session=sidecar_session,
            cwd=cwd,
            loop_command=loop_command,
            loop_log=loop_log,
            log_file=log_file,
            status_file=status_file,
            stop_conditions=stop_conditions,
        )
        if once:
            return 0
        time.sleep(interval)


def default_python_executable() -> str:
    return sys.executable
