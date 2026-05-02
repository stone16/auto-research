# source-seo-geo

Source digest auto-composed from 8 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- geo-aeo
- geo-seo-v2
- geowriter
- getuai-seo
- rankgale
- rankncompare
- rankncompare_v2
- seo-poster

---

# Repo: geo-aeo


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

Container IPs change after rebuild. Reload Caddy to 

[... truncated to 2500 bytes; full extract at sources/_raw/geo-seo-v2.md ...]


# Repo: geowriter

## README.md
```markdown
# geo-seo-v2
pr test

```


# Repo: getuai-seo

## README.md
```markdown
# GetUAI SEO Assistant

This application provides a comprehensive interface for managing and analyzing SEO campaigns. The system is built with a three-layer architecture:

1. **UI Layer** - Frontend interface for user interaction
2. **MCP Layer** - Middle layer for SEO tools and API integration
3. **AI Layer** - Backend for intelligent processing and recommendations

## System Requirements

- Node.js (v16+)
- Python (v3.9+)
- npm or yarn

## Environment Setup

Before running the application, make sure you have the following environment variables set:

```
DEEPSEEK_API_BASE_URL=<deepseek-api-url>
DEEPSEEK_API_KEY=<your-deepseek-api-key>
```

## Installation

Clone the repository and install dependencies for each component:

```bash
# Clone the repository
git clone <repository-url>
cd getuai-seo

# Install UI dependencies
cd v2-ui
npm install

# Install MCP layer dependencies
cd ../v2-mcp-seo
pip install -r requirements.txt

# Install AI layer dependencies
cd ../v2-ai
pip install -r requirements.txt
```

## Running the Application

The application consists of three components that need to run simultaneously. Open three separate terminal windows to run each component:

### 1. Frontend (UI Layer)

```bash
cd v2-ui
npm run dev
```

This will start the UI layer, typically accessible at `http://localhost:3000`.

### 2. MCP Layer (SEO Tools Integration)

```bash
cd v2-mcp-seo

# Development 
# You need to create a `.env.development`, otherwise it will read from the default `.env`
python -m main

# Production
python -m main --env=production
```

This starts the MCP (Micro Control Program) layer that interfaces with various SEO tools and APIs, typically running on port 8004.

### 3. AI Layer (Backend Processing)

```bash
cd v2-ai

# Development:
# You need to create a `.env.development`, otherwise it will read from the default `.env`
python -m main

# Production:
python -m main --env=production
```

This launches the AI backend with hot reload enabled, typically accessible at `http://localhost:8000`.

## Architecture Overview

- **v2-ui**: React-based frontend that provides the user interface
- **v2-mcp-seo**: Python-based middleware that handles SEO tools and API integration
- **v2-ai**: FastAPI backend that processes requests, manages sessions, and provides AI-powered recommendations

## Key Features

- SEO performance metrics and analysis
- Keyword research and tracking
- Content optimization recommendations
- Backlink

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-seo.md ...]


# Repo: rankgale


# Repo: rankncompare

## README.md
```markdown
# Rank&Compare

A web application for comparing and ranking products across different categories.

## Project Overview

Rank&Compare is a full-stack web application built with React and Express that allows users to compare products across different categories. The application features a clean, modern UI built with Tailwind CSS and Shadcn UI components.

## Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- Shadcn UI components (Radix UI)
- Vite (for building and development)
- React Query (for data fetching)
- React Hook Form (for form handling)
- Wouter (for routing)

### Backend
- Node.js
- Express
- JSON data storage
- Zod (for validation)

### DevOps
- Nginx (for production deployment)
- Node.js scripts for build and deployment

## Project Structure

```
rankncompare/
├── client/               # Frontend code
│   ├── dist/             # Built client assets
│   ├── public/           # Static assets
│   ├── src/              # Source code
│       ├── components/   # UI components
│       ├── hooks/        # Custom React hooks
│       ├── lib/          # Utility functions
│       ├── pages/        # Page components
│       ├── App.tsx       # Main application component
│       └── main.tsx      # Entry point
├── data/                 # JSON data for the application
├── server/               # Backend code
│   ├── index.ts          # Main server file
│   ├── category-api.ts   # Category API handlers
│   ├── seo-api.ts        # SEO metadata API handlers
│   ├── seo-routes.ts     # Sitemap and robots.txt routes
│   ├── sitemap-generator.ts # Sitemap and robots.txt generator
│   └── storage.ts        # Data storage operations
├── server-dist/          # Built server code
├── shared/               # Shared code between client and server
│   └── types.ts          # TypeScript types
├── scripts/              # Build and utility scripts
│   ├── build-search-index.js # Search index builder
│   └── generate-seo-files.ts # SEO files generator
├── nginx.conf            # Nginx configuration for deployment
├── package.json          # Project dependencies and scripts
├── start.sh              # Startup script
├── tailwind.config.ts    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript con

[... truncated to 2500 bytes; full extract at sources/_raw/rankncompare.md ...]


# Repo: rankncompare_v2

## README.md
```markdown
# rankncompare_v2
Rank and Compare 2.0

```


# Repo: seo-poster

