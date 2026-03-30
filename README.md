# LLM Auto Research

This project is a reusable skeleton for topic-specific, LLM-driven research loops.

It borrows the core abstraction from `karpathy/autoresearch`:

- keep a fixed evaluator boundary,
- mutate one primary artifact,
- score the change,
- keep or discard it,
- log every attempt.

The first version here is intentionally provider-agnostic. It ships with a `mock` provider for smoke testing and a `command` provider contract so you can wire in any LLM later with a thin wrapper.

## Core Model

Each research run lives in its own directory and contains:

- `program.md`: human-edited research protocol for the run
- `topic.md`: scope and goals for the topic
- `knowledge_base.md`: the single mutable artifact
- `benchmark.json`: fixed benchmark questions and rubrics
- `sources/`: frozen source documents for the run
- `results.tsv`: experiment history
- `state.json`: current best score and iteration state
- `artifacts/`: saved candidate outputs and evaluation reports

The loop is:

1. Load the current run state.
2. Ask a provider to propose a revised `knowledge_base.md` and answer benchmark questions.
3. Score the candidate answers against the fixed benchmark.
4. Keep the candidate if it improves the best score or ties while simplifying the artifact.
5. Append the result to `results.tsv`.

## Quick Start

Create an example run:

```bash
uv run autoresearch init runs/example --example
```

Run one iteration with the built-in mock provider:

```bash
uv run autoresearch iterate runs/example --provider mock
```

Inspect the run:

```bash
cat runs/example/results.tsv
cat runs/example/knowledge_base.md
```

## Reusing It For New Topics

Create a fresh run:

```bash
uv run autoresearch init runs/my-topic --topic "History of GLP-1 agonists"
```

Then edit:

- `runs/my-topic/topic.md`
- `runs/my-topic/program.md`
- `runs/my-topic/benchmark.json`
- files under `runs/my-topic/sources/`

After that, run iterations:

```bash
uv run autoresearch iterate runs/my-topic --provider mock
```

The `mock` provider is just for testing the framework. For a real model, use `--provider command`.

## Command Provider Contract

The command provider runs an external command, sends a JSON task to stdin, and expects JSON on stdout.

Example:

```bash
uv run autoresearch iterate runs/my-topic \
  --provider command \
  --provider-command "python scripts/my_provider.py"
```

The wrapper command receives a JSON payload like:

```json
{
  "task_type": "research_iteration",
  "instructions": "...run program and response schema...",
  "payload": {
    "topic": "...",
    "program": "...",
    "knowledge_base_markdown": "...",
    "benchmark": [...],
    "sources": [...],
    "history": [...],
    "state": {...}
  }
}
```

It must return JSON like:

```json
{
  "experiment_title": "tighten the chronology section",
  "change_summary": "Add a concise timeline and answer benchmark item q1 more directly.",
  "knowledge_base_markdown": "# ...",
  "benchmark_answers": [
    {
      "id": "q1",
      "answer": "....",
      "citations": ["source-1"]
    }
  ],
  "notes": ["optional free-form notes"]
}
```

A working local example wrapper is included at `scripts/example_command_provider.py`.

## Benchmark Design

The default evaluator is deterministic and rubric-driven. Each benchmark item can specify:

- `must_include`: phrases or facts that should appear in the answer
- `required_sources`: source IDs that should be cited

That means the quality of the loop depends heavily on benchmark design. For a serious run, spend time making `benchmark.json` strict and representative.

## Current Limitations

- No built-in vendor API integration yet
- Judge is deterministic, not LLM-based
- Keep/discard is file-level, not git-commit-level

Those are deliberate choices for the first version because they keep the framework portable and testable.
