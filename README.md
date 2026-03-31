# LLM Auto Research

A provider-agnostic framework for autonomous, LLM-driven research loops. Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — the core idea is simple: mutate a knowledge base, score the change, keep or discard, repeat.

This project generalizes that into a reusable CLI tool with pluggable providers, a git-backed ratchet mechanism, goal-anchored LLM judging, and a feedback engine that gives the producer directional signal across iterations.

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
     │  RunContext         │  │  commit_iteration()     │
     │  init_run()        │  │  reset_last_commit()     │
     │  load_run_context() │  │  get_current_sha()      │
     └────────┬───────────┘  │  ensure_clean_state()    │
              │              └──────────────────────────┘
              │
     ┌────────▼────────────────────────────────────────┐
     │              Iteration Loop (loop.py)            │
     │                                                  │
     │  1. Load context + feedback                      │
     │  2. Ask provider to produce candidate            │
     │  3. Evaluate (deterministic → LLM judge)         │
     │  4. Keep or discard                              │
     │  5. Git commit (keep) or git reset (discard)     │
     │  6. Accumulate feedback for next iteration       │
     └──┬──────────┬────────────┬───────────┬──────────┘
        │          │            │           │
   ┌────▼───┐ ┌───▼────┐ ┌────▼───┐ ┌─────▼──────┐
   │Provider│ │Evaluator│ │ Judge  │ │  Feedback   │
   │        │ │         │ │        │ │  Engine     │
   │mock    │ │determin-│ │LLM-    │ │             │
   │command │ │istic    │ │anchored│ │judge_feed-  │
   │cli     │ │rubric   │ │scoring │ │back.md      │
   │(codex, │ │matching │ │        │ │human_feed-  │
   │ claude)│ │         │ │        │ │back.md      │
   └────────┘ └─────────┘ └────────┘ └─────────────┘
```

### The Ratchet

Every iteration follows a strict keep/discard protocol:

1. **Produce** — The provider generates a revised `knowledge_base.md` and benchmark answers
2. **Evaluate** — Deterministic evaluator scores benchmark answers (coverage + citations)
3. **Judge** — LLM judge scores quality dimensions (causal completeness, evidence density, etc.)
4. **Decide** — Keep if improved; discard otherwise
5. **Commit** — On keep: `git commit`. On discard: `git reset HEAD~1`

The git history becomes a clean ratchet — only improvements survive. Every attempt is preserved in `artifacts/` for audit.

### Scoring Pipeline

```text
Candidate → Deterministic Evaluator (boolean gate)
                    │
                    ├── Below threshold → auto-discard (skip judge)
                    │
                    └── Above threshold → LLM Judge
                                              │
                                              ├── Score each quality dimension 0-10
                                              ├── Identify priority dimension
                                              ├── Suggest specific improvement
                                              │
                                              └── overall_score → _decision()
                                                                      │
                                                                      ├── keep
                                                                      └── discard
```

### Feedback Loop

The producer doesn't start from scratch each iteration. It receives:

- **Judge feedback** (`judge_feedback.md`) — Accumulates across iterations. Last N reviews with priority dimensions and specific suggestions.
- **Human feedback** (`human_feedback.md`) — Hot-reloaded each iteration. Edit it while the loop runs; changes take effect on the next cycle.

This gives the producer directional signal: "your evidence density is weak, strengthen citations for source-3."

## Providers

| Provider | Use Case | How |
|----------|----------|-----|
| `mock` | Framework testing | Built-in, deterministic output |
| `command` | Any external process | Pipe JSON via stdin/stdout |
| `cli` (codex, claude) | Real research | Spawns CLI agent as subprocess |

Providers are swappable via CLI flags:

```bash
# Mock (testing)
uv run autoresearch loop runs/my-topic --producer mock --judge mock

# Real agents
uv run autoresearch loop runs/my-topic --producer codex --judge claude

# Swap roles
uv run autoresearch loop runs/my-topic --producer claude --judge codex
```

## Run Directory Structure

Each research run is self-contained in a directory:

```text
runs/my-topic/
├── run.json              # Config (topic, slug, provider settings)
├── topic.md              # Scope, goal state, quality dimensions
├── program.md            # Research protocol for the producer
├── knowledge_base.md     # THE mutable artifact (what we're improving)
├── benchmark.json        # Fixed evaluation rubric
├── state.json            # Current iteration, best score, etc.
├── results.tsv           # Full experiment history
├── loop_status.json      # Current loop lifecycle + terminal stop reason
├── provider_status.json  # Current in-flight producer/judge activity
├── provider_activity.jsonl # Append-only provider lifecycle events
├── judge_feedback.md     # Accumulated judge reviews (auto-written)
├── human_feedback.md     # Your live steering input (hot-reloaded)
├── supervisor_status.json # Optional watchdog state written by `supervise`
├── supervisor.log        # Optional watchdog heartbeat log
├── sources/              # Frozen source documents
│   ├── source-1.md
│   └── source-2.md
└── artifacts/            # Every iteration's full output (audit trail)
    ├── iteration-0001/
    │   ├── task.json
    │   ├── candidate.json
    │   ├── candidate_knowledge_base.md
    │   ├── evaluation.json
    │   └── judge_review.md
    └── iteration-0002/
        └── ...
```

**Important**: `runs/` is gitignored. The framework is the open-source artifact; runs are per-user, per-topic working state. Each user creates their own runs for their own research topics.

## Quick Start

```bash
# Install
git clone https://github.com/stone16/auto-research.git
cd auto-research
uv sync

# Create an example run
uv run autoresearch init runs/example --example

# Single iteration (for debugging)
uv run autoresearch iterate runs/example --provider mock

# Continuous loop (the real deal)
uv run autoresearch loop runs/example \
  --producer mock --judge mock \
  --tag example-run \
  --max-iterations 10

# Inspect the current runtime state
uv run autoresearch status runs/example

# Run a watchdog that restarts the loop if the main tmux session dies
uv run autoresearch supervise runs/example \
  --tag example-run \
  --main-session example-run-main \
  --sidecar-session example-run-supervisor \
  --producer mock --judge mock

# Inspect results
cat runs/example/results.tsv
cat runs/example/knowledge_base.md
git log --oneline autoresearch/example-run  # Only kept iterations appear
```

## Creating a Research Topic

```bash
uv run autoresearch init runs/glp1-agonists --topic "History of GLP-1 agonists"
```

Then edit:
1. **`topic.md`** — Define the goal state and quality dimensions (what "done" looks like)
2. **`program.md`** — Instructions for the producer LLM
3. **`benchmark.json`** — Evaluation rubric with must-include facts and required citations
4. **`sources/`** — Add your source documents (the frozen evidence set)

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

`supervise` writes `supervisor_status.json` and `supervisor.log`, and will restart the
main loop session if it disappears. Restarts use `--resume-branch`, so the watchdog can
reattach to the existing `autoresearch/<tag>` branch instead of failing on branch reuse.
The watchdog also reads `loop_status.json`, so a loop that ended cleanly because of
`max_iterations`, `max_total_iterations`, `max_consecutive_discard`,
`dimension_threshold`, or operator shutdown is reported as `stopped` instead of being
treated like a crash and relaunched forever.

## Stop Conditions

The loop stops when any condition triggers:

| Flag | Effect |
|------|--------|
| `--max-iterations N` | Stop after N iterations |
| `--max-total-iterations N` | Stop after N total completed iterations across restarts |
| `--max-consecutive-discard N` | Stop after N consecutive discards (stuck) |
| `--dimension-threshold F` | Stop when all quality dimensions exceed F |
| Ctrl+C | Graceful shutdown (finishes current iteration) |
| 3 consecutive crashes | Auto-halt with diagnostic |

## Command Provider Contract

For custom integrations, the `command` provider pipes JSON to stdin and reads JSON from stdout:

**Input** (sent to your command's stdin):
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

**Output** (your command writes to stdout):
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

- `runs/` is intentionally gitignored. The framework code is shareable, but live research state, artifacts, logs, and watchdog files are local working data.
- `autoresearch status` reads `state.json`, `results.tsv`, `provider_status.json`, and `loop_status.json`. If a supervised run looks stuck, check that command before inspecting tmux manually.
- `autoresearch supervise` is meant for long-running real-agent runs. If you need a hard cap across restarts, use `--max-total-iterations`, not just `--max-iterations`.
- `run.json` role configs can set `producer.timeout_seconds` and `judge.timeout_seconds`. This is the right place to tune slow Codex / Claude jobs without changing framework defaults.
- Benchmark answers are expected to have non-empty `citations`. The loop can repair empty arrays from inline `[source-*]` tags or benchmark-required sources, but missing source discipline still costs iterations.

## Maintenance Notes

- Keep CLI choices, README examples, and provider factory aliases in sync. If the docs say `--producer codex --judge claude`, `create_provider()` and parser choices must accept those exact strings.
- Missing judge dimensions must count as `0`, not get dropped from the average. Partial judge payloads are a failure mode, not free score inflation.
- Large provider payloads must go through stdin or temp files, never argv. Real runs will hit OS argument-length limits.
- Any `subprocess.Popen(..., stdout=PIPE, stderr=PIPE)` path must close pipes in `finally`, including timeouts.
- Supervisor changes need to preserve terminal-stop semantics. A loop that finished cleanly should not be auto-restarted and misreported as unhealthy.
- Repo-specific agent guidance lives in `agents.md`.

## Development

```bash
# Run tests
uv run python -m pytest tests/ -v

# Run a single test file
uv run python -m pytest tests/test_git.py -v
```

## Design Principles

- **Zero external dependencies** — Pure Python, standard library + subprocess
- **Git as the ratchet** — Clean history of only improvements; full audit trail in artifacts
- **Provider agnostic** — Mock for testing, CLI agents for real work, command for anything else
- **Human-in-the-loop** — Hot-reload feedback without restarting the loop
- **Open-sourceable framework** — The tool is generic; your research runs are private

## License

MIT
