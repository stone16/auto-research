# source-shared-infra

Source digest auto-composed from 14 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- getuai-api
- getuai-console
- getuai-ui
- getuai-auth-center
- getuai-mvp
- getuai-plugin
- Pi
- Visionary
- clawcloud
- cloud-claw-k
- valuecell
- project-base
- optiminds-org-config
- optiminds-repo-template

---

# Repo: getuai-api

## README.md
```markdown
# GetU.ai API Layer

This repository contains the REST API layer for GetU.ai platform. It's built with FastAPI and serves as the central data management and session coordination layer for the entire platform.

## Architecture

The GetU.ai platform follows a three-tier architecture where this API service plays a central role:

```
Frontend (getuai-ui) → AI Agent (getuai-ai) → API Layer (getuai-api) → External Services
```

Additionally, the Frontend communicates directly with the API layer for form submissions and storage operations:

```
Frontend (getuai-ui) → API Layer (getuai-api)
```

### Key Responsibilities
- Acts as the source of truth for session management across all layers
- Provides temporary storage for session-based data (images, texts)
- Manages form submissions and data persistence
- Validates sessions for both frontend and AI layer requests
- Handles cleanup of expired sessions and associated data

## Features

- Session Management
  - Creation and validation of UUID v4 session IDs
  - Session expiration handling
  - Cross-layer session coordination
  - Automatic cleanup of expired sessions

- Storage Systems
  - Temporary image storage with session isolation
  - Text storage for form submissions
  - Automatic cleanup of old files
  - Support for various image formats

- Form Processing
  - Company information submission
  - Image upload handling
  - Data validation and sanitization

- REST API Endpoints
  - Session management endpoints
  - Storage operations (images, texts)
  - Form submission endpoints
  - Health check and monitoring

## Session Management

The API implements a comprehensive session management system:

### Session Endpoints

#### Create Session
```http
POST /api/v1/session
Response: {
    "session_id": "uuid-v4"
}
```

#### Validate Session
```http
GET /api/v1/session/validate
Headers: X-Session-Id: uuid-v4
Response: {
    "session_id": "uuid-v4"
}
```

#### Clear Session
```http
DELETE /api/v1/session
Headers: X-Session-Id: uuid-v4
```

### Session Flow
1. Session Creation:
   - Frontend or AI layer requests new session
   - API generates UUID v4 session ID
   - Session ID returned in response

2. Session Validation:
   - All requests must include  header
   - API validates session existence and expiration
   - Returns 404 if session expired/not found

3. Session Cleanup:
   - Automatic cleanup of expired sessions
   - Removal of associated storage data
   - Configurabl

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-api.md ...]


# Repo: getuai-console

## README.md
```markdown
# GetU Console

Internal admin console for managing GetU Ads platform users.

## Architecture

The console is built with a separated frontend/backend architecture:

- **Backend**: Python FastAPI service connecting to multiple databases:
  - GetU Ads MySQL database (primary operational data)
  - Attribution MySQL database (attribution tracking data)
  - MongoDB (tool usage logs and analytics)
  - Redis (caching layer)
- **Frontend**: Next.js React application with TypeScript and Tailwind CSS

## Features

- **Dashboard**: Real-time user statistics and growth metrics
- **User Management**: Browse, search, and filter all platform users
- **User Details**: View detailed information about individual users
- **Real Data**: Connects directly to GetU Ads database (no mock data)

## Setup

### Prerequisites

- Node.js 20+
- Python 3.11+
- MySQL 8.0+
- Access to GetU Ads database
- Access to Attribution database

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env.development
# Edit .env.development with your database credentials
```

5. Test database connection:
```bash
python test_connection.py
```

6. Run the backend:
```bash
uvicorn app.main:app --reload --port 8002
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
# Edit .env.local if needed (default points to localhost:8000)
```

4. Run the frontend:
```bash
npm run dev
```

5. Open http://localhost:3000 in your browser

## Docker Setup

Run both frontend and backend with Docker:

```bash
docker-compose up
```

This will start:
- Backend API at http://localhost:8002
- Frontend UI at http://localhost:3000
- MySQL database at localhost:3306

## API Documentation

Once the backend is running, visit http://localhost:8002/docs for interactive API documentation.

## Project Structure

```
getuai-console/
├── backend/              # FastAPI backend service
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Database models
│   │   └── schemas/     # Pydan

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-console.md ...]


# Repo: getuai-ui

## README.md
```markdown
# GetU.ai Frontend

This repository contains the frontend application for the GetU.ai platform. It's built with React and TypeScript, providing a modern interface for AI interactions and company information management.

## Architecture

The GetU.ai platform follows a three-tier architecture:

```
Frontend (getuai-ui) → AI Agent (getuai-ai) → API Layer (getuai-api)
```

Additionally, the frontend communicates directly with the API layer for form submissions and storage operations:

```
Frontend (getuai-ui) → API Layer (getuai-api)
```

### Key Responsibilities
- Provides user interface for AI chat interactions
- Manages company information forms and submissions
- Handles session management across services
- Coordinates image uploads and storage
- Manages streaming responses from AI service

## Features

### Session Management
- Automatic session initialization
- Session validation and retry mechanisms
- Session expiration handling
- Cross-layer session coordination

### Chat Interface
- Real-time message streaming
- Message history display
- Error handling and recovery
- Automatic reconnection
- Session persistence

### Company Profile Management
- Company information form
- Image upload handling
  - Company logo
  - Product images
  - Promotional images
- Form validation
- Progress tracking

### UI Components
- Material-UI based design
- Responsive layouts
- Loading states
- Error messages
- Form validation feedback

## Project Structure

```
src/
├── components/        # Reusable UI components
├── hooks/            # Custom React hooks
├── pages/            # Page components
├── services/         # API and service integrations
├── styles/           # Global styles and themes
└── utils/            # Helper functions
```

## Tech Stack

- React 18
- TypeScript
- Material-UI
- Axios
- React Router
- ESLint + Prettier

## Prerequisites

- Node.js 16+
- npm or yarn
- Running instances of:
  - getuai-api (port 8000)
  - getuai-ai (port 8001)

## Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_AI_URL=http://localhost:8001
```

3. Start development server:
```bash
npm start
# or
yarn start
```

## Available Scripts

- `npm start`: Start development server
- `npm build`: Build production version
- `npm test`: Run tests
- `npm lint`: Run linter
- `npm format`: Format c

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-ui.md ...]


# Repo: getuai-auth-center


# Repo: getuai-mvp

## README.md
```markdown
# GetUAI MVP

## Environment Setup

This project has been configured to support both local development and production environments, particularly regarding API routing.

### API Configuration

The application uses a configurable API prefix system:

- **Local Development**: Uses direct API paths (e.g., `/chat/session`)
- **Production**: Uses prefixed API paths (e.g., `/api/chat/session`)

### Frontend Configuration

The frontend automatically detects the environment and sets the appropriate API base URL:

```typescript
// In v2-ui/app/chat/components/Chat.tsx
const apiBaseUrl = process.env.NODE_ENV === 'development' ? '' : '/api';
```

This ensures that API requests are routed correctly in both development and production environments.

### Backend Configuration

The backend FastAPI application uses the `API_PREFIX` environment variable to determine the route prefix:

```python
# In v2-ai/api/config.py
API_PREFIX = os.getenv("API_PREFIX", "")  # Empty string for local development, "/api" for production
```

All route decorators use this prefix:

```python
@app.post(f"{API_PREFIX}/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    # ...
```

### Environment Configuration

#### Local Development

For local development, no additional configuration is needed. The default empty prefix will be used.

#### Production Deployment

For production deployment, set the `API_PREFIX` environment variable to `/api`:

```sh
# In your .env file or environment variables
API_PREFIX=/api
```

### Proxy Configuration (Production)

In production, configure your web server (Nginx, etc.) to route requests to the appropriate backend:

```nginx
# Example Nginx configuration
location /api/ {
    proxy_pass http://backend:8000/;  # Note the trailing slash
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location / {
    proxy_pass http://frontend:3000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Development Setup

1. Clone the repository
2. Set up the backend:
   ```sh
   cd v2-ai
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```sh
   cd v2-ui
   npm install
   ```
4. Start the development servers:
   ```sh
   # Backend
   cd v2-ai
   python main.py

   # Frontend
   cd v2-ui
   npm run dev
   ```


[... truncated to 2500 bytes; full extract at sources/_raw/getuai-mvp.md ...]


# Repo: getuai-plugin

## README.md
```markdown
# GetU AI Plugin Service

A comprehensive FastAPI-based plugin service for SEO and marketing intelligence tools, designed for seamless integration with Dify AI workflows.

## Features

### Original SEO Analysis Tools
- **Site Structure Analyzer**: Website crawling and internal link analysis
- **Meta Tags Analyzer**: Meta tags, Open Graph, and Twitter Cards analysis

### New Competitor Analysis & Keyword Research Tools
- **Google Search Analyzer**: Structured search results with SEO insights
- **Competitor Discovery**: AI-powered competitor identification and analysis
- **Keyword Ideas Generator**: Google Ads API integration for keyword research
- **URL Content Analyzer**: Content extraction and keyword analysis
- **Keyword Clustering**: Semantic keyword grouping and organization

### Technical Features
- FastAPI service with clean, layered architecture
- Comprehensive OpenAPI 3.0.3 schema documentation
- Async processing with performance optimization
- AI-powered analysis using OpenAI GPT models
- Google APIs integration (Ads API, Custom Search API)
- Comprehensive test suite with pytest
- Production-ready Docker containerization

## Project Structure

```
v2-pluging-tool/
  ├─ app/
  │  ├─ api/
  │  │  └─ v1/
  │  │     └─ routers/
  │  │        └─ site_structure.py
  │  ├─ core/
  │  │  └─ config.py
  │  ├─ models/
  │  │  ├─ requests.py
  │  │  └─ responses.py
  │  ├─ services/
  │  │  └─ site_structure_analyzer.py
  │  └─ main.py
  ├─ docs/
  │  └─ schemas/
  │     └─ site_structure.analyze.schema.json
  ├─ tests/
  │  ├─ test_api_site_structure.py
  │  └─ test_site_structure_analyzer.py
  └─ requirements.txt
```

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

#### For Local Development:
```bash
# Use the development configuration (includes testing features)
# .env.development contains all variables including mock API controls
```

#### For Production Deployment:
```bash
# .env.example contains only production-required variables (no comments)
# Copy the contents directly to your deployment pipeline web GUI
cat .env.example
```

**Required for full 

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-plugin.md ...]


# Repo: Pi

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

# Writing — 惜字如金

Every word must earn its place.

- No filler taglines, no marketing fluff, no sentences that restate the section title.
- Skip "uses these everywhere it works"-style copy. Cut the half of a sentence that adds nothing.
- A subtitle that doesn't tell the user *what to do* or *what just happened* doesn't ship.
- Only express the core product value. If you can't, say nothing.

Applies to UI copy, comments, commit messages, and chat replies alike.

# Setup / settings page

This is a foundation page, not a feed.

- Focus: connections + the firm's core info. No activity items, no "fir

[... truncated to 2500 bytes; full extract at sources/_raw/Pi.md ...]


# Repo: Visionary

## README.md
```markdown
# Visionary Lab

**Create high-quality visual content with GPT-Image-1 and Sora 2 on Azure OpenAI—tailored for professional use cases.**

## Key Features

### Video Generation (Sora 2)
- Create videos from text prompts with the **Sora 2** model
- Generate videos from text + images (image-to-video)
- Audio automatically included in all generated videos
- Support for multiple resolutions: 720p and 1080p (landscape and portrait)
- Durations: 4s, 8s, or 12s

### Image Generation (GPT-Image-1)
- Generate polished image assets from text prompts, input images, or both
- Refine prompts using AI best practices to ensure high-impact visuals
- Analyze outputs with AI for quality control, metadata tagging, and asset optimization
- Provide guardrails for content showing brands products (brand protection)

### Asset Management
- Manage your content in an organized asset library with folder support
- Automatic video analysis and metadata tagging

<img src="ui-sample.png" alt="description" width="800"/>

> You can also get started with our notebooks to explore the models and APIs:
>
> - Image generation: [gpt-image-1.ipynb](notebooks/gpt-image-1.ipynb)
> - Video generation: [sora-api-starter.ipynb](notebooks/sora-api-starter.ipynb)

## Prerequisites

Azure resources:

- Azure OpenAI resource with a deployed `gpt-image-1` model
- Azure OpenAI resource with a deployed **`Sora 2`** model (deployment name: `sora-2`)
- Azure OpenAI `gpt-4.1` model deployment (used for prompt enhancements and image/video analysis)
- Azure Storage Account with a Blob Container for your images and videos. You can use virtual folders to organize your content.

> **Note:** Sora 2 is available in Azure AI Foundry. Enterprise customers can apply for access via the [Sora-2 access application form](https://ai.azure.com/catalog/models/sora-2).

Compute environment:

- Python 3.12+
- Node.js 19+ and npm
- Git
- uv package manager
- Code editor (we are using VSCode in the instructions)

## Step 1: Installation (One-time)

### Option A: Quick Start with GitHub Codespaces

The quickest way to get started is using GitHub Codespaces, a hosted environment that is automatically set up for you. Click this button to create a Codespace (4-core machine recommended):

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=Azure-Samples/visionary-lab)

Wait for the Codespace to initiali

[... truncated to 2500 bytes; full extract at sources/_raw/Visionary.md ...]


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
- Resolve gallery image version `latest` to the actual latest version name before VM or VMSS cr

[... truncated to 2500 bytes; full extract at sources/_raw/clawcloud.md ...]


# Repo: cloud-claw-k


# Repo: valuecell

## README.md
```markdown
<p align="center">
  <img src="assets/valuecell.png" style="width: 100%; height: auto;">
</p>

<div align="center" style="line-height: 2;">
    <a href="https://www.python.org/downloads" target="_blank">
        <img src="https://img.shields.io/badge/python-3.12+-blue.svg"
            alt="Python version"></a>
    <a href="LICENSE" target="_blank">
        <img src="https://img.shields.io/badge/license-Apache2.0-red.svg"
            alt="License: Apache2.0"></a>  
    <br>
    <a href="https://discord.com/invite/84Kex3GGAh" target="_blank">
        <img src="https://img.shields.io/discord/1399603591471435907?logo=discord&labelColor=%20%235462eb&logoColor=%20%23f5f5f5&color=%20%235462eb"
            alt="chat on Discord"></a>
    <a href="https://twitter.com/intent/follow?screen_name=valuecell" target="_blank">
        <img src="https://img.shields.io/twitter/follow/valuecell?logo=X&color=%20%23f5f5f5"
            alt="follow on X(Twitter)"></a>
    <a href="https://www.linkedin.com/company/valuecell/" target="_blank">
        <img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff"
            alt="follow on LinkedIn"></a>
    <a href="https://www.facebook.com/people/ValueCell/61581410516790/" target="_blank">
        <img src="https://custom-icon-badges.demolab.com/badge/Facebook-1877F2?logo=facebook-white&logoColor=fff"
            alt="follow on Facebook"></a>
</div>

<div align="center">
  <a href="README.md" style="color: gray;">English</a>
  <a href="README.zh.md" style="color: gray;">中文（简体）</a>
  <a href="README.zh_Hant.md" style="color: auto;">中文（繁體）</a>
</div>


# ValueCell
ValueCell is a community-driven, multi-agent platform for financial applications.

It provides a team of TOP investment Agents to help manage your portfolio.

# Screenshot

<p align="center">
  <img src="assets/product/homepage.png" style="width: 100%; height: auto;">
</p>

<p align="center">
  <img src="assets/product/agent_welcome.png" style="width: 100%; height: auto;">
</p>

# Key Features

<p align="center">
  <img src="assets/architecture.png" style="width: 100%; height: auto;">
</p>


## Multi-Agent System
- **Trading Agents**: Agents work for market analysis, sentiment analysis, news analysis, and fundamentals analysis 
- **AI-Hedge-Fund**: Agents collaborate to provide comprehensive financial insights
- **SEC Agent**: Provides real-time updates from SEC 

[... truncated to 2500 bytes; full extract at sources/_raw/valuecell.md ...]


# Repo: project-base

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
docker push gcr.io/<PROJECT_ID>

[... truncated to 2500 bytes; full extract at sources/_raw/project-base.md ...]


# Repo: optiminds-org-config

## README.md
```markdown
# optiminds-org-config

Infrastructure-as-Code for the **Optiminds-Inc** GitHub organization.

All org-level policies (branch protection rulesets, org settings, webhooks, etc.) live here as version-controlled JSON. This repo is the **source of truth** — if a rule in GitHub's UI diverges from what's checked in here, the JSON wins and should be re-applied.

## Why this exists

Rulesets and org settings are editable directly in the GitHub UI, which means they can be silently changed or deleted. Without a git-tracked definition:

- Nobody can review changes before they happen
- Accidental deletion is unrecoverable without manual memory
- There's no history of *why* a rule exists

Storing the JSON here fixes all three.

## Layout

```
.
├── rulesets/               # Organization-level rulesets (one JSON per file)
│   ├── main-protection.json
│   └── README.md           # Rationale for each ruleset
├── webhooks/               # Organization-level webhooks (one JSON per file)
│   ├── pr-to-lark.json     # PR events → Lark group bot
│   └── README.md           # Rationale and event list
├── worker/                 # Cloudflare Worker that adapts GitHub → Lark payloads
│   └── README.md           # Deploy instructions
└── scripts/
    ├── apply-ruleset.sh    # Idempotent upsert: create or update ruleset from JSON
    └── apply-webhook.sh    # Idempotent upsert: create or update org webhook from JSON
```

## Prerequisites

- [`gh` CLI](https://cli.github.com/) authenticated as an org admin
- `gh` token must include `admin:org` scope:
  ```bash
  gh auth refresh -h github.com -s admin:org
  ```
- `jq` (`brew install jq`)

## Apply a ruleset

```bash
scripts/apply-ruleset.sh rulesets/main-protection.json
```

The script is **idempotent** — re-running it updates an existing ruleset in place rather than creating a duplicate.

## Apply a webhook

Webhooks ship in two parts: a JSON config (in `webhooks/`) and the Cloudflare Worker that adapts the payload (in `worker/`). Deploy the Worker first, then apply the webhook with the Worker URL injected from env:

```bash
# One-time: deploy the Worker (see worker/README.md for full instructions)
cd worker && npm install && npx wrangler login && \
  npx wrangler secret put GITHUB_WEBHOOK_SECRET && \
  npx wrangler secret put LARK_BOT_URL && \
  npm run deploy

# Then apply the org webhook
expor

[... truncated to 2500 bytes; full extract at sources/_raw/optiminds-org-config.md ...]


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

