from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import BenchmarkItem, RunConfig, RunState, SourceDocument
from .templates import (
    default_benchmark,
    default_knowledge_base,
    default_program,
    default_topic,
    example_benchmark,
    example_sources,
    example_topic,
)

RESULTS_HEADER = [
    "iteration",
    "timestamp",
    "score",
    "prev_best",
    "status",
    "knowledge_chars",
    "provider",
    "experiment",
    "change_summary",
]


@dataclass
class RunPaths:
    run_dir: Path
    config_path: Path
    topic_path: Path
    program_path: Path
    knowledge_path: Path
    benchmark_path: Path
    results_path: Path
    state_path: Path
    sources_dir: Path
    artifacts_dir: Path


@dataclass
class RunContext:
    paths: RunPaths
    config: RunConfig
    topic_markdown: str
    program_markdown: str
    knowledge_base_markdown: str
    benchmark: list[BenchmarkItem]
    state: RunState
    sources: list[SourceDocument]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    safe = [
        char.lower() if char.isalnum() else "-"
        for char in value.strip()
    ]
    slug = "".join(safe)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "run"


def build_paths(run_dir: Path) -> RunPaths:
    return RunPaths(
        run_dir=run_dir,
        config_path=run_dir / "run.json",
        topic_path=run_dir / "topic.md",
        program_path=run_dir / "program.md",
        knowledge_path=run_dir / "knowledge_base.md",
        benchmark_path=run_dir / "benchmark.json",
        results_path=run_dir / "results.tsv",
        state_path=run_dir / "state.json",
        sources_dir=run_dir / "sources",
        artifacts_dir=run_dir / "artifacts",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, Any] | list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def init_run(run_dir: Path, topic: str | None, provider_kind: str, example: bool) -> RunPaths:
    if run_dir.exists() and any(run_dir.iterdir()):
        raise ValueError(f"Run directory already exists and is not empty: {run_dir}")

    chosen_topic = topic or (example_topic() if example else "New research topic")
    slug = slugify(run_dir.name if run_dir.name else chosen_topic)
    paths = build_paths(run_dir)
    paths.run_dir.mkdir(parents=True, exist_ok=True)
    paths.sources_dir.mkdir(parents=True, exist_ok=True)
    paths.artifacts_dir.mkdir(parents=True, exist_ok=True)

    config = RunConfig(topic=chosen_topic, slug=slug)
    config.provider.kind = provider_kind

    benchmark_items = example_benchmark() if example else default_benchmark()
    source_map = example_sources() if example else {}

    write_json(paths.config_path, config.to_dict())
    write_text(paths.topic_path, default_topic(chosen_topic))
    write_text(paths.program_path, default_program(chosen_topic))
    write_text(paths.knowledge_path, default_knowledge_base(chosen_topic))
    write_json(paths.benchmark_path, [item.to_dict() for item in benchmark_items])
    write_json(paths.state_path, RunState().to_dict())

    with paths.results_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(RESULTS_HEADER)

    for filename, content in source_map.items():
        write_text(paths.sources_dir / filename, content)

    return paths


def parse_source_document(path: Path) -> SourceDocument:
    content = path.read_text(encoding="utf-8").strip()
    title = path.stem
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip() or title
            break
    return SourceDocument(
        id=path.stem,
        title=title,
        content=content,
        path=str(path),
    )


def load_run_context(run_dir: Path) -> RunContext:
    paths = build_paths(run_dir)
    required = [
        paths.config_path,
        paths.topic_path,
        paths.program_path,
        paths.knowledge_path,
        paths.benchmark_path,
        paths.results_path,
        paths.state_path,
        paths.sources_dir,
        paths.artifacts_dir,
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(f"Run is missing required path: {path}")

    config = RunConfig.from_dict(read_json(paths.config_path))
    benchmark = [BenchmarkItem.from_dict(item) for item in read_json(paths.benchmark_path)]
    state = RunState.from_dict(read_json(paths.state_path))
    sources = [
        parse_source_document(path)
        for path in sorted(paths.sources_dir.glob("*.md"))
    ]

    return RunContext(
        paths=paths,
        config=config,
        topic_markdown=paths.topic_path.read_text(encoding="utf-8"),
        program_markdown=paths.program_path.read_text(encoding="utf-8"),
        knowledge_base_markdown=paths.knowledge_path.read_text(encoding="utf-8"),
        benchmark=benchmark,
        state=state,
        sources=sources,
    )


def append_results_row(paths: RunPaths, row: dict[str, Any]) -> None:
    with paths.results_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULTS_HEADER, delimiter="\t")
        writer.writerow(row)


def load_recent_results(paths: RunPaths, limit: int = 5) -> list[dict[str, str]]:
    if not paths.results_path.exists():
        return []
    with paths.results_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return rows[-limit:]

