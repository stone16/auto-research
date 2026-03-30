from __future__ import annotations

import argparse
from pathlib import Path

from .loop import run_iteration, run_loop
from .models import StopConditions
from .run_files import init_run


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
        choices=["mock", "codex", "claude"],
        help="Producer provider kind (default: mock)",
    )
    loop_parser.add_argument(
        "--judge",
        default="mock",
        choices=["mock", "codex", "claude"],
        help="Judge provider kind (default: mock)",
    )
    loop_parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of iterations (default: unlimited)",
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
        max_consecutive_discard=args.max_consecutive_discard,
        dimension_threshold=args.dimension_threshold,
    )
    outcomes = run_loop(
        run_dir=Path(args.run_dir),
        producer_kind=args.producer,
        judge_kind=args.judge,
        tag=args.tag,
        stop_conditions=stop,
    )
    print(f"\nLoop complete: {len(outcomes)} iterations")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.subcommand == "init":
        return cmd_init(args)
    if args.subcommand == "iterate":
        return cmd_iterate(args)
    if args.subcommand == "loop":
        return cmd_loop(args)
    parser.error(f"Unsupported command: {args.subcommand}")
    return 2
