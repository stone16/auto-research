# LLM Auto Research

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](#quick-start)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Providers](https://img.shields.io/badge/providers-codex%20%7C%20claude%20%7C%20command-black.svg)](#providers)
[![Status: Experimental](https://img.shields.io/badge/status-experimental-orange.svg)](#llm-auto-research)

`LLM Auto Research` is a provider-agnostic framework for running autonomous research loops against a bounded source set. Instead of asking an agent for a one-off answer, you give it source documents, a mutable `knowledge_base.md`, benchmark questions, and a judge. The loop proposes changes, scores them, keeps the improvements, and discards the regressions.

Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch), but generalized from model-training experiments to reusable topic research workflows.

Read next:
- [Example outputs and use cases](examples/README.md)
- [Approach and operating insights](docs/README.md)

Keywords: llm auto research, autonomous research, agentic workflow, research automation, knowledge base generation, benchmarked writing, codex, claude, human-in-the-loop.

## What This Project Is For

This project is for teams or individuals who want a research artifact to improve over time instead of re-prompting from scratch every time.

Use it when you want to:

- turn a fixed corpus of documents into a denser, better-structured knowledge base
- run producer/judge loops with Codex, Claude, or any custom command provider
- preserve only accepted improvements in git while keeping a full artifact trail
- steer an active run with human feedback without restarting the loop

It works best when:

- the topic is bounded
- the source set is explicit
- the desired output can be benchmarked
- citations and auditability matter

It is not primarily designed for:

- open-web browsing and live source discovery
- unconstrained brainstorming with no scoring rubric
- code-editing loops where the primary artifact is software rather than a knowledge base

## What It Produces

At the end of a useful run, you do not just get "an answer". You get a research workspace with durable artifacts:

| Artifact | What it gives you |
|----------|-------------------|
| `knowledge_base.md` | The current best synthesized view of the topic |
| `benchmark_answers` | Direct answers to fixed evaluation questions, each with citations |
| `results.tsv` | Iteration-by-iteration score history |
| `judge_feedback.md` | Accumulated quality feedback from the judge |
| `artifacts/iteration-*/` | Full audit trail for every attempt, kept or discarded |
| `autoresearch/<tag>` git branch | Clean history containing only accepted improvements |

This makes the output inspectable, reviewable, and resumable. You can see what changed, why it was kept, and how the run improved over time.

## Use Cases

Good fits for this framework include:

- turning a folder of reports or papers into a grounded internal brief
- producing a cited explainer for a technical or scientific topic
- maintaining a living market, policy, or product research memo
- comparing competing hypotheses or source sets against a fixed rubric
- running overnight research loops with a supervisor and checking status in the morning

For a concrete worked example, see [examples/README.md](examples/README.md).

## Quick Start

```bash
# Install
git clone https://github.com/stone16/auto-research.git
cd auto-research
uv sync

# Create an example run
uv run autoresearch init runs/example --example

# Debug with one mock iteration
uv run autoresearch iterate runs/example --provider mock

# Run a short mock loop
uv run autoresearch loop runs/example \
  --producer mock --judge mock \
  --tag example-run \
  --max-iterations 5

# Inspect runtime state
uv run autoresearch status runs/example --json
```

When you are ready to run real agents:

```bash
uv run autoresearch loop runs/glp1-agonists \
  --producer codex --judge claude \
  --tag glp1-v1 \
  --max-total-iterations 25 \
  --dimension-threshold 0.8
```

For long-running real-agent runs, pair the loop with the built-in supervisor:

```bash
uv run autoresearch supervise runs/glp1-agonists \
  --tag glp1-v1 \
  --main-session glp1-v1-main \
  --sidecar-session glp1-v1-supervisor \
  --producer codex --judge claude \
  --max-total-iterations 25 \
  --dimension-threshold 0.8
```

## How To Use It

Each run lives in its own directory under `runs/`. A practical workflow looks like this:

1. Initialize a run with `autoresearch init`.
2. Define the topic in `topic.md`.
3. Write the producer instructions in `program.md`.
4. Add the frozen evidence set to `sources/`.
5. Define benchmark questions and required citations in `benchmark.json`.
6. Start with a mock loop to validate the run shape.
7. Swap in real producer and judge providers.
8. Steer the loop by editing `human_feedback.md` while it runs.

The four most important files to get right are:

- `topic.md` for scope and quality dimensions
- `program.md` for producer behavior
- `benchmark.json` for what "good" means
- `sources/` for the evidence boundary

## Common Usage Modes

### 1. Smoke-test the framework

```bash
uv run autoresearch init runs/example --example
uv run autoresearch loop runs/example --producer mock --judge mock --tag example-run --max-iterations 3
```

Use this first to validate the run layout and scoring pipeline.

### 2. Run a real producer/judge pair

```bash
uv run autoresearch loop runs/my-topic \
  --producer codex \
  --judge claude \
  --tag my-topic-v1
```

This is the normal mode for actual research.

### 3. Plug in your own external system

```bash
uv run autoresearch iterate runs/example \
  --provider command \
  --provider-command "python scripts/example_command_provider.py"
```

Use the `command` provider when you want to integrate your own retrieval stack, orchestration layer, or model wrapper.

## Architecture

```text
┌─────────────────────────────────────────────────────┐
│                     CLI (cli.py)                     │
│  autoresearch init | iterate | loop | status |      │
│  autoresearch supervise                              │
└──────────────┬────────────────────┬──────────────────┘
               │                    │
     ┌─────────▼─────────┐  ┌──────▼──────────────────┐
     │   Run Files Layer  │  │   Git Integration       │
     │   (run_files.py)   │  │   (git.py)              │
     │                    │  │                          │
     │  RunPaths          │  │  init_branch(tag)        │
     │  RunContext        │  │  commit_iteration()      │
     │  init_run()        │  │  reset_last_commit()     │
     │  load_run_context()│  │  get_current_sha()       │
     └────────┬───────────┘  │  ensure_clean_state()    │
              │              └──────────────────────────┘
              │
     ┌────────▼────────────────────────────────────────┐
     │              Iteration Loop (loop.py)           │
     │                                                 │
     │  1. Load context + feedback                     │
     │  2. Ask provider to produce candidate           │
     │  3. Evaluate (deterministic -> LLM judge)       │
     │  4. Keep or discard                             │
     │  5. Git commit (keep) or git reset (discard)    │
     │  6. Accumulate feedback for next iteration      │
     └──┬──────────┬────────────┬───────────┬─────────┘
        │          │            │           │
   ┌────▼───┐ ┌───▼────┐ ┌────▼───┐ ┌─────▼──────┐
   │Provider│ │Evaluator│ │ Judge  │ │ Feedback   │
   │        │ │         │ │        │ │ Engine     │
   │mock    │ │determin-│ │LLM-    │ │judge_feed- │
   │command │ │istic    │ │anchored│ │back.md     │
   │cli     │ │rubric   │ │scoring │ │human_feed- │
   │(codex, │ │matching │ │        │ │back.md     │
   │ claude)│ │         │ │        │ │            │
   └────────┘ └─────────┘ └────────┘ └────────────┘
```

## The Ratchet

Every iteration follows a strict keep/discard protocol:

1. Produce: the provider generates a revised `knowledge_base.md` and benchmark answers.
2. Evaluate: the deterministic evaluator scores benchmark answers for coverage and citations.
3. Judge: the judge scores quality dimensions such as causal completeness and evidence density.
4. Decide: the loop keeps the candidate if it improved enough.
5. Commit or discard: kept iterations become git commits; discarded iterations are reset.

The git history becomes a clean ratchet. Only accepted improvements survive in branch history, while every attempt is still preserved in `artifacts/` for audit.

## Scoring Pipeline

```text
Candidate -> Deterministic Evaluator (boolean gate)
                    |
                    +-- Below threshold -> auto-discard (skip judge)
                    |
                    +-- Above threshold -> LLM Judge
                                              |
                                              +-- Score each quality dimension 0-10
                                              +-- Identify priority dimension
                                              +-- Suggest specific improvement
                                              |
                                              +-- overall_score -> keep or discard
```

## Feedback Loop

The producer does not start from scratch each iteration. It receives:

- `judge_feedback.md`: accumulated judge reviews with priority dimensions and suggestions
- `human_feedback.md`: hot-reloaded operator notes that take effect on the next cycle

This gives the producer directional signal instead of making every iteration a blind rewrite.

## Providers

| Provider | Use Case | How |
|----------|----------|-----|
| `mock` | Framework testing | Built-in deterministic output |
| `command` | Any external process | Pipe JSON via stdin/stdout |
| `cli` | Generic CLI adapter | Spawns a CLI agent subprocess |
| `codex` | Real research producer or judge | Alias for the Codex CLI |
| `claude` | Real research producer or judge | Alias for the Claude CLI |

Providers are swappable via CLI flags:

```bash
# Mock
uv run autoresearch loop runs/my-topic --producer mock --judge mock --tag my-topic-test

# Real agents
uv run autoresearch loop runs/my-topic --producer codex --judge claude --tag my-topic-v1

# Swap roles
uv run autoresearch loop runs/my-topic --producer claude --judge codex --tag my-topic-v2
```

## Run Directory Structure

Each research run is self-contained in a directory:

```text
runs/my-topic/
├── run.json               # Config (topic, slug, provider settings)
├── topic.md               # Scope, goal state, quality dimensions
├── program.md             # Research protocol for the producer
├── knowledge_base.md      # The mutable artifact we are improving
├── benchmark.json         # Fixed evaluation rubric
├── state.json             # Current iteration, best score, etc.
├── results.tsv            # Full experiment history
├── loop_status.json       # Current loop lifecycle + terminal stop reason
├── provider_status.json   # Current in-flight producer/judge activity
├── provider_activity.jsonl # Append-only provider lifecycle events
├── judge_feedback.md      # Accumulated judge reviews
├── human_feedback.md      # Live steering input (hot-reloaded)
├── supervisor_status.json # Optional watchdog state written by `supervise`
├── supervisor.log         # Optional watchdog heartbeat log
├── sources/               # Frozen source documents
│   ├── source-1.md
│   └── source-2.md
└── artifacts/             # Every iteration's full output
    ├── iteration-0001/
    │   ├── task.json
    │   ├── candidate.json
    │   ├── candidate_knowledge_base.md
    │   ├── evaluation.json
    │   └── judge_review.md
    └── iteration-0002/
        └── ...
```

Important: `runs/` is gitignored. The framework is the shareable open-source artifact. Runs are local, per-topic working state.

## Creating A Research Topic

```bash
uv run autoresearch init runs/glp1-agonists --topic "History of GLP-1 agonists"
```

Then edit:

1. `topic.md` to define the goal state and quality dimensions
2. `program.md` to tell the producer how to work
3. `benchmark.json` to encode must-include facts and required citations
4. `sources/` to define the evidence boundary

Start the loop:

```bash
uv run autoresearch loop runs/glp1-agonists \
  --producer codex --judge claude \
  --tag glp1-v1 \
  --max-total-iterations 25 \
  --dimension-threshold 0.8
```

Steer while it runs by editing `runs/glp1-agonists/human_feedback.md`:

```markdown
Focus on the timeline of FDA approvals. The chronology section is weak.
Prioritize evidence from source-3 (the clinical trials meta-analysis).
```

## Stop Conditions

The loop stops when any condition triggers:

| Flag | Effect |
|------|--------|
| `--max-iterations N` | Stop after N iterations |
| `--max-total-iterations N` | Stop after N total completed iterations across restarts |
| `--max-consecutive-discard N` | Stop after N consecutive discards |
| `--dimension-threshold F` | Stop when all quality dimensions exceed `F` |
| `Ctrl+C` | Graceful shutdown after the current iteration |
| `3 consecutive crashes` | Auto-halt with diagnostic state |

## Command Provider Contract

For custom integrations, the `command` provider pipes JSON to stdin and reads JSON from stdout.

Input sent to your command's stdin:

```json
{
  "task_type": "research_iteration",
  "instructions": "...",
  "payload": {
    "topic": "...",
    "knowledge_base_markdown": "...",
    "benchmark": [...],
    "sources": [...],
    "judge_feedback": "...",
    "human_feedback": "..."
  }
}
```

Output your command must write to stdout:

```json
{
  "experiment_title": "tighten the chronology section",
  "change_summary": "Added timeline, strengthened source-3 citations",
  "knowledge_base_markdown": "# ...",
  "benchmark_answers": [
    { "id": "q1", "answer": "...", "citations": ["source-1"] }
  ]
}
```

See `scripts/example_command_provider.py` for a working example.

## Operator Notes

- `runs/` is intentionally gitignored. Live research state, artifacts, logs, and watchdog files are local data.
- `autoresearch status` reads `state.json`, `results.tsv`, `provider_status.json`, and `loop_status.json`. If a supervised run looks stuck, check that command before inspecting tmux manually.
- `autoresearch supervise` is meant for long-running real-agent runs. If you need a hard cap across restarts, use `--max-total-iterations`, not only `--max-iterations`.
- `run.json` role configs can set `producer.timeout_seconds` and `judge.timeout_seconds`.
- Benchmark answers are expected to have non-empty `citations`. The loop can repair empty arrays from inline `[source-*]` tags or benchmark-required sources, but missing source discipline still costs iterations.

## Development

```bash
# Run tests
python -m pytest -q

# Inspect a run
uv run autoresearch status runs/example --json

# Supervisor smoke check
uv run autoresearch supervise runs/example \
  --tag example-run \
  --main-session example-main \
  --producer mock --judge mock \
  --once
```

## Design Principles

- Git as the ratchet: keep a clean history of accepted improvements
- Provider agnostic: mock for testing, CLI agents for real work, command provider for anything else
- Human-in-the-loop: hot-reload feedback without restarting the loop
- Audit by default: full iteration artifacts even when a candidate is discarded
- Open-sourceable framework: the tool is generic; your runs remain private

## License

MIT
