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
| SSH User      | `getuai_dev`                                                     |
| Frontend Port | `8085` (nginx → serves SPA + proxies API/WS to backend)         |
| Backend Port  | `3457` (internal, not exposed to host)                           |
| Project Path  | `/home/getuai_dev/projects/geo-seo-v2`                           |
| Compose File  | `docker/docker-compose.staging.yml`                              |
| Compose Name  | `geo-seo-v2` (via `-p geo-seo-v2`)                              |
| DB Host       | `20.59.118.120:32476`                                            |
| Git Remote    | `git@github.com:Optiminds-Inc/geo-seo-v2.git` (alias: `origin`) |
| Git Branch    | `content`                                                        |
| Domain        | `geocontent.previewapps.org`                                     |
| Access URL    | `https://geocontent.previewapps.org` (also `http://20.228.94.67:8085`) |

## ⚠️ Co-located Services

This server also runs **lawyer_marketing** (Caddy on 80/443, app on 3456). Do NOT touch:
- `docker-app-1` / `docker-caddy-1` containers
- Ports 80, 443
- `/home/getuai_dev/projects/lawyer_marketing/`

## Deployment Steps

Execute these steps sequentially. Stop and report on any failure.

### 1. Push Local Code

```bash
cd d:/work-projects/geo-seo-v2
git push origin content
```

If there are uncommitted changes, warn the user before pushing.

### 2. Pull on Server

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && git pull origin content"
```

### 3. Sync Gitignored Config Files

These files are NOT tracked by git. Compare local versions with server versions and upload if they differ.
**Always do this before rebuilding containers** — frontend env vars are baked into the Vite build, backend env vars are read at runtime.

```bash
# Sync backend env (read at runtime by docker-entrypoint.sh)
scp d:/work-projects/geo-seo-v2/backend/.env.staging getuai_dev@20.228.94.67:~/projects/geo-seo-v2/backend/.env.staging

# Sync Claude Code settings
scp d:/work-projects/geo-seo-v2/backend/claudecode-setting.json getuai_dev@20.228.94.67:~/projects/geo-seo-v2/backend/claudecode-setting.json
```

If the local file does not exist or is unchanged, skip the corresponding scp.

### 4. Rebuild & Restart Containers

Run in background (takes ~3-4 minutes):

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml up -d --build"
```

Monitor build progress by reading the terminal output. Key milestones:

- `geo-seo-v2-backend` — pip install Python deps (~60s)
- `geo-seo-v2-frontend` — npm ci + vite build (~30s)
- `exporting to image` — final export (~30s)
- `Container geo-seo-v2-backend-1 Started` — backend done
- `Container geo-seo-v2-frontend-1 Started` — frontend done

### 5. Reload Caddy (Refresh Upstream DNS)

After container rebuild, container IPs change. Caddy caches DNS, so reload to prevent 504 errors:

```bash
ssh getuai_dev@20.228.94.67 "docker exec docker-caddy-1 caddy reload --config /etc/caddy/Caddyfile"
```

### 6. Verify Deployment

```bash
# Check containers are running (should see geo-seo-v2-backend-1 and geo-seo-v2-frontend-1)
ssh getuai_dev@20.228.94.67 "docker ps"

# Check backend logs for successful startup
ssh getuai_dev@20.228.94.67 "docker logs geo-seo-v2-backend-1 --tail 15"

# Check frontend/nginx logs
ssh getuai_dev@20.228.94.67 "docker logs geo-seo-v2-frontend-1 --tail 10"
```

Expected healthy backend log output:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3457 (Press CTRL+C to quit)
🗄️ Database pool initialized
👤 Admin user seeded: admin
🚀 Backend started on port 3457
```

### 7. Health Check

```bash
# Frontend (SPA)
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8085

# API proxy (login endpoint)
curl -s -o /dev/null -w '%{http_code}' http://20.228.94.67:8085/api/auth/login -X POST -H 'Content-Type: application/json' -d '{"username":"test","password":"test"}'
```

Expected: both return `200` (login returns 200 even with wrong credentials — returns error JSON).

### 8. Verify lawyer_marketing Unaffected

```bash
curl -s -o /dev/null -w '%{http_code}' https://lawyer.getu.ai
```

Expected: `200`

## Gitignored Server Config Files

These files exist on the server but are NOT in git. Preserve them during any destructive operations:

- `backend/.env.staging` — staging database URL, API keys
- `backend/claudecode-setting.json` — Claude Code settings

If a fresh clone is needed, back up these files first:

```bash
ssh getuai_dev@20.228.94.67 "mkdir -p /tmp/geo_seo_backup && \
  cp ~/projects/geo-seo-v2/backend/.env.staging /tmp/geo_seo_backup/ && \
  cp ~/projects/geo-seo-v2/backend/claudecode-setting.json /tmp/geo_seo_backup/"
```

## Troubleshooting

### Container Won't Start

```bash
ssh getuai_dev@20.228.94.67 "docker logs geo-seo-v2-backend-1 --tail 50"
ssh getuai_dev@20.228.94.67 "docker logs geo-seo-v2-frontend-1 --tail 50"
```

### Force Full Rebuild (no cache)

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml build --no-cache && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml up -d"
```

### Rollback to Previous Image

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && git log --oneline -5"
# Then reset to desired commit
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && git checkout <commit-hash> && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml up -d --build"
```

### Run Alembic Migrations Only

Migrations auto-run on container start. To manually run:

```bash
ssh getuai_dev@20.228.94.67 "docker exec geo-seo-v2-backend-1 python -m alembic -c /app/backend/alembic.ini upgrade head"
```

### Restart Without Rebuild

```bash
ssh getuai_dev@20.228.94.67 "cd ~/projects/geo-seo-v2 && docker compose -p geo-seo-v2 -f docker/docker-compose.staging.yml restart"
```

## Caddy Reverse Proxy

Caddy (from lawyer_marketing stack) proxies `geocontent.previewapps.org` → `geo-seo-v2-frontend-1:80` via the `shared-proxy` Docker network.

- Caddyfile location: `~/projects/lawyer_marketing/docker/Caddyfile`
- Both compose files declare `shared-proxy` as an external network
- Caddy auto-provisions TLS certificates via Let's Encrypt

After changing the Caddyfile:

```bash
ssh getuai_dev@20.228.94.67 "docker exec docker-caddy-1 caddy reload --config /etc/caddy/Caddyfile"
```

## Azure NSG

Port 8085 is open via NSG rule `geo-seo-v2` (priority 330) on `claw-mu-nsg` in resource group `ADS`.

```bash
# Verify rule exists
az network nsg rule show --resource-group ADS --nsg-name claw-mu-nsg --name geo-seo-v2 --output table
```

```
