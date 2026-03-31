from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from typing import Any

_SOURCE_TAG_PATTERN = re.compile(r"\[(source-[A-Za-z0-9_-]+)\]")


def _coerce_json_like(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped:
        return value
    if stripped[0] not in "[{":
        return value
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(stripped)
        except (ValueError, SyntaxError):
            return value


def _coerce_text_block(value: Any) -> str:
    value = _coerce_json_like(value)
    if value is None:
        return ""
    if isinstance(value, list):
        parts = [str(item).strip() for item in value if str(item).strip()]
        return "\n".join(f"- {part}" for part in parts)
    if isinstance(value, dict):
        return json.dumps(value, indent=2, sort_keys=True)
    return str(value)


def _coerce_string_list(value: Any) -> list[str]:
    value = _coerce_json_like(value)
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple | set):
        return [str(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if "," in stripped:
            parts = [part.strip() for part in stripped.split(",") if part.strip()]
            if parts:
                return parts
        return [stripped]
    return [str(value)]


def _ordered_unique_strings(values: list[str]) -> list[str]:
    normalized_values: list[str] = []
    seen: set[str] = set()

    for raw_value in values:
        normalized = str(raw_value).strip()
        if not normalized:
            continue
        match = _SOURCE_TAG_PATTERN.fullmatch(normalized)
        if match is not None:
            normalized = match.group(1)
        if normalized in seen:
            continue
        seen.add(normalized)
        normalized_values.append(normalized)

    return normalized_values


def _extract_source_tags(text: str) -> list[str]:
    if not text:
        return []
    return _ordered_unique_strings(_SOURCE_TAG_PATTERN.findall(text))


def _coerce_benchmark_answer_items(value: Any) -> list[dict[str, Any]]:
    value = _coerce_json_like(value)
    if value is None:
        return []
    if isinstance(value, list):
        return [BenchmarkAnswer.from_dict(item).to_dict() for item in value]
    if isinstance(value, dict):
        if "id" in value or "answer" in value or "text" in value:
            return [BenchmarkAnswer.from_dict(value).to_dict()]

        coerced_items: list[dict[str, Any]] = []
        for key, raw_item in value.items():
            if isinstance(raw_item, dict):
                item = dict(raw_item)
            else:
                item = {"answer": raw_item}
            item.setdefault("id", str(key))
            coerced_items.append(BenchmarkAnswer.from_dict(item).to_dict())
        return coerced_items
    raise ValueError(
        "benchmark_answers must be a list, dict, or JSON string encoding one of those shapes."
    )


@dataclass
class BenchmarkItem:
    id: str
    question: str
    rubric: str
    must_include: list[str] = field(default_factory=list)
    required_sources: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BenchmarkItem":
        return cls(
            id=str(data["id"]),
            question=str(data["question"]),
            rubric=str(data.get("rubric", "")),
            must_include=[str(item) for item in data.get("must_include", [])],
            required_sources=[str(item) for item in data.get("required_sources", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "question": self.question,
            "rubric": self.rubric,
            "must_include": list(self.must_include),
            "required_sources": list(self.required_sources),
        }


@dataclass
class BenchmarkAnswer:
    id: str
    answer: str
    citations: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BenchmarkAnswer":
        data = _coerce_json_like(data)
        if not isinstance(data, dict):
            raise ValueError(
                f"Benchmark answer must be an object, got {type(data).__name__}"
            )

        answer_value = data.get("answer")
        if answer_value is None and "text" in data:
            answer_value = data["text"]
        answer = _coerce_text_block(answer_value)
        citations = _ordered_unique_strings(
            _coerce_string_list(data.get("citations", [])) + _extract_source_tags(answer)
        )
        return cls(
            id=str(data["id"]),
            answer=answer,
            citations=citations,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "answer": self.answer,
            "citations": list(self.citations),
        }


@dataclass
class ResearchResponse:
    experiment_title: str
    change_summary: str
    knowledge_base_markdown: str
    benchmark_answers: list[BenchmarkAnswer]
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ResearchResponse":
        data = _coerce_json_like(data)
        if not isinstance(data, dict):
            raise ValueError(
                f"Research response must be an object, got {type(data).__name__}"
            )

        return cls(
            experiment_title=str(data["experiment_title"]),
            change_summary=_coerce_text_block(data.get("change_summary", "")),
            knowledge_base_markdown=str(data["knowledge_base_markdown"]),
            benchmark_answers=[
                BenchmarkAnswer.from_dict(item)
                for item in _coerce_benchmark_answer_items(data.get("benchmark_answers", []))
            ],
            notes=_coerce_string_list(data.get("notes", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_title": self.experiment_title,
            "change_summary": self.change_summary,
            "knowledge_base_markdown": self.knowledge_base_markdown,
            "benchmark_answers": [item.to_dict() for item in self.benchmark_answers],
            "notes": list(self.notes),
        }


@dataclass
class EvaluationDetail:
    benchmark_id: str
    score: float
    coverage_score: float
    citation_score: float
    matched_must_include: list[str]
    matched_sources: list[str]
    missing_must_include: list[str]
    missing_sources: list[str]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "benchmark_id": self.benchmark_id,
            "score": self.score,
            "coverage_score": self.coverage_score,
            "citation_score": self.citation_score,
            "matched_must_include": list(self.matched_must_include),
            "matched_sources": list(self.matched_sources),
            "missing_must_include": list(self.missing_must_include),
            "missing_sources": list(self.missing_sources),
            "explanation": self.explanation,
        }


@dataclass
class EvaluationReport:
    total_score: float
    details: list[EvaluationDetail]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_score": self.total_score,
            "details": [detail.to_dict() for detail in self.details],
        }


@dataclass
class SourceDocument:
    id: str
    title: str
    content: str
    path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "path": self.path,
        }


@dataclass
class RunState:
    iteration: int = 0
    best_score: float = 0.0
    best_iteration: int | None = None
    current_knowledge_chars: int = 0
    last_kept_experiment: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunState":
        return cls(
            iteration=int(data.get("iteration", 0)),
            best_score=float(data.get("best_score", 0.0)),
            best_iteration=(
                int(data["best_iteration"]) if data.get("best_iteration") is not None else None
            ),
            current_knowledge_chars=int(data.get("current_knowledge_chars", 0)),
            last_kept_experiment=str(data.get("last_kept_experiment", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "iteration": self.iteration,
            "best_score": self.best_score,
            "best_iteration": self.best_iteration,
            "current_knowledge_chars": self.current_knowledge_chars,
            "last_kept_experiment": self.last_kept_experiment,
        }


@dataclass
class EvaluationConfig:
    minimum_improvement: float = 0.01
    allow_tie_if_shorter: bool = True
    gate_threshold: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvaluationConfig":
        return cls(
            minimum_improvement=float(data.get("minimum_improvement", 0.01)),
            allow_tie_if_shorter=bool(data.get("allow_tie_if_shorter", True)),
            gate_threshold=float(data.get("gate_threshold", 0.0)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "minimum_improvement": self.minimum_improvement,
            "allow_tie_if_shorter": self.allow_tie_if_shorter,
            "gate_threshold": self.gate_threshold,
        }


@dataclass
class ProviderConfig:
    kind: str = "mock"
    command: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProviderConfig":
        return cls(
            kind=str(data.get("kind", "mock")),
            command=str(data.get("command", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "command": self.command,
        }


@dataclass
class CliAgentConfig:
    """Configuration for a CLI agent role (producer or judge)."""

    cli: str = ""
    flags: str = ""
    timeout_seconds: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CliAgentConfig":
        raw_timeout = data.get("timeout_seconds")
        return cls(
            cli=str(data.get("cli", "")),
            flags=str(data.get("flags", "")),
            timeout_seconds=int(raw_timeout) if raw_timeout is not None else None,
        )

    def to_dict(self) -> dict[str, Any]:
        data = {
            "cli": self.cli,
            "flags": self.flags,
        }
        if self.timeout_seconds is not None:
            data["timeout_seconds"] = self.timeout_seconds
        return data


@dataclass
class RunConfig:
    topic: str
    slug: str
    provider: ProviderConfig = field(default_factory=ProviderConfig)
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    producer: CliAgentConfig = field(default_factory=CliAgentConfig)
    judge: CliAgentConfig = field(default_factory=CliAgentConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunConfig":
        return cls(
            topic=str(data["topic"]),
            slug=str(data["slug"]),
            provider=ProviderConfig.from_dict(data.get("provider", {})),
            evaluation=EvaluationConfig.from_dict(data.get("evaluation", {})),
            producer=CliAgentConfig.from_dict(data.get("producer", {})),
            judge=CliAgentConfig.from_dict(data.get("judge", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "slug": self.slug,
            "provider": self.provider.to_dict(),
            "evaluation": self.evaluation.to_dict(),
            "producer": self.producer.to_dict(),
            "judge": self.judge.to_dict(),
        }


@dataclass
class QualityDimension:
    """A single quality dimension scored on a 0-10 scale (normalized to 0.0-1.0 by dividing by 10)."""

    name: str
    description: str


@dataclass
class GoalState:
    """Goal state for a research topic: defines when research is 'done' and how to measure quality."""

    done_definition: str
    dimensions: list[QualityDimension]


@dataclass
class StopConditions:
    """Configuration for when to stop the loop."""

    max_iterations: int | None = None
    max_total_iterations: int | None = None
    max_consecutive_discard: int | None = None
    dimension_threshold: float | None = None


@dataclass
class IterationOutcome:
    iteration: int
    status: str
    candidate_score: float
    previous_best: float
    knowledge_chars: int
    artifact_dir: str
    experiment_title: str
    change_summary: str
    priority_dimension: str = ""
    dimension_scores: dict[str, float] | None = None
