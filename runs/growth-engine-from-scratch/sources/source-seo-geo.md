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
   - Category pages prioritized (0.9 priority) for better indexing
   - Standard robots.txt with reference to sitemap location

2. **File Generation**
   - Files are automatically generated during the build process
   - Generated files are stored in `client/dist` directory
   - Server routes provide access at `/sitemap.xml` and `/robots.txt`
   - The generation script is located at `scripts/generate-seo-files.ts`

3. **Build Integration**
   - The `npm run build` command includes sitemap and robots.txt generation
   - Individual generation via `npm run build:seo-files`

4. **Customization**
   - Modify site URL in `server/sitemap-generator.ts`
   - Adjust priority and change frequency in the same file
   - Add additional static routes to the `STATIC_ROUTES` array

This implementation ensures search engines can discover all pages of the application, including dynamically generated category pages, which helps improve visibility in search results.

## SEO Improvements

The following SEO improvements have been implemented to enhance search engine visibility and user experience:

1. **Improved Meta Tags**
   - Standardized meta titles and descriptions with optimal length (under 60/160 characters)
   - Consistent meta tag formatting across all pages
   - Enhanced keyword coverage while maintaining readability

2. **Technical SEO**
   - Fixed viewport meta tag for better accessibility
   - Standardized canonical URLs to prevent duplicate content issues
   - Improved robots meta tag format

3. **Structured Data**
   - Added breadcrumb schema markup for improved navigation in search results
   - Implemented FAQ schema markup for each category
   - Enhanced product schema with detailed rating information

4. **On-Page Elements**
   - Added visible breadcrumb navigation for improved user experience
   - Added dynamically generated FAQs for each category
   - Consistently formatted title tags for better branding

5. **Site Structure**
   - Improved internal linking between categories
   - Enhanced sitemap.xml and robots.txt generation

These improvements follow SEO best practices to increase visibility in search results while providing a better user experience.

## Prerequisites

- Node.js 16+ (LTS recommended)
- npm or yarn

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rankncompare.git
   cd rankncompare
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   NODE_ENV=development
   SESSION_SECRET=your_session_secret
   ```

4. **Build the search index**
   ```bash
   npm run build:search-index
   ```
   This step is necessary if you're using the search functionality.

5. **Start the development server**
   ```bash
   npm run dev
   ```
   This will start both the client and server in development mode.

   Alternatively, you can run client and server separately:
   ```bash
   npm run client-dev  # Start client (vite dev server)
   npm run api-dev     # Start API server
   ```

6. **Open the application**
   The application will be available at http://localhost:3000

## Building for Production

1. **Build the search index (if using search functionality)**
   ```bash
   npm run build:search-index
   ```

2. **Build the client and server**
   ```bash
   npm run build
   ```
   This will:
   - Build the search index
   - Build the client assets to `client/dist`
   - Generate sitemap.xml and robots.txt
   - Bundle the server code to `server-dist`

3. **Generate SEO files separately (if needed)**
   ```bash
   npm run build:seo-files
   ```
   This will generate sitemap.xml and robots.txt based on the current data.

4. **Start the production server**
   ```bash
   npm run start
   ```
   This will run the application in production mode.

## Deployment to a Remote Server with Nginx

### Prerequisites
- A server with Ubuntu/Debian
- Node.js 16+ installed
- Nginx installed
- Domain name pointed to your server

### Setup Steps

1. **Clone the repository on your server**
   ```bash
   git clone https://github.com/yourusername/rankncompare.git
   cd rankncompare
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file with production settings:
   ```
   NODE_ENV=production
   SESSION_SECRET=your_production_secret
   ```

4. **Build the search index**
   ```bash
   npm run build:search-index
   ```
   This step is necessary for search functionality to work properly.

5. **Build the application**
   ```bash
   npm run build
   ```

6. **Configure Nginx**
   Copy the provided nginx.conf to your server:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/rankncompare
   ```

   Create a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/rankncompare /etc/nginx/sites-enabled/
   ```

   Edit the Nginx configuration to match your domain and file paths:
   ```bash
   sudo nano /etc/nginx/sites-available/rankncompare
   ```

   Test and restart Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **Set up a process manager (PM2 recommended)**
   ```bash
   sudo npm install -g pm2
   pm2 start server-dist/index.js --name rankncompare
   pm2 save
   pm2 startup
   ```

8. **Enable SSL with Let's Encrypt (optional but recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d rankncompare.com -d www.rankncompare.com
   ```

9. **Monitor the application**
   ```bash
   pm2 logs rankncompare
   ```

## Data Management

The application uses JSON files stored in the `data` directory to manage product and category information.

### Data Manager Script

The project includes a comprehensive data management script (`scripts/data_manager.py`) that helps maintain data consistency and manage content. This Python utility ensures that categories are properly ordered, products are correctly positioned, and trending data stays in sync.

#### Features

- **Data Validation**: Verify that categories are alphabetically ordered, products have valid category IDs and positions, and trending data matches source items
- **Data Fixing**: Automatically fix inconsistencies in category ordering, product positions, and trending data
- **Content Management**: Add new categories, products, and trending items through an interactive interface
- **Data Integrity**: Ensure products have proper ratings, positions, and IDs that align with their ranking within categories

#### Usage

```bash
# Verify data consistency
python scripts/data_manager.py --verify

# Fix data inconsistencies
python scripts/data_manager.py --fix

# Add a new category
python scripts/data_manager.py --add-category

# Add a new product
python scripts/data_manager.py --add-product

# Add a product or category to trending
python scripts/data_manager.py --add-trending

# Interactive mode (menu-driven interface)
python scripts/data_manager.py
```

The script maintains relationships between the three main JSON data files:
- `data/categories.json`: Categories with properties like name, slug, icon, and color
- `data/products.json`: Products with ratings, positions, features, pros, and cons
- `data/trending.json`: Trending products and categories with scores and metadata

When fixing data, the script ensures:
1. Categories are sorted alphabetically by name with sequential IDs
2. Product IDs align with their position within the dataset (sorted by category and rating)
3. References between files are properly updated when IDs change
4. Trending data stays synchronized with the source products and categories

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

```


# Repo: rankncompare_v2

## README.md
```markdown
# rankncompare_v2
Rank and Compare 2.0

```


# Repo: seo-poster

