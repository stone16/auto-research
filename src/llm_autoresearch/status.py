from __future__ import annotations

import csv
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=False,
    )


def session_alive(session: str) -> bool:
    if not session:
        return False
    return run_command(["tmux", "has-session", "-t", session]).returncode == 0


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def read_results(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_processes() -> list[dict[str, str]]:
    completed = run_command(["ps", "-axo", "pid=,ppid=,etime=,command="])
    processes: list[dict[str, str]] = []
    for line in completed.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        pid, ppid, etime, command = parts
        processes.append(
            {
                "pid": pid,
                "ppid": ppid,
                "etime": etime,
                "command": command,
            }
        )
    return processes


def find_active_stage(processes: list[dict[str, str]], run_name: str) -> tuple[str, str]:
    loop_pids = {
        proc["pid"]
        for proc in processes
        if "autoresearch loop" in proc["command"] and run_name in proc["command"]
    }
    if not loop_pids:
        return ("idle", "")

    descendants = set(loop_pids)
    changed = True
    while changed:
        changed = False
        for proc in processes:
            if proc["ppid"] in descendants and proc["pid"] not in descendants:
                descendants.add(proc["pid"])
                changed = True

    for proc in processes:
        if proc["pid"] not in descendants:
            continue
        command = proc["command"]
        if "codex exec" in command:
            return ("producer:codex", proc["etime"])
        if "claude -p" in command:
            return ("judge:claude", proc["etime"])

    return ("loop:python", "")


def format_elapsed_seconds(seconds: int) -> str:
    hours, remainder = divmod(max(seconds, 0), 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def elapsed_since(timestamp: str) -> str:
    if not timestamp:
        return ""
    try:
        started_at = datetime.fromisoformat(timestamp)
    except ValueError:
        return ""
    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return format_elapsed_seconds(int((now - started_at).total_seconds()))


def build_status_summary(
    run_dir: Path,
    session: str = "",
) -> dict[str, str | int | float | bool]:
    state = read_json(run_dir / "state.json")
    results = read_results(run_dir / "results.tsv")
    stage, stage_elapsed = find_active_stage(load_processes(), run_dir.name)
    provider_status = read_json(run_dir / "provider_status.json")
    loop_status = read_json(run_dir / "loop_status.json")
    iteration_dirs = sorted(run_dir.glob("artifacts/iteration-*"))
    last_row = results[-1] if results else {}

    return {
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "run_dir": str(run_dir),
        "session_alive": session_alive(session),
        "session": session,
        "stage": stage,
        "stage_elapsed": stage_elapsed,
        "completed_iterations": len(results),
        "state_iteration": int(state.get("iteration", 0) or 0),
        "best_score": float(state.get("best_score", 0.0) or 0.0),
        "last_kept_experiment": str(state.get("last_kept_experiment", "")),
        "artifact_iterations": len(iteration_dirs),
        "last_result_status": str(last_row.get("status", "")),
        "last_result_score": str(last_row.get("score", "")),
        "last_result_experiment": str(last_row.get("experiment", "")),
        "provider_role": str(provider_status.get("role", "")),
        "provider_kind": str(provider_status.get("provider_kind", "")),
        "provider_status": str(provider_status.get("status", "")),
        "provider_iteration": int(provider_status.get("iteration", 0) or 0),
        "provider_active": bool(provider_status.get("active", False)),
        "provider_timeout_seconds": int(provider_status.get("timeout_seconds", 0) or 0),
        "provider_prompt_chars": int(provider_status.get("prompt_chars", 0) or 0),
        "provider_elapsed": elapsed_since(str(provider_status.get("attempt_started_at", ""))),
        "provider_error": str(provider_status.get("error", "")),
        "loop_status": str(loop_status.get("status", "")),
        "loop_stop_reason": str(loop_status.get("stop_reason", "")),
        "loop_active": bool(loop_status.get("active", False)),
    }


def format_status_summary(summary: dict[str, str | int | float | bool]) -> str:
    provider_segment = ""
    if summary["provider_role"]:
        provider_segment = (
            f" | provider={summary['provider_role']}:{summary['provider_status']}"
            f"#{summary['provider_iteration']}"
        )
        if summary["provider_timeout_seconds"]:
            provider_segment += f" timeout={summary['provider_timeout_seconds']}s"
        if summary["provider_prompt_chars"]:
            provider_segment += f" prompt={summary['provider_prompt_chars']}"
        if summary["provider_elapsed"]:
            provider_segment += f" elapsed={summary['provider_elapsed']}"
        if summary["provider_error"]:
            provider_segment += f" error={str(summary['provider_error'])[:120]}"

    loop_segment = ""
    if summary["loop_status"] and summary["loop_status"] != "running":
        loop_segment = f" | loop={summary['loop_status']}"
        if summary["loop_stop_reason"]:
            loop_segment += f":{summary['loop_stop_reason']}"

    return (
        f"{summary['timestamp']} | "
        f"session={'up' if summary['session_alive'] else 'down'} | "
        f"stage={summary['stage']}"
        + (f" ({summary['stage_elapsed']})" if summary["stage_elapsed"] else "")
        + f" | completed={summary['completed_iterations']} | "
        f"state.iteration={summary['state_iteration']} | "
        f"best={float(summary['best_score']):.4f} | "
        f"artifacts={summary['artifact_iterations']}"
        + provider_segment
        + loop_segment
        + (
            f" | last={summary['last_result_status']}:{summary['last_result_experiment']}"
            if summary["last_result_experiment"]
            else ""
        )
    )


def append_log(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def write_status(path: Path, summary: dict[str, str | int | float | bool]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def notify(summary_line: str, title: str = "LLM Auto Research") -> None:
    if shutil.which("osascript") is None:
        return
    message = summary_line[:220].replace('"', '\\"')
    run_command(
        [
            "osascript",
            "-e",
            f'display notification "{message}" with title "{title}"',
        ]
    )


def poll_status(
    run_dir: Path,
    *,
    session: str = "",
    interval: int = 600,
    log_file: Path | None = None,
    status_file: Path | None = None,
    once: bool = False,
    notify_enabled: bool = False,
    notification_title: str = "LLM Auto Research",
) -> int:
    while True:
        summary = build_status_summary(run_dir, session=session)
        summary_line = format_status_summary(summary)
        if log_file is not None:
            append_log(log_file, summary_line)
        if status_file is not None:
            write_status(status_file, summary)
        if notify_enabled:
            notify(summary_line, title=notification_title)
        if once:
            return 0
        time.sleep(interval)
