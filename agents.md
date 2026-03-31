# agents.md

Repository-specific operating rules for AI coding agents working in this repo.

## Purpose

This repository is the reusable `llm_autoresearch` framework. It is not the place to
commit topic-specific run state. Treat runtime reliability as product behavior, not as
throwaway scripting.

## Non-Negotiables

- Do not commit anything under `runs/`. Live runs, artifacts, watchdog logs, and research corpora are local state.
- Preserve the ratchet contract. The only run files that the loop commits and resets are `knowledge_base.md`, `state.json`, and `results.tsv`.
- Keep `README.md`, CLI parser choices, and provider factory aliases aligned. A documented invocation is part of the public API.
- Missing judge dimensions must score as zero. Never average only the dimensions that happened to come back.
- Large prompts and task payloads must travel through stdin or temp files, not argv.
- Any subprocess with piped stdout/stderr must close descriptors in a `finally` block, including timeout paths.
- Supervisor logic must distinguish unhealthy exits from clean terminal stops. Do not auto-restart a loop that ended because of shutdown, convergence, or an explicit stop cap.
- Benchmark answers must carry non-empty `citations`. If inline `[source-*]` tags are present, mirror them into the structured citation list.

## Preferred Workflow

1. Read `README.md` first for runtime semantics and operator expectations.
2. Run `python -m pytest -q` before shipping behavior changes.
3. For loop / provider / supervisor edits, add or update tests in `tests/` in the same change.
4. When you change runtime behavior, update the run-directory docs in `README.md`.
5. Before pushing, inspect `git status --short`, `git diff --stat`, and the final PR diff for accidental run-state leakage.

## High-Signal Commands

```bash
python -m pytest -q
uv run autoresearch status runs/example --json
uv run autoresearch supervise runs/example --tag example --main-session example-main --producer mock --judge mock --once
```

## Current Failure Modes To Remember

- Provider factory/documentation drift breaks real-agent runs immediately.
- Partial judge payloads can silently inflate scores if dimensions are dropped.
- CLI wrappers that push the full task JSON into argv will fail on real runs.
- Watchdogs that ignore terminal stop reasons will restart completed jobs forever.
