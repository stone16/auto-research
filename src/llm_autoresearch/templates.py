from __future__ import annotations

from textwrap import dedent

from .models import BenchmarkItem


def default_program(topic: str) -> str:
    return dedent(
        f"""\
        # LLM Auto Research Program

        You are running a bounded research loop for this topic:

        {topic}

        Rules:
        - Treat `knowledge_base.md` as the primary artifact you are improving.
        - Use only the provided source documents for factual claims.
        - Answer benchmark questions directly and cite source IDs.
        - Prefer cleaner, denser, better-organized knowledge over bloated output.
        - If the current knowledge base is weak, rewrite it instead of appending noise.
        - Every answer should be grounded in the provided source set.

        Output contract:
        - Return JSON only.
        - Include `experiment_title`, `change_summary`, `knowledge_base_markdown`, `benchmark_answers`, and optional `notes`.
        """
    )


def default_topic(topic: str) -> str:
    return dedent(
        f"""\
        # Topic Brief

        Topic: {topic}

        Scope:
        - Define the boundaries of this run.
        - Describe what "good understanding" means for this topic.
        - Note which ambiguities should be resolved by future iterations.
        """
    )


def default_knowledge_base(topic: str) -> str:
    return dedent(
        f"""\
        # Knowledge Base

        Topic: {topic}

        Current status:
        - This file is the single mutable artifact for the run.
        - Rewrite and reorganize it when iterations improve understanding.
        """
    )


def default_benchmark() -> list[BenchmarkItem]:
    return [
        BenchmarkItem(
            id="q1",
            question="What are the two or three core ideas this run must capture?",
            rubric="A good answer should explain the central mechanisms or claims, not just list labels.",
            must_include=["core ideas", "mechanism"],
            required_sources=[],
        ),
        BenchmarkItem(
            id="q2",
            question="Which sources best support the strongest claim in this topic?",
            rubric="A good answer should connect claims to evidence and cite explicit source IDs.",
            must_include=["evidence", "source"],
            required_sources=[],
        ),
    ]


def example_topic() -> str:
    return "Why Roman concrete remained durable in marine environments"


def example_sources() -> dict[str, str]:
    return {
        "source-1.md": dedent(
            """\
            # Roman concrete and seawater interaction

            Studies of Roman harbor structures suggest that seawater slowly reacted with volcanic ash
            and lime to form new mineral phases. The reaction produced crystals such as aluminous
            tobermorite, which helped strengthen the concrete over time instead of degrading it.
            """
        ),
        "source-2.md": dedent(
            """\
            # Ingredients in Roman concrete

            Roman concrete differed from many modern mixes because it combined lime, volcanic ash,
            and rock aggregate. The volcanic ash enabled a pozzolanic reaction that contributed to
            long-term durability, especially in marine conditions.
            """
        ),
    }


def example_benchmark() -> list[BenchmarkItem]:
    return [
        BenchmarkItem(
            id="q1",
            question="Why was Roman concrete especially durable in marine environments?",
            rubric="Explain the seawater-driven mineral formation mechanism and why it increased durability.",
            must_include=["seawater", "aluminous tobermorite", "durability"],
            required_sources=["source-1"],
        ),
        BenchmarkItem(
            id="q2",
            question="Which ingredients distinguished Roman concrete from many modern mixes?",
            rubric="Name the characteristic ingredients and connect them to the pozzolanic reaction.",
            must_include=["lime", "volcanic ash", "pozzolanic reaction"],
            required_sources=["source-2"],
        ),
    ]
