# source-ads

Source digest auto-composed from 10 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- getuai-ads
- getuai-ads-attribution
- getuai-ads-attribution-sdk
- getuai-ads-data
- getuai-ads-sdk
- getu_ads_v2
- attribution_v2
- Fast-Attribution
- ads-library
- facebook-ads-library-api-demo

---

# Repo: getuai-ads

## README.md
```markdown
# Google Ads Campaign Assistant

This application provides a comprehensive interface for managing and analyzing Google Ads campaigns. The system is built with a three-layer architecture:

1. **UI Layer** - Frontend interface for user interaction
2. **MCP Layer** - Middle layer for Google Ads API integration
3. **AI Layer** - Backend for intelligent processing and recommendations

## System Requirements

- Node.js (v16+)
- Python (v3.9+)
- npm or yarn

## Environment Setup

Before running the application, make sure you have the following environment variables set:

```
GOOGLE_ADS_CREDENTIALS_PATH=<path-to-your-credentials-file>
GOOGLE_ADS_DEVELOPER_TOKEN=<your-developer-token>
GOOGLE_ADS_LOGIN_CUSTOMER_ID=<your-manager-account-id>
DEEPSEEK_API_BASE_URL=<deepseek-api-url>
DEEPSEEK_API_KEY=<your-deepseek-api-key>
```

## Installation

Clone the repository and install dependencies for each component:

```bash
# Clone the repository
git clone <repository-url>
cd getuai-ads

# Install UI dependencies
cd v2-ui
npm install

# Install MCP layer dependencies
cd ../v2-mcp
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

### 2. MCP Layer (Google Ads Integration)

```bash
cd v2-mcp-google-ads

# Development 
# You need to create a `.env.development`, otherwise it will read from the default `.env`
python -m main

# Production
python -m main --env=production

```

This starts the MCP (Micro Control Program) layer that interfaces with the Google Ads API, typically running on port 8003.

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
- **v2-mcp**: Python-based middleware that handles Google Ads API integration
- **v2-ai**: FastAPI backend that processes requests, manages sessions, and provides AI-powered recommendations

## Key Features

- Google Ads account data visualization and analysis
- Campaign performance metrics and insights
- Optimization recommendations based on performance data
- Support for file uploads for enhanced analysis
- AI-powered marketing advisor for Google Ads and email marketing

## Troubleshooting

- If you encounter issues with Google Ads API access, check your credentials and developer token
- For connection issues between layers, ensure all three components are running
- Check the console logs of each component for specific error messages

## Development

The codebase is organized as follows:

- `v2-ui`: Frontend code
- `v2-mcp`: Google Ads API integration
- `v2-ai`: FastAPI backend and AI processing
  - `api/`: API endpoints and core functionality
  - `features/`: Feature-specific modules, including ads campaigns
  - `agents/`: AI agent implementations


```


# Repo: getuai-ads-attribution

## README.md
```markdown
# getuai-ads-attribution
getu ai attribution, inlcude server and js sdk

```


# Repo: getuai-ads-attribution-sdk


# Repo: getuai-ads-data

## README.md
```markdown
# Data Platform | 数据中台

> 专业的广告数据管理和分析平台，支持Google Ads、Meta Ads、TikTok Ads多平台数据统一查询和分析

## 🚀 项目概述

Data Platform是一个现代化的广告数据中台，提供统一的API接口和Web界面，支持多平台广告数据的获取、存储、查询和分析。

### 核心功能

- 🔗 **多平台集成**: 支持Google Ads、Meta Ads、TikTok Ads数据同步
- 📊 **灵活查询**: 强大的Query Builder支持复杂数据查询
- 🎯 **实时分析**: 提供趋势分析、平台对比、效果排名等分析功能
- 🔐 **安全认证**: 与GetUI-Ads系统集成的统一身份认证
- 📱 **现代界面**: 响应式Web界面，支持中英文切换
- ⚡ **高性能**: 异步处理，支持大规模数据查询

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GetUI-Ads     │    │  Data Platform  │    │   PostgreSQL    │
│   (认证服务)     │◄──►│   (数据中台)     │◄──►│   (数据存储)     │
│   Port: 8001    │    │   Port: 8011    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   REST APIs     │    │   Data Tables   │
│   Port: 3010    │    │   /api/v1/*     │    │   campaigns     │
│   (管理界面)     │    │   (查询接口)     │    │   accounts      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 安装和部署

### 环境要求

- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (可选，用于前端开发)

### 快速启动

1. **克隆项目**
```bash
git clone <repository-url>
cd data
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

4. **初始化数据库**
```bash
alembic upgrade head
```

5. **启动服务**
```bash
# 启动数据平台服务
python start_server.py

# 启动Web界面 (可选)
./start_ui.sh
```

### 环境变量配置

```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dataplatform

# GetUI-Ads集成
GETUAI_ADS_ENABLE_INTEGRATION=true
GETUAI_ADS_AUTH_URL=http://localhost:8001/api/auth/verify
GETUAI_ADS_API_URL=http://localhost:8001

# 安全配置
JWT_SECRET=your-secret-key
API_ADMIN_KEY=admin-key-12345

# 服务配置
DATA_PLATFORM_PORT=8011
WEB_UI_PORT=3010
```

## 🔧 API 接口

### 认证方式

所有API请求需要在Header中包含认证信息：

```bash
Authorization: Bearer <getuai_ads_token>
```

### 核心接口

#### 1. 用户信息
```http
GET /api/v1/user/info
```

#### 2. 健康检查
```http
GET /api/v1/health
```

#### 3. 多级查询
```http
GET /api/v1/multi_level_query/{account_id}/account_overview
GET /api/v1/multi_level_query/{account_id}/platform_comparison
GET /api/v1/multi_level_query/{account_id}/campaign_ranking
GET /api/v1/multi_level_query/{account_id}/trend_analysis
```

#### 4. 灵活查询 (Query Builder)
```http
POST /api/v1/query_builder/{account_id}/execute
Content-Type: application/json

{
  "query_type": "aggregated",
  "data_source": "google_ads_campaigns",
  "fields": [
    {"field": "campaign_name", "alias": "campaign"},
    {"field": "impressions", "aggregate": "sum", "alias": "total_impressions"}
  ],
  "conditions": [
    {"field": "date", "operator": ">=", "value": "2024-01-01"}
  ],
  "group_by": ["campaign_name"],
  "limit": 20
}
```

### Query Builder 参数说明

#### 查询类型 (query_type)
- `simple`: 简单查询
- `aggregated`: 聚合查询
- `comparison`: 对比查询
- `trend`: 趋势查询

#### 数据源 (data_source)
- `google_ads_campaigns`: Google Ads广告系列数据
- `meta_ads_campaigns`: Meta Ads广告系列数据
- `tiktok_ads_campaigns`: TikTok Ads广告系列数据
- `cross_platform`: 跨平台数据
- `account_data`: 账户数据

#### 聚合函数 (aggregate)
- `sum`: 求和
- `avg`: 平均值
- `count`: 计数
- `max`: 最大值
- `min`: 最小值

#### 操作符 (operator)
- `=`, `!=`: 等于/不等于
- `>`, `<`, `>=`, `<=`: 大于/小于
- `in`, `not_in`: 包�

[... truncated to 5000 bytes; full extract at sources/_raw/getuai-ads-data.md ...]


# Repo: getuai-ads-sdk

## README.md
```markdown
# GetU AI Ads SDK

A comprehensive Python SDK for user authentication, third-party credentials management, and project configuration in advertising platforms.

## Features

- **User Authentication**: Token-based user authentication with Redis caching
- **Third-party Credentials**: Manage Google Ads, Meta Ads, and TikTok Ads credentials
- **Project Management**: Create, update, and manage project configurations
- **Caching**: Redis-based caching for improved performance
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Async Support**: Full async/await support for all operations

## Installation

### From Source

Add to `requirements.txt`:

```bash
git+https://github.com/Optiminds-Inc/getuai-ads-sdk.git@main
```

Or install locally:

```bash
git clone <repository-url>
cd ads-sdk
pip install -e .
```

## Quick Start

### Basic Usage

```python
import asyncio
from getuai_ads_sdk import GetUAdsSDK, PlatformType

async def main():
    # Initialize SDK
    sdk = GetUAdsSDK()

    try:
        # Get user information
        user = await sdk.get_user_by_token("your_access_token")
        if user:
            print(f"User: {user.name} ({user.email})")

            # Get user projects
            projects = await sdk.projects.get_user_projects(user.id, "your_access_token")
            print(f"User has {len(projects.get('list', []))} projects")

            # Get third-party credentials
            google_creds = await sdk.get_google_credentials(user.id)
            if google_creds:
                print("Google Ads credentials available")

    finally:
        # Close SDK connections
        await sdk.close()

asyncio.run(main())
```

### Using Context Manager

```python
import asyncio
from getuai_ads_sdk import GetUAdsSDK

async def main():
    async with GetUAdsSDK() as sdk:
        # SDK is automatically initialized and will be closed when exiting context
        user = await sdk.get_user_by_token("your_access_token")
        if user:
            print(f"User: {user.name}")

asyncio.run(main())
```

## Configuration

The SDK can be configured using environment variables or a configuration object:

```python
from getuai_ads_sdk import GetUAdsSDK, SDKConfig

# Method 1: Environment variables
# export REDIS_HOST=localhost
# export REDIS_PORT=6379
# export GETUAI_API_BASE_URL=http://localhost:8001

sdk = GetUAdsSDK()  # Loads from environment variables

# Method 2: Configuration object
config = SDKConfig(
    redis_host="localhost",
    redis_port=6379,
    api_base_url="http://localhost:8001"
)

sdk = GetUAdsSDK(config)
```

## API Reference

### Core Classes

#### GetUAdsSDK

Main SDK class providing access to all services.

```python
sdk = GetUAdsSDK(config=None)
await sdk.close()
```

#### SDKConfig

Configuration class for SDK settings.

```python
config = SDKConfig(
    redis_host="localhost",
    redis_port=6379,
    api_base_url="http://localhost:8001",
    cache_ttl=10
)
```

### Authentication Service

#### Get User Information

```python
user = await sdk.get_user_by_token(access_token)
```

### Credentials Service

#### Get Google Ads Credentials

```python
credentials = await sdk.get_google_credentials(user_id)
```

#### Get Meta Ads Credentials

```python
access_token = await sdk.get_meta_credentials(user_id)
```

#### Get TikTok Ads Credentials

```python
access_token = await sdk.get_tiktok_credentials(user_id)
```

### Project Service

#### Get Project Configuration

```python
project = await sdk.get_project(user_id, project_id, access_token)
```

#### Get User Projects

```python
projects = await sdk.projects.get_user_projects(user_id, access_token, page=1, page_size=10)
```

#### Get Project Integrations

```python
integrations = await sdk.get_project_integrations(user_id, project_id, access_token)
```

### Service Properties

You can also access services directly:

```python
# Auth service
user = await sdk.auth.get_user_by_token(access_token)

# Credentials service
google_creds = await sdk.credentials.get_google_credentials(user_id)
meta_creds = await sdk.credentials.get_meta_credentials(user_id)
tiktok_creds = await sdk.credentials.get_tiktok_credentials(user_id)

# Project service
projects = await sdk.projects.get_user_projects(user_id, access_token)
project = await sdk.projects.get_project(user_id, project_id, access_token)
```

## Data Models

### User

```python
from getuai_ads_sdk import User

user = User(
    id="user123",
    email="user@example.com",
    name="John Doe",
    company="Example Corp"
)
```

### ProjectConfig

```python
from getuai_ads_sdk import ProjectConfig

project = ProjectConfig(
    id="project123",
    title="My Project",
    type="copilot",
    description="Project description"
)
```

### PlatformType Enum

```python
from getuai_ads_sdk import PlatformType

platforms = [PlatformType.GOOGLE, PlatformType.META, PlatformType.TIKTOK]
```

## Error Handling

The SDK provides custom exceptions for di

[... truncated to 5000 bytes; full extract at sources/_raw/getuai-ads-sdk.md ...]


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


# Repo: Fast-Attribution

## README.md
```markdown
# Fast-Attribution
fast attribution

```


# Repo: ads-library

## README.md
```markdown
# AdScope — AI-Powered Ad Intelligence

Enter any company URL and let AI analyze their ad strategy across Meta and Google platforms.

## Project Structure

```
ads-library/
├── frontend/    # Next.js frontend (TypeScript, Tailwind, shadcn/ui)
├── server/      # FastAPI backend  (Python, SQLAlchemy, Azure OpenAI)
└── README.md
```

## Getting Started

### Backend

```bash
cd server
cp .env.example .env   # fill in your keys
pip install -e .
python -m src.main
```

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open [http://localhost:3103](http://localhost:3103) in your browser.

```


# Repo: facebook-ads-library-api-demo

## README.md
```markdown
# Facebook Ads Library API Demo Application

This application demonstrates how to use the Facebook Ads Library API to search for ads, view their details, and save them locally for further operations.

## Features

- Search for ads using keywords or phrases
- Filter ads by type, status, media type, and platform
- View detailed information about each ad
- Save ads to local storage for later viewing
- Filter and sort saved ads

## Tech Stack

### Frontend
- React with TypeScript
- Material-UI (MUI) for UI components
- Vite as the build tool
- Context API for state management
- LocalForage for local storage

### Backend
- Node.js with Express
- Axios for API requests

## Project Structure

```
facebook-ads-library-demo/
├── frontend/                  # Frontend React application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── detail/        # Ad detail components
│   │   │   ├── layout/        # Layout components
│   │   │   ├── results/       # Search results components
│   │   │   ├── saved/         # Saved ads components
│   │   │   └── search/        # Search form components
│   │   ├── context/           # React context providers
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API and storage services
│   │   ├── types/             # TypeScript type definitions
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── index.html             # HTML entry point
├── backend/                   # Backend Express server
│   └── server.js              # Server implementation
└── README.md                  # Project documentation
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Facebook Developer Account with access to the Ads Library API

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
PORT=5000
FB_ACCESS_TOKEN=your_facebook_access_token
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/facebook-ads-library-demo.git
cd facebook-ads-library-demo
```

2. Install backend dependencies:
```bash
cd backend
npm install
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

### Running the Application

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Start the backend server:
```bash
cd ../backend
npm start
```

3. Open your browser and navigate to `http://localhost:5000`

## Facebook Ads Library API Authentication

To use the Facebook Ads Library API, you need to:

1. **Create a Facebook Developer Account**:
   - Go to [Facebook for Developers](https://developers.facebook.com/)
   - Sign up or log in with your Facebook account

2. **Create a Facebook App**:
   - Go to the [Apps Dashboard](https://developers.facebook.com/apps/)
   - Click "Create App"
   - Select "Business" as the app type
   - Fill in the required information and create the app

3. **Add the Marketing API Product**:
   - In your app dashboard, click "Add Product"
   - Select "Marketing API"

4. **Generate an Access Token**:
   - Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   - Select your app from the dropdown
   - Select "Get Token" > "Get User Access Token"
   - Select the required permissions:
     - `ads_read`
     - `ads_management`
     - `business_management`
   - Click "Generate Access Token"

5. **Extend the Token Expiration**:
   - Go to the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
   - Paste your token and click "Debug"
   - Click "Extend Access Token"

6. **Confirm Identity for Political Ads Access**:
   - To access political ads, you need to confirm your identity
   - Go to [Facebook.com/ID](https://www.facebook.com/id)
   - Follow the confirmation process
   - This can take a few days to complete

7. **Add the Access Token to Your Environment Variables**:
   - Add the token to your `.env` file as `FB_ACCESS_TOKEN`

## API Endpoints

### Search Ads
```
POST /api/search
```
Request body:
```json
{
  "search_terms": "example",
  "ad_type": "ALL",
  "ad_active_status": "ACTIVE",
  "ad_reached_countries": ["US"],
  "media_type": "ALL",
  "publisher_platforms": ["FACEBOOK", "INSTAGRAM"]
}
```

### Fetch Next Page
```
GET /api/next?url={next_page_url}
```

### Get Ad Details
```
GET /api/ad/{ad_id}
```

## Local Storage

The application uses IndexedDB (via LocalForage) to store saved ads. The storage is structured as follows:

- **Store Name**: `saved_ads`
- **Key**: Ad ID
- **Value**: Ad object with additional properties:
  - `saved`: Boolean indicating the ad is saved
  - `savedAt`: Timestamp when the ad was saved

## License

This project i

[... truncated to 5000 bytes; full extract at sources/_raw/facebook-ads-library-api-demo.md ...]

