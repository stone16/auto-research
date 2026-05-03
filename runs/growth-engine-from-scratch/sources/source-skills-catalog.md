# source-skills-catalog

Source digest auto-composed from 10 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- openclaw-mu
- lawyer_finder
- lawyer_marketing
- getu_ads_v2
- optiminds-repo-template
- attribution_v2
- openfang
- geo-seo-v2
- OpenBox
- clawcloud

---

# Repo: openclaw-mu

## README.md
```markdown
# 🦞 OpenClaw — Personal AI Assistant

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text-dark.png">
        <img src="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text.png" alt="OpenClaw" width="500">
    </picture>
</p>

<p align="center">
  <strong>EXFOLIATE! EXFOLIATE!</strong>
</p>

<p align="center">
  <a href="https://github.com/openclaw/openclaw/actions/workflows/ci.yml?branch=main"><img src="https://img.shields.io/github/actions/workflow/status/openclaw/openclaw/ci.yml?branch=main&style=for-the-badge" alt="CI status"></a>
  <a href="https://github.com/openclaw/openclaw/releases"><img src="https://img.shields.io/github/v/release/openclaw/openclaw?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="https://discord.gg/clawd"><img src="https://img.shields.io/discord/1456350064065904867?label=Discord&logo=discord&logoColor=white&color=5865F2&style=for-the-badge" alt="Discord"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
</p>

## OpenClawMU — Multi-Tenant Fork

> **This is OpenClawMU**, a multi-tenant fork of [OpenClaw](https://github.com/openclaw/openclaw) that adds enterprise-grade multi-tenancy support.

### What OpenClawMU Adds

OpenClawMU extends OpenClaw with complete tenant isolation, allowing multiple users to share a single gateway instance while maintaining strict data separation:

- **Tenant Authentication** — Secure token-based auth with SHA-256 hashed storage and timing-safe comparison
- **Data Isolation** — Separate sessions, memory, plugins, sandboxes, and config per tenant
- **Web Terminal** — Browser-based terminal access to tenant sandboxes via xterm.js
- **Tenant Cron** — Isolated scheduled jobs per tenant
- **Skills & Config** — Per-tenant skill installation and configuration overlays
- **Usage Tracking** — Token usage, cost tracking, and quota enforcement
- **S3 Backup/Restore** — Backup tenant data to S3-compatible storage
- **HTTP API Scoping** — OpenAI and OpenResponses endpoints scoped to tenant sessions
- **Device/Node Pairing** — Tenant-isolated device and node pairing

### Quick Start (Multi-Tenant)

```bash
# Create a tenant
openclaw tenants create demo

# Connect as tenant
OPENCLAW_GATEWAY_TOKEN="tenant:demo:xxxxx" openclaw chat
```

Full documentation: [docs/multi-tenancy/README.md](docs/multi-tenancy/README.md)

---

**OpenClaw** is a _personal AI assistant_ you run on your own devices.
It answers you on the channels you already use (WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, Microsoft Teams, WebChat), plus extension channels like BlueBubbles, Matrix, Zalo, and Zalo Personal. It can speak and listen on macOS/iOS/Android, and can render a live Canvas you control. The Gateway is just the control plane — the product is the assistant.

If you want a personal, single-user assistant that feels local, fast, and always-on, this is it.

[Website](https://openclaw.ai) · [Docs](https://docs.openclaw.ai) · [DeepWiki](https://deepwiki.com/openclaw/openclaw) · [Getting Started](https://docs.openclaw.ai/start/getting-started) · [Updating](https://docs.openclaw.ai/install/updating) · [Showcase](https://docs.openclaw.ai/start/showcase) · [FAQ](https://docs.openclaw.ai/start/faq) · [Wizard](https://docs.openclaw.ai/start/wizard) · [Nix](https://github.com/openclaw/nix-openclaw) · [Docker](https://docs.openclaw.ai/install/docker) · [Discord](https://discord.gg/clawd)

Preferred setup: run the onboarding wizard (`openclaw onboard`) in your terminal.
The wizard guides you step by step through setting up the gateway, workspace, channels, and skills. The CLI wizard is the recommended path and works on **macOS, Linux, and Windows (via WSL2; strongly recommended)**.
Works with npm, pnpm, or bun.
New install? Start here: [Getting started](https://docs.openclaw.ai/start/getting-started)

**Subscriptions (OAuth):**

- **[Anthropic](https://www.anthropic.com/)** (Claude Pro/Max)
- **[OpenAI](https://openai.com/)** (ChatGPT/Codex)

Model note: while any model is supported, I strongly recommend **Anthropic Pro/Max (100/200) + Opus 4.6** for long‑context strength and better prompt‑injection resistance. See [Onboarding](https://docs.openclaw.ai/start/onboarding).

## Models (selection + auth)

- Models config + CLI: [Models](https://docs.openclaw.ai/concepts/models)
- Auth profile rotation (OAuth vs API keys) + fallbacks: [Model failover](https://docs.openclaw.ai/concepts/model-failover)

## Install (recommended)

Runtime: **Node ≥22**.

```bash
npm install -g openclaw@latest
# or: pnpm add -g openclaw@latest

openclaw onboard --install-daemon
```

The wizard installs the Gateway daemon (launchd/systemd user service) so 

[... truncated to 5000 bytes; full extract at sources/_raw/openclaw-mu.md ...]


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
Ki

[... truncated to 5000 bytes; full extract at sources/_raw/lawyer_finder.md ...]


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
- **Agent**: claude-agent-sdk for AI chat ses

[... truncated to 5000 bytes; full extract at sources/_raw/lawyer_marketing.md ...]


# Repo: getu_ads_v2

## README.md
```markdown
# getu_ads_v2
getu ads v2

```

## skills/google-ads-cli/SKILL.md
```markdown
---
name: google-ads-cli
description: >
  Google Ads Search Campaign CLI for automated campaign management via shell commands.
  Provides 38 operations covering campaigns, ad groups, keywords, RSA ads, budgets, criteria,
  composite creation, reporting, and GAQL query building/validation/execution.
  Use when an agent needs to create/update/list/remove Google Ads resources, run performance
  reports, build full campaign structures end-to-end, discover API fields/resources,
  programmatically construct GAQL queries, or validate and execute arbitrary GAQL.
  Triggers on: google ads, create campaign, manage ads, ad group, keyword management,
  RSA ad, budget update, campaign report, search terms, GAQL query, GAQL build, GAQL validate,
  field discovery, resource discovery, composite create, google ads cli, exec run operation.
---

# Google Ads CLI

A standalone CLI for managing Google Ads Search campaigns. Designed for agent automation
via a unified `exec run` interface that accepts JSON payloads and returns structured JSON.

## Invocation

```bash
echo '<json_payload>' | python -m google_ads_cli exec run \
  --operation <operation_name> --stdin --compact \
  -c <path_to>/config.yaml
```

Or with a file:

```bash
python -m google_ads_cli exec run \
  --operation <operation_name> -f payload.json --compact \
  -c <path_to>/config.yaml
```

### Key Flags

| Flag | Description |
|------|-------------|
| `--operation` | Operation identifier (e.g. `search.campaign.create`) |
| `--stdin` | Read JSON payload from stdin |
| `-f, --file` | Read payload from JSON/YAML file |
| `-c, --config` | Path to config.yaml with credentials |
| `--compact` | Single-line JSON output (recommended for agents) |
| `--format` | Output format: `json` (default) or `yaml` |
| `-o, --output` | Write output to file instead of stdout |

### Response Format

All operations return a `ResultEnvelope`:

```json
{
  "success": true,
  "command": "exec search.campaign.list",
  "result": { ... },
  "elapsed_ms": 2239.9
}
```

On failure: `success: false`, `errors: [...]`, exit code `1`.

### Error Discovery

Pass an unknown operation to list all available operations:

```bash
echo '{}' | python -m google_ads_cli exec run --operation help --stdin --compact -c config.yaml
```

## Available Operations (38)

| Scenario | Ops | Detail | Key operations |
|----------|-----|--------|----------------|
| Campaign Management | 6 | [campaign.md](references/campaign.md) | `search.campaign.create`, `list`, `find`, `update`, `update_bidding`, `copy` |
| Ad Group Management | 5 | [ad_group.md](references/ad_group.md) | `search.ad_group.create`, `list`, `find`, `update_status`, `remove` |
| Keyword Management | 3 | [keyword.md](references/keyword.md) | `search.keyword.add`, `list`, `remove` |
| Ad / RSA Creative | 7 | [ad.md](references/ad.md) | `search.ad.create_rsa`, `get_rsa`, `update_rsa`, `update_status`, `list`, `remove`, `copy_rsa` |
| Targeting & Budget | 5 | [targeting.md](references/targeting.md) | `search.budget.update`, `search.criteria.add`, `list`, `remove`, `add_negatives` |
| Composite Build | 2 | [composite.md](references/composite.md) | `search.composite.create_full`, `create_groups` |
| Reporting | 4 | [report.md](references/report.md) | `report.campaign`, `ad`, `search_terms`, `gaql` |
| GAQL Builder | 6 | [gaql.md](references/gaql.md) | `gaql.resources`, `fields`, `field`, `build`, `validate`, `run` |

Click the **Detail** link for payload schemas and examples of each operation.
For a quick decision guide, see [references/operations.md](references/operations.md).

## Quick Examples

### List enabled campaigns

```bash
echo '{"campaign_type":"SEARCH","status_filter":"ENABLED"}' | \
  python -m google_ads_cli exec run --operation search.campaign.list --stdin --compact -c config.yaml
```

### Create a full campaign structure in one shot

```bash
python -m google_ads_cli exec run \
  --operation search.composite.create_full -f full_campaign.json --compact -c config.yaml
```

### Get campaign performance report

```bash
echo '{"date_range":"LAST_7_DAYS"}' | \
  python -m google_ads_cli exec run --operation report.campaign --stdin --compact -c config.yaml
```

### Run custom GAQL query

```bash
echo '{"query":"SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = '\''ENABLED'\'' LIMIT 10"}' | \
  python -m google_ads_cli exec run --operation report.gaql --stdin --compact -c config.yaml
```

### Build and execute GAQL programmatically

```bash
echo '{"resource":"campaign","fields":["campaign.id","campaign.name","metrics.clicks"],"conditions":["campaign.status = '\''ENABLED'\''"],"order_by":"metrics.clicks DESC","limit":10,"date_range":"LAST_30_DAYS"}' | \
  python -m google_ads_cli exec run --operation gaql.build --stdin --compact -c config.yaml
```

### Discover available fields for a resource

```bash
echo '{"r

[... truncated to 5000 bytes; full extract at sources/_raw/getu_ads_v2.md ...]


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
| `.github/workflows/codex-review.yml` | 3-pass Codex AI review

[... truncated to 5000 bytes; full extract at sources/_raw/optiminds-repo-template.md ...]


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
- **Met

[... truncated to 5000 bytes; full extract at sources/_raw/attribution_v2.md ...]


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
| **Researcher** | Deep autonomous researcher. Cross-references multiple sources, evaluates credibility using CRAAP criteria (Currency, Relevance, Authority, Accuracy,

[... truncated to 5000 bytes; full extract at sources/_raw/openfang.md ...]


# Repo: geo-seo-v2

## README.md
```markdown
# geo-seo-v2
```

## .cursor/skills/commit-push-deploy/SKILL.md
```markdown
---
name: commit-push-deploy
description: Commit all uncommitted changes, push to origin, and deploy to staging in one flow. Use when the user says "提交推送部署", "提交代码推送后再部署staging", "commit push deploy", "push and deploy", or any combination of commit/push/deploy in a single request.
---

# Commit → Push → Deploy Staging (One-Shot)

Full workflow that commits local changes, pushes to `origin/content`, and deploys to the staging server.

## Prerequisites

- Local workspace: `d:/work-projects/geo-seo-v2`
- Branch: `content`
- Staging skill at `.cursor/skills/deploy-staging/SKILL.md` has infra details

## Workflow

Execute steps sequentially. Stop and report on any failure.

### Step 1: Check Local State

```bash
cd /d/work-projects/geo-seo-v2
git status -sb
git diff --stat
```

- If working tree is clean and branch is up to date with origin → skip to Step 4 (deploy only)
- If there are uncommitted changes → continue to Step 2

### Step 2: Commit

```bash
git add <all modified and untracked files listed in status>
git commit -m "<conventional commit message based on changed files>"
```

Commit message rules:
- Use conventional commits: `feat`, `fix`, `refactor`, `chore`, etc.
- Scope from the primary area changed (e.g. `content-agent`, `frontend`, `articles`)
- Brief summary of what changed

### Step 3: Push

```bash
git push origin content
```

If push fails (e.g. rejected), warn the user and stop.

### Step 4: Server Pull + Config Sync

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && git pull origin content"
```

Sync gitignored config files (always, they may have changed locally):

```bash
scp d:/work-projects/geo-seo-v2/backend/.env.staging getuai_dev@20.228.94.67:~/projects/geo-seo-v2/backend/.env.staging
scp d:/work-projects/geo-seo-v2/backend/claudecode-setting.json getuai_dev@20.228.94.67:~/projects/geo-seo-v2/backend/claudecode-setting.json
```

### Step 5: Docker Rebuild

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml up -d --build"
```

- Set `block_until_ms: 360000` (up to 6 min)
- If frontend build fails (e.g. TypeScript error), fix the error locally, commit the fix, push again, pull on server, and retry the build

### Step 6: Caddy Reload

Container IPs change after rebuild. Reload Caddy to refresh upstream DNS:

```bash
ssh getuai_dev@20.228.94.67 "docker exec docker-caddy-1 caddy reload --config /etc/caddy/Caddyfile"
```

### Step 7: Verify

Run these together:

```bash
# Backend logs
ssh getuai_dev@20.228.94.67 "docker logs geo-seo-v2-backend-1 --tail 12"

# SPA health
curl -s -o /dev/null -w 'SPA: %{http_code}\n' http://20.228.94.67:8085
```

Expected:
- Backend log contains `🚀 Backend started on port 3457`
- SPA returns `200`

### Step 8: Report

Summarize in a table:

| Item | Result |
|------|--------|
| Commit | `<hash>` — `<message>` |
| Push | `origin/content` updated |
| Server pull | Fast-forward to `<hash>` |
| Docker build | Success / Fail |
| Caddy reload | Done |
| Backend | 🚀 Started |
| SPA | 200 |

Include the public URL: `https://geocontent.previewapps.org`

## Error Recovery

### TypeScript Build Failure

If `docker compose ... --build` exits with code 1 and the frontend builder shows a TS error:

1. Read the error message (file + line)
2. Fix the issue locally
3. `git add <file> && git commit -m "fix: <describe TS error>"`
4. `git push origin content`
5. `ssh ... "git pull origin content"`
6. Retry `docker compose ... up -d --build`

### .env.staging Changed But Containers Already Running

If only `.env.staging` was updated (no code change), force-recreate backend without rebuilding:

```bash
scp d:/work-projects/geo-seo-v2/backend/.env.staging getuai_dev@20.228.94.67:~/projects/geo-seo-v2/backend/.env.staging
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml up -d --no-build --force-recreate backend"
ssh getuai_dev@20.228.94.67 "docker exec docker-caddy-1 caddy reload --config /etc/caddy/Caddyfile"
```

```

## .cursor/skills/deploy-staging/SKILL.md
```markdown
---
name: geo-seo-v2-deploy
description: Deploy the geo-seo-v2 project to staging server (20.228.94.67:8085). Use when the user asks to "deploy", "deploy to staging", "publish to staging", "update staging", "release to staging", or mentions "geo-seo-v2 deployment". Handles git push, SSH into server, git pull, docker rebuild, and health verification.
---

# GEO SEO v2 — Staging Deployment

## Infrastructure

| Item          | Value                                                            |
| ------------- | ---------------------------------------------------------------- |
| Server IP     | `20.228.94.67`                                                   |
| SSH User      | `getua

[... truncated to 5000 bytes; full extract at sources/_raw/geo-seo-v2.md ...]


# Repo: OpenBox

## .cursor/skills/gke-full-deploy/SKILL.md
```markdown
---
name: gke-full-deploy
description: Full GKE deployment of OpenBox from scratch. Use when setting up a new GKE cluster, doing a fresh deployment, or migrating OpenBox to a new environment.
---

# GKE 全新部署

从零将 OpenBox 部署到 GKE 集群的完整流程。

## 架构概览

```
同一个 GKE 集群
├── Namespace: openbox              ← 应用层
│   ├── Backend Deployment (FastAPI)
│   ├── Frontend Deployment (Nginx)
│   ├── Ingress (对外入口 + HTTPS)
│   └── Secret (凭证)
└── Namespace: openbox-sandbox      ← 沙箱层
    ├── Pod sandbox-{user_id}       ← 动态创建
    ├── Service sandbox-{user_id}
    └── PVC workspace-{user_id}     ← 持久化存储
```

## 前置条件

- [ ] `gcloud` CLI 已安装并认证
- [ ] `kubectl` 已安装
- [ ] Docker 已安装
- [ ] 拥有域名 DNS 管理权限
- [ ] 准备好以下凭证（不要写入代码或 skill）：
  - PostgreSQL 连接串
  - Redis URL（密码中特殊字符需 URL 编码）
  - Blob Storage 连接串
  - JWT Secret
  - LLM API Key
  - Search API Key（如 Tavily）

## 部署步骤

### Step 1: 创建 GKE 集群

```bash
gcloud container clusters create <CLUSTER_NAME> \
  --region=<REGION> \
  --num-nodes=1 \
  --machine-type=e2-standard-2 \
  --disk-size=50 \
  --workload-pool=<PROJECT_ID>.svc.id.goog \
  --enable-ip-alias \
  --release-channel=regular \
  --project=<PROJECT_ID>
```

验证连接：`kubectl get nodes`

### Step 2: 创建 Namespace

```bash
kubectl create namespace openbox
kubectl create namespace openbox-sandbox
```

### Step 3: 创建 PostgreSQL 数据库

如果数据库在 GKE 内网，通过集群内 Pod 连接：

```bash
kubectl run pg-client --rm -i --tty --restart=Never --namespace=openbox \
  --image=postgres:16-alpine \
  --command -- psql "<POSTGRES_URL>" -c "CREATE DATABASE openbox;"
```

### Step 4: 构建并推送 Docker 镜像

**必须使用 `--platform linux/amd64`**（GKE 节点是 amd64）。

```bash
gcloud auth configure-docker gcr.io --quiet

# 三个镜像并行构建
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-sandbox:latest ./container
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-backend:latest ./backend
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-frontend:latest ./frontend

# 推送
docker push gcr.io/<PROJECT_ID>/openbox-sandbox:latest
docker push gcr.io/<PROJECT_ID>/openbox-backend:latest
docker push gcr.io/<PROJECT_ID>/openbox-frontend:latest
```

### Step 5: 创建 K8s Secret

**重要**：Redis 密码中的特殊字符 `!@#$%` 等必须 URL 编码。

```bash
kubectl create secret generic openbox-secrets -n openbox \
  --from-literal=DATABASE_URL='<ASYNCPG_URL>' \
  --from-literal=REDIS_URL='<REDIS_URL_ENCODED>' \
  --from-literal=JWT_SECRET='<JWT_SECRET>' \
  --from-literal=SANDBOX_IMAGE='gcr.io/<PROJECT_ID>/openbox-sandbox:latest' \
  --from-literal=OPENBOX_API_KEY='<API_KEY>' \
  --from-literal=BLOB_AZURE_CONNECTION_STRING='<BLOB_CONN>' \
  --from-literal=BLOB_AZURE_CONTAINER='<CONTAINER_NAME>' \
  --from-literal=TAVILY_API_KEY='<TAVILY_KEY>' \
  --from-literal=OPENAI_API_KEY='<OPENAI_KEY>'
```

### Step 6: 创建镜像拉取凭证

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
for NS in openbox openbox-sandbox; do
  kubectl create secret docker-registry gcr-pull-secret -n $NS \
    --docker-server=gcr.io --docker-username=oauth2accesstoken \
    --docker-password="$ACCESS_TOKEN" --docker-email=<EMAIL>
done

# 绑定到 ServiceAccount
kubectl patch serviceaccount default -n openbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
```

### Step 7: 部署 K8s 资源

`k8s/base.yaml` 包含所有资源定义。部署前需：

1. 确认 `BLOB_PROVIDER` 值（azure 或 gcs）
2. 确认环境变量与 Secret key 匹配

```bash
sed "s/PROJECT_ID/<PROJECT_ID>/g" k8s/base.yaml | kubectl apply -f -
```

部署后绑定 imagePullSecret 到创建的 ServiceAccount：

```bash
kubectl patch serviceaccount openbox-backend -n openbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
kubectl patch serviceaccount sandbox-pods -n openbox-sandbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
```

### Step 8: 运行数据库 Migration

```bash
kubectl exec -n openbox deployment/openbox-backend -- uv run alembic upgrade head
```

**注意**：检查 migration 中的列长度是否与 ORM 模型一致（常见问题：`VARCHAR(26)` vs `String(64)`）。如不一致需手动 ALTER。

### Step 9: 配置外部访问（Ingress + HTTPS）

#### 预留静态 IP

```bash
gcloud compute addresses create <APP>-static-ip --global --project=<PROJECT_ID>
gcloud compute addresses describe <APP>-static-ip --global --format='get(address)'
```

#### 创建 ManagedCertificate + Ingress

参考 `.claude/gke-ingress-setup/SKILL.md` 中的完整流程。

[... truncated to 5000 bytes; full extract at sources/_raw/OpenBox.md ...]


# Repo: clawcloud

## README.md
```markdown
# clawcloud
claw on cloud

```

## .cursor/skills/clawcloud-azure-desktop-gallery-pipeline/SKILL.md
```markdown
---
name: clawcloud-azure-desktop-gallery-pipeline
description: Deploy and troubleshoot the ClawCloud Azure desktop runtime built on Ubuntu, KasmVNC, OpenClaw, Compute Gallery, builder VMs, and flexible VMSS. Use when creating or updating the Azure image pipeline, fixing VMSS desktop reachability, wiring OpenClaw gateway access, or reproducing the ClawCloud cloud desktop environment.
---

# ClawCloud Azure Desktop Gallery Pipeline

## Use This Skill When

- Working on `infra/azure/` scripts.
- Publishing a new gallery image for the cloud desktop runtime.
- Creating or repairing the builder VM or flexible VMSS.
- Fixing KasmVNC reachability, iframe embedding, or OpenClaw gateway exposure.
- Wiring backend control plane startup to Azure desktop instances.

## Source Of Truth

- `infra/azure/create_base_resources.sh`
- `infra/azure/create_gallery_image.sh`
- `infra/azure/install_desktop_runtime.sh`
- `infra/azure/create_builder_vm.sh`
- `infra/azure/create_vmss.sh`
- `backend/core/azure_vmss_provider.py`
- `backend/core/control_plane_service.py`

## Current Runtime Shape

- Base network is a single VNet + subnet with a shared NSG.
- Image is published through Azure Compute Gallery.
- A low-spec builder VM is kept for debugging.
- User-facing cloud desktops run on a flexible VMSS.
- Desktop transport is KasmVNC on `8444`.
- OpenClaw gateway is exposed on `18789`.
- Backend issues machine start/stop and desktop session requests, then talks directly to Azure and the remote OpenClaw gateway.

## Default Workflow

1. Verify Azure login and subscription context first.
2. Create or update base resources with `create_base_resources.sh`.
3. Build or refresh the gallery image with `create_gallery_image.sh`.
4. Keep one builder VM available for debugging with `create_builder_vm.sh`.
5. Create or update the flexible VMSS with `create_vmss.sh`.
6. Verify ports:
   - `22`
   - `8444`
   - `18789`
7. Verify runtime health:
   - `https://<ip>:8444`
   - `http://<ip>:18789/health`
8. If embedding the desktop in the frontend, confirm KasmVNC is running with `-disableBasicAuth`.

## Required Deployment Rules

- Prefer project scripts over ad hoc Azure commands.
- Reuse the project NSG instead of letting Azure auto-create NIC NSGs.
- Resolve gallery image version `latest` to the actual latest version name before VM or VMSS creation.
- Keep the builder VM separate from the image-build VM lifecycle.
- Use LF line endings for scripts uploaded to Linux.
- Treat `8444` and `18789` as first-class deployment ports, not optional debug ports.

## Windows Execution Guidance

- On Windows, prefer `powershell.exe -NoProfile -Command "& 'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd' ..."` for Azure CLI automation.
- Avoid mixing Git Bash quoting rules with long `az.cmd` command lines.
- If a backend or script needs Azure CLI from Python, call the executable directly with argument arrays instead of shell-joined strings.
- For SSH and SCP on Windows, rely on executable argument arrays and explicit key paths.

## KasmVNC Rules

- `claw-kasmvnc.service` must start KasmVNC with `-disableBasicAuth` for iframe embedding in the workbench.
- A `401 Unauthorized` on `8444` means basic auth is still enabled and the right-side desktop pane will not embed cleanly.
- After patching the service unit, run:
  - `systemctl daemon-reload`
  - `systemctl restart claw-kasmvnc.service`
- For quick verification, external reachability matters more than local process state.

## OpenClaw Rules

- Gateway default port is `18789`.
- Remote runtime config must enable HTTP responses and chat completions endpoints.
- Backend startup should inject runtime config and env files into `/home/claw/.openclaw/`.
- Backend task dispatch should use the remote gateway only after `/health` is reachable.
- If the desktop is ready but the gateway is not, machine state should not become fully ready.

## Troubleshooting Checklist

- Gallery version stuck in `Creating`:
  - Check Azure activity log.
  - Confirm source managed image succeeded.
  - Continue with the managed image if gallery replication is the only blocker.
- VM or VMSS has public IP but `8444` times out:
  - Check subnet NSG.
  - Check NIC-level auto-created NSG.
  - Confirm the instance inherited or attached the intended NSG.
- `8444` returns `401`:
  - KasmVNC basic auth is still active.
- `18789` is unreachable:
  - NSG rule is missing, or OpenClaw gateway is not healthy.
- Backend can start the machine but chat still behaves like mock:
  - Confirm `CLOUD_MACHINE_PROVIDER=azure_vmss`.
  - Confirm the remote runtime config was pushed successfully.
  - Confirm `/v1/responses` is enabled on the gateway.
- Bash command works badly with Azure CLI on Windows:
  - Move the command to PowerShell or Python subprocess arrays.

## Known Pitfalls To Remember

- CRLF line

[... truncated to 5000 bytes; full extract at sources/_raw/clawcloud.md ...]

