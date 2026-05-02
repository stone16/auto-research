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
