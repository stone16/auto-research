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
