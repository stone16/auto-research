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
"Structure first, naming later."

---

## References Submodules

`references/` carries three concept-reference repos pinned as submodules:

- `lawyer_marketing/` — ads management reference
- `cloud-claw-k/` — social media management reference
- `geo-seo-v2/` — SEO/GEO reference

Initialize / refresh:

```bash
git submodule update --init --recursive   # after fresh clone
git submodule update --remote             # pull upstream (explicit opt-in only)
```

Their toolchains are isolated; `cd` into one before running its commands. The
previous Growth Engine attempt is preserved at `Optiminds-Inc/growth-engine-legacy`
for concept reference only — not imported here.

---

## Local Dev (After GE-01)

The skeleton runs; full feature set requires GE-02 onwards. Local test paths
(hermetic testcontainers, existing-Postgres reuse, `.env.example`) live in
[`backend/README.md`](backend/README.md). `docker-compose.yml` at the repo root
brings up Postgres; `scripts/run-backend-tests.sh` is the canonical test runner.

Cloud runtime (Azure / AKS / Terraform / CI-CD) is owned by **GE-09a → GE-09b → GE-27** —
not present until those lanes land.

```

## CLAUDE.md
```markdown
# Identity & Context Awareness

**CRITICAL**: Address the user as "stometa" at the start of EVERY response.

This serves as a context-awareness signal — if missing, indicates context drift.

---

# Growth Engine

@AGENTS.md

**Status**: Greenfield rewrite. Previous attempt is preserved at `Optiminds-Inc/growth-engine-legacy` for concept reference only — do not import its scaffolding wholesale.

## Architecture Map

```
growth-engine/
├── AGENTS.md              # Cross-tool rules (loaded above via @AGENTS.md)
├── CLAUDE.md              # This file — Claude Code overlay
├── references/            # Read-only git submodules (concept references)
│   ├── lawyer_marketing/      # Ads management reference
│   ├── cloud-claw-k/          # Social media management reference
│   └── geo-seo-v2/            # SEO/GEO reference
└── .harness/              # Harness orchestration scaffolding
```

Production directory layout is deliberately deferred. **Structure first, naming later** — do not lock module names or boundaries until the rewrite scope is defined.

## Commands

No build commands yet — repo is pre-implementation. Reference repos under `references/` carry their own toolchains; `cd` into one before running its commands.

```bash
git submodule update --init --recursive   # initialize references after clone
git submodule update --remote             # pull upstream changes (explicit opt-in)
```

## Progressive Disclosure

| Task | Read First |
|------|------------|
| Hard rules, writing discipline | `@AGENTS.md` |
| Reference: ads management | `references/lawyer_marketing/` |
| Reference: social media management | `references/cloud-claw-k/` |
| Reference: SEO/GEO | `references/geo-seo-v2/` |

## Do Not

- Don't propose ADRs to track renames (structure first, naming later).
- Don't import legacy paths verbatim — they exist in `Optiminds-Inc/growth-engine-legacy`, not here.

```

## AGENTS.md
```markdown
# AGENTS.md

Repo-wide rules. Loaded by Claude Code (via `@AGENTS.md` in `CLAUDE.md`), Codex CLI, Cursor, Aider, Continue.

## Hard Rules

Apply every task.

**Cite file:line for any code claim.** "The handler verifies tenant scoping" is not evidence; `path/to/file.py:88` is. If you cannot cite, you have not verified — say so.

**Never fabricate command output.** Run the test, run the migration, run `curl`. Paste the real output. Inferred output is fiction — discard it. If you cannot run a command (no env, no perms), say so explicitly.

**Restate before multi-file edits.** Restate the goal, target directory, and deliverable in one sentence each. If you cannot, ask one clarifying question — do not proceed on assumed scope.

**Challenge before endorsing.** In architecture discussions, surface counterpoints first. Name the constraint that rules out alternatives. If you cannot name one, you have made a guess — not a recommendation.

## Writing Discipline

Principles in this AGENTS.md and in design docs use **imperative prose**, not bullet checklists. Six patterns: refusal ("Do not X until Y"), anchor ("**This is the rule.**"), falsifiability ("If you cannot X, the Y is a vibe — discard"), contrast ("A; not-A"), action-observation ("Action. Watch result."), inline don't (do + negation in same sentence).

Tables are for lookup (config defaults, parameter mappings, schemas). Prose for discipline.

```

## agents.md
```markdown
# AGENTS.md

Repo-wide rules. Loaded by Claude Code (via `@AGENTS.md` in `CLAUDE.md`), Codex CLI, Cursor, Aider, Continue.

## Hard Rules

Apply every task.

**Cite file:line for any code claim.** "The handler verifies tenant scoping" is not evidence; `path/to/file.py:88` is. If you cannot cite, you have not verified — say so.

**Never fabricate command output.** Run the test, run the migration, run `curl`. Paste the real output. Inferred output is fiction — discard it. If you cannot run a command (no env, no perms), say so explicitly.

**Restate before multi-file edits.** Restate the goal, target directory, and deliverable in one sentence each. If you cannot, ask one clarifying question — do not proceed on assumed scope.

**Challenge before endorsing.** In architecture discussions, surface counterpoints first. Name the constraint that rules out alternatives. If you cannot name one, you have made a guess — not a recommendation.

## Writing Discipline

Principles in this AGENTS.md and in design docs use **imperative prose**, not bullet checklists. Six patterns: refusal ("Do not X until Y"), anchor ("**This is the rule.**"), falsifiability ("If you cannot X, the Y is a vibe — discard"), contrast ("A; not-A"), action-observation ("Action. Watch result."), inline don't (do + negation in same sentence).

Tables are for lookup (config defaults, parameter mappings, schemas). Prose for discipline.

```
