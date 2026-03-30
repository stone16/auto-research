from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
        return cls(
            id=str(data["id"]),
            answer=str(data.get("answer", "")),
            citations=[str(item) for item in data.get("citations", [])],
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
        return cls(
            experiment_title=str(data["experiment_title"]),
            change_summary=str(data.get("change_summary", "")),
            knowledge_base_markdown=str(data["knowledge_base_markdown"]),
            benchmark_answers=[
                BenchmarkAnswer.from_dict(item) for item in data.get("benchmark_answers", [])
            ],
            notes=[str(item) for item in data.get("notes", [])],
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvaluationConfig":
        return cls(
            minimum_improvement=float(data.get("minimum_improvement", 0.01)),
            allow_tie_if_shorter=bool(data.get("allow_tie_if_shorter", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "minimum_improvement": self.minimum_improvement,
            "allow_tie_if_shorter": self.allow_tie_if_shorter,
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CliAgentConfig":
        return cls(
            cli=str(data.get("cli", "")),
            flags=str(data.get("flags", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "cli": self.cli,
            "flags": self.flags,
        }


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
class IterationOutcome:
    iteration: int
    status: str
    candidate_score: float
    previous_best: float
    knowledge_chars: int
    artifact_dir: str
    experiment_title: str
    change_summary: str

