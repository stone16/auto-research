#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.supervisor import supervise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sidecar monitor and self-heal loop for autoresearch runs."
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--main-session", required=True)
    parser.add_argument("--sidecar-session", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--restart-command", required=True)
    parser.add_argument("--loop-log", required=True)
    parser.add_argument("--interval", type=int, default=600)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    return supervise(
        run_dir=run_dir,
        main_session=args.main_session,
        sidecar_session=args.sidecar_session,
        cwd=Path(args.cwd),
        loop_command=args.restart_command,
        loop_log=Path(args.loop_log),
        log_file=run_dir / "sidecar-agent.log",
        status_file=run_dir / "sidecar-agent-status.json",
        interval=args.interval,
        once=args.once,
    )


if __name__ == "__main__":
    raise SystemExit(main())
