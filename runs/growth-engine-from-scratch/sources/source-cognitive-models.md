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
"Str

[... truncated to 2500 bytes; full extract at sources/_raw/growth-engine.md ...]


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
               │ M

[... truncated to 2500 bytes; full extract at sources/_raw/attribution_v2.md ...]


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
- **Reusable Skills** — every solution becomes a reusable skill for the whole team. Deployments, migrations, code reviews — skills compound

[... truncated to 2500 bytes; full extract at sources/_raw/multica.md ...]


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
~/.optiminds/scripts

[... truncated to 2500 bytes; full extract at sources/_raw/optiminds-repo-template.md ...]


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
- Consult official docs before i

[... truncated to 2500 bytes; full extract at sources/_raw/lawyer_finder.md ...]


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
# Dashboard l

[... truncated to 2500 bytes; full extract at sources/_raw/openfang.md ...]


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
pnpm install          # Install dep

[... truncated to 2500 bytes; full extract at sources/_raw/claw-mu.md ...]


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
- Don't start new

[... truncated to 2500 bytes; full extract at sources/_raw/cuilawgroup.md ...]


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

##

[... truncated to 2500 bytes; full extract at sources/_raw/lawyer_marketing.md ...]

