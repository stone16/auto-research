#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.status import poll_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor an autoresearch run.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--interval", type=int, default=600)
    parser.add_argument("--log-file", required=True)
    parser.add_argument("--status-file", required=True)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--no-notify", action="store_true")
    args = parser.parse_args()

    return poll_status(
        Path(args.run_dir),
        session=args.session,
        interval=args.interval,
        log_file=Path(args.log_file),
        status_file=Path(args.status_file),
        once=args.once,
        notify_enabled=not args.no_notify,
        notification_title="Polymarket Deep Research",
    )


if __name__ == "__main__":
    raise SystemExit(main())
