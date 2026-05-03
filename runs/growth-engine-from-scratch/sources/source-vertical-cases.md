# source-vertical-cases

Source digest auto-composed from 4 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- lawyer_marketing
- lawyer_finder
- law-intake
- cuilawgroup

---

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


# Repo: law-intake

## README.md
```markdown
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

```

## CLAUDE.md
```markdown
@AGENTS.md

```

## AGENTS.md
```markdown
<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

```

## agents.md
```markdown
<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

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

