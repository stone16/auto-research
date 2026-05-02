# source-cognitive-models

Source digest auto-composed from 10 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- growth-engine
- growth-engine-legacy
- attribution_v2
- multica
- optiminds-repo-template
- lawyer_finder
- openfang
- claw-mu
- cuilawgroup
- lawyer_marketing

---

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
│   ├── runs/                    workflow_runs, engine_runs, run_events ledgers
│   ├── credentials/             credential records and lease issuer
│   ├── schedules/               workflow_schedules and poller
│   ├── observability/           Sentry/Langfuse helpers, run-event redactor
│   ├── core_sdk/                transport abstraction (in-process + signed-http)
│   └── engines/<name>/          in-process engine modules (default for new engines)
├── engines/<name>/              remote engine services (existing SEO/GEO; new engines that opt remote)
└── docs/                        specs, ADRs, runbooks, FUTURE_SCOPE
```

The `core/engines/` and `engines/` split encodes the deployment-mode choice from
ADR-0001: `core/engines/<name>/` is in-process under Core, `engines/<name>/` is a
separate deployable.

## Moat-binding rules

| # | Rule | Source | Breaks if violated |
|---|---|---|---|
| 1 | Core is the only browser-facing surface; engines never receive raw Logto tokens. The trust boundary is logical — applies to in-process modules and remote services equally | series/11 §6, series/12 §2; ADR-0001 | identity stitching |
| 2 | Platform facts written through `core_sdk` (`workflow_runs`, `engine_runs`, `run_events`, `growth_artifacts`, `action_ledger`) | series/11 §2 | attribution graph; audit trail |
| 3 | Credentials never leave Core; engines get scoped, time-bound leases | series/11 §7, series/12 §4.1 | credential rotation |
| 4 | Sentry + Langfuse + run-event log via `core/observability` only | series/11 §11 | trace correlation |
| 5 | Industry adaptation = domain packs, not `if industry == "..."`; generic labels (`SaaS`, `legal`, `e-commerce`) forbidden — require product-vertical specificity | series/12 §1; Stometa 2026-04-28 | scaling to N industries |
| 6 | Schedules registered in Core in Phase 1; engines do NOT run own cron loops | series/11 §4.1, series/12 §2 | Phase 2 Temporal migration |

## Established rules

- Branches: `feat/`, `fix/`, `docs/`, `refactor/` — never push to `main`
- Commits: Conventional Commits; no `Co-Authored-By`; atomic (one concern per commit)
- No secrets in git; if leaked, rotate FIRST then clean history
- No `--no-verify`, no force-push to shared branches, no `--amend` on pushed commits without permission
- No PII in logs; observability helpers must redact before write
- Doc-first for non-trivial changes — needs `docs/series/` or `docs/adr/` paper trail before code lands
- PR descriptions: Summary + Why + Out of scope + Validation

## Hard Rules

Extend the **Moat-binding rules** and **Established rules** above. Apply every task.

**Cite file:line for any code claim.** "Core verifies tenant scoping" is not evidence; `core/identity/verify.py:88` is. If you cannot cite, you have not verified — say so.

**Never fabricate command output.** Run `pytest`, run the migration, run `curl`. Paste the real output. Inferred output is fiction — discard it. If you cannot run a command (no env, no perms), say so explicitly.

**Restate before multi-file edits.** Restate the goal, target directory, and deliverable in one sentence each. If you cannot, ask one clarifying question — do not proceed on assumed scope.

**Challenge before endorsing.** In architecture discussions, surface counterpoints first. Name the constraint that rules out alternatives. If you cannot name one, you have made a guess — not a recommendation.

## Writing Discipline

Principles in this AGENTS.md and in `docs/series/`, `docs/adr/` use **imperative prose**, not bullet checklists. Six patterns: refusal ("Do not X until Y"), anchor ("**This is the rule.**"), falsifiability ("If you cannot X, the Y is a vibe — discard"), contrast ("A; not-A"), action-observation ("Action. Watch result."), inline don't (do + negation in same sentence).

Tables are for lookup (config defaults, parameter mappings, schemas). Prose for discipline. The Moat-binding rules table above is a reference table and stays as a table.

```

## agents.md
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
│   ├── runs/                    workflow_runs, engine_runs, run_events ledgers
│   ├── credentials/             credential records and lease issuer
│   ├── schedules/               workflow_schedules and poller
│   ├── observability/           Sentry/Langfuse helpers, run-event redactor
│   ├── core_sdk/                transport abstraction (in-process + signed-http)
│   └── engines/<name>/          in-process engine modules (default for new engines)
├── engines/<name>/              remote engine services (existing SEO/GEO; new engines that opt remote)
└── docs/                        specs, ADRs, runbooks, FUTURE_SCOPE
```

The `core/engines/` and `engines/` split encodes the deployment-mode choice from
ADR-0001: `core/engines/<name>/` is in-process under Core, `engines/<name>/` is a
separate deployable.

## Moat-binding rules

| # | Rule | Source | Breaks if violated |
|---|---|---|---|
| 1 | Core is the only browser-facing surface; engines never receive raw Logto tokens. The trust boundary is logical — applies to in-process modules and remote services equally | series/11 §6, series/12 §2; ADR-0001 | identity stitching |
| 2 | Platform facts written through `core_sdk` (`workflow_runs`, `engine_runs`, `run_events`, `growth_artifacts`, `action_ledger`) | series/11 §2 | attribution graph; audit trail |
| 3 | Credentials never leave Core; engines get scoped, time-bound leases | series/11 §7, series/12 §4.1 | credential rotation |
| 4 | Sentry + Langfuse + run-event log via `core/observability` only | series/11 §11 | trace correlation |
| 5 | Industry adaptation = domain packs, not `if industry == "..."`; generic labels (`SaaS`, `legal`, `e-commerce`) forbidden — require product-vertical specificity | series/12 §1; Stometa 2026-04-28 | scaling to N industries |
| 6 | Schedules registered in Core in Phase 1; engines do NOT run own cron loops | series/11 §4.1, series/12 §2 | Phase 2 Temporal migration |

## Established rules

- Branches: `feat/`, `fix/`, `docs/`, `refactor/` — never push to `main`
- Commits: Conventional Commits; no `Co-Authored-By`; atomic (one concern per commit)
- No secrets in git; if leaked, rotate FIRST then clean history
- No `--no-verify`, no force-push to shared branches, no `--amend` on pushed commits without permission
- No PII in logs; observability helpers must redact before write
- Doc-first for non-trivial changes — needs `docs/series/` or `docs/adr/` paper trail before code lands
- PR descriptions: Summary + Why + Out of scope + Validation

## Hard Rules

Extend the **Moat-binding rules** and **Established rules** above. Apply every task.

**Cite file:line for any code claim.** "Core verifies tenant scoping" is not evidence; `core/identity/verify.py:88` is. If you cannot cite, you have not verified — say so.

**Never fabricate command output.** Run `pytest`, run the migration, run `curl`. Paste the real output. Inferred output is fiction — discard it. If you cannot run a command (no env, no perms), say so explicitly.

**Restate before multi-file edits.** Restate the goal, target directory, and deliverable in one sentence each. If you cannot, ask one clarifying question — do not proceed on assumed scope.

**Challenge before endorsing.** In architecture discussions, surface counterpoints first. Name the constraint that rules out alternatives. If you cannot name one, you have made a guess — not a recommendation.

## Writing Discipline

Principles in this AGENTS.md and in `docs/series/`, `docs/adr/` use **imperative prose**, not bullet checklists. Six patterns: refusal ("Do not X until Y"), anchor ("**This is the rule.**"), falsifiability ("If you cannot X, the Y is a vibe — discard"), contrast ("A; not-A"), action-observation ("Action. Watch result."), inline don't (do + negation in same sentence).

Tables are for lookup (config defaults, parameter mappings, schemas). Prose for discipline. The Moat-binding rules table above is a reference table and stays as a table.

```


# Repo: attribution_v2

## README.md
```markdown
# attribution_v2

GetuAI ads attribution and lead tracking — v2. A browser SDK + two FastAPI services + a Next.js dashboard for turning UTM-tagged, cross-subdomain user journeys into scored, enriched leads.

## What

`attribution_v2` replaces the first-generation Getu attribution stack with a cleaner split:

- **`sdk/`** — a TypeScript browser SDK customers embed on their sites to emit events, carry UTM parameters across subdomains, and bridge anonymous sessions to identified users.
- **`events-track-server/`** — a Python/FastAPI pair (ingress + consumer) that takes SDK events, enriches them (GeoIP, device, ad params), queues via GCP Pub/Sub, and persists into the event tables.
- **`server/`** — the Python/FastAPI dashboard API: attribution aggregation, lead extraction, scoring, billing, and auth.
- **`frontend-v2/`** — a Next.js 14 UI for analysts to explore campaigns, cohorts, and lead pipelines. (`frontend/` is the legacy v1 React+Vite app, kept only for parity during the migration.)

The active refactor goals are tracked in [`target.md`](target.md): reshape backend/tracker/SDK to power the `frontend-v2` UI while keeping legacy APIs and historical data intact.

## Status

- **Lifecycle stage**: MVP → Scaling (v2 refactor in progress)
- **Live traffic**: yes (production)
- **Primary owner**: @Optiminds-Inc/engineering  <!-- refine once team boundaries are set -->

## Architecture

```
                  ┌──────────────────┐
  customer site → │   sdk (browser)  │
                  └────────┬─────────┘
                           │  HTTPS, events+attribution
                           ▼
   ┌──────────────────────────────────────────────┐
   │  nginx (see nginx.conf)                       │
   │   /tracker/api/  → events-track-server (ingress)
   │   /consumer/api/ → events-track-server (consumer)
   │   /dashboard/api/→ server (dashboard API)
   │   /              → frontend-v2 (:3103)
   └──────────────────┬────────────────┬──────────┘
                      │                │
               ┌──────▼──────┐   ┌─────▼─────┐
               │ MySQL         │   │ MySQL      │
               │ DATA_DB       │   │ ADS_DB     │
               │ (events, leads)│   │ (attribution)
               └───────────────┘   └────────────┘
                      ▲
                      │
               ┌──────┴──────────┐
               │ GCP Pub/Sub     │
               │ (event queue +  │
               │  dead-letter)   │
               └─────────────────┘
```

Full architectural landmines (dual-DB routing, cross-subdomain session, SDK dispatch bifurcation, user-id rotation semantics) live in [CLAUDE.md](CLAUDE.md). Read it before writing non-trivial code.

## Run Locally

### Prerequisites

- **Node 20+** (SDK, frontend)
- **Python 3.12+** (server), **3.11+** (events-track-server)
- **uv** (Python package manager) — `brew install uv`
- **MySQL** running locally (or access to a dev instance)
- **Docker** (optional, for supporting services)
- Access to shared secrets (GCP Pub/Sub credentials, DB credentials)

### Setup

```bash
# 1. SDK
cd sdk && npm install && npm run build

# 2. Dashboard API (server/)
cd ../server
uv sync
cp env.example .env                 # fill DB_HOST / ADS_DB_NAME / DATA_DB_NAME
alembic upgrade head
python start.py                     # :8000

# 3. Event ingress + consumer (events-track-server/)
cd ../events-track-server
uv sync
cp configs/env.example .env         # DB, Redis, Pub/Sub credentials
python -m api.main                  # :8019

# 4. Frontend v2 (current UI)
cd ../frontend-v2
npm install
npm run dev                         # http://localhost:3103
```

### Expected

`curl http://localhost:8000/dashboard/api/health` → 200. `curl http://localhost:8019/tracker/api/health` → 200. The Next.js dev server at :3103 renders without API errors in the browser console.

## Run Tests

- **SDK**: `cd sdk && npm test` / `npm run test:regression` (cross-subdomain + session rotation).
- **Server / events-track-server**: `pytest tests/` (per-sub-package; coverage wiring still evolving).

## Deploy

`cd deploy && ./deploy.sh -b main -e production -y`. Full rollout procedure, branches-to-env mapping, and rollback steps are in [`deploy/DEPLOYMENT.md`](deploy/DEPLOYMENT.md) and [`docs/runbooks/deploy.md`](docs/runbooks/deploy.md).

## Observability

- **Logs**: <!-- TODO: paste production log aggregator link -->
- **Metrics / Traces**: <!-- TODO: Grafana dashboard URL -->
- **Errors**: <!-- TODO: Sentry project link -->

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| SDK cookies not shared across subdomains | eTLD+1 landed on a public suffix (`.vercel.app`, `.github.io`) | Pass explicit `domain` to the SDK init |
| `alembic upgrade head` hits "multiple heads" | Feature branches added migrations in parallel | `alembic merge heads -m "..."` then upgrade |
| Lead table missing rows for known users | Event extracts `name`/`email` lazily; `setUserId` hasn't fired yet | Check SDK `setUserId` wiring on the customer site |

## Contributing

- Read [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md) before non-trivial changes.
- PR expectations: [.github/pull_request_template.md](.github/pull_request_template.md).
- Architecture decisions: [docs/adr/](docs/adr/).

## Related Repos

- Downstream consumers of the SDK — <!-- TODO: list known integrators -->

---

<sub>Scaffolded from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template).</sub>

```

## CLAUDE.md
```markdown
# CLAUDE.md

<!-- Per-repo identity. Org-wide rules live in AGENTS.md. Keep <~50 lines. -->

@AGENTS.md

## Purpose

GetuAI Attribution v2 — ads attribution and lead tracking. A browser SDK captures UTM-driven user journeys across subdomains; two FastAPI services ingest events and expose a dashboard API; a Next.js app renders analytics and lead management. Current focus: refactor `server/` / `events-track-server/` / `sdk/` to feed `frontend-v2/`'s new UI. Current refactor scope is tracked in `target.md`.

## Architecture (5 landmines)

- **Monorepo, 4 active deployables**: `sdk/` (browser JS), `events-track-server/` (FastAPI ingress + consumer), `server/` (FastAPI dashboard API), `frontend-v2/` (Next.js 14, :3103). `frontend/` is legacy v1 — prefer `frontend-v2/` for anything new.
- **Dual MySQL schemas in `server/`** — `ADS_DB_NAME` (default; alembic migrations target this) + `DATA_DB_NAME`. Writes/reads may land in either depending on the table; check `server/core/database.py` before adding a model.
- **Cross-subdomain session via root-domain cookies** — SDK auto-detects eTLD+1 and writes `_getuai_session` / `_getuai_attrib` / `getuai_user_id` there. Public suffixes (`.vercel.app`, `.github.io`) break auto-detection and need an explicit `domain` config. See `sdk/src/session/`.
- **Event dispatch bifurcates** — `PURCHASE` / `LOGIN` / `SIGNUP` / `FORM_SUBMIT` / `EMAIL_VERIFICATION` / `AUDIT_APPROVED` send **immediately**; all others batch every 2s or at 100 events. Don't silently add a new "conversion-type" event to the batch path — data loss is invisible.
- **`setUserId` session rotation** — anonymous → `setUserId(A)` keeps the same `session_id` (backend backfills). `setUserId(A)` → `setUserId(B)` **rotates** `session_id`. Logout alone does NOT rotate.

## Domain Vocabulary

- **tracking_user_id** — per-company identifier: UUID for anonymous, caller-provided for identified users.
- **lead** — `(company_id, tracking_user_id)` tuple with name/email/phone extracted from form_submit / signup / login events; fields: `score` 0–100, `status` ∈ {new, engaged, qualified, opportunity, customer, churned}, `signal_strength` ∈ {hot, warm, cold}.
- **attribution** — first-touch + last-touch UTM snapshot, one record per session (not per user).
- **session_id** — survives cross-subdomain navigation; rotates only on user-identity change.

## Run Locally

```bash
# SDK
cd sdk && npm install && npm run build

# Dashboard API (server/)
cd server && uv sync && cp env.example .env    # fill DB_HOST / ADS_DB_NAME / DATA_DB_NAME
alembic upgrade head && python start.py         # :8000

# Event ingress + consumer (events-track-server/)
cd events-track-server && uv sync && cp configs/env.example .env
python -m api.main                              # :8019

# Frontend v2 (current UI)
cd frontend-v2 && npm install && npm run dev    # :3103
```

## Common Tasks

- **SDK tests**: `cd sdk && npm test` — cross-subdomain + session-rotation regressions via `npm run test:regression`.
- **SDK version bump**: edit `sdk/package.json` version → `npm run build` (scripts/update-version.js syncs `src/version.ts`).
- **DB migrations**: `alembic upgrade head` — run in `server/` and `events-track-server/` separately (each has its own `alembic/`).
- **Deploy**: `cd deploy && ./deploy.sh -b main -e production -y`; full docs in `deploy/DEPLOYMENT.md`.

## File Ownership (per-repo caution levels)

- **High caution** (ask before editing): `server/alembic/`, `events-track-server/alembic/`, `sdk/src/` public API surface, `nginx.conf` routing.
- **Legacy — prefer `frontend-v2/`**: `frontend/` is v1 React+Vite, only touch for critical bugs.
- **AGENTS.md §Core Principles #3 known exception**: `events-track-server/consumer/dead_letter_service.py` and `events-track-server/service/queue/pubsub_queue_client.py` directly import `google.cloud.pubsub_v1`. See `docs/adr/0001-accept-gcp-pubsub-in-events-tracker.md`.
- **Active security debt**: see `docs/security/known-leaks.md` — a GCP service-account private key is currently tracked in HEAD (`events-track-server/credentials/gcp-pub-sub.json`), rotation deferred. New credentials MUST go through env / Secret Manager, never into a file under `credentials/`.

<!-- Path-based review routing: see .github/CODEOWNERS (pending team setup) -->

每次做spec最终测试，都需要把env和credentials通过worktree-setup.shcp到相关的worktree，来启动浏览器测试环境或者必要的带环境的代码测试

---

<sub>Org-wide rules: [AGENTS.md](AGENTS.md). Deep guides auto-trigger as skills — list via `~/.optiminds/scripts/install-skills.sh list`.</sub>

```

## AGENTS.md
```markdown
# AGENTS.md

<!--
Organization-wide agent instructions for every Optiminds repository. This
file is the single source of truth for cross-repo rules. It is readable by
Claude Code (via `@AGENTS.md` reference in CLAUDE.md), Codex CLI (native),
Cursor, Aider, and Continue (all auto-load AGENTS.md).

Per-repo identity lives in CLAUDE.md, not here. This file should almost
never diverge between repos — if you feel the urge to override a rule
here for one repo, write an ADR instead.

Keep under ~200 lines. When a topic needs more depth, add it as a skill in
`skills/optiminds-<topic>/SKILL.md` — skills auto-trigger on matching
context and don't bloat the always-loaded AGENTS.md.
-->

## Core Principles

<!-- DRAFT: Stometa to finalize. These 7 principles were drafted from the
2026-04-21 CTO brainstorm (rankgale incident, cloud migration, harness
model). Refine the wording / ordering / add-remove as needed before the
first major adoption. -->

1. **Never commit secrets.** Every `.env*`, `credentials/`, `keys/`, token,
   or API key must be in `.gitignore` **before** the file is written.
   If a secret leaks to git history: rotate first in Key Vault, then clean
   history. Never reverse that order.

2. **CI must pass to merge.** No `--no-verify`, no skipping checks, no
   direct-to-main commits. If CI is broken and the fix is unclear, stop
   and ask. Broken CI is a P1.

3. **No cloud-vendor SDK in business code.** No `azure.*`, `@azure/*`,
   `google-cloud-*`, `@aws-sdk/*` imports under `/src/`, `/backend/`, `/api/`,
   `/frontend/`, `/sdk/`, `/cli/`. Secrets, storage, queues all come
   through `os.environ[...]` / `process.env.*`. Cloud migration must cost
   days, not months.

4. **Structured logs + metrics + traces on every production code path.**
   New endpoint / new agent / new background job = three signals emitted.
   No `print()`, no bare `logging.info("...")`. See skill `optiminds-obs`
   for the exact conventions (skill auto-triggers on relevant tasks).

5. **Tests ship with the code.** Same PR, not a follow-up. If a bugfix has
   no regression test, the bug will come back.

6. **Architectural changes need an ADR.** Any decision that's "1+ week of
   work", introduces a new external dependency, or changes a public
   contract goes in `docs/adr/` as a MADR-style record before or with the
   implementation PR.

7. **When in doubt, stop and ask.** Read AGENTS.md first, check relevant
   skill descriptions, consult `docs/adr/`, then ask a human. Never
   fabricate conventions under pressure.

## Git & PR Workflow

- **Branches**: `feature/<slug>` or `fix/<slug>`. Never push to `main`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `perf:`, `ci:`). Short subject, body explains WHY.
- **No `Co-Authored-By:` lines** on AI-assisted commits. Authorship =
  the human who approved the PR.
- **PR template**: see `.github/pull_request_template.md`. All 8 sections
  are required — "rollback" and "observability" especially.
- **Review**: every PR gets (a) Codex 3-pass AI review, (b) at least one
  human reviewer per CODEOWNERS. Strict paths (`billing/`, `auth/`,
  `migrations/`) require human approval to merge.
- **Merge**: squash-merge by default; merge commit for release PRs.

## Security Red Lines

These are non-negotiable. Violation = immediate revert + incident ticket.

| Red line | Enforcement |
|---|---|
| No secrets in git (past or present) | `gitleaks` pre-commit + CI + nightly full-history scan |
| No cloud-SDK in business code | (v0.3) `lint-cloud-sdk-imports.sh` in CI |
| No plaintext PII in logs | observability lint (v0.3) + manual review |
| No dynamic code execution on user input | code review + ruff / eslint rules |
| No disabling CI to merge | branch protection rules |
| No force-push to `main` | branch protection rules |

## Testing

- Minimum coverage: 80% on lines changed in a PR.
- TDD discipline: write the failing test first, implement to green, refactor.
- Unit + integration + at least one E2E per critical user flow.
- Never mock what you can inject (dependency inversion > magic mocks).
- See skill `optiminds-testing` for stack-specific patterns (Python pytest,
  TS vitest, etc.) — skill auto-triggers when you're writing tests.

## Engineering Discipline

Rules distilled from harness retros. Each bullet is a load-bearing
invariant — a past task shipped or nearly shipped a bug because the rule
wasn't followed. Source retros tagged `harness-retro` in the issue tracker.

### Planning discipline

- **SC / CP scope parity** — when a Success Criterion uses a universal-tree
  predicate ("no references in surviving files", "all callers", "nothing
  imports X"), the enforcing Checkpoint acceptance criterion MUST evaluate
  the same scope. If the CP is narrower, require BOTH a CP-local check AND
  a spec-level residual check (whole-tree grep against a sentinel whitelist).
  Narrower-CP-only defers drift detection to E2E. _(retro: v0.3.0 ship)_
- **Tool-behaviour claims need evidence at spec time** — any spec assertion
  about a third-party tool (bats, jq, shellcheck, release-please,
  actions/checkout, etc.) must cite evidence against the repo's **pinned**
  version: a runnable command + literal output (≤20 lines) + ISO-8601 date,
  OR a changelog/docs link for that version. Tool behaviour changes across
  versions; "it should work" is not a spec claim. _(retro: version-check-e2e)_

### Code discipline

- **Git worktree detection** — detect a working tree with
  `git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1`,
  NEVER `[[ -d "$TARGET/.git" ]]` or `[[ -e "$TARGET/.git" ]]`. In worktrees
  and submodules, `.git` is a regular file pointing into the main repo's
  `.git/worktrees/` dir — the directory test fails silently on valid
  setups. Regression-test any such check with `git worktree add`.
  _(retro: v0.3.0 ship)_
- **Atomic file writes require same-filesystem tempfile** — use
  `tmp=$(mktemp "${target}.XXXXXX")` (same dir → same fs), then
  `write_to "$tmp" && mv "$tmp" "$target"`. Naked `mktemp` defaults to
  `$TMPDIR` (typically `/tmp`), which on macOS, CI runners, and most
  Linux distros is a separate filesystem — cross-fs `mv` degrades to
  copy-then-unlink and is NOT atomic. Reviewers: an unadorned `mktemp`
  on an "atomic writer" AC is a finding, not a pass. _(retro: version-check-e2e)_
- **Bash arithmetic on parsed integers needs `10#` base prefix** — any
  `$((expr))` whose operands come from parsed string input (arguments,
  file content, SemVer components, line numbers) MUST prefix each
  operand: `(( 10#$major > 10#$other_major ))`. Bash parses leading-zero
  decimals as octal; `08` and `09` are invalid octal digits → "value
  too great for base". Literal integers written in script source are
  exempt (author controls their form). Every shell lib doing arithmetic
  on parsed integers must include a leading-zero test. _(retro: version-check-e2e)_

### CI discipline

- **Default `GITHUB_TOKEN` does NOT trigger downstream workflows** —
  GitHub intentionally skips downstream workflow triggers for events
  produced by actions running with the default token (security feature
  to prevent action self-escalation). For `workflow-A creates event →
  workflow-B runs` chains, choose one: (a) **inline** the downstream
  work into A (preferred — self-contained, no token management), (b)
  use a PAT or GitHub App token in A, or (c) document explicitly that
  B runs only on human-pushed events. Every cross-workflow handoff
  needs a dry-run or CI test before shipping.
  Ref: <https://docs.github.com/en/actions/security-guides/automatic-token-authentication>
  _(retro: v0.3.0 ship)_

### Documentation discipline

- **Flow-change doc-sync** — when changing a user-visible flow (release,
  deploy, adoption, onboarding), (1) grep the tree for every doc that
  describes the flow BEFORE changing it, (2) update every match in the
  SAME commit/PR as the code change, (3) cross-model review must
  explicitly verify doc-to-code consistency after the change. Three
  docs can describe a single flow; the old description silently outlives
  the code if doc-sync isn't forced. _(retro: v0.3.0 ship — README,
  CONTRIBUTING, CHANGELOG each independently described the broken
  pre-fix release flow and all three survived the first-pass review)_

### Evaluation discipline

- **Malformed-input fault-path probe** — every backend check whose code
  reads or parses external input (files, env vars, stdin, arguments
  that flow into `jq` / `sed` / `awk` / `python` / bash parameter
  expansion) MUST test the malformed-input branch in its evaluation:
  either (a) a test in the CP suite feeding invalid JSON / non-numeric
  version / trailing backslash / embedded newline and asserting a
  well-defined behaviour (error message + exit code, or graceful-
  degrade), OR (b) an evaluator-led simulation documenting
  stdout/stderr/exit code under a `Fault-path probe` heading. Pure-
  computation CPs with no external input must state
  `Fault-path probe: N/A` explicitly so the question is visibly asked
  and answered. Atomic-writer patterns require the same-fs tempfile
  check from Code discipline above. _(retro: version-check-e2e — 3
  malformed-input crashes caught by peer after all internal evaluators
  passed happy-path)_

## Tooling Setup

This repo assumes Optiminds organization-wide AI skills and subagents are
installed — once per developer machine. Skills auto-trigger in your CLI
based on task context. For the exact install / update / troubleshoot
commands, see [`docs/tooling-setup.md`](../docs/tooling-setup.md).

## Cross-Repo Glossary

<!-- Terms that mean the same thing across all Optiminds repos. Resist the
urge to redefine per-repo. Additions to this glossary happen via platform-
owners review. -->

- **Consumer** — a paying end-user of an Optiminds product (e.g., a law firm
  on lawyer_marketing). NOT synonymous with "customer" in billing contexts.
- **Tenant** — a logical isolation boundary in multi-tenant services
  (one customer org = one tenant = one `tenant_id` on every structured log).
- **Service** — a deployable unit (a FastAPI app, a worker, a CLI). Each
  repo may host multiple services under separate directories.
- **Agent** — an LLM-orchestrated workflow (Claude / Codex / in-house).
  NOT a user role.

## References

- Per-repo identity: `CLAUDE.md` (repo root)
- Deep guides: skills auto-trigger from `~/.claude/plugins/optiminds/skills/`
  (or your CLI's equivalent). List them: `~/.optiminds/scripts/install-skills.sh list`
- PR template: `.github/pull_request_template.md`
- CODEOWNERS: `.github/CODEOWNERS`
- Review rules: `.codex.yaml`
- Incident SLA: `SECURITY.md`
- Change governance: `CONTRIBUTING.md`

---

<sub>Structure from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template). Do not edit Core Principles / Security Red Lines without platform-owners review. Domain-specific sections can be added below this line per-repo if strictly necessary — prefer `CLAUDE.md` or a skill first.</sub>

```

## agents.md
```markdown
# AGENTS.md

<!--
Organization-wide agent instructions for every Optiminds repository. This
file is the single source of truth for cross-repo rules. It is readable by
Claude Code (via `@AGENTS.md` reference in CLAUDE.md), Codex CLI (native),
Cursor, Aider, and Continue (all auto-load AGENTS.md).

Per-repo identity lives in CLAUDE.md, not here. This file should almost
never diverge between repos — if you feel the urge to override a rule
here for one repo, write an ADR instead.

Keep under ~200 lines. When a topic needs more depth, add it as a skill in
`skills/optiminds-<topic>/SKILL.md` — skills auto-trigger on matching
context and don't bloat the always-loaded AGENTS.md.
-->

## Core Principles

<!-- DRAFT: Stometa to finalize. These 7 principles were drafted from the
2026-04-21 CTO brainstorm (rankgale incident, cloud migration, harness
model). Refine the wording / ordering / add-remove as needed before the
first major adoption. -->

1. **Never commit secrets.** Every `.env*`, `credentials/`, `keys/`, token,
   or API key must be in `.gitignore` **before** the file is written.
   If a secret leaks to git history: rotate first in Key Vault, then clean
   history. Never reverse that order.

2. **CI must pass to merge.** No `--no-verify`, no skipping checks, no
   direct-to-main commits. If CI is broken and the fix is unclear, stop
   and ask. Broken CI is a P1.

3. **No cloud-vendor SDK in business code.** No `azure.*`, `@azure/*`,
   `google-cloud-*`, `@aws-sdk/*` imports under `/src/`, `/backend/`, `/api/`,
   `/frontend/`, `/sdk/`, `/cli/`. Secrets, storage, queues all come
   through `os.environ[...]` / `process.env.*`. Cloud migration must cost
   days, not months.

4. **Structured logs + metrics + traces on every production code path.**
   New endpoint / new agent / new background job = three signals emitted.
   No `print()`, no bare `logging.info("...")`. See skill `optiminds-obs`
   for the exact conventions (skill auto-triggers on relevant tasks).

5. **Tests ship with the code.** Same PR, not a follow-up. If a bugfix has
   no regression test, the bug will come back.

6. **Architectural changes need an ADR.** Any decision that's "1+ week of
   work", introduces a new external dependency, or changes a public
   contract goes in `docs/adr/` as a MADR-style record before or with the
   implementation PR.

7. **When in doubt, stop and ask.** Read AGENTS.md first, check relevant
   skill descriptions, consult `docs/adr/`, then ask a human. Never
   fabricate conventions under pressure.

## Git & PR Workflow

- **Branches**: `feature/<slug>` or `fix/<slug>`. Never push to `main`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `perf:`, `ci:`). Short subject, body explains WHY.
- **No `Co-Authored-By:` lines** on AI-assisted commits. Authorship =
  the human who approved the PR.
- **PR template**: see `.github/pull_request_template.md`. All 8 sections
  are required — "rollback" and "observability" especially.
- **Review**: every PR gets (a) Codex 3-pass AI review, (b) at least one
  human reviewer per CODEOWNERS. Strict paths (`billing/`, `auth/`,
  `migrations/`) require human approval to merge.
- **Merge**: squash-merge by default; merge commit for release PRs.

## Security Red Lines

These are non-negotiable. Violation = immediate revert + incident ticket.

| Red line | Enforcement |
|---|---|
| No secrets in git (past or present) | `gitleaks` pre-commit + CI + nightly full-history scan |
| No cloud-SDK in business code | (v0.3) `lint-cloud-sdk-imports.sh` in CI |
| No plaintext PII in logs | observability lint (v0.3) + manual review |
| No dynamic code execution on user input | code review + ruff / eslint rules |
| No disabling CI to merge | branch protection rules |
| No force-push to `main` | branch protection rules |

## Testing

- Minimum coverage: 80% on lines changed in a PR.
- TDD discipline: write the failing test first, implement to green, refactor.
- Unit + integration + at least one E2E per critical user flow.
- Never mock what you can inject (dependency inversion > magic mocks).
- See skill `optiminds-testing` for stack-specific patterns (Python pytest,
  TS vitest, etc.) — skill auto-triggers when you're writing tests.

## Engineering Discipline

Rules distilled from harness retros. Each bullet is a load-bearing
invariant — a past task shipped or nearly shipped a bug because the rule
wasn't followed. Source retros tagged `harness-retro` in the issue tracker.

### Planning discipline

- **SC / CP scope parity** — when a Success Criterion uses a universal-tree
  predicate ("no references in surviving files", "all callers", "nothing
  imports X"), the enforcing Checkpoint acceptance criterion MUST evaluate
  the same scope. If the CP is narrower, require BOTH a CP-local check AND
  a spec-level residual check (whole-tree grep against a sentinel whitelist).
  Narrower-CP-only defers drift detection to E2E. _(retro: v0.3.0 ship)_
- **Tool-behaviour claims need evidence at spec time** — any spec assertion
  about a third-party tool (bats, jq, shellcheck, release-please,
  actions/checkout, etc.) must cite evidence against the repo's **pinned**
  version: a runnable command + literal output (≤20 lines) + ISO-8601 date,
  OR a changelog/docs link for that version. Tool behaviour changes across
  versions; "it should work" is not a spec claim. _(retro: version-check-e2e)_

### Code discipline

- **Git worktree detection** — detect a working tree with
  `git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1`,
  NEVER `[[ -d "$TARGET/.git" ]]` or `[[ -e "$TARGET/.git" ]]`. In worktrees
  and submodules, `.git` is a regular file pointing into the main repo's
  `.git/worktrees/` dir — the directory test fails silently on valid
  setups. Regression-test any such check with `git worktree add`.
  _(retro: v0.3.0 ship)_
- **Atomic file writes require same-filesystem tempfile** — use
  `tmp=$(mktemp "${target}.XXXXXX")` (same dir → same fs), then
  `write_to "$tmp" && mv "$tmp" "$target"`. Naked `mktemp` defaults to
  `$TMPDIR` (typically `/tmp`), which on macOS, CI runners, and most
  Linux distros is a separate filesystem — cross-fs `mv` degrades to
  copy-then-unlink and is NOT atomic. Reviewers: an unadorned `mktemp`
  on an "atomic writer" AC is a finding, not a pass. _(retro: version-check-e2e)_
- **Bash arithmetic on parsed integers needs `10#` base prefix** — any
  `$((expr))` whose operands come from parsed string input (arguments,
  file content, SemVer components, line numbers) MUST prefix each
  operand: `(( 10#$major > 10#$other_major ))`. Bash parses leading-zero
  decimals as octal; `08` and `09` are invalid octal digits → "value
  too great for base". Literal integers written in script source are
  exempt (author controls their form). Every shell lib doing arithmetic
  on parsed integers must include a leading-zero test. _(retro: version-check-e2e)_

### CI discipline

- **Default `GITHUB_TOKEN` does NOT trigger downstream workflows** —
  GitHub intentionally skips downstream workflow triggers for events
  produced by actions running with the default token (security feature
  to prevent action self-escalation). For `workflow-A creates event →
  workflow-B runs` chains, choose one: (a) **inline** the downstream
  work into A (preferred — self-contained, no token management), (b)
  use a PAT or GitHub App token in A, or (c) document explicitly that
  B runs only on human-pushed events. Every cross-workflow handoff
  needs a dry-run or CI test before shipping.
  Ref: <https://docs.github.com/en/actions/security-guides/automatic-token-authentication>
  _(retro: v0.3.0 ship)_

### Documentation discipline

- **Flow-change doc-sync** — when changing a user-visible flow (release,
  deploy, adoption, onboarding), (1) grep the tree for every doc that
  describes the flow BEFORE changing it, (2) update every match in the
  SAME commit/PR as the code change, (3) cross-model review must
  explicitly verify doc-to-code consistency after the change. Three
  docs can describe a single flow; the old description silently outlives
  the code if doc-sync isn't forced. _(retro: v0.3.0 ship — README,
  CONTRIBUTING, CHANGELOG each independently described the broken
  pre-fix release flow and all three survived the first-pass review)_

### Evaluation discipline

- **Malformed-input fault-path probe** — every backend check whose code
  reads or parses external input (files, env vars, stdin, arguments
  that flow into `jq` / `sed` / `awk` / `python` / bash parameter
  expansion) MUST test the malformed-input branch in its evaluation:
  either (a) a test in the CP suite feeding invalid JSON / non-numeric
  version / trailing backslash / embedded newline and asserting a
  well-defined behaviour (error message + exit code, or graceful-
  degrade), OR (b) an evaluator-led simulation documenting
  stdout/stderr/exit code under a `Fault-path probe` heading. Pure-
  computation CPs with no external input must state
  `Fault-path probe: N/A` explicitly so the question is visibly asked
  and answered. Atomic-writer patterns require the same-fs tempfile
  check from Code discipline above. _(retro: version-check-e2e — 3
  malformed-input crashes caught by peer after all internal evaluators
  passed happy-path)_

## Tooling Setup

This repo assumes Optiminds organization-wide AI skills and subagents are
installed — once per developer machine. Skills auto-trigger in your CLI
based on task context. For the exact install / update / troubleshoot
commands, see [`docs/tooling-setup.md`](../docs/tooling-setup.md).

## Cross-Repo Glossary

<!-- Terms that mean the same thing across all Optiminds repos. Resist the
urge to redefine per-repo. Additions to this glossary happen via platform-
owners review. -->

- **Consumer** — a paying end-user of an Optiminds product (e.g., a law firm
  on lawyer_marketing). NOT synonymous with "customer" in billing contexts.
- **Tenant** — a logical isolation boundary in multi-tenant services
  (one customer org = one tenant = one `tenant_id` on every structured log).
- **Service** — a deployable unit (a FastAPI app, a worker, a CLI). Each
  repo may host multiple services under separate directories.
- **Agent** — an LLM-orchestrated workflow (Claude / Codex / in-house).
  NOT a user role.

## References

- Per-repo identity: `CLAUDE.md` (repo root)
- Deep guides: skills auto-trigger from `~/.claude/plugins/optiminds/skills/`
  (or your CLI's equivalent). List them: `~/.optiminds/scripts/install-skills.sh list`
- PR template: `.github/pull_request_template.md`
- CODEOWNERS: `.github/CODEOWNERS`
- Review rules: `.codex.yaml`
- Incident SLA: `SECURITY.md`
- Change governance: `CONTRIBUTING.md`

---

<sub>Structure from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template). Do not edit Core Principles / Security Red Lines without platform-owners review. Domain-specific sections can be added below this line per-repo if strictly necessary — prefer `CLAUDE.md` or a skill first.</sub>

```


# Repo: multica

## README.md
```markdown
<p align="center">
  <img src="docs/assets/banner.jpg" alt="Multica — humans and agents, side by side" width="100%">
</p>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo-light.svg">
  <img alt="Multica" src="docs/assets/logo-light.svg" width="50">
</picture>

# Multica

**Your next 10 hires won't be human.**

The open-source managed agents platform.<br/>
Turn coding agents into real teammates — assign tasks, track progress, compound skills.

[![CI](https://github.com/multica-ai/multica/actions/workflows/ci.yml/badge.svg)](https://github.com/multica-ai/multica/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/multica-ai/multica?style=flat)](https://github.com/multica-ai/multica/stargazers)

[Website](https://multica.ai) · [Cloud](https://multica.ai/app) · [X](https://x.com/MulticaAI) · [Self-Hosting](SELF_HOSTING.md) · [Contributing](CONTRIBUTING.md)

**English | [简体中文](README.zh-CN.md)**

</div>

## What is Multica?

Multica turns coding agents into real teammates. Assign issues to an agent like you'd assign to a colleague — they'll pick up the work, write code, report blockers, and update statuses autonomously.

No more copy-pasting prompts. No more babysitting runs. Your agents show up on the board, participate in conversations, and compound reusable skills over time. Think of it as open-source infrastructure for managed agents — vendor-neutral, self-hosted, and designed for human + AI teams. Works with **Claude Code**, **Codex**, **OpenClaw**, **OpenCode**, **Hermes**, **Gemini**, **Pi**, and **Cursor Agent**.

<p align="center">
  <img src="docs/assets/hero-screenshot.png" alt="Multica board view" width="800">
</p>

## Features

Multica manages the full agent lifecycle: from task assignment to execution monitoring to skill reuse.

- **Agents as Teammates** — assign to an agent like you'd assign to a colleague. They have profiles, show up on the board, post comments, create issues, and report blockers proactively.
- **Autonomous Execution** — set it and forget it. Full task lifecycle management (enqueue, claim, start, complete/fail) with real-time progress streaming via WebSocket.
- **Reusable Skills** — every solution becomes a reusable skill for the whole team. Deployments, migrations, code reviews — skills compound your team's capabilities over time.
- **Unified Runtimes** — one dashboard for all your compute. Local daemons and cloud runtimes, auto-detection of available CLIs, real-time monitoring.
- **Multi-Workspace** — organize work across teams with workspace-level isolation. Each workspace has its own agents, issues, and settings.

---

## Quick Install

### macOS / Linux (Homebrew - recommended)

```bash
brew install multica-ai/tap/multica
```

Use `brew upgrade multica-ai/tap/multica` to keep the CLI current.

### macOS / Linux (install script)

```bash
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash
```

Use this if Homebrew is not available. The script installs the Multica CLI on macOS and Linux by using Homebrew when it is on `PATH`, otherwise it downloads the binary directly.

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.ps1 | iex
```

Then configure, authenticate, and start the daemon in one command:

```bash
multica setup          # Connect to Multica Cloud, log in, start daemon
```

> **Self-hosting?** Add `--with-server` to deploy a full Multica server on your machine:
>
> ```bash
> curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash -s -- --with-server
> multica setup self-host
> ```
>
> Requires Docker. See the [Self-Hosting Guide](SELF_HOSTING.md) for details.

---

## Getting Started

### 1. Set up and start the daemon

```bash
multica setup           # Configure, authenticate, and start the daemon
```

The daemon runs in the background and auto-detects agent CLIs (`claude`, `codex`, `openclaw`, `opencode`, `hermes`, `gemini`, `pi`, `cursor-agent`) on your PATH.

### 2. Verify your runtime

Open your workspace in the Multica web app. Navigate to **Settings → Runtimes** — you should see your machine listed as an active **Runtime**.

> **What is a Runtime?** A Runtime is a compute environment that can execute agent tasks. It can be your local machine (via the daemon) or a cloud instance. Each runtime reports which agent CLIs are available, so Multica knows where to route work.

### 3. Create an agent

Go to **Settings → Agents** and click **New Agent**. Pick the runtime you just connected and choose a provider (Claude Code, Codex, OpenClaw, OpenCode, Hermes, Gemini, Pi, or Cursor Agent). Give your agent a name — this is how it will appear on the board, in comments, and in assignments.

### 4. Assign your first task

Create an issue from the board (or via `multica issue create`), then assign it to your new agent. The agent will automatically pick up the task, execute it on your runtime, and report progress — just like a human teammate.

---

## Multica vs Paperclip

| | Multica | Paperclip |
|---|---------|-----------|
| **Focus** | Team AI agent collaboration platform | Solo AI agent company simulator |
| **User model** | Multi-user teams with roles & permissions | Single board operator |
| **Agent interaction** | Issues + Chat conversations | Issues + Heartbeat |
| **Deployment** | Cloud-first | Local-first |
| **Management depth** | Lightweight (Issues / Projects / Labels) | Heavy governance (Org chart / Approvals / Budgets) |
| **Extensibility** | Skills system | Skills + Plugin system |

**TL;DR — Multica is built for teams that want to collaborate with AI agents on real projects together.**

---

## CLI

The `multica` CLI connects your local machine to Multica — authenticate, manage workspaces, and run the agent daemon.

| Command | Description |
|---------|-------------|
| `multica login` | Authenticate (opens browser) |
| `multica daemon start` | Start the local agent runtime |
| `multica daemon status` | Check daemon status |
| `multica setup` | One-command setup for Multica Cloud (configure + login + start daemon) |
| `multica setup self-host` | Same, but for self-hosted deployments |
| `multica issue list` | List issues in your workspace |
| `multica issue create` | Create a new issue |
| `multica update` | Update to the latest version |

See the [CLI and Daemon Guide](CLI_AND_DAEMON.md) for the full command reference.

---

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Next.js    │────>│  Go Backend  │────>│   PostgreSQL     │
│   Frontend   │<────│  (Chi + WS)  │<────│   (pgvector)     │
└──────────────┘     └──────┬───────┘     └──────────────────┘
                            │
                     ┌──────┴───────┐
                     │ Agent Daemon │  runs on your machine
                     └──────────────┘  (Claude Code, Codex, OpenCode,
                                        OpenClaw, Hermes, Gemini,
                                        Pi, Cursor Agent)
```

| Layer | Stack |
|-------|-------|
| Frontend | Next.js 16 (App Router) |
| Backend | Go (Chi router, sqlc, gorilla/websocket) |
| Database | PostgreSQL 17 with pgvector |
| Agent Runtime | Local daemon executing Claude Code, Codex, OpenClaw, OpenCode, Hermes, Gemini, Pi, or Cursor Agent |

## Development

For contributors working on the Multica codebase, see the [Contributing Guide](CONTRIBUTING.md).

**Prerequisites:** [Node.js](https://nodejs.org/) v20+, [pnpm](https://pnpm.io/) v10.28+, [Go](https://go.dev/) v1.26+, [Docker](https://www.docker.com/)

```bash
make dev
```

`make dev` auto-detects your environment (main checkout or worktree), creates the env file, installs dependencies, sets up the database, runs migrations, and starts all services.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development workflow, worktree support, testing, and troubleshooting.

## Star History

<a href="https://www.star-history.com/?repos=multica-ai%2Fmultica&type=date&legend=bottom-right">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=multica-ai/multica&type=date&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=multica-ai/multica&type=date&legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=multica-ai/multica&type=date&legend=top-left" />
  </picture>
</a>

```

## CLAUDE.md
```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

Multica is an AI-native task management platform — like Linear, but with AI agents as first-class citizens.

- Agents can be assigned issues, create issues, comment, and change status
- Supports local (daemon) and cloud agent runtimes
- Built for 2-10 person AI-native teams

## Architecture

**Go backend + monorepo frontend (pnpm workspaces + Turborepo) with shared packages.**

- `server/` — Go backend (Chi router, sqlc for DB, gorilla/websocket for real-time)
- `apps/web/` — Next.js frontend (App Router)
- `apps/desktop/` — Electron desktop app (electron-vite)
- `packages/core/` — Headless business logic (zero react-dom, all-platform reuse)
- `packages/ui/` — Atomic UI components (zero business logic)
- `packages/views/` — Shared business pages/components (zero next/* imports, zero react-router imports)
- `packages/tsconfig/` — Shared TypeScript configuration

### Key Architectural Decisions

**Internal Packages pattern** — all shared packages export raw `.ts`/`.tsx` files (no pre-compilation). The consuming app's bundler compiles them directly. This gives zero-config HMR and instant go-to-definition.

**Dependency direction:** `views/ → core/ + ui/`. Core and UI are independent of each other. No package imports from `next/*`, `react-router-dom`, or app-specific code.

**Platform bridge:** `packages/core/platform/` provides `CoreProvider` — initializes API client, auth/workspace stores, WS connection, and QueryClient. Each app wraps its root with `<CoreProvider>` and provides its own `NavigationAdapter` for routing.

**pnpm catalog** — `pnpm-workspace.yaml` defines `catalog:` for version pinning. All shared deps use `catalog:` references to guarantee a single version across all packages. When adding new shared deps (including test deps), add to catalog first.

### State Management

The architecture relies on a strict split between server state and client state. Mixing them is the most common way to break it.

- **TanStack Query owns all server state.** Issues, users, workspaces, inbox — anything fetched from the API lives in the Query cache. WS events keep it fresh via invalidation; no polling, no `staleTime` workarounds.
- **Zustand owns all client state.** UI selections, filters, drafts, modal state, navigation history. Stores live in `packages/core/` (never in `packages/views/`) so both apps share them.
- **React Context** is reserved for cross-cutting platform plumbing — `WorkspaceIdProvider`, `NavigationProvider`. Don't reach for it for general state.
- **Auth and workspace stores are the only stores allowed to call `api.*` directly**, because they manage critical state that must exist before queries can run. They're created via factory + injected dependencies, registered by the platform layer.

**Hard rules — these are how the architecture stays coherent:**

- **Never duplicate server data into Zustand.** If it came from the API, it belongs in the Query cache. Copying it into a store creates two sources of truth and they will drift.
- **Workspace-scoped queries must key on `wsId`.** This is what makes workspace switching automatic — the cache key changes, the right data appears, no manual invalidation needed.
- **Mutations are optimistic by default.** Apply the change locally, send the request, roll back on failure, invalidate on settle. The user shouldn't wait for the server.
- **WS events invalidate queries — they never write to stores directly.** This keeps the cache as the single source of truth and avoids race conditions.
- **Persist what's worth preserving across restarts** (user preferences, drafts, tab layout). **Don't persist ephemeral UI state** (modal open/close, transient selections) or server data.

**Common Zustand footguns to avoid:**

- Selectors must return stable references. Returning a freshly built object or array on every call (e.g. `s => ({ a: s.a, b: s.b })` or `s => s.items.map(...)`) triggers infinite re-renders. Either select primitives separately or use shallow comparison.
- Hooks that need workspace context should accept `wsId` as a parameter, not call `useWorkspaceId()` internally — this lets them work outside the `WorkspaceIdProvider` (e.g. in a sidebar that renders before workspace is loaded).

## Commands

```bash
# One-command dev (auto-setup + start everything)
make dev              # Auto-creates env, installs deps, starts DB, migrates, launches app

# Explicit setup & run (if you prefer separate steps)
make setup            # First-time: ensure shared DB, create app DB, migrate
make start            # Start backend + frontend together
make stop             # Stop app processes for the current checkout
make db-down          # Stop the shared PostgreSQL container

# Frontend (all commands go through Turborepo)
pnpm install
pnpm dev:web          # Next.js dev server (port 3000)
pnpm dev:desktop      # Electron dev (electron-vite, HMR)
pnpm build            # Build all frontend apps
pnpm typecheck        # TypeScript check (all packages + apps via turbo)
pnpm lint             # ESLint
pnpm test             # TS tests (Vitest, all packages + apps via turbo)

# Backend (Go)
make server           # Run Go server only (port 8080)
make daemon           # Run local daemon
make build            # Build server + CLI binaries to server/bin/
make cli ARGS="..."   # Run multica CLI (e.g. make cli ARGS="config")
make test             # Go tests
make sqlc             # Regenerate sqlc code after editing SQL in server/pkg/db/queries/
make migrate-up       # Run database migrations
make migrate-down     # Rollback migrations

# Run a single TS test (works for any package with a test script)
pnpm --filter @multica/views exec vitest run auth/login-page.test.tsx
pnpm --filter @multica/core exec vitest run runtimes/version.test.ts
pnpm --filter @multica/web exec vitest run app/\(auth\)/login/page.test.tsx

# Run a single Go test
cd server && go test ./internal/handler/ -run TestName

# Run a single E2E test (requires backend + frontend running)
pnpm exec playwright test e2e/tests/specific-test.spec.ts

# Desktop build & package
pnpm --filter @multica/desktop build      # Compile TS → JS (reads .env.production)
pnpm --filter @multica/desktop package    # Package into .app/.dmg/.exe (current platform only)

# shadcn — config lives in packages/ui/components.json (Base UI variant, base-nova style)
pnpm ui:add badge                # Adds component to packages/ui/components/ui/

# Infrastructure
make db-up            # Start shared PostgreSQL (pgvector/pg17 image)
make db-down          # Stop shared PostgreSQL
make db-reset         # Drop + recreate current env's DB, then re-run migrations (local only; stop backend first)
```

### CI Requirements

CI runs on Node 22 and Go 1.26.1 with a `pgvector/pgvector:pg17` PostgreSQL service. See `.github/workflows/ci.yml`.

### Worktree Support

All checkouts share one PostgreSQL container. Isolation is at the database level — each worktree gets its own DB name and unique ports via `.env.worktree`. Main checkouts use `.env`.

`make dev` auto-detects worktrees and handles everything. For explicit control:

```bash
make worktree-env       # Generate .env.worktree with unique DB/ports
make setup-worktree     # Setup using .env.worktree
make start-worktree     # Start using .env.worktree
```

## Coding Rules

- TypeScript strict mode is enabled; keep types explicit.
- Go code follows standard Go conventions (gofmt, go vet).
- Keep comments in code **English only**.
- Prefer existing patterns/components over introducing parallel abstractions.
- Unless the user explicitly asks for backwards compatibility, do **not** add compatibility layers, fallback paths, dual-write logic, legacy adapters, or temporary shims.
- If a flow or API is being replaced and the product is not yet live, prefer removing the old path instead of preserving both old and new behavior.
- Avoid broad refactors unless required by the task.
- New global (pre-workspace) routes MUST use a single word (`/login`, `/inbox`) or a `/{noun}/{verb}` pair (`/workspaces/new`). NEVER add hyphenated word-group root routes (`/new-workspace`, `/create-team`) — they collide with common user workspace names and force endless reserved-slug audits. Reserving the noun (`workspaces`) automatically protects the entire `/workspaces/*` subtree.

### Package Boundary Rules

These are hard constraints. Violating them breaks the cross-platform architecture:

- `packages/core/` — zero react-dom, zero localStorage (use StorageAdapter), zero process.env, zero UI libraries. **All shared Zustand stores live here**, even view-related ones (filters, view modes) — stores are pure state, not UI.
- `packages/ui/` — zero `@multica/core` imports (pure UI, no business logic).
- `packages/views/` — zero `next/*` imports, zero `react-router-dom` imports, zero stores. Use `NavigationAdapter` for all routing.
- `apps/web/platform/` — the only place for Next.js APIs (`next/navigation`).
- `apps/desktop/src/renderer/src/platform/` — the only place for react-router-dom navigation wiring.

### The No-Duplication Rule

**If the same logic exists in both apps, it must be extracted to a shared package.**

This applies to everything: components, hooks, guards, providers, utility functions. The decision process:

1. Does this code depend on Next.js or Electron APIs? → Keep in the respective app.
2. Does it depend on `react-router-dom` or `next/navigation`? → Keep in app's `platform/` layer.
3. Everything else → belongs in `packages/core/` (headless logic) or `packages/views/` (UI components).

When the two apps need different behavior for the same concept (e.g., different loading UI), extract the shared logic into a component with props/slots for the differences. Don't duplicate the logic.

### Cross-Platform Development Rules

When adding a new page or feature:

1. **New page component** → add to `packages/views/<domain>/`. Never import from `next/*` or `react-router-dom`.
2. **Wire it in both apps** → add a route in `apps/web/app/` (Next.js page file) AND in the desktop router. **Exception**: pre-workspace transition flows (create workspace, accept invite) are NOT routes on desktop — they're `WindowOverlay` state. See *Desktop-specific Rules → Route categories*.
3. **Navigation** → use `useNavigation().push()` or `<AppLink>`. Never use framework-specific link/router APIs in shared code.
4. **Shared guards/providers** → use `DashboardGuard` from `packages/views/layout/`. Don't create separate guard logic per app.
5. **Platform-specific UI** → if a feature is web-only or desktop-only, keep it in the respective app. Use props slots (`extra`, `topSlot`) on shared layout components to inject platform-specific UI.
6. **New hooks that need workspace context** → accept `wsId` as parameter instead of reading from `useWorkspaceId()` Context, so they work both inside and outside `WorkspaceIdProvider`.

### CSS Architecture

Both apps share the same CSS foundation from `packages/ui/styles/`.

- **Design tokens** → use semantic tokens (`bg-background`, `text-muted-foreground`). Never use hardcoded Tailwind colors (`text-red-500`, `bg-gray-100`).
- **Shared styles** → `packages/ui/styles/`. Never duplicate scrollbar styling, keyframes, or base layer rules in app CSS.
- **`@source` directives** → both apps scan shared packages so Tailwind sees all class names.

## Desktop-specific Rules

These rules apply to `apps/desktop/` only. Web has different constraints (URL bar, SSR, no tabs) and doesn't share these concerns. Every rule in this section was added after a concrete bug — treat them as enforced, not suggestions.

### Route categories

Every path in the desktop app falls into exactly one category. Choosing the wrong one reproduces bugs we've already fixed.

- **Session routes** — workspace-scoped pages (`/:slug/issues`, `/:slug/settings`). Rendered by the per-tab memory router under `WorkspaceRouteLayout`. These are legitimate tab destinations.
- **Transition flows** — pre-workspace / one-shot actions (create workspace, accept invite). **NOT routes.** They live as `WindowOverlay` state, dispatched when the navigation adapter sees `push('/workspaces/new')` or `push('/invite/<id>')`. The shared view (`NewWorkspacePage`, `InvitePage`) is the content; the overlay wrapper supplies platform chrome.
- **Error / stale states** — "workspace not available", tabs pointing at a revoked workspace. **NOT pages.** `WorkspaceRouteLayout` auto-heals by dropping the stale tab group from the store; the user never lands on an explicit error screen. Web keeps `NoAccessPage` (shareable URL makes the error state meaningful); desktop has no URL bar so stale = heal silently.

**Adding a new pre-workspace flow on desktop**: register a new `WindowOverlay` type in `stores/window-overlay-store.ts`. Do NOT add it to `routes.tsx`. If a shared view needs the flow on both platforms, add the route on web (`apps/web/app/(auth)/...`) AND the overlay type on desktop — the shared view component is identical.

### Workspace identity singleton

`setCurrentWorkspace(slug, uuid)` in `@multica/core/platform` is the single source of truth for "which workspace is active right now". Three consumers depend on it:

1. API client's `X-Workspace-Slug` header.
2. Zustand per-workspace storage namespace.
3. Chrome gating (`{slug && <AppSidebar />}` on desktop, similar on web).

Normally set by `WorkspaceRouteLayout` when its route mounts. Critically: **unmount does NOT clear it.** Any code that leaves workspace context (leave workspace, delete workspace, force navigation to overlay) must call `setCurrentWorkspace(null, null)` explicitly — otherwise the realtime `workspace:deleted` handler races the mutation, chrome gating stays truthy while the workspace is gone from cache, and `useWorkspaceId` throws.

### Workspace destructive operations

Leave / Delete workspace flows must follow this order:

1. Read destination from cached workspace list (no extra fetch).
2. `setCurrentWorkspace(null, null)`.
3. `navigation.push(destination)` — switch to next workspace or open new-workspace overlay.
4. THEN `await mutation.mutateAsync(workspaceId)`.

Reversing step 4 with steps 1–3 (mutate first, navigate after) causes a three-way race between the mutation's `onSettled` invalidate, the explicit `navigateAway`, and the realtime handler's `relocateAfterWorkspaceLoss` — all refetching the same `workspaces` query concurrently. One gets cancelled, bubbles as `CancelledError`, and triggers `window.location.assign` → full renderer reload / white screen.

### Tab isolation

Tabs are grouped per workspace in `stores/tab-store.ts`. The TabBar shows only the active workspace's tabs; cross-workspace tab leakage is impossible by construction (no flat global tabs array).

Cross-workspace `push(path)` is detected by the navigation adapter (`platform/navigation.tsx`) and translated into `switchWorkspace(slug, targetPath)` — NOT a navigation within the current tab's router. Don't bypass the adapter; always go through `useNavigation()` from shared code.

### Drag region (macOS window-move)

Every full-window desktop view (login, onboarding, new-workspace, invite, no-access, create-workspace modal) — i.e. anything that isn't inside the dashboard shell — needs a top drag strip so users can move the window. The native macOS traffic lights are **kept visible** for every such surface (Linear/Notion/Arc pattern); no `useImmersiveMode` by default.

**Pattern**: use the shared `<DragStrip />` from `@multica/views/platform` as the first flex child of the page root. It's a 48px transparent row with `-webkit-app-region: drag` — the parent's bg fills through it so the page reads edge-to-edge while the top 48px stays draggable under the traffic lights.

```tsx
import { DragStrip } from "@multica/views/platform";

return (
  <div className="flex min-h-svh flex-col bg-background">
    <DragStrip />
    <div className="flex flex-1 flex-col px-6 pb-12">
      {/* page content — interactive elements placed at y ≥ 48 clear the strip;
          any element at y < 48 needs WebkitAppRegion: "no-drag" */}
    </div>
  </div>
);
```

Why flex, not absolute: the absolute-strip + `z-index` approach relies on stacking-context hit-testing, which isn't reliable for `-webkit-app-region`. A real flex row with no siblings at that pixel is unambiguous. Web browsers silently ignore `-webkit-app-region`, so shared views render the strip as a plain 48px spacer on web — safe cross-platform.

**Horizontal clearance**: traffic lights occupy roughly x ∈ [16, 76] on macOS. Interactive UI (Back buttons, menus) should start at x ≥ 80 on desktop-sized viewports. The shared views default to sufficient `lg:px-20` padding; re-examine when laying out anything in the top-left corner.

Canonical example: `packages/views/platform/drag-strip.tsx`. Used by `onboarding/steps/step-welcome.tsx` (per-column), `onboarding/onboarding-flow.tsx`, `workspace/new-workspace-page.tsx`, `invite/invite-page.tsx`, `workspace/no-access-page.tsx`, `modals/create-workspace.tsx`, and desktop's `pages/login.tsx`.

**When to use `useImmersiveMode`**: only when a view must place interactive UI in the traffic-light hit-zone (y < 28 AND x < 80). For every current non-dashboard surface, buttons sit at y ≥ 48, so immersive mode is unnecessary. Hook is preserved as an escape hatch but has no callers.

### UX vs platform chrome

UX affordances (Back button, Log out button, welcome copy, invite card) belong in `packages/views/` so web and desktop render identical content. Platform chrome (tab system interaction, native-window IPC, `useImmersiveMode`) lives in desktop-only code. The `DragStrip` + `useImmersiveMode` primitives live in `packages/views/platform/` because they're cross-platform safe (web no-op) and need to be callable from shared views that own the page layout — keeping them in desktop-only would force every shared page to leave top-padding decisions to the platform shell, fragmenting the design.

## UI/UX Rules

- Prefer shadcn components over custom implementations. Install via `pnpm ui:add <component>` from project root — adds to `packages/ui/components/ui/`. All components use Base UI primitives (`@base-ui/react`), not Radix.
- Use shadcn design tokens for styling. Avoid hardcoded color values.
- Do not introduce extra state (useState, context, reducers) unless explicitly required by the design.
- Pay close attention to **overflow** (truncate long text, scrollable containers), **alignment**, and **spacing** consistency.
- **If a component is identical between web and desktop, it belongs in a shared package.** Do not copy-paste between apps.

## Testing Rules

### Where to write tests

Tests follow the code, not the app. This is the most important testing principle in this monorepo:

| What you're testing | Where the test lives | Why |
|---|---|---|
| Shared business logic (stores, queries, hooks) | `packages/core/*.test.ts` | No DOM needed, pure logic |
| Shared UI components (pages, forms, modals) | `packages/views/*.test.tsx` | jsdom, no framework mocks |
| Platform-specific wiring (cookies, redirects, searchParams) | `apps/web/*.test.tsx` or `apps/desktop/` | Needs framework-specific mocks |
| End-to-end user flows | `e2e/*.spec.ts` | Real browser, real backend |

**Never test shared component behavior in an app's test file.** If a test requires mocking `next/navigation` or `react-router-dom` to test a component from `@multica/views`, the test is in the wrong place — move it to `packages/views/` and mock `@multica/core` instead.

### Test infrastructure

- `packages/core/` — Vitest, Node environment (no DOM)
- `packages/views/` — Vitest, jsdom environment, `@testing-library/react`
- `apps/web/` — Vitest, jsdom environment, framework-specific mocks
- `e2e/` — Playwright
- `server/` — Go standard `go test`

All test deps are in the pnpm catalog for unified versioning.

### Mocking conventions

- Mock `@multica/core` stores with `vi.hoisted()` + `Object.assign(selectorFn, { getState })` pattern (Zustand stores are both callable and have `.getState()`).
- Mock `@multica/core/api` for API calls.
- In `packages/views/` tests: never mock `next/*` or `react-router-dom` — those don't exist here.
- In `apps/web/` tests: mock framework-specific APIs only for platform-specific behavior.

### TDD workflow

1. Write failing test in the **correct package** first.
2. Write implementation.
3. Run `pnpm test` (Turborepo discovers all packages).
4. Green → done.

### Go tests

Standard `go test`. Tests should create their own fixture data in a test database.

### E2E tests

E2E tests should be self-contained. Use the `TestApiClient` fixture for data setup/teardown:

```typescript
import { loginAsDefault, createTestApi } from "./helpers";
import type { TestApiClient } from "./fixtures";

let api: TestApiClient;

test.beforeEach(async ({ page }) => {
  api = await createTestApi();
  await loginAsDefault(page);
});

test.afterEach(async () => {
  await api.cleanup();
});

test("example", async ({ page }) => {
  const issue = await api.createIssue("Test Issue");
  await page.goto(`/issues/${issue.id}`);
});
```

## Commit Rules

- Use atomic commits grouped by logical intent.
- Conventional format: `feat(scope)`, `fix(scope)`, `refactor(scope)`, `docs`, `test(scope)`, `chore(scope)`.

## Minimum Pre-Push Checks

```bash
make check    # Runs all checks: typecheck, unit tests, Go tests, E2E
```

Run verification only when the user explicitly asks for it.

For targeted checks when requested:
```bash
pnpm typecheck        # TypeScript type errors only
pnpm test             # TS unit tests only (Vitest, all packages)
make test             # Go tests only
pnpm exec playwright test   # E2E only (requires backend + frontend running)
```

## AI Agent Verification Loop

After writing or modifying code, always run the full verification pipeline:

```bash
make check
```

**Workflow:**
- Write code to satisfy the requirement
- Run `make check`
- If any step fails, read the error output, fix the code, and re-run
- Repeat until all checks pass
- Only then consider the task complete

**Quick iteration:** If you know only TypeScript or Go is affected, run individual checks first for faster feedback, then finish with a full `make check` before marking work complete.

## CLI Release

**Prerequisite:** A CLI release must accompany every Production deployment.

1. Create a tag on the `main` branch: `git tag v0.x.x`
2. Push the tag: `git push origin v0.x.x`
3. GitHub Actions automatically triggers `release.yml`: runs Go tests → GoReleaser builds multi-platform binaries → publishes to GitHub Releases + Homebrew tap

By default, bump the patch version each release (e.g. `v0.1.12` → `v0.1.13`), unless the user specifies a specific version.

## Multi-tenancy

All queries filter by `workspace_id`. Membership checks gate access. `X-Workspace-ID` header routes requests to the correct workspace.

## Agent Assignees

Assignees are polymorphic — can be a member or an agent. `assignee_type` + `assignee_id` on issues. Agents render with distinct styling (purple background, robot icon).

```

## AGENTS.md
```markdown
# Repository Guidelines

This file provides guidance to AI agents when working with code in this repository.

> **Single source of truth:** This file is a concise pointer document.
> All authoritative architecture, coding rules, commands, and conventions
> live in **CLAUDE.md** at the project root. Read that file first.

## Quick Reference

### Architecture

Go backend + monorepo frontend (pnpm workspaces + Turborepo) with shared packages.

- `server/` — Go backend (Chi router, sqlc, gorilla/websocket)
- `apps/web/` — Next.js frontend (App Router)
- `apps/desktop/` — Electron desktop app
- `packages/core/` — Headless business logic (Zustand stores, React Query hooks, API client)
- `packages/ui/` — Atomic UI components (shadcn/Base UI, zero business logic)
- `packages/views/` — Shared business pages/components
- `packages/tsconfig/` — Shared TypeScript config

### State Management (critical)

- **React Query** owns all server state (issues, members, agents, inbox, workspace list)
- **Zustand** owns all client state (current workspace selection, view filters, drafts, modals)
- All Zustand stores live in `packages/core/` — never in `packages/views/` or app directories
- WS events invalidate React Query — never write directly to stores

### Package Boundaries (hard rules)

- `packages/core/` — zero react-dom, zero localStorage, zero process.env
- `packages/ui/` — zero `@multica/core` imports
- `packages/views/` — zero `next/*`, zero `react-router-dom`, use `NavigationAdapter` for routing
- `apps/web/platform/` — only place for Next.js APIs

### Commands

```bash
make dev              # Auto-setup + start everything
pnpm typecheck        # TypeScript check
pnpm test             # TS unit tests (Vitest)
make test             # Go tests
make check            # Full verification pipeline
```

See CLAUDE.md for the complete command reference.

```

## agents.md
```markdown
# Repository Guidelines

This file provides guidance to AI agents when working with code in this repository.

> **Single source of truth:** This file is a concise pointer document.
> All authoritative architecture, coding rules, commands, and conventions
> live in **CLAUDE.md** at the project root. Read that file first.

## Quick Reference

### Architecture

Go backend + monorepo frontend (pnpm workspaces + Turborepo) with shared packages.

- `server/` — Go backend (Chi router, sqlc, gorilla/websocket)
- `apps/web/` — Next.js frontend (App Router)
- `apps/desktop/` — Electron desktop app
- `packages/core/` — Headless business logic (Zustand stores, React Query hooks, API client)
- `packages/ui/` — Atomic UI components (shadcn/Base UI, zero business logic)
- `packages/views/` — Shared business pages/components
- `packages/tsconfig/` — Shared TypeScript config

### State Management (critical)

- **React Query** owns all server state (issues, members, agents, inbox, workspace list)
- **Zustand** owns all client state (current workspace selection, view filters, drafts, modals)
- All Zustand stores live in `packages/core/` — never in `packages/views/` or app directories
- WS events invalidate React Query — never write directly to stores

### Package Boundaries (hard rules)

- `packages/core/` — zero react-dom, zero localStorage, zero process.env
- `packages/ui/` — zero `@multica/core` imports
- `packages/views/` — zero `next/*`, zero `react-router-dom`, use `NavigationAdapter` for routing
- `apps/web/platform/` — only place for Next.js APIs

### Commands

```bash
make dev              # Auto-setup + start everything
pnpm typecheck        # TypeScript check
pnpm test             # TS unit tests (Vitest)
make test             # Go tests
make check            # Full verification pipeline
```

See CLAUDE.md for the complete command reference.

```


# Repo: optiminds-repo-template

## README.md
```markdown
# optiminds-repo-template

Lightweight harness for Optiminds, Inc. repositories. Two deliverables:

1. **Org-wide AI skills** that auto-trigger across Claude Code / Codex / Gemini / OpenCode.
2. **A baseline CI + governance layer** that any repo can adopt via one command.

No code scaffolding, no stack templates — those are the agent's job once the rules
and skills are in place.

## What you get

Three concerns, cleanly separated:

```
WHAT (rules, always-loaded)      — AGENTS.md                cross-repo, ~200 lines
                                   Core Principles, Security Red Lines,
                                   Git/PR workflow, Testing bar, Glossary

HOW (deep guides, on-demand)     — skills/optiminds-*/      org-wide, auto-trigger
                                   secrets, observability, cloud portability,
                                   testing, API patterns, LLM cost

WHO (per-repo identity)          — CLAUDE.md                per-repo, <50 lines
                                   Purpose, Architecture, Domain vocab,
                                   @AGENTS.md reference

ENFORCEMENT (hard gates)         — .github/workflows/       per-repo, copied by apply.sh
                                   + .pre-commit-config     + CODEOWNERS
```

Per-repo business logic, owners, and product specifics are **out of scope** — those
live in each consumer repo and this template never touches them.

## Quick start

**Once per developer machine** — install org-wide skills into all detected CLIs:

```bash
git clone git@github.com:Optiminds-Inc/optiminds-repo-template.git ~/.optiminds
~/.optiminds/scripts/install-skills.sh
~/.optiminds/scripts/install-skills.sh status
```

**Per repo** — apply Layer 0 (AGENTS.md, CLAUDE.md, CI workflows, hygiene):

```bash
./scripts/apply.sh /path/to/target-repo
```

`apply.sh` is idempotent (File-SHA + gitignore marker/fingerprint checks), so
re-running it on an already-adopted repo is a no-op unless the template itself
has new files.

## Version check

`apply.sh --check` is a read-only query that answers "am I behind the
template, and by how much?" by comparing the consumer repo's recorded
`template_version` against the template clone's `origin/main:version.txt`.
It reuses whatever git auth the template clone already has (SSH or HTTPS),
so it works against private repos without `gh` or a PAT.

Default (pull-mode) usage:

```bash
~/.optiminds/scripts/apply.sh --check ~/dev/my-repo
```

Sample up-to-date output:

```
==> Fetching latest template version...
==> Current applied:  0.4.1
==> Template latest:  0.4.1  (up-to-date)
```

Strict mode for CI exits non-zero when the consumer is behind, so a
pipeline step can surface the drift:

```bash
~/.optiminds/scripts/apply.sh --check --strict ~/dev/my-repo
```

Sample behind output:

```
==> Fetching latest template version...
==> Current applied:  0.3.0
==> Template latest:  0.4.1  (behind 1 minor, 1 patch)

Files that would change if you re-apply:
  M  .github/workflows/codex-review.yml         (template updated)
  !  AGENTS.md                                   (consumer modified — would skip without --force)
  +  docs/runbooks/cost-monitoring.template.md   (new in template)

Run: ~/.optiminds/scripts/apply.sh ~/dev/my-repo
```

Exit codes follow the `grep`/`diff` convention: `0` for up-to-date,
`2` for behind (under `--strict` only; default always exits 0), `1` for
real errors (missing metadata, malformed JSON, target not a git repo).

A compact push-mode banner fires automatically on `apply.sh <target>`
when the consumer's `template_version` is behind the template's current
version — no separate command needed. Sample banner when the consumer is
one minor + one patch behind:

```
==> Template metadata upgrade: 0.3.0 → 0.4.1 (1 minor + 1 patch)
==>   Run `apply.sh --check ~/dev/my-repo` for file-level diff before re-applying.
```

Set `OPTIMINDS_QUIET_VERSION=1` to silence the push-mode banner for
CI/scripted consumers that have already acknowledged the drift and don't
want log noise:

```bash
OPTIMINDS_QUIET_VERSION=1 ~/.optiminds/scripts/apply.sh ~/dev/my-repo
```

- Suppresses the minor / patch / ahead / first-tracking banners.
- Does **not** suppress the BREAKING banner for major version jumps — by
  design. Silently crossing a major boundary is the exact failure mode
  SemVer's major signal exists to prevent, so the BREAKING line is the
  one guard rail you cannot disable.

**Known limitation** — `--check` relies on the template clone's local
`origin/main` ref. A stale clone (corporate proxy that caches DNS, an
offline laptop, or a long-lived checkout) can report a false "up-to-date".
Run `git -C ~/.optiminds pull` periodically — or before a `--check` run
you care about — to refresh the local ref.

## What's in Layer 0 (the always-applies set)

| File | Purpose |
|---|---|
| `.github/workflows/codex-review.yml` | 3-pass Codex AI review on every PR (quality / security / dependencies) |
| `.github/workflows/secrets-scan.yml` | gitleaks + trufflehog on PR + nightly + `.gitignore` audit |
| `.github/CODEOWNERS.template` | Path-based review routing (billing / auth / migrations / infra) |
| `.github/pull_request_template.md` | 8-section PR template — what / why / test / obs / rollback / cost / cross-repo |
| `.github/ISSUE_TEMPLATE/` | Bug / feature / incident templates |
| `.pre-commit-config.base.yaml` | gitleaks + detect-secrets + basic hygiene hooks |
| `.gitignore.base` | Comprehensive secret + OS + IDE + build artifact patterns |
| `.codex.yaml.base` | Path-based Codex review strictness (strict for billing/auth, lenient for tests/docs) |
| **`AGENTS.md.template`** | **Org-wide agent rules — Core Principles + Security Red Lines + Tooling Setup. Loaded by Claude Code via `@AGENTS.md` in CLAUDE.md; natively read by Codex/Cursor/Aider.** |
| `CLAUDE.md.template` | Per-repo identity skeleton (<50 lines) — references `@AGENTS.md` for org rules |
| `README.md.template` | 6-section README skeleton |
| `docs/adr/0000-TEMPLATE.md` | ADR template (MADR-style) |
| `docs/runbooks/deploy.template.md` | Deploy runbook skeleton |
| `docs/runbooks/incident-response.template.md` | Incident response runbook skeleton |

## Org-wide skills (ship via `~/.optiminds`, not per-repo)

| Skill | Triggers on | Status |
|---|---|---|
| `optiminds-secrets` | `.env*`, credentials, Azure Key Vault, OIDC auth | ✓ shipped |
| `optiminds-obs` | logging, metrics, traces, LLM cost attribution | planned |
| `optiminds-cloud-port` | cloud SDK imports, blob / queue / DB drivers | planned |
| `optiminds-testing` | writing tests, fixtures, CI test stages | planned |
| `optiminds-api` | API routes, request/response schemas, versioning | planned |
| `optiminds-llm-cost` | Anthropic / OpenAI calls, agent logic, LLM tracing | planned |

Skills live once in this repo's `skills/` directory and symlink into each
CLI via `./scripts/install-skills.sh`. Updating a skill = `git pull` on
`~/.optiminds` + re-run install; every repo on your machine sees the new
version instantly (no per-repo PR).

## How updates propagate

| What | Mechanism | Propagation |
|---|---|---|
| Skills (`skills/optiminds-*/`) | `~/.optiminds` clone + `install-skills.sh` symlinks | Seconds — just `git pull` |
| Layer 0 files (workflows, AGENTS.md, CLAUDE.md, etc.) | `apply.sh` re-run on consumer repo (idempotent; preserves consumer edits) | Manual, per repo |

Skills are the fast-path: organization-wide knowledge that's identical across
every Optiminds repo, so it lives once and symlinks everywhere. Layer 0 files
live per-consumer-repo because CODEOWNERS, pre-commit config, and CLAUDE.md
are customized; `apply.sh` uses File-SHA tracking so re-applying never
overwrites consumer edits.

### Open TODO: auto-PR for Layer 0 drift

Layer 0 propagation today is **manual** — consumers re-run `apply.sh` when
they choose, and `apply.sh --check --strict` in consumer CI can surface
drift as a red light. This is sufficient at current scale (~7-8 consumer
repos), but has a known UX flaw as the consumer count grows: the CI signal
lands on whichever unrelated PR happens to open next, not on the repo
owner who should actually decide about template updates. Friction falls on
the wrong person.

**Upgrade path** (trigger: consumer count ≥ ~10, or misrouted-friction
complaints start surfacing):

1. Scheduled workflow in this template repo that runs `apply.sh --check`
   against every registered consumer repo.
2. On drift, `gh pr create` in the consumer repo with the proposed diff —
   Dependabot / Renovate-style. Consumer repo owner reviews and merges
   at their own pace, preserving the "human decides adoption" principle.
3. Auth via a short-lived GitHub App installation token, not a long-lived PAT.

Deferred for now — the manual `apply.sh` flow has better ROI than bot
maintenance at current scale. When picked up, design decisions belong in
an ADR under `docs/adr/`.

## Governance

- Major changes (breaking policy, removing files) require ADR in `docs/adr/` + approval from platform owners.
- Minor changes (tightening rules, adding new skills) follow normal PR flow via Conventional Commits.
- Releases are automated via release-please: merge the "Release PR" it opens; the `release-please.yml` workflow creates the tag + GitHub Release and sends the Lark notification inline. (`release.yml` handles the manual-tag path — human-pushed tags from `scripts/release.sh` — since default `GITHUB_TOKEN` events don't cascade to trigger it from release-please.)
- Every tagged release has a `CHANGELOG.md` entry with migration notes if breaking.

## Who maintains this

| Surface | Owner |
|---|---|
| Layer 0 (CI workflows, AGENTS.md, CLAUDE.md template) | `@Optiminds-Inc/platform-owners` |
| Skills (`skills/optiminds-*/`) | Domain owner per skill (secrets → security lead, obs → platform lead, etc.) |
| Per-repo adoption (CODEOWNERS, CLAUDE.md content) | Consumer repo team (not this template) |

## Repository layout

```
optiminds-repo-template/
├── layer0-core/              # What apply.sh copies into consumer repos
│   ├── .github/              # Workflows, CODEOWNERS, PR/issue templates
│   ├── docs/                 # ADR + runbook templates
│   ├── AGENTS.md.template    # Org-wide rules
│   ├── CLAUDE.md.template    # Per-repo identity skeleton
│   ├── README.md.template
│   ├── .pre-commit-config.base.yaml
│   ├── .codex.yaml.base
│   └── .gitignore.base
├── skills/                   # Org-wide AI skills (Channel C)
│   ├── README.md
│   └── optiminds-secrets/    # First shipped skill
├── scripts/
│   ├── apply.sh              # Copies layer0-core/ into a target repo
│   ├── install-skills.sh     # Symlinks skills/* into Claude/Codex/Gemini/OpenCode
│   ├── bootstrap.sh          # Dev-tool audit
│   └── release.sh            # Manual version bump (auto-bumper lives in workflow)
├── .github/workflows/        # Template's OWN CI — not copied to consumers
│   ├── validate.yml          # shellcheck + yamllint + bats
│   ├── release-please.yml    # Auto-bumper: Conventional Commits → Release PR
│   └── release.yml           # On tag push: GitHub Release + Lark notify
├── tests/                    # bats suite for apply.sh + release.sh
├── docs/                     # Reference docs (not copied by apply.sh)
└── CONTRIBUTING.md / SECURITY.md / LICENSE / CHANGELOG.md / version.txt
```

```

## skills/README.md
```markdown
# Optiminds Skills — organization-wide AI agent knowledge

Single source of truth for Optiminds-wide AI skills. Skills auto-trigger in
Claude Code / Codex / Gemini / OpenCode based on their `description` fields —
no manual invocation needed.

## Why here (not per-repo)

Skills are **organization-level assets**. A convention for `observability`,
`secrets`, or `cloud-portability` should be identical across every Optiminds
repo. Embedding them per-repo would mean 30 copies and a per-repo PR cycle
on every update. Centralizing here = update once, 30 repos see it instantly
(symlink-based propagation — see top-level `README.md`'s "How updates propagate").

## Structure

```
skills/
├── optiminds-secrets/SKILL.md        secrets handling (Azure KV pattern + rankgale lessons)
├── optiminds-obs/SKILL.md            observability conventions         [v0.4 planned]
├── optiminds-cloud-port/SKILL.md     cloud-portability rules           [v0.4 planned]
├── optiminds-testing/SKILL.md        testing standards                 [v0.4 planned]
├── optiminds-api/SKILL.md            FastAPI route patterns            [v0.4 planned]
└── optiminds-llm-cost/SKILL.md       LLM cost attribution              [v0.4 planned]
```

## Install to your CLI

One-time per developer machine:

```bash
git clone git@github.com:Optiminds-Inc/optiminds-repo-template.git ~/.optiminds
~/.optiminds/scripts/install-skills.sh
```

This symlinks skills into all detected CLIs:

| CLI         | Target path                                | Mechanism                         |
|-------------|--------------------------------------------|-----------------------------------|
| Claude Code | `~/.claude/plugins/optiminds/skills/`      | symlinks (Bug #14836 workaround)  |
| Codex       | `~/.codex/skills/`                         | native symlinks                   |
| Gemini      | `~/.gemini/skills/`                        | native symlinks                   |
| OpenCode    | `~/.config/opencode/agent/`                | format-converted copies           |

## Update

```bash
cd ~/.optiminds && git pull
./scripts/install-skills.sh
```

## Adding a new skill

1. Create `skills/optiminds-<name>/SKILL.md` with frontmatter:
   ```yaml
   ---
   name: optiminds-<name>
   version: 0.1.0
   description: |
     Use when <concrete trigger keywords>. <What this skill enforces>.
   ---
   ```
2. Description must contain **specific technical keywords** that match real
   task context (e.g. "Azure Key Vault", "OpenTelemetry", not "observability
   stuff").
3. Verify with `./scripts/install-skills.sh list`
4. PR per [`CONTRIBUTING.md`](../CONTRIBUTING.md)

Use [`optiminds-secrets/SKILL.md`](optiminds-secrets/SKILL.md) as the reference
pattern.

## Governance

Skills live in Layer 0 (stack-agnostic, organization-wide). Per-repo
specializations belong in that repo's own `.claude/skills/` — not here.

```

## skills/optiminds-secrets/SKILL.md
```markdown
---
name: optiminds-secrets
version: 0.1.0
description: |
  Use when touching .env, .envrc, credentials/, secrets/, Azure Key Vault,
  OIDC federated credentials, or any code path that reads API keys /
  database URLs / OAuth client secrets. Enforces the "no Azure SDK in
  business code" rule and the three-location pattern (local dev via direnv,
  CI via azure/cli OIDC, production via managed identity). Prevents
  rankgale-style credential leaks to git history.
---

# Optiminds Secrets Handling

Canonical pattern for every Optiminds service. Defines three concrete
scenarios (local dev, GitHub Actions, production) and the one hard rule
that keeps us cloud-portable.

## The hard rule

> **Azure SDK MUST NOT appear in business code.**

The moment a request handler imports `azure.keyvault.*`, we lose cloud
portability. Migrating Azure → GCP then means rewriting every handler,
not just deploy YAML.

### Forbidden in `/backend*/`, `/server/`, `/api/`, `/frontend/`, `/sdk/`, `/cli/`

```python
# FORBIDDEN
import azure.identity
import azure.keyvault.secrets
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url=..., credential=DefaultAzureCredential())
secret = client.get_secret("stripe-secret-key-prod").value
```

TypeScript equivalent (also forbidden in business code):

```typescript
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";
```

### Permitted paths only

- `/scripts/` — bootstrap / rotation tooling
- `/tools/` — template-repo internal tooling
- `/deploy/` — infra-only bootstrap
- `/.github/workflows/*.yml` — CI steps (uses `azure/cli@v2`, not SDK from app)

Business code reads secrets through `os.environ[...]` / `process.env.*` only.

## The three-location pattern

| Location       | Mechanism                                     | App code sees    |
|----------------|-----------------------------------------------|------------------|
| Local dev      | `az keyvault secret show` → `export` via direnv | `os.environ[...]` |
| GitHub Actions | `azure/cli@v2` → `$GITHUB_ENV`                | `os.environ[...]` |
| Container Apps | `secretRef` + managed identity                | `os.environ[...]` |

**The app code column never changes. That is the invariant.**

## Pattern 1 — Local development (direnv + az)

Prereqs: `az` CLI + `Key Vault Secrets User` role on `dev-optiminds-kv`.

```bash
# one-time
az login
az account set --subscription optiminds-dev
```

Per-project `.envrc` (gitignored; `.envrc.template` is the committed skeleton):

```bash
export ENV=development
export AZURE_KEY_VAULT_NAME=dev-optiminds-kv
export SERVICE_NAME=<service>

# One az call per secret — individual env vars, never one JSON blob
export STRIPE_SECRET_KEY=$(az keyvault secret show \
    --vault-name "$AZURE_KEY_VAULT_NAME" --name stripe-secret-key-dev \
    --query value -o tsv)
export DATABASE_URL=$(az keyvault secret show \
    --vault-name "$AZURE_KEY_VAULT_NAME" --name <service>-db-url-dev \
    --query value -o tsv)
# ... one line per secret
```

**Why individual env vars, not a JSON blob**:
- App code stays vanilla: `os.environ["STRIPE_SECRET_KEY"]`, no parsing.
- Rotate one key → `direnv reload` → no app change.
- Git-leak forensics: one leaked env-var name = one secret, not all of them.

## Pattern 2 — GitHub Actions (OIDC federated, no long-lived secret)

```yaml
permissions:
  id-token: write          # required for OIDC
  contents: read

jobs:
  deploy:
    steps:
      - uses: actions/checkout@v4
      - name: Azure login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Hydrate secrets from Key Vault
        uses: azure/cli@v2
        with:
          inlineScript: |
            set -euo pipefail
            VAULT=prod-optiminds-kv
            for pair in \
              "STRIPE_SECRET_KEY:stripe-secret-key-prod" \
              "DATABASE_URL:<service>-db-url-prod" \
              "OPENAI_API_KEY:openai-api-key-prod"
            do
              name=${pair%%:*}
              secret=${pair#*:}
              value=$(az keyvault secret show --vault-name "$VAULT" \
                      --name "$secret" --query value -o tsv)
              echo "::add-mask::$value"
              echo "$name=$value" >> "$GITHUB_ENV"
            done

      - name: Deploy (reads env vars, no Key Vault import)
        run: ./scripts/deploy.sh
```

**Why OIDC over service-principal password**: zero long-lived secrets in
`GITHUB_SECRETS`; identity scoped per-repo + per-environment; revocation is
one Azure AD click.

## Pattern 3 — Production (Azure Container Apps)

App reads `os.environ["STRIPE_SECRET_KEY"]`. Period. Platform injects the env
var via user-assigned managed identity bound to the container.

```yaml
# deploy/container-app.yaml (excerpt)
spec:
  identity:
    type: UserAssigned
    userAssignedIdentities:
      "/subscriptions/.../userAssignedIdentities/<service>-prod-mi": {}
  configuration:
    secrets:
      - name: stripe-secret-key
        keyVaultUrl: https://prod-optiminds-kv.vault.azure.net/secrets/stripe-secret-key-prod
        identity: /subscriptions/.../userAssignedIdentities/<service>-prod-mi
  template:
    containers:
      - image: optimindsacr.azurecr.io/<service>:v1.4.2
        env:
          - name: STRIPE_SECRET_KEY
            secretRef: stripe-secret-key
```

AKS equivalent: Secret Store CSI Driver + same managed-identity binding.

## Rotation

```bash
# Rotate a secret (runs against Key Vault; app picks up on next pod restart)
az keyvault secret set --vault-name prod-optiminds-kv \
    --name stripe-secret-key-prod \
    --value "<new-value>"

# Set expiration window (drives monitoring alerts)
az keyvault secret set-attributes --vault-name prod-optiminds-kv \
    --name stripe-secret-key-prod \
    --expires 2026-10-21T00:00:00Z
```

If a secret is **leaked to git history** (the rankgale-2026-04 lesson):
1. **Rotate first** — new value in Key Vault before cleanup
2. Then BFG / `git filter-repo` the old value from history
3. Force-push with coordinated team notification
4. Document in `docs/incidents/`

## Cloud-migration tax (Azure → GCP, 6-18mo)

What changes vs. what stays portable:

| Component                                      | Change needed     | Why                                     |
|------------------------------------------------|-------------------|-----------------------------------------|
| Business code `os.environ["X"]`                | **0 LOC**         | SDK never imported                      |
| Logger / structlog processors                  | 0 LOC             | Env-var driven                          |
| `.github/workflows/*.yml` hydrate step         | ~30 LOC           | `azure/cli` → `google-github-actions`   |
| Local dev `.envrc`                             | ~60 LOC           | `az` loop → `gcloud secrets` loop       |
| Production deploy manifest                     | ~90 LOC           | Container Apps `secretRef` → Cloud Run `--set-secrets` |
| OIDC federation                                | 1-day org setup   | Azure AD federated → GCP Workload Identity |
| **Total**                                      | **≈ 3 engineer-days** | Paid once                          |

The 3-day migration budget is the justification for choosing AKV over a
vendor-neutral secrets manager. Paying $0 today + 3 days in 2027 beats
paying $X K / year forever.

## What to do when you encounter

### "I need to add a new secret to this service"

1. Add it to Azure Key Vault: `az keyvault secret set --vault-name dev-optiminds-kv --name <secret-name>-dev --value "..."`
2. Add corresponding `-staging` and `-prod` entries (or ask platform-owners for prod)
3. Add one `export` line in `.envrc.template` (with placeholder)
4. Add one entry in the CI `for pair in ...` loop in `.github/workf

[... truncated to 8KB ...]

```


# Repo: lawyer_finder

## README.md
```markdown
# Lawyer Finder

Monorepo for a lawyer discovery product: a public marketing site, an operations admin, and a FastAPI backend.

## Repository layout

| Directory   | Role |
|------------|------|
| `frontend` | Public site (React + Vite + Tailwind): home, cities, blog, lead capture. Dev server default **5173**. |
| `admin`    | Internal console (React + Vite + Tailwind): lawyers, leads, content (blogs, FAQs), geography, knowledge, settings. Dev server default **5174**. |
| `backend`  | REST API (FastAPI, async SQLAlchemy, PostgreSQL, Redis, Alembic). Default **8030** (`API_PORT`). |
| `docs`     | Additional integration notes (e.g. auth, analytics). |

## Prerequisites

- **Node.js** (current LTS recommended) for `frontend` and `admin`
- **Python 3.11** and **[uv](https://github.com/astral-sh/uv)** for `backend`
- **PostgreSQL** and **Redis** (see `backend/.env.example`)

## Quick start

### Backend

```bash
cd backend
uv sync
cp .env.example .env.development   # then edit to match your DB/Redis
uv run python main.py
```

API base URL defaults to `http://localhost:8030`. More detail: [backend/README.md](backend/README.md).

### Frontend (public site)

```bash
cd frontend
npm install
# Set VITE_API_BASE_URL for production builds; dev can rely on Vite proxy /api → 8030
npm run dev
```

Open `http://localhost:5173` (or the port Vite prints).

### Admin

```bash
cd admin
npm install
npm run dev
```

Open `http://localhost:5174`. `/api` is proxied to `http://localhost:8030` in development.

## Configuration notes

- **Backend**: Environment variables live under `backend/` (see `.env.example`). Paths use underscores (e.g. API routes), not hyphens.
- **Frontends**: Use `VITE_API_BASE_URL` where needed; the Vite dev configs proxy `/api` to the backend for local work.

## License

See individual packages where applicable (e.g. MIT in `frontend` / `admin` metadata).

```

## AGENTS.md
```markdown
<!-- OMC:START -->
<!-- OMC:VERSION:4.9.3 -->

# oh-my-Codex - Intelligent Multi-Agent Orchestration

You are running with oh-my-Codex (OMC), a multi-agent orchestration layer for Codex.
Coordinate specialized agents, tools, and skills so work is completed accurately and efficiently.

<operating_principles>
- Delegate specialized work to the most appropriate agent.
- Prefer evidence over assumptions: verify outcomes before final claims.
- Choose the lightest-weight path that preserves quality.
- Consult official docs before implementing with SDKs/frameworks/APIs.
</operating_principles>

<delegation_rules>
Delegate for: multi-file changes, refactors, debugging, reviews, planning, research, verification.
Work directly for: trivial ops, small clarifications, single commands.
Route code to `executor` (use `model=opus` for complex work). Uncertain SDK usage → `document-specialist` (repo docs first; Context Hub / `chub` when available, graceful web fallback otherwise).
</delegation_rules>

<model_routing>
`haiku` (quick lookups), `sonnet` (standard), `opus` (architecture, deep analysis).
Direct writes OK for: `~/.Codex/**`, `.omc/**`, `.Codex/**`, `AGENTS.md`, `AGENTS.md`.
</model_routing>

<skills>
Invoke via `/oh-my-Codex:<name>`. Trigger patterns auto-detect keywords.
Tier-0 workflows include `autopilot`, `ultrawork`, `ralph`, `team`, and `ralplan`.
Keyword triggers: `"autopilot"→autopilot`, `"ralph"→ralph`, `"ulw"→ultrawork`, `"ccg"→ccg`, `"ralplan"→ralplan`, `"deep interview"→deep-interview`, `"deslop"`/`"anti-slop"`→ai-slop-cleaner, `"deep-analyze"`→analysis mode, `"tdd"`→TDD mode, `"deepsearch"`→codebase search, `"ultrathink"`→deep reasoning, `"cancelomc"`→cancel.
Team orchestration is explicit via `/team`.
Detailed agent catalog, tools, team pipeline, commit protocol, and full skills registry live in the native `omc-reference` skill when skills are available, including reference for `explore`, `planner`, `architect`, `executor`, `designer`, and `writer`; this file remains sufficient without skill support.
</skills>

<verification>
Verify before claiming completion. Size appropriately: small→haiku, standard→sonnet, large/security→opus.
If verification fails, keep iterating.
</verification>

<execution_protocols>
Broad requests: explore first, then plan. 2+ independent tasks in parallel. `run_in_background` for builds/tests.
Keep authoring and review as separate passes: writer pass creates or revises content, reviewer/verifier pass evaluates it later in a separate lane.
Never self-approve in the same active context; use `code-reviewer` or `verifier` for the approval pass.
Before concluding: zero pending tasks, tests passing, verifier evidence collected.
</execution_protocols>

<hooks_and_context>
Hooks inject `<system-reminder>` tags. Key patterns: `hook success: Success` (proceed), `[MAGIC KEYWORD: ...]` (invoke skill), `The boulder never stops` (ralph/ultrawork active).
Persistence: `<remember>` (7 days), `<remember priority>` (permanent).
Kill switches: `DISABLE_OMC`, `OMC_SKIP_HOOKS` (comma-separated).
</hooks_and_context>

<cancellation>
`/oh-my-Codex:cancel` ends execution modes. Cancel when done+verified or blocked. Don't cancel if work incomplete.
</cancellation>

<worktree_paths>
State: `.omc/state/`, `.omc/state/sessions/{sessionId}/`, `.omc/notepad.md`, `.omc/project-memory.json`, `.omc/plans/`, `.omc/research/`, `.omc/logs/`
</worktree_paths>

## Setup

Say "setup omc" or run `/oh-my-Codex:omc-setup`.

<!-- OMC:END -->

```

## agents.md
```markdown
<!-- OMC:START -->
<!-- OMC:VERSION:4.9.3 -->

# oh-my-Codex - Intelligent Multi-Agent Orchestration

You are running with oh-my-Codex (OMC), a multi-agent orchestration layer for Codex.
Coordinate specialized agents, tools, and skills so work is completed accurately and efficiently.

<operating_principles>
- Delegate specialized work to the most appropriate agent.
- Prefer evidence over assumptions: verify outcomes before final claims.
- Choose the lightest-weight path that preserves quality.
- Consult official docs before implementing with SDKs/frameworks/APIs.
</operating_principles>

<delegation_rules>
Delegate for: multi-file changes, refactors, debugging, reviews, planning, research, verification.
Work directly for: trivial ops, small clarifications, single commands.
Route code to `executor` (use `model=opus` for complex work). Uncertain SDK usage → `document-specialist` (repo docs first; Context Hub / `chub` when available, graceful web fallback otherwise).
</delegation_rules>

<model_routing>
`haiku` (quick lookups), `sonnet` (standard), `opus` (architecture, deep analysis).
Direct writes OK for: `~/.Codex/**`, `.omc/**`, `.Codex/**`, `AGENTS.md`, `AGENTS.md`.
</model_routing>

<skills>
Invoke via `/oh-my-Codex:<name>`. Trigger patterns auto-detect keywords.
Tier-0 workflows include `autopilot`, `ultrawork`, `ralph`, `team`, and `ralplan`.
Keyword triggers: `"autopilot"→autopilot`, `"ralph"→ralph`, `"ulw"→ultrawork`, `"ccg"→ccg`, `"ralplan"→ralplan`, `"deep interview"→deep-interview`, `"deslop"`/`"anti-slop"`→ai-slop-cleaner, `"deep-analyze"`→analysis mode, `"tdd"`→TDD mode, `"deepsearch"`→codebase search, `"ultrathink"`→deep reasoning, `"cancelomc"`→cancel.
Team orchestration is explicit via `/team`.
Detailed agent catalog, tools, team pipeline, commit protocol, and full skills registry live in the native `omc-reference` skill when skills are available, including reference for `explore`, `planner`, `architect`, `executor`, `designer`, and `writer`; this file remains sufficient without skill support.
</skills>

<verification>
Verify before claiming completion. Size appropriately: small→haiku, standard→sonnet, large/security→opus.
If verification fails, keep iterating.
</verification>

<execution_protocols>
Broad requests: explore first, then plan. 2+ independent tasks in parallel. `run_in_background` for builds/tests.
Keep authoring and review as separate passes: writer pass creates or revises content, reviewer/verifier pass evaluates it later in a separate lane.
Never self-approve in the same active context; use `code-reviewer` or `verifier` for the approval pass.
Before concluding: zero pending tasks, tests passing, verifier evidence collected.
</execution_protocols>

<hooks_and_context>
Hooks inject `<system-reminder>` tags. Key patterns: `hook success: Success` (proceed), `[MAGIC KEYWORD: ...]` (invoke skill), `The boulder never stops` (ralph/ultrawork active).
Persistence: `<remember>` (7 days), `<remember priority>` (permanent).
Kill switches: `DISABLE_OMC`, `OMC_SKIP_HOOKS` (comma-separated).
</hooks_and_context>

<cancellation>
`/oh-my-Codex:cancel` ends execution modes. Cancel when done+verified or blocked. Don't cancel if work incomplete.
</cancellation>

<worktree_paths>
State: `.omc/state/`, `.omc/state/sessions/{sessionId}/`, `.omc/notepad.md`, `.omc/project-memory.json`, `.omc/plans/`, `.omc/research/`, `.omc/logs/`
</worktree_paths>

## Setup

Say "setup omc" or run `/oh-my-Codex:omc-setup`.

<!-- OMC:END -->

```

## .claude/skills/deploy-production/SKILL.md
```markdown
---
name: lawyer-finder-deploy-production
description: Deploy lawyer_finder to production (104.45.215.114). Use for "deploy to production", "publish to production", "deploy prod", etc. Prefer scripts/deploy-production.sh; supports full stack, frontend-only (no backend recreate), frontend restart-only, --no-cache, --skip-push, --yes.
---

# Lawyer Finder — Production Deployment

## Infrastructure

| Item              | Value                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Server IP         | `104.45.215.114`                                                      |
| SSH User          | `getuai_deploy`                                                       |
| SSH Key           | `~/.ssh/id_rsa` (generated for this server)                           |
| Domain (Frontend) | `lawyerfinder.ai` (Caddy auto-HTTPS)                                 |
| Domain (Admin)    | `admin.lawyerfinder.ai` (Caddy auto-HTTPS)                           |
| Caddy Ports       | `80` (HTTP→redirect), `443` (HTTPS) — only exposed ports             |
| Backend Port      | `8030` (internal, not exposed to host)                                |
| Frontend Port     | `3000` (internal, not exposed to host)                                |
| Nginx Ports       | `80/81` (internal, not exposed to host)                               |
| Redis             | Azure Managed Redis (`lawyer.westus.redis.azure.net:10000`, SSL)      |
| DB Host           | `lawyer-finder.postgres.database.azure.com:5432` (Azure PostgreSQL)   |
| Project Path      | `/home/getuai_deploy/projects/lawyer_finder`                          |
| Compose File      | `docker/docker-compose.production.yml`                                |
| Compose Name      | `lawyer-finder-prod` (via `-p lawyer-finder-prod`)                    |
| Git Remote        | `git@github-getu:Optiminds-Inc/lawyer_finder.git` (alias: `origin`)  |
| Git Branch        | `main`                                                                |
| VM Size           | `Standard_B2ms` (2 vCPU, 8GB RAM, 64GB Premium SSD)                  |
| Azure NSG         | `lawyer-finder-prod-nsg` in resource group `ADS`                      |

## Security Configuration

This production server has been hardened with:

- **SSH**: Key-only auth, password disabled, root login disabled, MaxAuthTries=3
- **UFW Firewall**: Only ports 22, 80, 443 open (double-layered with Azure NSG)
- **Azure NSG**: Only ports 22, 80, 443 allowed, all other inbound denied
- **fail2ban**: SSH brute-force protection (3 attempts → 2h ban)
- **Unattended Upgrades**: Automatic security patches
- **Kernel Hardening**: SYN cookies, ICMP filtering, source routing disabled
- **Docker**: Log rotation (10MB x 3 files), live-restore enabled
- **Caddy**: Auto TLS with Let's Encrypt, security headers (HSTS, X-Frame-Options, etc.)
- **Nginx**: Rate limiting (30r/s API, 50r/s general), exploit path blocking, server_tokens off
- **CORS**: Restricted to `lawyerfinder.ai` and `admin.lawyerfinder.ai` only

## Deployment Steps

**Preferred:** run from repo root (same workflow style as staging):

```bash
cd d:/work-projects/lawyer_finder
./scripts/deploy-production.sh                      # full stack
./scripts/deploy-production.sh --frontend-only      # Next + nginx only; backend container not recreated
./scripts/deploy-production.sh --restart-frontend   # no build; restart frontend + web only
./scripts/deploy-production.sh --no-cache           # full stack rebuild without Docker cache
./scripts/deploy-production.sh --skip-push          # server pull + redeploy only
./scripts/deploy-production.sh --yes                # non-interactive if working tree is dirty
```

See `./scripts/deploy-production.sh --help` for all flags.

### Why `--frontend-only` uses `build frontend web` + `up --no-deps`?

Same rationale as staging: `docker compose up -d --build frontend` still joins the **full** Compose bake/dependency graph and often **recreates `lawyer-finder-prod-backend`** even when backend layers are cache hits. The script:

1. Runs `docker compose build frontend web` — only those images rebuild (backend image is not built).
2. Runs `docker compose up -d --no-deps frontend web` — replace only those containers; **do not** reconcile dependent services.

`web` is nginx (admin SPA + proxy to Next.js). Rebuilding it with `frontend` matches staging’s `deploy-staging.sh` and avoids touching the API container.

Manual equivalent:

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && \
  docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml build frontend web && \
  docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml up -d --no-deps frontend web"
```

---

If not using the script, execute the following sequentially. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/lawyer_finder
git push origin main
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && git pull origin main"
```

### 3. Sync Env Files (SSH-encrypted)

Upload production env files via `scp` **before** rebuilding containers.

**Backend** (runtime secrets, DB, Redis, etc.):

```bash
scp d:/work-projects/lawyer_finder/backend/.env.production getuai_deploy@104.45.215.114:~/projects/lawyer_finder/backend/.env.production
```

**Frontend** (Next.js; `env_file` in compose):

```bash
scp d:/work-projects/lawyer_finder/frontend/.env.production getuai_deploy@104.45.215.114:~/projects/lawyer_finder/frontend/.env.production
```

If a local file does not exist, skip that upload.

### 4. Rebuild & Restart Containers

**Full stack** (takes ~3-5 minutes):

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml up -d --build"
```

**Frontend-only** — use `./scripts/deploy-production.sh --frontend-only` or the manual block above.

Monitor build progress by reading the terminal output. Key milestones:

- `lawyer-finder-prod-backend` — pip install Python deps (~60s)
- `lawyer-finder-prod-web` — npm ci + vite build for admin (~30s)
- `lawyer-finder-prod-frontend` — npm ci + Next.js build (~60s)
- `exporting to image` — final export (~30s)
- `Container lawyer-finder-prod-caddy Started` — Caddy ready (auto TLS)
- `Container lawyer-finder-prod-backend Started` — backend done
- `Container lawyer-finder-prod-web Started` — web done

### 5. Verify Deployment

```bash
# Check all 4 containers are running
ssh getuai_deploy@104.45.215.114 "docker ps --filter name=lawyer-finder-prod"

# Check backend logs for successful startup
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-backend --tail 20"

# Check nginx (web) logs
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-web --tail 10"

# Check Caddy logs for TLS certificate
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-caddy --tail 20"
```

Expected healthy backend log output:

```
🔄 Running Alembic database migrations...
✅ Migrations applied successfully
🚀 Starting backend on port 8030 with 4 workers...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8030
```

### 6. Health Check

```bash
# Frontend (HTTPS; follow locale redirect / → /en|/zh)
curl -sL -o /dev/null -w '%{http_code}' https://lawyerfinder.ai/

# Admin console (HTTPS; -L if your admin entry redirects)
curl -sL -o /dev/null -w '%{http_code}' https://admin.lawyerfinder.ai

# API health
curl -s https://lawyerfinder.ai/api/health

# TLS certificate verification
curl -vI https://lawyerfinder.ai 2>&1 | grep -E 'subject:|expire'
```

Expected: HTML endpoints return `200` after redirects, API returns JSON with `"healthy"`, TLS certificate issued by Let's Encrypt.

## Container Architecture

`

[... truncated to 8KB ...]

```

## .claude/skills/deploy-staging/SKILL.md
```markdown
---
name: lawyer-finder-deploy
description: Deploy lawyer_finder to staging (20.228.94.67). Use for "deploy", "deploy to staging", "update staging", etc. Prefer scripts/deploy-staging.sh (full stack, --frontend-only, --restart-frontend, --no-cache, --skip-push, --yes). Production uses scripts/deploy-production.sh — see skill lawyer-finder-deploy-production.
---

# Lawyer Finder — Staging Deployment

## Infrastructure

| Item              | Value                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Server IP         | `20.228.94.67`                                                        |
| SSH User          | `getuai_dev`                                                          |
| Frontend Port     | `8086` (nginx → serves public SPA + proxies API to backend)          |
| Admin Port        | `8087` (nginx → serves admin SPA + proxies API to backend)           |
| Backend Port      | `8030` (internal, not exposed to host)                                |
| Redis             | Internal container (port 6379, not exposed to host)                   |
| Project Path      | `/home/getuai_dev/projects/lawyer_finder`                             |
| Compose File      | `docker/docker-compose.staging.yml`                                   |
| Compose Name      | `lawyer-finder` (via `-p lawyer-finder`)                              |
| DB Host           | `20.59.118.120:32476` (external PostgreSQL)                           |
| Git Remote        | `git@github-getu:Optiminds-Inc/lawyer_finder.git` (alias: `origin`)  |
| Git Branch        | `main`                                                                |
| Frontend URL      | `http://20.228.94.67:8086`                                            |
| Admin URL         | `http://20.228.94.67:8087`                                            |

## ⚠️ Co-located Services

This server also runs other projects. Do NOT touch:
- **lawyer_marketing**: Caddy on 80/443, app on 3456 → containers `docker-app-1` / `docker-caddy-1`
- **geo-seo-v2**: nginx on 8085, backend on 3457 → containers `geo-seo-v2-frontend-1` / `geo-seo-v2-backend-1`
- Ports 80, 443, 3456, 3457, 8085

## Deployment Steps

**Preferred:** run from repo root after committing and pushing (or rely on the script’s push step):

```bash
cd d:/work-projects/lawyer_finder
./scripts/deploy-staging.sh --frontend-only   # Next + nginx only; backend container not recreated
./scripts/deploy-staging.sh                 # full stack
./scripts/deploy-staging.sh --restart-frontend   # no build; restart frontend + web only
./scripts/deploy-staging.sh --yes           # non-interactive if working tree is dirty
```

Script flags: `--no-cache`, `--skip-push`, `--yes` / `-y`. See `scripts/deploy-staging.sh --help`.

### Why `--frontend-only` instead of `up -d --build frontend web`?

`docker compose up -d --build frontend web` still loads the **whole** Compose bake graph and, because of `depends_on`, often **recreates `lawyer-finder-backend`** even when backend layers are cache hits. The script uses:

1. `docker compose build frontend web` — only those Dockerfiles run.
2. `docker compose up -d --no-deps frontend web` — replace only those containers; **do not** reconcile dependent services.

Manual equivalent:

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && \
  docker compose -p lawyer-finder -f docker/docker-compose.staging.yml build frontend web && \
  docker compose -p lawyer-finder -f docker/docker-compose.staging.yml up -d --no-deps frontend web"
```

---

Execute the following sequentially if not using the script. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/lawyer_finder
git push origin main
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && git pull origin main"
```

### 3. Sync Env File (SSH-encrypted)

Upload `.env.staging` to the server via `scp` (transferred over SSH encrypted channel).
**Always do this before rebuilding containers** — backend env vars are read at runtime.

```bash
scp d:/work-projects/lawyer_finder/backend/.env.staging getuai_dev@20.228.94.67:~/projects/lawyer_finder/backend/.env.staging
```

If the local file does not exist, skip this step.

### 4. Ensure Shared Docker Network

First deployment only — create the `shared-proxy` network if it doesn't exist:

```bash
ssh getuai_dev@20.228.94.67 "docker network create shared-proxy 2>/dev/null || true"
```

### 5. Rebuild & Restart Containers

**Full stack** (takes ~3–5 minutes):

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && docker compose -p lawyer-finder -f docker/docker-compose.staging.yml up -d --build"
```

**Frontend-only** (Next public site + nginx `web`; avoids backend recreate) — use the script or the manual block in the “Preferred” section above.

Monitor build progress by reading the terminal output. Key milestones:

- `lawyer-finder-backend` — pip install Python deps (~60s)
- `lawyer-finder-web` — npm ci + vite build for frontend (~30s) + admin (~30s)
- `exporting to image` — final export (~30s)
- `Container lawyer-finder-redis Started` — Redis ready
- `Container lawyer-finder-backend Started` — backend done
- `Container lawyer-finder-web Started` — web done

### 6. Verify Deployment

```bash
# Check all stack containers are running (redis, backend, frontend, web)
ssh getuai_dev@20.228.94.67 "docker ps --filter name=lawyer-finder"

# Check backend logs for successful startup
ssh getuai_dev@20.228.94.67 "docker logs lawyer-finder-backend --tail 20"

# Check web/nginx logs
ssh getuai_dev@20.228.94.67 "docker logs lawyer-finder-web --tail 10"
```

Expected healthy backend log output:

```
🔄 Running Alembic database migrations...
✅ Migrations applied successfully
🚀 Starting backend on port 8030 with 2 workers...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8030
```

### 7. Health Check (direct IP)

```bash
# Frontend (public SPA; follow locale redirect / → /en|/zh)
curl -sL -o /dev/null -w '%{http_code}' http://20.228.94.67:8086/

# Admin console
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8087

# API health (via frontend nginx proxy)
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8086/api/health
```

Expected: all return `200`.

### 8. Verify Co-located Services Unaffected

```bash
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8085
```

Expected: returns `200`.

## Container Architecture

```
┌──────────────────────────────────────────────────┐
│  Docker Compose (lawyer-finder)                  │
│                                                  │
│  ┌────────────────┐   ┌──────────────────────┐   │
│  │  redis:7-alpine │   │  lawyer-finder-web   │   │
│  │  (internal)     │   │  nginx on :80 :81    │   │
│  └────────┬───────┘   │  :8086 → frontend    │   │
│           │           │  :8087 → admin        │   │
│           │           │  /api → backend:8030  │   │
│  ┌────────┴───────┐   └──────────────────────┘   │
│  │  lawyer-finder- │                              │
│  │  backend        │                              │
│  │  FastAPI :8030  │                              │
│  │  Alembic        │                              │
│  └────────────────┘                              │
└──────────────────────────────────────────────────┘
```

## Gitignored Server Config Files

These files exist on the server but are NOT in git. Preserve them during any destructive operations:

- `backend/.env.staging` — staging database URL, API keys, JWT secret

All file transfers use `scp` which is SSH-encrypted in transit.

If a fresh clone is needed, back up first:

```bash
ssh getuai_dev@20.228.94.67 "mkdir -p /tmp/lawyer_finder_backup && \
  cp ~/projects/lawyer_finder/backend/.env.staging /tmp/lawyer_finder_backup/.env.staging.\$(d

[... truncated to 8KB ...]

```

## .claude/skills/omc-reference/SKILL.md
```markdown
---
name: omc-reference
description: OMC agent catalog, available tools, team pipeline routing, commit protocol, and skills registry. Auto-loads when delegating to agents, using OMC tools, orchestrating teams, making commits, or invoking skills.
user-invocable: false
---

# OMC Reference

Use this built-in reference when you need detailed OMC catalog information that does not need to live in every `CLAUDE.md` session.

## Agent Catalog

Prefix: `oh-my-claudecode:`. See `agents/*.md` for full prompts.

- `explore` (haiku) — fast codebase search and mapping
- `analyst` (opus) — requirements clarity and hidden constraints
- `planner` (opus) — sequencing and execution plans
- `architect` (opus) — system design, boundaries, and long-horizon tradeoffs
- `debugger` (sonnet) — root-cause analysis and failure diagnosis
- `executor` (sonnet) — implementation and refactoring
- `verifier` (sonnet) — completion evidence and validation
- `tracer` (sonnet) — trace gathering and evidence capture
- `security-reviewer` (sonnet) — trust boundaries and vulnerabilities
- `code-reviewer` (opus) — comprehensive code review
- `test-engineer` (sonnet) — testing strategy and regression coverage
- `designer` (sonnet) — UX and interaction design
- `writer` (haiku) — documentation and concise content work
- `qa-tester` (sonnet) — runtime/manual validation
- `scientist` (sonnet) — data analysis and statistical reasoning
- `document-specialist` (sonnet) — SDK/API/framework documentation lookup
- `git-master` (sonnet) — commit strategy and history hygiene
- `code-simplifier` (opus) — behavior-preserving simplification
- `critic` (opus) — plan/design challenge and review

## Model Routing

- `haiku` — quick lookups, lightweight inspection, narrow docs work
- `sonnet` — standard implementation, debugging, and review
- `opus` — architecture, deep analysis, consensus planning, and high-risk review

## Tools Reference

### External AI / orchestration
- `/team N:executor "task"`
- `omc team N:codex|gemini "..."`
- `omc ask <claude|codex|gemini>`
- `/ccg`

### OMC state
- `state_read`, `state_write`, `state_clear`, `state_list_active`, `state_get_status`

### Team runtime
- `TeamCreate`, `TeamDelete`, `SendMessage`, `TaskCreate`, `TaskList`, `TaskGet`, `TaskUpdate`

### Notepad
- `notepad_read`, `notepad_write_priority`, `notepad_write_working`, `notepad_write_manual`

### Project memory
- `project_memory_read`, `project_memory_write`, `project_memory_add_note`, `project_memory_add_directive`

### Code intelligence
- LSP: `lsp_hover`, `lsp_goto_definition`, `lsp_find_references`, `lsp_diagnostics`, and related helpers
- AST: `ast_grep_search`, `ast_grep_replace`
- Utility: `python_repl`

## Skills Registry

Invoke built-in workflows via `/oh-my-claudecode:<name>`.

### Workflow skills
- `autopilot` — full autonomous execution from idea to working code
- `ralph` — persistence loop until completion with verification
- `ultrawork` — high-throughput parallel execution
- `visual-verdict` — structured visual QA verdicts
- `team` — coordinated team orchestration
- `ccg` — Codex + Gemini + Claude synthesis lane
- `ultraqa` — QA cycle: test, verify, fix, repeat
- `omc-plan` — planning workflow and `/plan`-safe alias
- `ralplan` — consensus planning workflow
- `sciomc` — science/research workflow
- `external-context` — external docs/research workflow
- `deepinit` — hierarchical AGENTS.md generation
- `deep-interview` — Socratic ambiguity-gated requirements workflow
- `ai-slop-cleaner` — regression-safe cleanup workflow

### Utility skills
- `ask`, `cancel`, `note`, `learner`, `omc-setup`, `mcp-setup`, `hud`, `omc-doctor`, `trace`, `release`, `project-session-manager`, `skill`, `writer-memory`, `configure-notifications`

### Keyword triggers kept compact in CLAUDE.md
- `"autopilot"→autopilot`
- `"ralph"→ralph`
- `"ulw"→ultrawork`
- `"ccg"→ccg`
- `"ralplan"→ralplan`
- `"deep interview"→deep-interview`
- `"deslop" / "anti-slop"→ai-slop-cleaner`
- `"deep-analyze"→analysis mode`
- `"tdd"→TDD mode`
- `"deepsearch"→codebase search`
- `"ultrathink"→deep reasoning`
- `"cancelomc"→cancel`
- Team orchestration is explicit via `/team`.

## Team Pipeline

Stages: `team-plan` → `team-prd` → `team-exec` → `team-verify` → `team-fix` (loop).

- Use `team-fix` for bounded remediation loops.
- `team ralph` links the team pipeline with Ralph-style sequential verification.
- Prefer team mode when independent parallel lanes justify the coordination overhead.

## Commit Protocol

Use git trailers to preserve decision context in every commit message.

### Format
- Intent line first: why the change was made
- Optional body with context and rationale
- Structured trailers when applicable

### Common trailers
- `Constraint:` active constraint shaping the decision
- `Rejected:` alternative considered | reason for rejection
- `Directive:` forward-looking warning or instruction
- `Confidence:` `high` | `medium` | `low`
- `Scope-risk:` `narrow` | `moderate` | `broad`
- `Not-tested:` known verification gap

### Example
```text
feat(docs): reduce always-loaded OMC instruction footprint

Move reference-only orchestration content into a native Claude skill so
session-start guidance stays small while detailed OMC reference remains available.

Constraint: Preserve CLAUDE.md marker-based installation flow
Rejected: Sync all built-in skills in legacy install | broader behavior change than issue requires
Confidence: high
Scope-risk: narrow
Not-tested: End-to-end plugin marketplace install in a fresh Claude profile
```

```

## .cursor/skills/deploy-production/SKILL.md
```markdown
---
name: lawyer-finder-deploy-production
description: Deploy lawyer_finder to production (104.45.215.114). Use for "deploy to production", "publish to production", "deploy prod", etc. Prefer scripts/deploy-production.sh; supports full stack, frontend-only (no backend recreate), frontend restart-only, --no-cache, --skip-push, --yes.
---

# Lawyer Finder — Production Deployment

## Infrastructure

| Item              | Value                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Server IP         | `104.45.215.114`                                                      |
| SSH User          | `getuai_deploy`                                                       |
| SSH Key           | `~/.ssh/id_rsa` (generated for this server)                           |
| Domain (Frontend) | `lawyerfinder.ai` (Caddy auto-HTTPS)                                 |
| Domain (Admin)    | `admin.lawyerfinder.ai` (Caddy auto-HTTPS)                           |
| Caddy Ports       | `80` (HTTP→redirect), `443` (HTTPS) — only exposed ports             |
| Backend Port      | `8030` (internal, not exposed to host)                                |
| Frontend Port     | `3000` (internal, not exposed to host)                                |
| Nginx Ports       | `80/81` (internal, not exposed to host)                               |
| Redis             | Azure Managed Redis (`lawyer.westus.redis.azure.net:10000`, SSL)      |
| DB Host           | `lawyer-finder.postgres.database.azure.com:5432` (Azure PostgreSQL)   |
| Project Path      | `/home/getuai_deploy/projects/lawyer_finder`                          |
| Compose File      | `docker/docker-compose.production.yml`                                |
| Compose Name      | `lawyer-finder-prod` (via `-p lawyer-finder-prod`)                    |
| Git Remote        | `git@github-getu:Optiminds-Inc/lawyer_finder.git` (alias: `origin`)  |
| Git Branch        | `main`                                                                |
| VM Size           | `Standard_B2ms` (2 vCPU, 8GB RAM, 64GB Premium SSD)                  |
| Azure NSG         | `lawyer-finder-prod-nsg` in resource group `ADS`                      |

## Security Configuration

This production server has been hardened with:

- **SSH**: Key-only auth, password disabled, root login disabled, MaxAuthTries=3
- **UFW Firewall**: Only ports 22, 80, 443 open (double-layered with Azure NSG)
- **Azure NSG**: Only ports 22, 80, 443 allowed, all other inbound denied
- **fail2ban**: SSH brute-force protection (3 attempts → 2h ban)
- **Unattended Upgrades**: Automatic security patches
- **Kernel Hardening**: SYN cookies, ICMP filtering, source routing disabled
- **Docker**: Log rotation (10MB x 3 files), live-restore enabled
- **Caddy**: Auto TLS with Let's Encrypt, security headers (HSTS, X-Frame-Options, etc.)
- **Nginx**: Rate limiting (30r/s API, 50r/s general), exploit path blocking, server_tokens off
- **CORS**: Restricted to `lawyerfinder.ai` and `admin.lawyerfinder.ai` only

## Deployment Steps

**Preferred:** run from repo root (same workflow style as staging):

```bash
cd d:/work-projects/lawyer_finder
./scripts/deploy-production.sh                      # full stack
./scripts/deploy-production.sh --frontend-only      # Next + nginx only; backend container not recreated
./scripts/deploy-production.sh --restart-frontend   # no build; restart frontend + web only
./scripts/deploy-production.sh --no-cache           # full stack rebuild without Docker cache
./scripts/deploy-production.sh --skip-push          # server pull + redeploy only
./scripts/deploy-production.sh --yes                # non-interactive if working tree is dirty
```

See `./scripts/deploy-production.sh --help` for all flags.

### Why `--frontend-only` uses `build frontend web` + `up --no-deps`?

Same rationale as staging: `docker compose up -d --build frontend` still joins the **full** Compose bake/dependency graph and often **recreates `lawyer-finder-prod-backend`** even when backend layers are cache hits. The script:

1. Runs `docker compose build frontend web` — only those images rebuild (backend image is not built).
2. Runs `docker compose up -d --no-deps frontend web` — replace only those containers; **do not** reconcile dependent services.

`web` is nginx (admin SPA + proxy to Next.js). Rebuilding it with `frontend` matches staging’s `deploy-staging.sh` and avoids touching the API container.

Manual equivalent:

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && \
  docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml build frontend web && \
  docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml up -d --no-deps frontend web"
```

---

If not using the script, execute the following sequentially. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/lawyer_finder
git push origin main
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && git pull origin main"
```

### 3. Sync Env Files (SSH-encrypted)

Upload production env files via `scp` **before** rebuilding containers.

**Backend** (runtime secrets, DB, Redis, etc.):

```bash
scp d:/work-projects/lawyer_finder/backend/.env.production getuai_deploy@104.45.215.114:~/projects/lawyer_finder/backend/.env.production
```

**Frontend** (Next.js; `env_file` in compose):

```bash
scp d:/work-projects/lawyer_finder/frontend/.env.production getuai_deploy@104.45.215.114:~/projects/lawyer_finder/frontend/.env.production
```

If a local file does not exist, skip that upload.

### 4. Rebuild & Restart Containers

**Full stack** (takes ~3-5 minutes):

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml up -d --build"
```

**Frontend-only** — use `./scripts/deploy-production.sh --frontend-only` or the manual block above.

Monitor build progress by reading the terminal output. Key milestones:

- `lawyer-finder-prod-backend` — pip install Python deps (~60s)
- `lawyer-finder-prod-web` — npm ci + vite build for admin (~30s)
- `lawyer-finder-prod-frontend` — npm ci + Next.js build (~60s)
- `exporting to image` — final export (~30s)
- `Container lawyer-finder-prod-caddy Started` — Caddy ready (auto TLS)
- `Container lawyer-finder-prod-backend Started` — backend done
- `Container lawyer-finder-prod-web Started` — web done

### 5. Verify Deployment

```bash
# Check all 4 containers are running
ssh getuai_deploy@104.45.215.114 "docker ps --filter name=lawyer-finder-prod"

# Check backend logs for successful startup
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-backend --tail 20"

# Check nginx (web) logs
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-web --tail 10"

# Check Caddy logs for TLS certificate
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-caddy --tail 20"
```

Expected healthy backend log output:

```
🔄 Running Alembic database migrations...
✅ Migrations applied successfully
🚀 Starting backend on port 8030 with 4 workers...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8030
```

### 6. Health Check

```bash
# Frontend (HTTPS; follow locale redirect / → /en|/zh)
curl -sL -o /dev/null -w '%{http_code}' https://lawyerfinder.ai/

# Admin console (HTTPS; -L if your admin entry redirects)
curl -sL -o /dev/null -w '%{http_code}' https://admin.lawyerfinder.ai

# API health
curl -s https://lawyerfinder.ai/api/health

# TLS certificate verification
curl -vI https://lawyerfinder.ai 2>&1 | grep -E 'subject:|expire'
```

Expected: HTML endpoints return `200` after redirects, API returns JSON with `"healthy"`, TLS certificate issued by Let's Encrypt.

## Container Architecture

`

[... truncated to 8KB ...]

```

## .cursor/skills/deploy-staging/SKILL.md
```markdown
---
name: lawyer-finder-deploy
description: Deploy lawyer_finder to staging (20.228.94.67). Use for "deploy", "deploy to staging", "update staging", etc. Prefer scripts/deploy-staging.sh (full stack, --frontend-only, --restart-frontend, --no-cache, --skip-push, --yes). Production uses scripts/deploy-production.sh — see skill lawyer-finder-deploy-production.
---

# Lawyer Finder — Staging Deployment

## Infrastructure

| Item              | Value                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Server IP         | `20.228.94.67`                                                        |
| SSH User          | `getuai_dev`                                                          |
| Frontend Port     | `8086` (nginx → serves public SPA + proxies API to backend)          |
| Admin Port        | `8087` (nginx → serves admin SPA + proxies API to backend)           |
| Backend Port      | `8030` (internal, not exposed to host)                                |
| Redis             | Internal container (port 6379, not exposed to host)                   |
| Project Path      | `/home/getuai_dev/projects/lawyer_finder`                             |
| Compose File      | `docker/docker-compose.staging.yml`                                   |
| Compose Name      | `lawyer-finder` (via `-p lawyer-finder`)                              |
| DB Host           | `20.59.118.120:32476` (external PostgreSQL)                           |
| Git Remote        | `git@github-getu:Optiminds-Inc/lawyer_finder.git` (alias: `origin`)  |
| Git Branch        | `main`                                                                |
| Frontend URL      | `http://20.228.94.67:8086`                                            |
| Admin URL         | `http://20.228.94.67:8087`                                            |

## ⚠️ Co-located Services

This server also runs other projects. Do NOT touch:
- **lawyer_marketing**: Caddy on 80/443, app on 3456 → containers `docker-app-1` / `docker-caddy-1`
- **geo-seo-v2**: nginx on 8085, backend on 3457 → containers `geo-seo-v2-frontend-1` / `geo-seo-v2-backend-1`
- Ports 80, 443, 3456, 3457, 8085

## Deployment Steps

**Preferred:** run from repo root after committing and pushing (or rely on the script’s push step):

```bash
cd d:/work-projects/lawyer_finder
./scripts/deploy-staging.sh --frontend-only   # Next + nginx only; backend container not recreated
./scripts/deploy-staging.sh                 # full stack
./scripts/deploy-staging.sh --restart-frontend   # no build; restart frontend + web only
./scripts/deploy-staging.sh --yes           # non-interactive if working tree is dirty
```

Script flags: `--no-cache`, `--skip-push`, `--yes` / `-y`. See `scripts/deploy-staging.sh --help`.

### Why `--frontend-only` instead of `up -d --build frontend web`?

`docker compose up -d --build frontend web` still loads the **whole** Compose bake graph and, because of `depends_on`, often **recreates `lawyer-finder-backend`** even when backend layers are cache hits. The script uses:

1. `docker compose build frontend web` — only those Dockerfiles run.
2. `docker compose up -d --no-deps frontend web` — replace only those containers; **do not** reconcile dependent services.

Manual equivalent:

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && \
  docker compose -p lawyer-finder -f docker/docker-compose.staging.yml build frontend web && \
  docker compose -p lawyer-finder -f docker/docker-compose.staging.yml up -d --no-deps frontend web"
```

---

Execute the following sequentially if not using the script. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/lawyer_finder
git push origin main
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && git pull origin main"
```

### 3. Sync Env File (SSH-encrypted)

Upload `.env.staging` to the server via `scp` (transferred over SSH encrypted channel).
**Always do this before rebuilding containers** — backend env vars are read at runtime.

```bash
scp d:/work-projects/lawyer_finder/backend/.env.staging getuai_dev@20.228.94.67:~/projects/lawyer_finder/backend/.env.staging
```

If the local file does not exist, skip this step.

### 4. Ensure Shared Docker Network

First deployment only — create the `shared-proxy` network if it doesn't exist:

```bash
ssh getuai_dev@20.228.94.67 "docker network create shared-proxy 2>/dev/null || true"
```

### 5. Rebuild & Restart Containers

**Full stack** (takes ~3–5 minutes):

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && docker compose -p lawyer-finder -f docker/docker-compose.staging.yml up -d --build"
```

**Frontend-only** (Next public site + nginx `web`; avoids backend recreate) — use the script or the manual block in the “Preferred” section above.

Monitor build progress by reading the terminal output. Key milestones:

- `lawyer-finder-backend` — pip install Python deps (~60s)
- `lawyer-finder-web` — npm ci + vite build for frontend (~30s) + admin (~30s)
- `exporting to image` — final export (~30s)
- `Container lawyer-finder-redis Started` — Redis ready
- `Container lawyer-finder-backend Started` — backend done
- `Container lawyer-finder-web Started` — web done

### 6. Verify Deployment

```bash
# Check all stack containers are running (redis, backend, frontend, web)
ssh getuai_dev@20.228.94.67 "docker ps --filter name=lawyer-finder"

# Check backend logs for successful startup
ssh getuai_dev@20.228.94.67 "docker logs lawyer-finder-backend --tail 20"

# Check web/nginx logs
ssh getuai_dev@20.228.94.67 "docker logs lawyer-finder-web --tail 10"
```

Expected healthy backend log output:

```
🔄 Running Alembic database migrations...
✅ Migrations applied successfully
🚀 Starting backend on port 8030 with 2 workers...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8030
```

### 7. Health Check (direct IP)

```bash
# Frontend (public SPA; follow locale redirect / → /en|/zh)
curl -sL -o /dev/null -w '%{http_code}' http://20.228.94.67:8086/

# Admin console
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8087

# API health (via frontend nginx proxy)
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8086/api/health
```

Expected: all return `200`.

### 8. Verify Co-located Services Unaffected

```bash
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8085
```

Expected: returns `200`.

## Container Architecture

```
┌──────────────────────────────────────────────────┐
│  Docker Compose (lawyer-finder)                  │
│                                                  │
│  ┌────────────────┐   ┌──────────────────────┐   │
│  │  redis:7-alpine │   │  lawyer-finder-web   │   │
│  │  (internal)     │   │  nginx on :80 :81    │   │
│  └────────┬───────┘   │  :8086 → frontend    │   │
│           │           │  :8087 → admin        │   │
│           │           │  /api → backend:8030  │   │
│  ┌────────┴───────┐   └──────────────────────┘   │
│  │  lawyer-finder- │                              │
│  │  backend        │                              │
│  │  FastAPI :8030  │                              │
│  │  Alembic        │                              │
│  └────────────────┘                              │
└──────────────────────────────────────────────────┘
```

## Gitignored Server Config Files

These files exist on the server but are NOT in git. Preserve them during any destructive operations:

- `backend/.env.staging` — staging database URL, API keys, JWT secret

All file transfers use `scp` which is SSH-encrypted in transit.

If a fresh clone is needed, back up first:

```bash
ssh getuai_dev@20.228.94.67 "mkdir -p /tmp/lawyer_finder_backup && \
  cp ~/projects/lawyer_finder/backend/.env.staging /tmp/lawyer_finder_backup/.env.staging.\$(d

[... truncated to 8KB ...]

```

## .agents/skills/deploy-production/SKILL.md
```markdown
---
name: lawyer-finder-deploy-production
description: Deploy lawyer_finder to production (104.45.215.114). Use for "deploy to production", "publish to production", "deploy prod", etc. Prefer scripts/deploy-production.sh; supports full stack, frontend-only (no backend recreate), frontend restart-only, --no-cache, --skip-push, --yes.
---

# Lawyer Finder — Production Deployment

## Infrastructure

| Item              | Value                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Server IP         | `104.45.215.114`                                                      |
| SSH User          | `getuai_deploy`                                                       |
| SSH Key           | `~/.ssh/id_rsa` (generated for this server)                           |
| Domain (Frontend) | `lawyerfinder.ai` (Caddy auto-HTTPS)                                 |
| Domain (Admin)    | `admin.lawyerfinder.ai` (Caddy auto-HTTPS)                           |
| Caddy Ports       | `80` (HTTP→redirect), `443` (HTTPS) — only exposed ports             |
| Backend Port      | `8030` (internal, not exposed to host)                                |
| Frontend Port     | `3000` (internal, not exposed to host)                                |
| Nginx Ports       | `80/81` (internal, not exposed to host)                               |
| Redis             | Azure Managed Redis (`lawyer.westus.redis.azure.net:10000`, SSL)      |
| DB Host           | `lawyer-finder.postgres.database.azure.com:5432` (Azure PostgreSQL)   |
| Project Path      | `/home/getuai_deploy/projects/lawyer_finder`                          |
| Compose File      | `docker/docker-compose.production.yml`                                |
| Compose Name      | `lawyer-finder-prod` (via `-p lawyer-finder-prod`)                    |
| Git Remote        | `git@github-getu:Optiminds-Inc/lawyer_finder.git` (alias: `origin`)  |
| Git Branch        | `main`                                                                |
| VM Size           | `Standard_B2ms` (2 vCPU, 8GB RAM, 64GB Premium SSD)                  |
| Azure NSG         | `lawyer-finder-prod-nsg` in resource group `ADS`                      |

## Security Configuration

This production server has been hardened with:

- **SSH**: Key-only auth, password disabled, root login disabled, MaxAuthTries=3
- **UFW Firewall**: Only ports 22, 80, 443 open (double-layered with Azure NSG)
- **Azure NSG**: Only ports 22, 80, 443 allowed, all other inbound denied
- **fail2ban**: SSH brute-force protection (3 attempts → 2h ban)
- **Unattended Upgrades**: Automatic security patches
- **Kernel Hardening**: SYN cookies, ICMP filtering, source routing disabled
- **Docker**: Log rotation (10MB x 3 files), live-restore enabled
- **Caddy**: Auto TLS with Let's Encrypt, security headers (HSTS, X-Frame-Options, etc.)
- **Nginx**: Rate limiting (30r/s API, 50r/s general), exploit path blocking, server_tokens off
- **CORS**: Restricted to `lawyerfinder.ai` and `admin.lawyerfinder.ai` only

## Deployment Steps

**Preferred:** run from repo root (same workflow style as staging):

```bash
cd d:/work-projects/lawyer_finder
./scripts/deploy-production.sh                      # full stack
./scripts/deploy-production.sh --frontend-only      # Next + nginx only; backend container not recreated
./scripts/deploy-production.sh --restart-frontend   # no build; restart frontend + web only
./scripts/deploy-production.sh --no-cache           # full stack rebuild without Docker cache
./scripts/deploy-production.sh --skip-push          # server pull + redeploy only
./scripts/deploy-production.sh --yes                # non-interactive if working tree is dirty
```

See `./scripts/deploy-production.sh --help` for all flags.

### Why `--frontend-only` uses `build frontend web` + `up --no-deps`?

Same rationale as staging: `docker compose up -d --build frontend` still joins the **full** Compose bake/dependency graph and often **recreates `lawyer-finder-prod-backend`** even when backend layers are cache hits. The script:

1. Runs `docker compose build frontend web` — only those images rebuild (backend image is not built).
2. Runs `docker compose up -d --no-deps frontend web` — replace only those containers; **do not** reconcile dependent services.

`web` is nginx (admin SPA + proxy to Next.js). Rebuilding it with `frontend` matches staging’s `deploy-staging.sh` and avoids touching the API container.

Manual equivalent:

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && \
  docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml build frontend web && \
  docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml up -d --no-deps frontend web"
```

---

If not using the script, execute the following sequentially. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/lawyer_finder
git push origin main
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && git pull origin main"
```

### 3. Sync Env Files (SSH-encrypted)

Upload production env files via `scp` **before** rebuilding containers.

**Backend** (runtime secrets, DB, Redis, etc.):

```bash
scp d:/work-projects/lawyer_finder/backend/.env.production getuai_deploy@104.45.215.114:~/projects/lawyer_finder/backend/.env.production
```

**Frontend** (Next.js; `env_file` in compose):

```bash
scp d:/work-projects/lawyer_finder/frontend/.env.production getuai_deploy@104.45.215.114:~/projects/lawyer_finder/frontend/.env.production
```

If a local file does not exist, skip that upload.

### 4. Rebuild & Restart Containers

**Full stack** (takes ~3-5 minutes):

```bash
ssh getuai_deploy@104.45.215.114 "cd ~/projects/lawyer_finder && docker compose -p lawyer-finder-prod -f docker/docker-compose.production.yml up -d --build"
```

**Frontend-only** — use `./scripts/deploy-production.sh --frontend-only` or the manual block above.

Monitor build progress by reading the terminal output. Key milestones:

- `lawyer-finder-prod-backend` — pip install Python deps (~60s)
- `lawyer-finder-prod-web` — npm ci + vite build for admin (~30s)
- `lawyer-finder-prod-frontend` — npm ci + Next.js build (~60s)
- `exporting to image` — final export (~30s)
- `Container lawyer-finder-prod-caddy Started` — Caddy ready (auto TLS)
- `Container lawyer-finder-prod-backend Started` — backend done
- `Container lawyer-finder-prod-web Started` — web done

### 5. Verify Deployment

```bash
# Check all 4 containers are running
ssh getuai_deploy@104.45.215.114 "docker ps --filter name=lawyer-finder-prod"

# Check backend logs for successful startup
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-backend --tail 20"

# Check nginx (web) logs
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-web --tail 10"

# Check Caddy logs for TLS certificate
ssh getuai_deploy@104.45.215.114 "docker logs lawyer-finder-prod-caddy --tail 20"
```

Expected healthy backend log output:

```
🔄 Running Alembic database migrations...
✅ Migrations applied successfully
🚀 Starting backend on port 8030 with 4 workers...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8030
```

### 6. Health Check

```bash
# Frontend (HTTPS; follow locale redirect / → /en|/zh)
curl -sL -o /dev/null -w '%{http_code}' https://lawyerfinder.ai/

# Admin console (HTTPS; -L if your admin entry redirects)
curl -sL -o /dev/null -w '%{http_code}' https://admin.lawyerfinder.ai

# API health
curl -s https://lawyerfinder.ai/api/health

# TLS certificate verification
curl -vI https://lawyerfinder.ai 2>&1 | grep -E 'subject:|expire'
```

Expected: HTML endpoints return `200` after redirects, API returns JSON with `"healthy"`, TLS certificate issued by Let's Encrypt.

## Container Architecture

`

[... truncated to 8KB ...]

```

## .agents/skills/deploy-staging/SKILL.md
```markdown
---
name: lawyer-finder-deploy
description: Deploy lawyer_finder to staging (20.228.94.67). Use for "deploy", "deploy to staging", "update staging", etc. Prefer scripts/deploy-staging.sh (full stack, --frontend-only, --restart-frontend, --no-cache, --skip-push, --yes). Production uses scripts/deploy-production.sh — see skill lawyer-finder-deploy-production.
---

# Lawyer Finder — Staging Deployment

## Infrastructure

| Item              | Value                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Server IP         | `20.228.94.67`                                                        |
| SSH User          | `getuai_dev`                                                          |
| Frontend Port     | `8086` (nginx → serves public SPA + proxies API to backend)          |
| Admin Port        | `8087` (nginx → serves admin SPA + proxies API to backend)           |
| Backend Port      | `8030` (internal, not exposed to host)                                |
| Redis             | Internal container (port 6379, not exposed to host)                   |
| Project Path      | `/home/getuai_dev/projects/lawyer_finder`                             |
| Compose File      | `docker/docker-compose.staging.yml`                                   |
| Compose Name      | `lawyer-finder` (via `-p lawyer-finder`)                              |
| DB Host           | `20.59.118.120:32476` (external PostgreSQL)                           |
| Git Remote        | `git@github-getu:Optiminds-Inc/lawyer_finder.git` (alias: `origin`)  |
| Git Branch        | `main`                                                                |
| Frontend URL      | `http://20.228.94.67:8086`                                            |
| Admin URL         | `http://20.228.94.67:8087`                                            |

## ⚠️ Co-located Services

This server also runs other projects. Do NOT touch:
- **lawyer_marketing**: Caddy on 80/443, app on 3456 → containers `docker-app-1` / `docker-caddy-1`
- **geo-seo-v2**: nginx on 8085, backend on 3457 → containers `geo-seo-v2-frontend-1` / `geo-seo-v2-backend-1`
- Ports 80, 443, 3456, 3457, 8085

## Deployment Steps

**Preferred:** run from repo root after committing and pushing (or rely on the script’s push step):

```bash
cd d:/work-projects/lawyer_finder
./scripts/deploy-staging.sh --frontend-only   # Next + nginx only; backend container not recreated
./scripts/deploy-staging.sh                 # full stack
./scripts/deploy-staging.sh --restart-frontend   # no build; restart frontend + web only
./scripts/deploy-staging.sh --yes           # non-interactive if working tree is dirty
```

Script flags: `--no-cache`, `--skip-push`, `--yes` / `-y`. See `scripts/deploy-staging.sh --help`.

### Why `--frontend-only` instead of `up -d --build frontend web`?

`docker compose up -d --build frontend web` still loads the **whole** Compose bake graph and, because of `depends_on`, often **recreates `lawyer-finder-backend`** even when backend layers are cache hits. The script uses:

1. `docker compose build frontend web` — only those Dockerfiles run.
2. `docker compose up -d --no-deps frontend web` — replace only those containers; **do not** reconcile dependent services.

Manual equivalent:

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && \
  docker compose -p lawyer-finder -f docker/docker-compose.staging.yml build frontend web && \
  docker compose -p lawyer-finder -f docker/docker-compose.staging.yml up -d --no-deps frontend web"
```

---

Execute the following sequentially if not using the script. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/lawyer_finder
git push origin main
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && git pull origin main"
```

### 3. Sync Env File (SSH-encrypted)

Upload `.env.staging` to the server via `scp` (transferred over SSH encrypted channel).
**Always do this before rebuilding containers** — backend env vars are read at runtime.

```bash
scp d:/work-projects/lawyer_finder/backend/.env.staging getuai_dev@20.228.94.67:~/projects/lawyer_finder/backend/.env.staging
```

If the local file does not exist, skip this step.

### 4. Ensure Shared Docker Network

First deployment only — create the `shared-proxy` network if it doesn't exist:

```bash
ssh getuai_dev@20.228.94.67 "docker network create shared-proxy 2>/dev/null || true"
```

### 5. Rebuild & Restart Containers

**Full stack** (takes ~3–5 minutes):

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/lawyer_finder && docker compose -p lawyer-finder -f docker/docker-compose.staging.yml up -d --build"
```

**Frontend-only** (Next public site + nginx `web`; avoids backend recreate) — use the script or the manual block in the “Preferred” section above.

Monitor build progress by reading the terminal output. Key milestones:

- `lawyer-finder-backend` — pip install Python deps (~60s)
- `lawyer-finder-web` — npm ci + vite build for frontend (~30s) + admin (~30s)
- `exporting to image` — final export (~30s)
- `Container lawyer-finder-redis Started` — Redis ready
- `Container lawyer-finder-backend Started` — backend done
- `Container lawyer-finder-web Started` — web done

### 6. Verify Deployment

```bash
# Check all stack containers are running (redis, backend, frontend, web)
ssh getuai_dev@20.228.94.67 "docker ps --filter name=lawyer-finder"

# Check backend logs for successful startup
ssh getuai_dev@20.228.94.67 "docker logs lawyer-finder-backend --tail 20"

# Check web/nginx logs
ssh getuai_dev@20.228.94.67 "docker logs lawyer-finder-web --tail 10"
```

Expected healthy backend log output:

```
🔄 Running Alembic database migrations...
✅ Migrations applied successfully
🚀 Starting backend on port 8030 with 2 workers...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8030
```

### 7. Health Check (direct IP)

```bash
# Frontend (public SPA; follow locale redirect / → /en|/zh)
curl -sL -o /dev/null -w '%{http_code}' http://20.228.94.67:8086/

# Admin console
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8087

# API health (via frontend nginx proxy)
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8086/api/health
```

Expected: all return `200`.

### 8. Verify Co-located Services Unaffected

```bash
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8085
```

Expected: returns `200`.

## Container Architecture

```
┌──────────────────────────────────────────────────┐
│  Docker Compose (lawyer-finder)                  │
│                                                  │
│  ┌────────────────┐   ┌──────────────────────┐   │
│  │  redis:7-alpine │   │  lawyer-finder-web   │   │
│  │  (internal)     │   │  nginx on :80 :81    │   │
│  └────────┬───────┘   │  :8086 → frontend    │   │
│           │           │  :8087 → admin        │   │
│           │           │  /api → backend:8030  │   │
│  ┌────────┴───────┐   └──────────────────────┘   │
│  │  lawyer-finder- │                              │
│  │  backend        │                              │
│  │  FastAPI :8030  │                              │
│  │  Alembic        │                              │
│  └────────────────┘                              │
└──────────────────────────────────────────────────┘
```

## Gitignored Server Config Files

These files exist on the server but are NOT in git. Preserve them during any destructive operations:

- `backend/.env.staging` — staging database URL, API keys, JWT secret

All file transfers use `scp` which is SSH-encrypted in transit.

If a fresh clone is needed, back up first:

```bash
ssh getuai_dev@20.228.94.67 "mkdir -p /tmp/lawyer_finder_backup && \
  cp ~/projects/lawyer_finder/backend/.env.staging /tmp/lawyer_finder_backup/.env.staging.\$(d

[... truncated to 8KB ...]

```

## .agents/skills/omc-reference/SKILL.md
```markdown
---
name: omc-reference
description: OMC agent catalog, available tools, team pipeline routing, commit protocol, and skills registry. Auto-loads when delegating to agents, using OMC tools, orchestrating teams, making commits, or invoking skills.
user-invocable: false
---

# OMC Reference

Use this built-in reference when you need detailed OMC catalog information that does not need to live in every `AGENTS.md` session.

## Agent Catalog

Prefix: `oh-my-Codex:`. See `agents/*.md` for full prompts.

- `explore` (haiku) — fast codebase search and mapping
- `analyst` (opus) — requirements clarity and hidden constraints
- `planner` (opus) — sequencing and execution plans
- `architect` (opus) — system design, boundaries, and long-horizon tradeoffs
- `debugger` (sonnet) — root-cause analysis and failure diagnosis
- `executor` (sonnet) — implementation and refactoring
- `verifier` (sonnet) — completion evidence and validation
- `tracer` (sonnet) — trace gathering and evidence capture
- `security-reviewer` (sonnet) — trust boundaries and vulnerabilities
- `code-reviewer` (opus) — comprehensive code review
- `test-engineer` (sonnet) — testing strategy and regression coverage
- `designer` (sonnet) — UX and interaction design
- `writer` (haiku) — documentation and concise content work
- `qa-tester` (sonnet) — runtime/manual validation
- `scientist` (sonnet) — data analysis and statistical reasoning
- `document-specialist` (sonnet) — SDK/API/framework documentation lookup
- `git-master` (sonnet) — commit strategy and history hygiene
- `code-simplifier` (opus) — behavior-preserving simplification
- `critic` (opus) — plan/design challenge and review

## Model Routing

- `haiku` — quick lookups, lightweight inspection, narrow docs work
- `sonnet` — standard implementation, debugging, and review
- `opus` — architecture, deep analysis, consensus planning, and high-risk review

## Tools Reference

### External AI / orchestration
- `/team N:executor "task"`
- `omc team N:codex|gemini "..."`
- `omc ask <Codex|codex|gemini>`
- `/ccg`

### OMC state
- `state_read`, `state_write`, `state_clear`, `state_list_active`, `state_get_status`

### Team runtime
- `TeamCreate`, `TeamDelete`, `SendMessage`, `TaskCreate`, `TaskList`, `TaskGet`, `TaskUpdate`

### Notepad
- `notepad_read`, `notepad_write_priority`, `notepad_write_working`, `notepad_write_manual`

### Project memory
- `project_memory_read`, `project_memory_write`, `project_memory_add_note`, `project_memory_add_directive`

### Code intelligence
- LSP: `lsp_hover`, `lsp_goto_definition`, `lsp_find_references`, `lsp_diagnostics`, and related helpers
- AST: `ast_grep_search`, `ast_grep_replace`
- Utility: `python_repl`

## Skills Registry

Invoke built-in workflows via `/oh-my-Codex:<name>`.

### Workflow skills
- `autopilot` — full autonomous execution from idea to working code
- `ralph` — persistence loop until completion with verification
- `ultrawork` — high-throughput parallel execution
- `visual-verdict` — structured visual QA verdicts
- `team` — coordinated team orchestration
- `ccg` — Codex + Gemini + Codex synthesis lane
- `ultraqa` — QA cycle: test, verify, fix, repeat
- `omc-plan` — planning workflow and `/plan`-safe alias
- `ralplan` — consensus planning workflow
- `sciomc` — science/research workflow
- `external-context` — external docs/research workflow
- `deepinit` — hierarchical AGENTS.md generation
- `deep-interview` — Socratic ambiguity-gated requirements workflow
- `ai-slop-cleaner` — regression-safe cleanup workflow

### Utility skills
- `ask`, `cancel`, `note`, `learner`, `omc-setup`, `mcp-setup`, `hud`, `omc-doctor`, `trace`, `release`, `project-session-manager`, `skill`, `writer-memory`, `configure-notifications`

### Keyword triggers kept compact in AGENTS.md
- `"autopilot"→autopilot`
- `"ralph"→ralph`
- `"ulw"→ultrawork`
- `"ccg"→ccg`
- `"ralplan"→ralplan`
- `"deep interview"→deep-interview`
- `"deslop" / "anti-slop"→ai-slop-cleaner`
- `"deep-analyze"→analysis mode`
- `"tdd"→TDD mode`
- `"deepsearch"→codebase search`
- `"ultrathink"→deep reasoning`
- `"cancelomc"→cancel`
- Team orchestration is explicit via `/team`.

## Team Pipeline

Stages: `team-plan` → `team-prd` → `team-exec` → `team-verify` → `team-fix` (loop).

- Use `team-fix` for bounded remediation loops.
- `team ralph` links the team pipeline with Ralph-style sequential verification.
- Prefer team mode when independent parallel lanes justify the coordination overhead.

## Commit Protocol

Use git trailers to preserve decision context in every commit message.

### Format
- Intent line first: why the change was made
- Optional body with context and rationale
- Structured trailers when applicable

### Common trailers
- `Constraint:` active constraint shaping the decision
- `Rejected:` alternative considered | reason for rejection
- `Directive:` forward-looking warning or instruction
- `Confidence:` `high` | `medium` | `low`
- `Scope-risk:` `narrow` | `moderate` | `broad`
- `Not-tested:` known verification gap

### Example
```text
feat(docs): reduce always-loaded OMC instruction footprint

Move reference-only orchestration content into a native Codex skill so
session-start guidance stays small while detailed OMC reference remains available.

Constraint: Preserve AGENTS.md marker-based installation flow
Rejected: Sync all built-in skills in legacy install | broader behavior change than issue requires
Confidence: high
Scope-risk: narrow
Not-tested: End-to-end plugin marketplace install in a fresh Codex profile
```

```


# Repo: openfang

## README.md
```markdown
<p align="center">
  <img src="public/assets/openfang-logo.png" width="160" alt="OpenFang Logo" />
</p>

<h1 align="center">OpenFang</h1>
<h3 align="center">The Agent Operating System</h3>

<p align="center">
  Open-source Agent OS built in Rust. 137K LOC. 14 crates. 1,767+ tests. Zero clippy warnings.<br/>
  <strong>One binary. Battle-tested. Agents that actually work for you.</strong>
</p>

<p align="center">
  <a href="https://openfang.sh/docs">Documentation</a> &bull;
  <a href="https://openfang.sh/docs/getting-started">Quick Start</a> &bull;
  <a href="https://x.com/openfangg">Twitter / X</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/language-Rust-orange?style=flat-square" alt="Rust" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT" />
  <img src="https://img.shields.io/badge/version-0.1.0-green?style=flat-square" alt="v0.1.0" />
  <img src="https://img.shields.io/badge/tests-1,767%2B%20passing-brightgreen?style=flat-square" alt="Tests" />
  <img src="https://img.shields.io/badge/clippy-0%20warnings-brightgreen?style=flat-square" alt="Clippy" />
  <a href="https://www.buymeacoffee.com/openfang" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee" /></a>
</p>

---

> **v0.1.0 — First Release (February 2026)**
>
> OpenFang is feature-complete but this is the first public release. You may encounter instability, rough edges, or breaking changes between minor versions. We ship fast and fix fast. Pin to a specific commit for production use until v1.0. [Report issues here.](https://github.com/RightNow-AI/openfang/issues)

---

## What is OpenFang?

OpenFang is an **open-source Agent Operating System** — not a chatbot framework, not a Python wrapper around an LLM, not a "multi-agent orchestrator." It is a full operating system for autonomous agents, built from scratch in Rust.

Traditional agent frameworks wait for you to type something. OpenFang runs **autonomous agents that work for you** — on schedules, 24/7, building knowledge graphs, monitoring targets, generating leads, managing your social media, and reporting results to your dashboard.

The entire system compiles to a **single ~32MB binary**. One install, one command, your agents are live.

```bash
curl -fsSL https://openfang.sh/install | sh
openfang init
openfang start
# Dashboard live at http://localhost:4200
```

<details>
<summary><strong>Windows</strong></summary>

```powershell
irm https://openfang.sh/install.ps1 | iex
openfang init
openfang start
```

</details>

---

## Hands: Agents That Actually Do Things

<p align="center"><em>"Traditional agents wait for you to type. Hands work <strong>for</strong> you."</em></p>

**Hands** are OpenFang's core innovation — pre-built autonomous capability packages that run independently, on schedules, without you having to prompt them. This is not a chatbot. This is an agent that wakes up at 6 AM, researches your competitors, builds a knowledge graph, scores the findings, and delivers a report to your Telegram before you've had coffee.

Each Hand bundles:
- **HAND.toml** — Manifest declaring tools, settings, requirements, and dashboard metrics
- **System Prompt** — Multi-phase operational playbook (not a one-liner — these are 500+ word expert procedures)
- **SKILL.md** — Domain expertise reference injected into context at runtime
- **Guardrails** — Approval gates for sensitive actions (e.g. Browser Hand requires approval before any purchase)

All compiled into the binary. No downloading, no pip install, no Docker pull.

### The 7 Bundled Hands

| Hand | What It Actually Does |
|------|----------------------|
| **Clip** | Takes a YouTube URL, downloads it, identifies the best moments, cuts them into vertical shorts with captions and thumbnails, optionally adds AI voice-over, and publishes to Telegram and WhatsApp. 8-phase pipeline. FFmpeg + yt-dlp + 5 STT backends. |
| **Lead** | Runs daily. Discovers prospects matching your ICP, enriches them with web research, scores 0-100, deduplicates against your existing database, and delivers qualified leads in CSV/JSON/Markdown. Builds ICP profiles over time. |
| **Collector** | OSINT-grade intelligence. You give it a target (company, person, topic). It monitors continuously — change detection, sentiment tracking, knowledge graph construction, and critical alerts when something important shifts. |
| **Predictor** | Superforecasting engine. Collects signals from multiple sources, builds calibrated reasoning chains, makes predictions with confidence intervals, and tracks its own accuracy using Brier scores. Has a contrarian mode that deliberately argues against consensus. |
| **Researcher** | Deep autonomous researcher. Cross-references multiple sources, evaluates credibility using CRAAP criteria (Currency, Relevance, Authority, Accuracy, Purpose), generates cited reports with APA formatting, supports multiple languages. |
| **Twitter** | Autonomous Twitter/X account manager. Creates content in 7 rotating formats, schedules posts for optimal engagement, responds to mentions, tracks performance metrics. Has an approval queue — nothing posts without your OK. |
| **Browser** | Web automation agent. Navigates sites, fills forms, clicks buttons, handles multi-step workflows. Uses Playwright bridge with session persistence. **Mandatory purchase approval gate** — it will never spend your money without explicit confirmation. |

```bash
# Activate the Researcher Hand — it starts working immediately
openfang hand activate researcher

# Check its progress anytime
openfang hand status researcher

# Activate lead generation on a daily schedule
openfang hand activate lead

# Pause without losing state
openfang hand pause lead

# See all available Hands
openfang hand list
```

**Build your own.** Define a `HAND.toml` with tools, settings, and a system prompt. Publish to FangHub.

---

## OpenFang vs The Landscape

<p align="center">
  <img src="public/assets/openfang-vs-claws.png" width="600" alt="OpenFang vs OpenClaw vs ZeroClaw" />
</p>

### Benchmarks: Measured, Not Marketed

All data from official documentation and public repositories — February 2026.

#### Cold Start Time (lower is better)

```
ZeroClaw   ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   10 ms
OpenFang   ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  180 ms    ★
LangGraph  █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  2.5 sec
CrewAI     ████████████████████░░░░░░░░░░░░░░░░░░░░░░  3.0 sec
AutoGen    ██████████████████████████░░░░░░░░░░░░░░░░░  4.0 sec
OpenClaw   █████████████████████████████████████████░░  5.98 sec
```

#### Idle Memory Usage (lower is better)

```
ZeroClaw   █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    5 MB
OpenFang   ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   40 MB    ★
LangGraph  ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  180 MB
CrewAI     ████████████████████░░░░░░░░░░░░░░░░░░░░░░░  200 MB
AutoGen    █████████████████████████░░░░░░░░░░░░░░░░░░  250 MB
OpenClaw   ████████████████████████████████████████░░░░  394 MB
```

#### Install Size (lower is better)

```
ZeroClaw   █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  8.8 MB
OpenFang   ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   32 MB    ★
CrewAI     ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  100 MB
LangGraph  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  150 MB
AutoGen    ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░  200 MB
OpenClaw   ████████████████████████████████████████░░░░  500 MB
```

#### Security Systems (higher is better)

```
OpenFang   ████████████████████████████████████████████   16      ★
ZeroClaw   ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░    6
OpenClaw   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    3
AutoGen    █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    2
LangGraph  █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    2
CrewAI     ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    1
```

#### Channel Adapters (higher is better)

```
OpenFang   ████████████████████████████████████████████   40      ★
ZeroClaw   ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   15
OpenClaw   █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   13
CrewAI     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    0
AutoGen    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    0
LangGraph  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    0
```

#### LLM Providers (higher is better)

```
ZeroClaw   ████████████████████████████████████████████   28
OpenFang   ██████████████████████████████████████████░░   27      ★
LangGraph  ██████████████████████░░░░░░░░░░░░░░░░░░░░░   15
CrewAI     ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   10
OpenClaw   ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   10
AutoGen    ███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    8
```

### Feature-by-Feature Comparison

| Feature | OpenFang | OpenClaw | ZeroClaw | CrewAI | AutoGen | LangGraph |
|---------|----------|----------|----------|--------|---------|-----------|
| **Language** | **Rust** | TypeScript | **Rust** | Python | Python | Python |
| **Autonomous Hands** | **7 built-in** | None | None | None | None | None |
| **Security Layers** | **16 discrete** | 3 basic | 6 layers | 1 basic | Docker | AES enc. |
| **Agent Sandbox** | **WASM dual-metered** | None | Allowlists | None | Docker | None |
| **Channel Adapters** | **40** | 13 | 15 | 0 | 0 | 0 |
| **Built-in Tools** | **53 + MCP + A2A** | 50+ | 12 | Plugins | MCP | LC tools |
| **Memory** | **SQLite + vector** | File-based | SQLite FTS5 | 4-layer | External | Checkpoints |
| **Desktop App** | **Tauri 2.0** | None | None | None | Studio | None |
| **Audit Trail** | **Merkle hash-chain** | Logs | Logs | Tracing | Logs | Checkpoints |
| **Cold Start** | **<200ms** | ~6s | ~10ms | ~3s | ~4s | ~2.5s |
| **Install Size** | **~32 MB** | ~500 MB | ~8.8 MB | ~100 MB | ~200 MB | ~150 MB |
| **License** | MIT | MIT | MIT | MIT | Apache 2.0 | MIT |

---

## 16 Security Systems — Defense in Depth

OpenFang doesn't bolt security on after the fact. Every layer is independently testable and operates without a single point of failure.

| # | System | What It Does |
|---|--------|-------------|
| 1 | **WASM Dual-Metered Sandbox** | Tool code runs in WebAssembly with fuel metering + epoch interruption. A watchdog thread kills runaway code. |
| 2 | **Merkle Hash-Chain Audit Trail** | Every action is cryptographically linked to the previous one. Tamper with one entry and the entire chain breaks. |
| 3 | **Information Flow Taint Tracking** | Labels propagate through execution — secrets are tracked from source to sink. |
| 4 | **Ed25519 Signed Agent Manifests** | Every agent identity and capability set is cryptographically signed. |
| 5 | **SSRF Protection** | Blocks private IPs, cloud metadata endpoints, and DNS rebinding attacks. |
| 6 | **Secret Zeroization** | `Zeroizing<String>` auto-wipes API keys from memory the instant they're no longer needed. |
| 7 | **OFP Mutual Authentication** | HMAC-SHA256 nonce-based, constant-time verification for P2P networking. |
| 8 | **Capability Gates** | Role-based access control — agents declare required tools, the kernel enforces it. |
| 9 | **Security Headers** | CSP, X-Frame-Options, HSTS, X-Content-Type-Options on every response. |
| 10 | **Health Endpoint Redaction** | Public health check returns minimal info. Full diagnostics require authentication. |
| 11 | **Subprocess Sandbox** | `env_clear()` + selective variable passthrough. Process tree isolation with cross-platform kill. |
| 12 | **Prompt Injection Scanner** | Detects override attempts, data exfiltration patterns, and shell reference injection in skills. |
| 13 | **Loop Guard** | SHA256-based tool call loop detection with circuit breaker. Handles ping-pong patterns. |
| 14 | **Session Repair** | 7-phase message history validation and automatic recovery from corruption. |
| 15 | **Path Traversal Prevention** | Canonicalization with symlink escape prevention. `../` doesn't work here. |
| 16 | **GCRA Rate Limiter** | Cost-aware token bucket rate limiting with per-IP tracking and stale cleanup. |

---

## Architecture

14 Rust crates. 137,728 lines of code. Modular kernel design.

```
openfang-kernel      Orchestration, workflows, metering, RBAC, scheduler, budget tracking
openfang-runtime     Agent loop, 3 LLM drivers, 53 tools, WASM sandbox, MCP, A2A
openfang-api         140+ REST/WS/SSE endpoints, OpenAI-compatible API, dashboard
openfang-channels    40 messaging adapters with rate limiting, DM/group policies
openfang-memory      SQLite persistence, vector embeddings, canonical sessions, compaction
openfang-types       Core types, taint tracking, Ed25519 manifest signing, model catalog
openfang-skills      60 bundled skills, SKILL.md parser, FangHub marketplace
openfang-hands       7 autonomous Hands, HAND.toml parser, lifecycle management
openfang-extensions  25 MCP templates, AES-256-GCM credential vault, OAuth2 PKCE
openfang-wire        OFP P2P protocol with HMAC-SHA256 mutual authentication
openfang-cli         CLI with daemon management, TUI dashboard, MCP server mode
openfang-desktop     Tauri 2.0 native app (system tray, notifications, global shortcuts)
openfang-migrate     OpenClaw, LangChain, AutoGPT migration engine
xtask                Build automation
```

---

## 40 Channel Adapters

Connect your agents to every platform your users are on.

**Core:** Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email (IMAP/SMTP)
**Enterprise:** Microsoft Teams, Mattermost, Google Chat, Webex, Feishu/Lark, Zulip
**Social:** LINE, Viber, Facebook Messenger, Mastodon, Bluesky, Reddit, LinkedIn, Twitch
**Community:** IRC, XMPP, Guilded, Revolt, Keybase, Discourse, Gitter
**Privacy:** Threema, Nostr, Mumble, Nextcloud Talk, Rocket.Chat, Ntfy, Gotify
**Workplace:** Pumble, Flock, Twist, DingTalk, Zalo, Webhooks

Each adapter supports per-channel model overrides, DM/group policies, rate limiting, and output formatting.

---

## 27 LLM Providers — 123+ Models

3 native drivers (Anthropic, Gemini, OpenAI-compatible) route to 27 providers:

Anthropic, Gemini, OpenAI, Groq, DeepSeek, OpenRouter, Together, Mistral, Fireworks, Cohere, Perplexity, xAI, AI21, Cerebras, SambaNova, HuggingFace, Replicate, Ollama, vLLM, LM Studio, Qwen, MiniMax, Zhipu, Moonshot, Qianfan, Bedrock, and more.

Intelligent routing with task complexity scoring, automatic fallback, cost tracking, and per-model pricing.

---

## Migrate from OpenClaw

Already running OpenClaw? One command:

```bash
# Migrate everything — agents, memory, skills, configs
openfang migrate --from openclaw

# Migrate from a specific path
openfang migrate --from openclaw --path ~/.openclaw

# Dry run first to see what would change
openfang migrate --from openclaw --dry-run
```

The migration engine imports your agents, conversation history, skills, and configuration. OpenFang reads SKILL.md natively and is compatible with the ClawHub marketplace.

---

## OpenAI-Compatible API

Drop-in replacement. Point your existing tools at OpenFang:

```bash
curl -X POST localhost:4200/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "researcher",
    "messages": [{"role": "user", "content": "Analyze Q4 market trends"}],
    "stream": true
  }'
```

140+ REST/WS/SSE endpoints covering agents, memory, workflows, channels, models, skills, A2A, Hands, and more.

---

## Quick Start

```bash
# 1. Install (macOS/Linux)
curl -fsSL https://openfang.sh/install | sh

# 2. Initialize — walks you through provider setup
openfang init

# 3. Start the daemon
openfang start

# 4. Dashboard is live at http://localhost:4200

# 5. Activate a Hand — it starts working for you
openfang hand activate researcher

# 6. Chat with an agent
openfang chat researcher
> "What are the emerging trends in AI agent frameworks?"

# 7. Spawn a pre-built agent
openfang agent spawn coder
```

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
irm https://openfang.sh/install.ps1 | iex
openfang init
openfang start
```

</details>

---

## Development

```bash
# Build the workspace
cargo build --workspace --lib

# Run all tests (1,767+)
cargo test --workspace

# Lint (must be 0 warnings)
cargo clippy --workspace --all-targets -- -D warnings

# Format
cargo fmt --all -- --check
```

---

## Stability Notice

OpenFang v0.1.0 is the first public release. The architecture is solid, the test suite is comprehensive, and the security model is comprehensive. That said:

- **Breaking changes** may occur between minor versions until v1.0
- **Some Hands** are more mature than others (Browser and Researcher are the most battle-tested)
- **Edge cases** exist — if you find one, [open an issue](https://github.com/RightNow-AI/openfang/issues)
- **Pin to a specific commit** for production deployments until v1.0

We ship fast and fix fast. The goal is a rock-solid v1.0 by mid-2026.

---

## License

MIT — use it however you want.

---

## Links

- [Website & Documentation](https://openfang.sh)
- [Quick Start Guide](https://openfang.sh/docs/getting-started)
- [GitHub](https://github.com/RightNow-AI/openfang)
- [Discord](https://discord.gg/sSJqgNnq6X)
- [Twitter / X](https://x.com/openfangg)

---

## Built by RightNow

<p align="center">
  <a href="https://www.rightnowai.co/">
    <img src="public/assets/rightnow-logo.webp" width="60" alt="RightNow Logo" />
  </a>
</p>

<p align="center">
  OpenFang is built and maintained by <a href="https://x.com/Akashi203"><strong>Jaber</strong></a>, Founder of <a href="https://www.rightnowai.co/"><strong>RightNow</strong></a>.
</p>

<p align="center">
  <a href="https://www.rightnowai.co/">Website</a> &bull;
  <a href="https://x.com/Akashi203">Twitter / X</a> &bull;
  <a href="https://www.buymeacoffee.com/openfang" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</p>

---

<p align="center">
  <strong>Built with Rust. Secured with 16 layers. Agents that actually work for you.</strong>
</p>

```

## CLAUDE.md
```markdown
# OpenFang — Agent Instructions

## Project Overview
OpenFang is an open-source Agent Operating System written in Rust (14 crates).
- Config: `~/.openfang/config.toml`
- Default API: `http://127.0.0.1:4200`
- CLI binary: `target/release/openfang.exe` (or `target/debug/openfang.exe`)

## Build & Verify Workflow
After every feature implementation, run ALL THREE checks:
```bash
cargo build --workspace --lib          # Must compile (use --lib if exe is locked)
cargo test --workspace                 # All tests must pass (currently 1744+)
cargo clippy --workspace --all-targets -- -D warnings  # Zero warnings
```

## MANDATORY: Live Integration Testing
**After implementing any new endpoint, feature, or wiring change, you MUST run live integration tests.** Unit tests alone are not enough — they can pass while the feature is actually dead code. Live tests catch:
- Missing route registrations in server.rs
- Config fields not being deserialized from TOML
- Type mismatches between kernel and API layers
- Endpoints that compile but return wrong/empty data

### How to Run Live Integration Tests

#### Step 1: Stop any running daemon
```bash
tasklist | grep -i openfang
taskkill //PID <pid> //F
# Wait 2-3 seconds for port to release
sleep 3
```

#### Step 2: Build fresh release binary
```bash
cargo build --release -p openfang-cli
```

#### Step 3: Start daemon with required API keys
```bash
GROQ_API_KEY=<key> target/release/openfang.exe start &
sleep 6  # Wait for full boot
curl -s http://127.0.0.1:4200/api/health  # Verify it's up
```
The daemon command is `start` (not `daemon`).

#### Step 4: Test every new endpoint
```bash
# GET endpoints — verify they return real data, not empty/null
curl -s http://127.0.0.1:4200/api/<new-endpoint>

# POST/PUT endpoints — send real payloads
curl -s -X POST http://127.0.0.1:4200/api/<endpoint> \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'

# Verify write endpoints persist — read back after writing
curl -s -X PUT http://127.0.0.1:4200/api/<endpoint> -d '...'
curl -s http://127.0.0.1:4200/api/<endpoint>  # Should reflect the update
```

#### Step 5: Test real LLM integration
```bash
# Get an agent ID
curl -s http://127.0.0.1:4200/api/agents | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['id'])"

# Send a real message (triggers actual LLM call to Groq/OpenAI)
curl -s -X POST "http://127.0.0.1:4200/api/agents/<id>/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Say hello in 5 words."}'
```

#### Step 6: Verify side effects
After an LLM call, verify that any metering/cost/usage tracking updated:
```bash
curl -s http://127.0.0.1:4200/api/budget       # Cost should have increased
curl -s http://127.0.0.1:4200/api/budget/agents  # Per-agent spend should show
```

#### Step 7: Verify dashboard HTML
```bash
# Check that new UI components exist in the served HTML
curl -s http://127.0.0.1:4200/ | grep -c "newComponentName"
# Should return > 0
```

#### Step 8: Cleanup
```bash
tasklist | grep -i openfang
taskkill //PID <pid> //F
```

### Key API Endpoints for Testing
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Basic health check |
| `/api/agents` | GET | List all agents |
| `/api/agents/{id}/message` | POST | Send message (triggers LLM) |
| `/api/budget` | GET/PUT | Global budget status/update |
| `/api/budget/agents` | GET | Per-agent cost ranking |
| `/api/budget/agents/{id}` | GET | Single agent budget detail |
| `/api/network/status` | GET | OFP network status |
| `/api/peers` | GET | Connected OFP peers |
| `/api/a2a/agents` | GET | External A2A agents |
| `/api/a2a/discover` | POST | Discover A2A agent at URL |
| `/api/a2a/send` | POST | Send task to external A2A agent |
| `/api/a2a/tasks/{id}/status` | GET | Check external A2A task status |

## Architecture Notes
- **Don't touch `openfang-cli`** — user is actively building the interactive CLI
- `KernelHandle` trait avoids circular deps between runtime and kernel
- `AppState` in `server.rs` bridges kernel to API routes
- New routes must be registered in `server.rs` router AND implemented in `routes.rs`
- Dashboard is Alpine.js SPA in `static/index_body.html` — new tabs need both HTML and JS data/methods
- Config fields need: struct field + `#[serde(default)]` + Default impl entry + Serialize/Deserialize derives

## Common Gotchas
- `openfang.exe` may be locked if daemon is running — use `--lib` flag or kill daemon first
- `PeerRegistry` is `Option<PeerRegistry>` on kernel but `Option<Arc<PeerRegistry>>` on `AppState` — wrap with `.as_ref().map(|r| Arc::new(r.clone()))`
- Config fields added to `KernelConfig` struct MUST also be added to the `Default` impl or build fails
- `AgentLoopResult` field is `.response` not `.response_text`
- CLI command to start daemon is `start` not `daemon`
- On Windows: use `taskkill //PID <pid> //F` (double slashes in MSYS2/Git Bash)

```


# Repo: claw-mu

## CLAUDE.md
```markdown
## Workflow Orchestration

### 1. Plan Node Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

## Build Commands

### Frontend/Backend (Turbo Monorepo)

```bash
pnpm install          # Install dependencies
pnpm build            # Build all apps (api, admin, chat)
pnpm dev              # Development mode
```

### Worker Docker Image (4-Layer Architecture)

| Layer | Image | Content | Rebuild When |
|-------|-------|---------|--------------|
| base | `claw-base-latest` | Ubuntu + Node 22 + Bun | Toolchain update |
| deps | `claw-deps-latest` | openclaw node_modules (1.9GB) | Dependencies change |
| openclaw | `claw-openclaw-latest` | dist/ + assets (~50MB) | Code change |
| worker | `claw-worker-latest` | worker-api | API change |

**Quick Commands:**

```bash
# Most common: openclaw code changed
./docker/build-worker.sh code

# worker-api only
./docker/build-worker.sh api

# Dependencies changed (package.json)
./docker/build-worker.sh deps

# Full rebuild
./docker/build-worker.sh base
```

**Manual Build (openclaw code change):**

```bash
cd openclaw && pnpm build
docker build -f docker/Dockerfile.openclaw -t getuai/getu_ads:claw-openclaw-latest .
docker build -f docker/Dockerfile.worker -t getuai/getu_ads:claw-worker-latest .
```

### OpenClaw CLI

```bash
cd openclaw
pnpm install          # Install dependencies
pnpm build            # Build (generates dist/)
pnpm dev              # Development mode
```

### Chrome Extension

```bash
# Development: Load unpacked from apps/chat/public/extension/claw-extension/
# Chrome: chrome://extensions -> Load unpacked

# Production zip:
cd apps/chat/public/extension/claw-extension
zip -r ../claw-extension.zip .
```

### Staging Deployment

```bash
# On staging server (20.228.94.67)
cd ~/projects/claw-mu
docker compose up -d --build    # Rebuild and start
docker compose logs -f          # View logs
docker compose restart          # Restart all
```

```


# Repo: cuilawgroup

## AGENTS.md
```markdown
<!-- VERCEL BEST PRACTICES START -->
## Best practices for developing on Vercel

These defaults are optimized for AI coding agents (and humans) working on apps that deploy to Vercel.

- Treat Vercel Functions as stateless + ephemeral (no durable RAM/FS, no background daemons), use Blob or marketplace integrations for preserving state
- Edge Functions (standalone) are deprecated; prefer Vercel Functions
- Don't start new projects on Vercel KV/Postgres (both discontinued); use Marketplace Redis/Postgres instead
- Store secrets in Vercel Env Variables; not in git or `NEXT_PUBLIC_*`
- Provision Marketplace native integrations with `vercel integration add` (CI/agent-friendly)
- Sync env + project settings with `vercel env pull` / `vercel pull` when you need local/offline parity
- Use `waitUntil` for post-response work; avoid the deprecated Function `context` parameter
- Set Function regions near your primary data source; avoid cross-region DB/service roundtrips
- Tune Fluid Compute knobs (e.g., `maxDuration`, memory/CPU) for long I/O-heavy calls (LLMs, APIs)
- Use Runtime Cache for fast **regional** caching + tag invalidation (don't treat it as global KV)
- Use Cron Jobs for schedules; cron runs in UTC and triggers your production URL via HTTP GET
- Use Vercel Blob for uploads/media; Use Edge Config for small, globally-read config
- If Enable Deployment Protection is enabled, use a bypass secret to directly access them
- Add OpenTelemetry via `@vercel/otel` on Node; don't expect OTEL support on the Edge runtime
- Enable Web Analytics + Speed Insights early
- Use AI Gateway for model routing, set AI_GATEWAY_API_KEY, using a model string (e.g. 'anthropic/claude-sonnet-4.6'), Gateway is already default in AI SDK
  needed. Always curl https://ai-gateway.vercel.sh/v1/models first; never trust model IDs from memory
- For durable agent loops or untrusted code: use Workflow (pause/resume/state) + Sandbox; use Vercel MCP for secure infra access
<!-- VERCEL BEST PRACTICES END -->

```

## agents.md
```markdown
<!-- VERCEL BEST PRACTICES START -->
## Best practices for developing on Vercel

These defaults are optimized for AI coding agents (and humans) working on apps that deploy to Vercel.

- Treat Vercel Functions as stateless + ephemeral (no durable RAM/FS, no background daemons), use Blob or marketplace integrations for preserving state
- Edge Functions (standalone) are deprecated; prefer Vercel Functions
- Don't start new projects on Vercel KV/Postgres (both discontinued); use Marketplace Redis/Postgres instead
- Store secrets in Vercel Env Variables; not in git or `NEXT_PUBLIC_*`
- Provision Marketplace native integrations with `vercel integration add` (CI/agent-friendly)
- Sync env + project settings with `vercel env pull` / `vercel pull` when you need local/offline parity
- Use `waitUntil` for post-response work; avoid the deprecated Function `context` parameter
- Set Function regions near your primary data source; avoid cross-region DB/service roundtrips
- Tune Fluid Compute knobs (e.g., `maxDuration`, memory/CPU) for long I/O-heavy calls (LLMs, APIs)
- Use Runtime Cache for fast **regional** caching + tag invalidation (don't treat it as global KV)
- Use Cron Jobs for schedules; cron runs in UTC and triggers your production URL via HTTP GET
- Use Vercel Blob for uploads/media; Use Edge Config for small, globally-read config
- If Enable Deployment Protection is enabled, use a bypass secret to directly access them
- Add OpenTelemetry via `@vercel/otel` on Node; don't expect OTEL support on the Edge runtime
- Enable Web Analytics + Speed Insights early
- Use AI Gateway for model routing, set AI_GATEWAY_API_KEY, using a model string (e.g. 'anthropic/claude-sonnet-4.6'), Gateway is already default in AI SDK
  needed. Always curl https://ai-gateway.vercel.sh/v1/models first; never trust model IDs from memory
- For durable agent loops or untrusted code: use Workflow (pause/resume/state) + Sandbox; use Vercel MCP for secure infra access
<!-- VERCEL BEST PRACTICES END -->

```


# Repo: lawyer_marketing

## README.md
```markdown
# Lawyer Marketing Platform

AI-powered legal marketing platform for law firm Google Ads campaign management, keyword research, and market intelligence.

## Features

- **Google Ads Management** — Create, monitor, and optimize Search campaigns via AI-driven chat
- **Keyword Research** — Discover keyword ideas and get search volume metrics via Google Keyword Planner
- **Market Intelligence** — Court opinions, demographics, traffic incidents, SEO competitor analysis
- **AI Chat** — Claude-powered conversational interface for campaign operations

## Architecture

```
frontend/          React 19 + Vite + Tailwind + Zustand
    │
    ▼  /api, /ws
backend-py/        FastAPI + SQLAlchemy + asyncpg (PRIMARY)
    │
    ├── PostgreSQL
    ├── google-ads/    Google Ads CLI (38 ops) + Keyword Planner CLI
    └── law-data/      Legal market intelligence CLI (10 commands)
```

> **Note:** A legacy Node.js/Express backend exists at `backend/` but is no longer actively maintained. All new development targets `backend-py/`.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript, Vite 8, Tailwind CSS 4, Zustand |
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0, asyncpg |
| Database | PostgreSQL |
| Auth | Logto (self-hosted) |
| AI Agent | Claude Agent SDK |
| Scheduling | APScheduler (Redis / memory) |
| Reverse Proxy | Caddy (staging) |
| Containerization | Docker + Docker Compose |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Environment files configured (see `backend-py/.env.staging` as reference)

### Local Development

```bash
# Python backend (recommended)
docker compose -f docker/docker-compose.dev.py.yml up --build

# Node.js backend (legacy)
docker compose -f docker/docker-compose.dev.yml up --build
```

### Staging Deployment

```bash
docker compose -f docker/docker-compose.staging.yml up --build -d
```

Staging URL: `https://lawyer-marketing.previewapps.org`

## Project Structure

```
├── frontend/          React SPA
├── backend-py/        FastAPI backend (active)
├── backend/           Express backend (legacy, retained)
├── google-ads/        Google Ads & Keyword Planner CLI tools
├── law-data/          Legal market intelligence CLI tools
├── docker/            Dockerfiles & Compose configs
├── scripts/           Utility scripts
└── docs/              Documentation
```

## Environment Files

| File | Purpose |
|------|---------|
| `backend-py/.env.staging` | Staging environment config |
| `frontend/.env.staging` | Frontend staging build vars |
| `*.env.production` | Reserved for future production deployment |

## CLI Tools

### Google Ads CLI

Campaign management with 38 operations — campaigns, ad groups, keywords, RSA ads, budgets, criteria, reporting, and GAQL queries.

### Keyword Planner CLI

Keyword research via MCC service account — generate ideas and get historical metrics.

### Law Data CLI

Legal market intelligence with 10 commands — court opinions, demographics, traffic incidents, SEO keywords, and competitor analysis.

```

## CLAUDE.md
```markdown
# Lawyer Marketing Platform

AI-powered legal marketing platform for Google Ads campaign management, keyword research, and market intelligence.

## Architecture Overview

```
lawyer_marketing/
├── frontend/          # React + Vite SPA
├── backend-py/        # Python/FastAPI backend (PRIMARY)
├── backend/           # Node.js/Express backend (LEGACY — retained, not updated)
├── google-ads/        # Google Ads CLI tools (campaign management + keyword planner)
├── law-data/          # Legal market intelligence CLI tools
├── docker/            # Docker configs (Compose + Dockerfiles)
├── scripts/           # Utility scripts
└── docs/              # Documentation
```

## Backend Status

| Backend | Path | Status | Notes |
|---------|------|--------|-------|
| **Python/FastAPI** | `backend-py/` | **Active** | Primary backend, all new development here |
| Node.js/Express | `backend/` | Retained | No longer updated; kept for reference only |

Both backends expose the same API surface (`/api/*`) and share the same PostgreSQL database. The frontend is backend-agnostic — Docker Compose file selection determines which backend runs.

## Tech Stack

### Frontend (`frontend/`)
- **Framework**: React 19 + TypeScript
- **Build**: Vite 8
- **Styling**: Tailwind CSS 4
- **State**: Zustand
- **Auth**: Logto (`@logto/react`)
- **Routing**: React Router DOM 7
- **Notable**: Leaflet maps, React Markdown rendering

### Backend — Python (`backend-py/`)
- **Framework**: FastAPI
- **Python**: 3.11+
- **Database**: PostgreSQL via asyncpg + SQLAlchemy 2.0
- **Migrations**: Alembic
- **Auth**: Logto (JWT verification via python-jose)
- **Scheduling**: APScheduler (Redis-backed, memory fallback)
- **Agent**: claude-agent-sdk for AI chat sessions + optimization pipeline

### Database
- **Engine**: PostgreSQL
- **Staging DB**: `20.59.118.120:32476`
- **Schema**: managed by Alembic migrations (`backend-py/alembic/`)

### Auth
- **Provider**: Logto (self-hosted at `account.rankgale.ai`)
- **Flow**: Frontend obtains token via `@logto/react` → Backend verifies JWT
- **Fallback**: Local username/password auth (dev mode)

## CLI Tools

### Google Ads CLI (`google-ads/`)
- Campaign management (38 operations): create, list, update, report
- Keyword Planner (2 operations): generate ideas, get metrics
- Credentials pre-injected via env vars and service account

### Law Data CLI (`law-data/`)
- Court opinions and judge search
- County demographics
- Real-time traffic incidents (TomTom)
- SEO keyword research, competitor analysis (DataForSEO)

## Docker / Deployment

### Compose Files
| File | Purpose | Backend |
|------|---------|---------|
| `docker-compose.staging.yml` | Staging (Caddy + app) | Python |
| `docker-compose.dev.py.yml` | Local dev | Python |
| `docker-compose.dev.yml` | Local dev | Node.js (legacy) |
| `docker-compose.yml` | Production (TBD) | Node.js (legacy) |

### Environment Files
| File | Used By |
|------|---------|
| `backend-py/.env.local` | `scripts/start-local.sh` (non-Docker local dev) |
| `backend-py/.env.staging` | `docker-compose.staging.yml` |
| `frontend/.env.staging` | Vite build args in staging |
| `backend-py/.env.production` | Reserved for future production deployment |
| `frontend/.env.production` | Reserved for future production deployment |

### Staging
- Reverse proxy: Caddy (auto-HTTPS)
- Domain: `lawyer-marketing.previewapps.org`

## Development

### Local dev (non-Docker, recommended for testing with local Claude Code)

Prerequisites: Python 3.11+, PostgreSQL, Redis, claude CLI installed locally.

```bash
# First time setup
cd backend-py
python -m venv .venv
pip install -e ".[dev]"

# Start backend (bash / Git Bash on Windows)
./scripts/start-local.sh

# Start backend (Windows CMD)
scripts\start-local.bat
```

The script will:
1. Activate the Python venv
2. Load env vars from `backend-py/.env.local`
3. Check PostgreSQL and Redis connectivity
4. Run Alembic migrations
5. Install system skills to `~/.claude/skills/`
6. Start uvicorn with hot-reload on port 3456

| File | Purpose |
|------|---------|
| `backend-py/.env.local` | Local dev environment config |
| `scripts/start-local.sh` | Bash startup script |
| `scripts/start-local.bat` | Windows CMD startup script |

### Docker dev

```bash
# Local dev (Python backend)
docker compose -f docker/docker-compose.dev.py.yml up --build

# Local dev (Node.js backend — legacy)
docker compose -f docker/docker-compose.dev.yml up --build
```

## Optimization Pipeline

Campaign optimization uses a **Plan-Validate-Execute** architecture (see `docs/optimization-pipeline-architecture.md`):

1. **Analysis Agent** (read-only) — collects data via CLI reports, writes `execution_plan.json`
2. **Validation** (Python) — validates each action payload against CLI Pydantic schemas from `google-ads/cli/`
3. **Execution** (Python) — runs validated CLI commands via subprocess, captures `ResultEnvelope`
4. **Action Logging** — stores real CLI results (campaign_id, counts) in action records

Key files:
- `backend-py/schemas/execution_plan.py` — plan schema
- `backend-py/services/execution_engine.py` — validation + execution engine
- `backend-py/services/optimization_service.py` — pipeline orchestration + prompts
- `backend-py/configs/operation_tiers.py` — canonical read/write operation classification
- `backend-py/services/tool_enforcement.py` — PreToolUse hook enforcement for read/write boundaries

### Read/Write Skill Boundary

CLI operations are split into two skills enforcing a hard read/write boundary:

| Skill | Operations | Agents |
|-------|-----------|--------|
| `google-ads-query` | 16 read-only (report, list, find, GAQL) | All Google Ads agents |
| `google-ads-exec` | 23 write/mutate (create, update, remove) | Execution agents only |

Analysis agents (e.g., `google-ads-analyst`) receive **only** `google-ads-query` and are blocked from write operations at both the skill layer (no write docs) and code layer (`PreToolUse` hook enforcement via `tool_enforcement.py`). This boundary is enforced in both chat sessions and automated optimization runs.

## Industry Registry (Skill Injection)

Agent definitions support **dynamic industry skill injection** via the Industry Registry (`backend-py/configs/industry_registry.py`). Each user has an `industry` field in `user_profiles` (default: `"lawyer"`).

### How it works

```
user_profiles.industry → resolve_user_industry() → "lawyer"
                                                       ↓
get_agent_definitions(industry="lawyer")
  ├─ Build base agents (general skills only)
  ├─ Apply base domain prompts (_DOMAIN_PROMPTS)
  └─ Apply INDUSTRY_REGISTRY["lawyer"] overlays:
       ├─ add_skills: ["lawyer"] (single unified skill)
       ├─ add_prompt_lines: point to specific references
       └─ add_domain_prompts: e.g., legal_context.md
```

### Industry Skill Structure

Each industry has a single unified skill with internal reference files organized by optimization dimension:

```
google-ads/skills/lawyer/
├── SKILL.md                    # Entry point, index, directory exclusions, lawdata CLI
└── references/
    ├── practice-areas.md       # 7 practice area profiles
    ├── legal-compliance.md     # State bar rules, Google policies
    ├── budget-strategy.md      # Budgets, bidding, seasonal patterns
    ├── keyword-strategy.md     # Keywords, negatives, intent tiers
    ├── ad-copy-strategy.md     # Tone, pinning, URL paths, multilingual
    ├── copy-templates.md       # RSA headline/description templates
    ├── ad-compliance.md        # RSA-specific compliance checks
    └── legal-benchmarks.md     # CPC/CTR/CVR by area and tier
```

General skills are industry-agnostic; the `lawyer` skill extends all three:

| General Skill | What `lawyer` adds |
|---|---|
| campaign-strategist | Practice area profiles, CPC benchmarks, budgets, compliance |
| ads-copy-analysis | Legal templates, state bar disclaimers, tone guidance |
| competitor-intel | CPC/CTR/CVR benchmarks, legal directory exclusions |

### Adding a New Industry

1. Create a single skill directory (e.g., `dentist/`) with `references/`
2. Add `"dentist": IndustryConfig(...)` to `INDUSTRY_REGISTRY` in `industry_registry.py`
3. New DB migration expanding the CHECK constraint on `user_profiles.industry`
4. **No changes** needed in `agents.py`, `optimization_service.py`, or `session_manager.py`

### Key Files

| File | Purpose |
|------|---------|
| `backend-py/configs/industry_registry.py` | Registry + `resolve_user_industry()` |
| `backend-py/configs/agents.py` | Agent definitions + overlay application |
| `google-ads/skills/lawyer/` | Lawyer industry skill (unified) |
| `google-ads/skills/` (others) | General (industry-agnostic) skill files |

## Eval System (Self-Improving Agent Loop)

Standalone eval system (`eval/`) for automated testing and improvement of agent skills and prompts. See `eval/ARCHITECTURE.md` for full details.

### How it works

1. **Scenarios** (JSON) define synthetic campaign data + expected agent actions
2. **Agent Runner** executes the agent against mock CLI (PYTHONPATH injection, no real API calls)
3. **Scorer** evaluates output with 3 layers: rule-based structural, LLM-as-judge semantic, schema validation
4. **Skills Writer** uses Claude to rewrite SKILL.md files based on failures
5. **Prompts Writer** (optional, `--optimize-prompts`) uses Claude to rewrite agent description + prompt text
6. **Version Store** snapshots skills + agent prompts per iteration with diffs and rollback
7. **Convergence** stops when 5 delta functions all pass (error rate, scenario stability, skill content, prompt content, semantic equivalence)

### Two improvement levers

| Lever | Controls | Target |
|-------|----------|--------|
| Skills Writer | *What knowledge* the agent has | `SKILL.md` files |
| Prompts Writer | *How the agent reasons* | `AgentDefinition.description` + `.prompt` |

The Prompts Writer uses a `prompt_overrides` parameter on `get_agent_definitions()` — overrides apply to the base prompt before domain/industry layers are appended. Production callers are unaffected.

### Key files

| File | Purpose |
|------|---------|
| `eval/run.py` | Main CLI entry point + loop orchestration |
| `eval/core/agent_runner.py` | Workspace setup + mock CLI injection |
| `eval/core/scorer.py` | 3-layer scoring |
| `eval/core/skills_writer.py` | AI-powered SKILL.md improvement |
| `eval/core/agent_prompts_writer.py` | AI-powered agent description+prompt improvement |
| `eval/core/convergence.py` | 5 delta functions + regression detector |
| `eval/core/version_store.py` | File-based version management |
| `eval/scenarios/` | Test scenario JSON files |

## Benchmark System

Offline replay harness (`scripts/benchmark/`) that scores the optimization
agent's execution plan against human-labeled ground truth for one or more
past days. Unlike `eval/`, benchmark runs the **real** production
`optimization_service.run_account_optimization` code path and substitutes
only the data-access layer (Google Ads CLI + Attribution API + temporal
DB filters) with pre-captured fixtures.

### Entry points

| Command | Purpose |
|---|---|
| `python scripts/benchmark/build_benchmark_fixture.py --customer-id <cid> --as-of-date <YYYY-MM-DD>` | Pull a day's fixtures (requires live Google Ads + Attribution creds) |
| `python scripts/benchmark/run_benchmark.py --customer-id <cid> --days <d1> [<d2> ...]` | Run the benchmark + generate report |
| `pytest backend-py/tests/benchmark/test_smoke_day.py` | 1-day smoke test against `run_account_optimization(pipeline_mode='benchmark')` |
| `pytest backend-py/tests/benchmark/test_temporal_isolation.py` | 5-part temporal-isolation audit (CP15) |

### Key runtime flags

- `--canned-pipeline` (default): deterministic stub that emits the 9
  unconditional tracer taps + `validate` + writes a labels-echoing
  `execution_plan.json`. CI-safe, no live SDK.
- `--live-pipeline`: calls the real `run_account_optimization` end-to-end.
  Requires `ANTHROPIC_API_KEY` + a live PostgreSQL pool.
- `--min-hit-rate FLOAT` (default `0.4`): controls the warning banner
  threshold. When any day has a fixture hit-rate below this, the
  top-level report surfaces a banner.

### V1 honest limits

1. Fixture ≠ snapshot-at-`as_of_date`. The builder pulls with
   `segments.date <= as_of_date - 1` filters, but between build time and
   `as_of_date` the account state can drift. Every report surfaces a
   "fixture pulled at {ts}" disclaimer.
2. `--canned-pipeline` has L1 F1 ≈ 1.0 by construction (perfect label
   match). Use `--live-pipeline` for real agent variance.
3. `semantic_score` defaults to SKIPPED without `ANTHROPIC_API_KEY`.
4. Days are processed sequentially (no parallel).

### The 22 read-only Google Ads ops

Benchmark fixtures cover exactly the 22 read-only operations CP02+CP03+CP04
fixture-backed. See `google-ads/skills/google-ads-query/SKILL.md` for the
authoritative list:

| Family | Count | Operations |
|--------|------:|------------|
| Search / Listing | 10 | `search.campaign.list/find`, `search.ad_group.list/find`, `search.keyword.list`, `search.ad.list/get_rsa`, `search.criteria.list`, `search.shared_set.list`, `search.shared_criterion.list` |
| Reporting | 6 | `report.campaign`, `report.ad_group`, `report.keyword`, `report.ad`, `report.search_terms`, `report.gaql` |
| GAQL Builder | 6 | `gaql.resources`, `gaql.fields`, `gaql.field`, `gaql.build`, `gaql.validate`, `gaql.run` |

### Key files

| File | Purpose |
|---|---|
| `scripts/benchmark/run_benchmark.py` | Main CLI |
| `scripts/benchmark/build_benchmark_fixture.py` | Fixture builder |
| `scripts/benchmark/matcher.py` + `evaluator.py` | 3-layer scoring |
| `scripts/benchmark/report_generator.py` + `report_templates.py` | Markdown report |
| `backend-py/services/benchmark_context.py` | `BenchmarkContext` dataclass |
| `backend-py/services/benchmark_tracer.py` | `BenchmarkTracer` (11 `emit_*` methods) |
| `backend-py/tests/benchmark/_sdk_mocks.py` | Shared stub helper for SDK layer |
| `backend-py/tests/benchmark/test_smoke_day.py` | 1-day end-to-end smoke |
| `backend-py/tests/benchmark/test_temporal_isolation.py` | CP15 isolation audit |

Full spec: `.harness/benchmark-os-04211500/spec.md`.

## Frontend Workspace Layout (0408-redesign)

The frontend is organized as a **chat-side + right-side account workspace** inspired by the 0408 prototype. Two distinct layouts:

| Layout | Used by routes | Chrome |
|---|---|---|
| `WorkspaceLayout` | `/`, `/session/:id`, `/auto-optimize`, `/auto-optimize/runs/:runId`, `/campaigns`, `/keywords`, `/outcomes` | TopBar (brand + tabs + approval mode + decisions + account) / ChatDock (left, collapsible) / Outlet (right main) |
| `MainLayout` | `/accidents`, `/ads-dashboard`, `/profile`, `/attribution/*` | Legacy `Sidebar` (new chat + nav + recents + Google auth + user profile) |

**Key decoupling rule**: chat session selection never drives the right-side tab, and vice versa. User-initiated clicks (e.g. action chips in AI messages) may set `workspaceStore.activeTab` + show a toast, but messages never auto-switch tabs.

### Design tokens

Extended in [frontend/src/index.css](frontend/src/index.css):
- Fonts: `--font-serif` (Newsreader, for AI voice & headings), `--font-mono` (JetBrains Mono, for metrics/state), `--font-sans` (system-ui, for UI)
- Semantic colors: `teal` (success/high-certainty), `amber` (warning/pending), `coral` (failure/low-certainty), `sage` (info), on top of existing `warm` + `cream`

### Key files

| File | Purpose |
|---|---|
| `frontend/src/layouts/WorkspaceLayout.tsx` | Primary chat + right-workspace layout |
| `frontend/src/components/workspace/TopBar.tsx` | Brand + tabs + right cluster |
| `frontend/src/components/workspace/TopBarAccount.tsx` | Google Ads connect/disconnect + customer pill + user menu. Splits `LogtoUserMenu` vs `DevUserMenu` — `useLogto()` is only called when Logto is actually configured (provider in tree) |
| `frontend/src/components/workspace/ChatDock.tsx` | Left chat panel: session list + ChatPanel/NewChatPanel + collapse button |
| `frontend/src/components/workspace/DecisionsInbox.tsx` | 🔔 popover for awaiting_approval runs |
| `frontend/src/components/workspace/ApprovalModeToggle.tsx` | localStorage preference (UI preview; backend field pending) |
| `frontend/src/components/workspace/ToastStack.tsx` | Bottom-right toasts |
| `frontend/src/stores/workspaceStore.ts` | `activeTab` / `selectedRunId` / `chatCollapsed` / toasts |
| `frontend/src/components/optimization/ExecutionPlanV3.tsx` | Account-level execution plan rendered as Campaign → AdGroup → Keywords/Ads tree, all expanded by default, with filters |
| `frontend/src/components/optimization/PipelineSummaryBar.tsx` | Progress / elapsed / cost / cancel for live optimization runs |
| `frontend/src/components/optimization/shared.tsx` | `groupActionsByCampaign` + `extractCampaignId/AdGroupId` + `summarizePlanGroups` |
| `frontend/src/components/ui/*` | Zero-dependency UI primitives (Pill, Dot, Toggle, MetricCard, AlertBar, StatusBadge, ConfidenceBar) |
| `frontend/src/pages/OutcomesPage.tsx` | `/outcomes` tab: action log + verdicts |

The old `ExecutionPlanReview.tsx` + `MultiPhaseView.tsx` are retained for one sprint as rollback targets.

## Conventions

- All new backend work goes in `backend-py/`. Do not modify `backend/`.
- Frontend proxies `/api` and `/ws` to the backend (port 3456).
- Environment variables must be fetched at runtime, not cached at module load time.
- Credentials are mounted read-only into containers; never commit secrets.
- Industry skills must never be mixed — one `industry` value per optimization run, applied to all agents uniformly.
- When running spec final tests in a git worktree (browser/E2E tests, or any code test that needs runtime env), first copy the relevant `.env*` files and `credentials/` directory from the main checkout into the worktree — they are gitignored and are not auto-propagated to worktrees, so dev servers, Logto auth, Google Ads CLI, and live integration tests will fail without them. Typical files: `backend-py/.env.local`, `backend-py/.env.staging`, `frontend/.env.staging`, `credentials/` (Google Ads service account + OAuth tokens).
- Spec final verifications default to **local** via `scripts/start-local.sh` (backend on port 3456) + `pnpm dev` in `frontend/` — never staging unless explicitly requested. Staging deploys are reserved for confirming a release after local verification passes.

```

## .claude/skills/deploy-staging/SKILL.md
```markdown
---
name: deploy-staging
description: Deploy the current project to a staging server via SSH + Docker Compose. Use when the user asks to "deploy", "deploy to staging", "publish to staging", "update staging", "release to staging". Handles git push, SSH pull, config sync, docker rebuild, and health verification.
---

# Staging Deployment Skill

A **parameterized** deployment workflow. The agent resolves all variables at runtime — nothing is hardcoded.

---

## Step 0 — Resolve Variables

Before executing ANY command, resolve every variable below. Read project files, git config, and SSH config to populate them. **Do NOT assume values — discover them.**

### Variable Table

| Variable              | How to Resolve                                                                                              |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| `LOCAL_PROJECT_DIR`   | Cursor workspace root (the directory containing `.git`)                                                     |
| `BRANCH`              | `git branch --show-current`                                                                                 |
| `GIT_REMOTE`          | `git remote -v` — pick the `push` remote (usually `origin`)                                                |
| `SSH_HOST`            | Read from `deploy.staging` section in project config, or fall back to `~/.ssh/config` matching the project  |
| `SERVER_PROJECT_DIR`  | Read from project config, or default to `~/projects/<repo-name>`                                            |
| `COMPOSE_FILE`        | Auto-discover: list `docker/docker-compose.staging*.yml` and pick the one matching the current backend      |
| `BACKEND_TYPE`        | Detect from branch/project: if `backend-py/` exists and branch contains `py` → `python`; else → `node`     |
| `BACKEND_DIR`         | `python` → `backend-py`, `node` → `backend`                                                                |
| `BACKEND_ENV_FILE`    | `<BACKEND_DIR>/.env.staging`                                                                                |
| `FRONTEND_ENV_FILE`   | `frontend/.env.staging` (if `frontend/` exists)                                                             |
| `DOMAIN`              | Parse from `docker/Caddyfile` (first server name), or from frontend env `VITE_APP_URL`                     |
| `APP_CONTAINER`       | `docker compose -f <COMPOSE_FILE> ps --format json` → extract main app service container name               |
| `MIGRATION_TOOL`      | `python` → Alembic (`python -m alembic`), `node` → node-pg-migrate                                        |

### Config Overrides (optional)

If the project root contains `deploy.staging.json`, read it to override any variable:

```json
{
  "ssh_host": "1.2.3.4",
  "server_project_dir": "/home/user/my-project",
  "compose_file": "docker/docker-compose.staging.yml",
  "domain": "staging.example.com"
}
```

If this file does not exist, resolve everything from project files as described above.

### Discovery Commands

Run these in **parallel** to resolve variables:

```bash
git branch --show-current
git remote -v
ls docker/docker-compose.staging*.yml
cat docker/Caddyfile 2>/dev/null | head -1
```

Also read:
- `~/.ssh/config` — to find SSH user/key for the target host
- `docker/Caddyfile` — to extract domain
- `frontend/.env.production` — to extract `VITE_APP_URL` as fallback domain

Print the resolved variable table to the user for confirmation before proceeding.

---

## Step 1 — Pre-flight Checks

```bash
cd ${LOCAL_PROJECT_DIR}
git status --short
```

- If uncommitted changes exist → **warn the user**, ask whether to commit first.
- If clean → proceed.

---

## Step 2 — Push Local Code

```bash
cd ${LOCAL_PROJECT_DIR}
git push ${GIT_REMOTE} ${BRANCH}
```

---

## Step 3 — Pull on Server

```bash
ssh ${SSH_HOST} "cd ${SERVER_PROJECT_DIR} && git fetch origin && git checkout ${BRANCH} && git pull origin ${BRANCH}"
```

---

## Step 4 — Sync Gitignored Config Files

These files are NOT in git. Compare local vs server, upload if they differ.
**Always sync BEFORE rebuilding** — frontend env vars are baked into the Vite build.

### Auto-discover files to sync

Scan the project for these patterns (relative to project root):

| Pattern                                  | Purpose                         |
| ---------------------------------------- | ------------------------------- |
| `${BACKEND_DIR}/.env.staging`            | Backend runtime env             |
| `${BACKEND_DIR}/.env`                    | Backend env (if separate)       |
| `frontend/.env.staging`                  | Frontend build-time env         |
| `${BACKEND_DIR}/claudecode-setting.json` | Claude Code settings            |
| `${BACKEND_DIR}/src/credentials/*`       | OAuth / service account secrets |
| `google-ads/credentials/*`               | Google Ads credentials          |

For each file that **exists locally**:

```bash
scp ${LOCAL_PROJECT_DIR}/<file> ${SSH_HOST}:${SERVER_PROJECT_DIR}/<file>
```

Skip files that do not exist locally.

---

## Step 5 — Rebuild & Restart Containers

```bash
ssh ${SSH_HOST} "cd ${SERVER_PROJECT_DIR} && docker compose -f ${COMPOSE_FILE} up -d --build"
```

This runs in background (~2-4 min). Monitor terminal output for milestones:

- Dependency install (`pip install` / `npm ci`) ~30s
- Frontend build (`vite build`) ~30s
- File permissions (`chown`) ~15s
- Image export ~30s
- `Container ... Started` → done

---

## Step 6 — Verify Deployment

```bash
# Container status
ssh ${SSH_HOST} "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# App logs
ssh ${SSH_HOST} "docker compose -f ${SERVER_PROJECT_DIR}/${COMPOSE_FILE} logs --tail 20 app 2>/dev/null || docker logs ${APP_CONTAINER} --tail 20"
```

### Expected healthy signals

**Python (FastAPI):**
```
✅ PostgreSQL is ready
📦 Running Alembic migrations...
✅ Database migrations complete
🚀 Starting Python server...
🚀 Server ready on port ...
```

**Node.js (Express):**
```
✅ Database schema initialized
✅ No pending migrations
🚀 Server running on http://localhost:...
```

---

## Step 7 — Health Check

```bash
curl -s -o /dev/null -w '%{http_code}' https://${DOMAIN}
```

Expected: `200`. If not, check reverse proxy logs:

```bash
ssh ${SSH_HOST} "docker compose -f ${SERVER_PROJECT_DIR}/${COMPOSE_FILE} logs --tail 20 caddy 2>/dev/null"
```

---

## Database Migrations (on-demand)

Migrations auto-run on container start. Manual triggers are only for hot-patching or rollback.

### Python (Alembic)

```bash
# Apply pending
ssh ${SSH_HOST} "docker exec ${APP_CONTAINER} sh -c 'cd /app/${BACKEND_DIR} && python -m alembic upgrade head'"

# Current revision
ssh ${SSH_HOST} "docker exec ${APP_CONTAINER} sh -c 'cd /app/${BACKEND_DIR} && python -m alembic current'"

# Rollback 1
ssh ${SSH_HOST} "docker exec ${APP_CONTAINER} sh -c 'cd /app/${BACKEND_DIR} && python -m alembic downgrade -1'"
```

### Node.js (node-pg-migrate)

```bash
# Apply pending
ssh ${SSH_HOST} "docker exec -w /app/${BACKEND_DIR} ${APP_CONTAINER} npx node-pg-migrate up -m src/db/migrations -t pgmigrations"

# Rollback 1
ssh ${SSH_HOST} "docker exec -w /app/${BACKEND_DIR} ${APP_CONTAINER} npx node-pg-migrate down 1 -m src/db/migrations -t pgmigrations"
```

---

## Backup Gitignored Files (before destructive ops)

```bash
ssh ${SSH_HOST} "mkdir -p /tmp/project_backup && cd ${SERVER_PROJECT_DIR} && \
  for f in \
    ${BACKEND_DIR}/.env.staging \
    ${BACKEND_DIR}/.env \
    ${BACKEND_DIR}/claudecode-setting.json \
    frontend/.env.staging \
    google-ads/credentials \
  ; do \
    [ -e \"\$f\" ] && cp -r \"\$f\" /tmp/project_backup/ 2>/dev/null; \
  done && echo 'Backup done' && ls -la /tmp/project_backup/"
```

---

## Troubleshooting

### SSH Host Key Changed

```bash
ssh-keygen -R ${SSH_HOST}
ssh-keyscan -H ${SSH_HOST} >> ~/.ssh/known_hosts
```

### Container Won't Start

```bash

[... truncated to 8KB ...]

```

