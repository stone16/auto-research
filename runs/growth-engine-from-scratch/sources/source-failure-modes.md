# source-failure-modes

Source digest auto-composed from 2 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- growth-engine-legacy
- growth-engine

---

# Repo: growth-engine-legacy

## CLAUDE.md
```markdown
# Growth Engine

@AGENTS.md

## Architecture

Growth Core (single backend) + Engines (plug-in domain modules). Browser → Core only. Start with `docs/migration/README.md`; use `docs/series/11_growth_core_phase1_tech_spec.md` as deeper Phase 1 reference.

## Current structure

Architecture and migration docs live under `docs/`; start at `docs/INDEX.md`.
The repository also contains an existing SEO/GEO engine tree at
`engines/geo-seo/`. The Growth Core runtime tree (`core/`) has not been created
yet.

## Target structure

`core/` (identity, credentials, ledgers, observability, core_sdk) + `engines/<name>/` + `docs/`

## Rules

Full rules: `AGENTS.md` (loaded above). Operating constraints:

- Migration architecture changes should update `docs/migration/` before runtime
  code changes
- Engine names are provisional — don't lock new names in specs
- Restate goal + target before multi-file edits

```

## AGENTS.md
```markdown
# AGENTS.md

Repo-wide rules. Loaded by Claude Code (via `@AGENTS.md` in `CLAUDE.md`), Codex CLI, Cursor, Aider, Continue.

## Architecture

Growth Engine = Growth Core (single backend) + Engines (plug-in domain modules).

- Browser talks to Core only.
- Engines never see raw Logto tokens.
  - In-process engines (default for new engines) receive a `RequestContext` constructed by Core in the same process.
  - Remote engines (existing services like SEO/GEO) receive a Core-signed internal context envelope and verify it.
- Core owns all platform facts (identity, tenancy, credentials, runs, artifacts, actions, schedules, observability). Engines own domain logic only.
- Engine deployment mode is per-engine: in-process module under Core by default; remote service when justified (existing service, different language stack, hard isolation requirement). See [`docs/adr/0001-engine-deployment-mode.md`](docs/adr/0001-engine-deployment-mode.md).

## Current structure

Architecture and migration docs live under `docs/`; navigation starts at
`docs/INDEX.md`. The repository also contains an existing SEO/GEO engine tree at
`engines/geo-seo/`. The Growth Core runtime tree (`core/`) has not been created
yet and should be introduced only through the migration plan.

## Target structure (Phase 1+)

```
growth-engine/
├── core/                        Core platform service (single deployable)
│   ├── identity/                Logto verify, user/org sync, role/flag evaluator
│   ├── runs

[... truncated to 2500 bytes; full extract at sources/_raw/growth-engine-legacy.md ...]


# Repo: growth-engine

## README.md
```markdown
# Growth Engine

> 为"实体"（公司、品牌、网站、个人、律所、产品 —— 任何有增长目标的对象）做增长的统一平台。
> 一个 tenant 拥有 N 个 growth_target；每个 target 上跑 OODA cycle；cycle 调度 SEO/GEO / Ads / Social engine 的 step；engine 内部编排 skills；行业差异以 industry pack 注入。

**Status**: Greenfield rewrite (v0.3 draft, 2026-04-29). Pre-implementation —
backend skeleton landed via **GE-01**; schema layer (GE-02), tenant-scoped auth (GE-03),
and engine vertical slice (GE-14a) are next on the P0 critical path. Live status in
[`docs/IMPLEMENTATION_PROGRESS.md`](docs/IMPLEMENTATION_PROGRESS.md).

---

## Read First

Architecture-first routing. Start with the overview, then drill down by concern.

| You want to understand | Read |
|---|---|
| Architecture, domain model, decision log (start here) | [`docs/00-overview.md`](docs/00-overview.md) |
| Task graph, status, parallel lane plan, prompt templates | [`docs/IMPLEMENTATION_PROGRESS.md`](docs/IMPLEMENTATION_PROGRESS.md) |
| Domain layers / DB schema / entity relationships | [`docs/10-domain-model/`](docs/10-domain-model/) |
| Engine contract | [`docs/20-engines/`](docs/20-engines/) |
| Skill mechanism | [`docs/22-skills/`](docs/22-skills/) |
| Industry pack mechanism | [`docs/30-industry-packs/`](docs/30-industry-packs/) |
| OODA cycle / attribution v2 / token & billing | [`docs/40-execution-and-attribution/`](docs/40-execution-and-attribution/) |
| Multi-tenancy / i18n / Logto / observability (Sentry + Grafana + Langfuse) / Terraform / Claude Agent SDK | [`docs/50-cross-cutting/`](docs/50-cross-cutting/) |
| Cross-tool agent rules (Claude Code / Codex / Cursor / Aider) | [`AGENTS.md`](AGENTS.md) |
| Claude Code overlay (project-specific rules) | [`CLAUDE.md`](CLAUDE.md) |
| Harness execution conventions | [`docs/HARNESS_CONVENTIONS.md`](docs/HARNESS_CONVENTIONS.md) |

---

## Repo Layout

```
docs/         # SSOT: architecture, task tracker, design decisions
backend/      # FastAPI app skeleton (GE-01); see backend/README.md for local test paths
tests/        # backend test suite
scripts/      # dev/test runner scripts (run-backend-tests.sh etc.)
.harness/     # Harness orchestration scaffolding
references/   # Read-only git submodules — concept reference only, DO NOT import wholesale
```

Production directory boundaries are deliberately **not** locked yet — see `CLAUDE.md`:
"Str

[... truncated to 2500 bytes; full extract at sources/_raw/growth-engine.md ...]

