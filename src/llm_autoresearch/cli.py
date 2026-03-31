from __future__ import annotations

import argparse
import json
from pathlib import Path

from .loop import run_iteration, run_loop
from .models import StopConditions
from .run_files import init_run
from .status import build_status_summary, format_status_summary
from .supervisor import build_loop_command, default_python_executable, supervise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reusable LLM Auto Research skeleton")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a new research run")
    init_parser.add_argument("run_dir", help="Directory for the run")
    init_parser.add_argument("--topic", help="Topic title for the run")
    init_parser.add_argument(
        "--provider",
        default="mock",
        choices=["mock", "command"],
        help="Default provider to write into run.json",
    )
    init_parser.add_argument(
        "--example",
        action="store_true",
        help="Seed the run with example sources and benchmark items",
    )

    iterate_parser = subparsers.add_parser("iterate", help="Run one research iteration")
    iterate_parser.add_argument("run_dir", help="Directory for the run")
    iterate_parser.add_argument(
        "--provider",
        choices=["mock", "command"],
        help="Override the provider defined in run.json",
    )
    iterate_parser.add_argument(
        "--provider-command",
        help="Command string for the command provider",
    )

    loop_parser = subparsers.add_parser(
        "loop",
        help="Run continuous research iterations with produce-judge-feedback cycle",
    )
    loop_parser.add_argument("run_dir", help="Directory for the run")
    loop_parser.add_argument(
        "--tag",
        required=True,
        help="Tag for the autoresearch branch (creates autoresearch/<tag>)",
    )
    loop_parser.add_argument(
        "--producer",
        default="mock",
        choices=["mock", "cli", "codex", "claude"],
        help="Producer provider kind (default: mock)",
    )
    loop_parser.add_argument(
        "--judge",
        default="mock",
        choices=["mock", "cli", "codex", "claude"],
        help="Judge provider kind (default: mock)",
    )
    loop_parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of iterations (default: unlimited)",
    )
    loop_parser.add_argument(
        "--max-total-iterations",
        type=int,
        default=None,
        help="Maximum total completed iterations across restarts (default: unlimited)",
    )
    loop_parser.add_argument(
        "--max-consecutive-discard",
        type=int,
        default=None,
        help="Stop after N consecutive discards (default: unlimited)",
    )
    loop_parser.add_argument(
        "--dimension-threshold",
        type=float,
        default=None,
        help="Stop when all dimension scores exceed this threshold (default: none)",
    )
    loop_parser.add_argument(
        "--resume-branch",
        action="store_true",
        help="Reuse an existing autoresearch/<tag> branch instead of failing on restart",
    )

    status_parser = subparsers.add_parser("status", help="Inspect current run status")
    status_parser.add_argument("run_dir", help="Directory for the run")
    status_parser.add_argument(
        "--session",
        default="",
        help="Optional tmux session name for the main loop",
    )
    status_parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print machine-readable JSON instead of the formatted status line",
    )

    supervise_parser = subparsers.add_parser(
        "supervise",
        help="Watch a loop, write health files, and restart it if the main session dies",
    )
    supervise_parser.add_argument("run_dir", help="Directory for the run")
    supervise_parser.add_argument("--tag", required=True, help="Tag for the autoresearch branch")
    supervise_parser.add_argument(
        "--main-session",
        required=True,
        help="tmux session name for the main loop process",
    )
    supervise_parser.add_argument(
        "--sidecar-session",
        default="",
        help="Optional label for the supervising process/session",
    )
    supervise_parser.add_argument(
        "--producer",
        default="mock",
        choices=["mock", "cli", "codex", "claude"],
        help="Producer provider kind used when (re)starting the loop",
    )
    supervise_parser.add_argument(
        "--judge",
        default="mock",
        choices=["mock", "cli", "codex", "claude"],
        help="Judge provider kind used when (re)starting the loop",
    )
    supervise_parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of iterations (default: unlimited)",
    )
    supervise_parser.add_argument(
        "--max-total-iterations",
        type=int,
        default=None,
        help="Maximum total completed iterations across restarts (default: unlimited)",
    )
    supervise_parser.add_argument(
        "--max-consecutive-discard",
        type=int,
        default=None,
        help="Stop after N consecutive discards (default: unlimited)",
    )
    supervise_parser.add_argument(
        "--dimension-threshold",
        type=float,
        default=None,
        help="Stop when all dimension scores exceed this threshold (default: none)",
    )
    supervise_parser.add_argument(
        "--interval",
        type=int,
        default=600,
        help="Seconds between health checks (default: 600)",
    )
    supervise_parser.add_argument(
        "--cwd",
        default=".",
        help="Working directory used when launching the main loop (default: current directory)",
    )
    supervise_parser.add_argument(
        "--python-executable",
        default="",
        help="Python executable used for restart commands (default: current interpreter)",
    )
    supervise_parser.add_argument(
        "--loop-log",
        default="",
        help="Path for the loop stdout/stderr log (default: runs/<name>/loop-<tag>.log)",
    )
    supervise_parser.add_argument(
        "--log-file",
        default="",
        help="Path for supervisor heartbeat log (default: runs/<name>/supervisor.log)",
    )
    supervise_parser.add_argument(
        "--status-file",
        default="",
        help="Path for supervisor status JSON (default: runs/<name>/supervisor_status.json)",
    )
    supervise_parser.add_argument(
        "--once",
        action="store_true",
        help="Run one health check iteration and exit",
    )
    return parser


def cmd_init(args: argparse.Namespace) -> int:
    paths = init_run(
        run_dir=Path(args.run_dir),
        topic=args.topic,
        provider_kind=args.provider,
        example=args.example,
    )
    print(f"Initialized run at {paths.run_dir}")
    print(f"Edit sources in {paths.sources_dir}")
    print(f"Edit benchmark in {paths.benchmark_path}")
    return 0


def cmd_iterate(args: argparse.Namespace) -> int:
    outcome = run_iteration(
        run_dir=Path(args.run_dir),
        provider_kind=args.provider,
        command=args.provider_command,
    )
    print(f"Iteration:      {outcome.iteration}")
    print(f"Status:         {outcome.status}")
    print(f"Score:          {outcome.candidate_score:.4f}")
    print(f"Knowledge chars:{outcome.knowledge_chars}")
    print(f"Experiment:     {outcome.experiment_title}")
    print(f"Artifacts:      {outcome.artifact_dir}")
    return 0


def cmd_loop(args: argparse.Namespace) -> int:
    stop = StopConditions(
        max_iterations=args.max_iterations,
        max_total_iterations=getattr(args, "max_total_iterations", None),
        max_consecutive_discard=args.max_consecutive_discard,
        dimension_threshold=args.dimension_threshold,
    )
    outcomes = run_loop(
        run_dir=Path(args.run_dir),
        producer_kind=args.producer,
        judge_kind=args.judge,
        tag=args.tag,
        stop_conditions=stop,
        resume_branch=getattr(args, "resume_branch", False),
    )
    print(f"\nLoop complete: {len(outcomes)} iterations")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    summary = build_status_summary(Path(args.run_dir), session=args.session)
    if args.json_output:
        print(json.dumps(summary, indent=2))
    else:
        print(format_status_summary(summary))
    return 0


def cmd_supervise(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    stop = StopConditions(
        max_iterations=args.max_iterations,
        max_total_iterations=getattr(args, "max_total_iterations", None),
        max_consecutive_discard=args.max_consecutive_discard,
        dimension_threshold=args.dimension_threshold,
    )
    python_executable = args.python_executable or default_python_executable()
    loop_command = build_loop_command(
        python_executable=python_executable,
        run_dir=run_dir,
        producer=args.producer,
        judge=args.judge,
        tag=args.tag,
        stop_conditions=stop,
        resume_branch=True,
    )
    loop_log = Path(args.loop_log) if args.loop_log else run_dir / f"loop-{args.tag}.log"
    log_file = Path(args.log_file) if args.log_file else run_dir / "supervisor.log"
    status_file = (
        Path(args.status_file) if args.status_file else run_dir / "supervisor_status.json"
    )
    return supervise(
        run_dir=run_dir,
        main_session=args.main_session,
        sidecar_session=args.sidecar_session,
        cwd=Path(args.cwd),
        loop_command=loop_command,
        loop_log=loop_log,
        log_file=log_file,
        status_file=status_file,
        stop_conditions=stop,
        interval=args.interval,
        once=args.once,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.subcommand == "init":
        return cmd_init(args)
    if args.subcommand == "iterate":
        return cmd_iterate(args)
    if args.subcommand == "loop":
        return cmd_loop(args)
    if args.subcommand == "status":
        return cmd_status(args)
    if args.subcommand == "supervise":
        return cmd_supervise(args)
    parser.error(f"Unsupported command: {args.subcommand}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
