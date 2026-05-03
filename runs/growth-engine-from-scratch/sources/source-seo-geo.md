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
- Backlink analysis and management
- Competitor analysis
- AI-powered SEO strategy advisor
- Support for file uploads for enhanced analysis

## Troubleshooting

- If you encounter issues with API access, check your credentials and API keys
- For connection issues between layers, ensure all three components are running
- Check the console logs of each component for specific error messages

## Development

The codebase is organized as follows:

- `v2-ui`: Frontend code
- `v2-mcp`: Google Ads API integration
- `v2-ai`: FastAPI backend and AI processing
  - `api/`: API endpoints and core functionality
  - `features/`: Feature-specific modules, including SEO campaigns
  - `agents/`: AI agent implementations


```


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
├── tsconfig.json         # TypeScript configuration
└── vite.config.ts        # Vite configuration
```

## Google Analytics Integration

The application is integrated with Google Analytics 4 (GA4) to track user interactions and gain insights into user behavior.

### Implementation Details

1. **GA4 Configuration**
   - The Google Analytics tracking ID (`G-RF6K20FCM8`) is configured in two places:
     - In `client/index.html` via the standard Google Analytics script
     - In `client/src/App.tsx` via the `AnalyticsProvider` component

2. **Analytics Architecture**
   - `client/src/lib/analytics.ts`: Core analytics utility functions
   - `client/src/lib/analytics-provider.tsx`: React context provider that initializes GA
   - `client/src/hooks/useAnalytics.ts`: Custom hook for tracking events throughout the application

3. **Tracked Events**
   The application tracks the following events:
   - Page views
   - Navigation events
   - Search queries and search result clicks
   - Category clicks
   - Product view events
   - UI interactions (mobile menu toggle, etc.)

4. **Testing Analytics Locally**
   When testing locally:
   - GA tracking code executes but data may not appear in your GA reports
   - GA typically filters out localhost traffic
   - Use Google Analytics Debugger extension or browser developer tools to verify tracking calls
   - Check Network tab for requests to `www.google-analytics.com`

5. **Customizing Analytics**
   To modify the tracking ID:
   - Update the `GA_MEASUREMENT_ID` constant in `client/src/App.tsx`
   - Update the measurement ID in the script tags in `client/index.html`

### Adding New Tracking Events

To add tracking for new user interactions:

1. Import the `useAnalytics` hook:
   ```tsx
   import { useAnalytics } from '@/hooks/useAnalytics';
   ```

2. Use the appropriate tracking method:
   ```tsx
   const { trackEvent, trackPageView } = useAnalytics();
   
   // Track a custom event
   trackEvent('my_custom_event', {
     event_category: 'User Engagement',
     event_label: 'Custom Interaction'
   });
   ```

## SEO Features

The application includes built-in SEO features to improve search engine indexability and visibility.

### Sitemap and Robots.txt

The site automatically generates and serves a `sitemap.xml` and `robots.txt` file to help search engines discover and index all pages.

1. **Implementation Details**
   - Dynamic sitemap generation based on available categories
   - Static routes (home, about, contact, trending) included in sitemap
   - Catego

[... truncated to 5000 bytes; full extract at sources/_raw/rankncompare.md ...]


# Repo: rankncompare_v2

## README.md
```markdown
# rankncompare_v2
Rank and Compare 2.0

```


# Repo: seo-poster

