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

