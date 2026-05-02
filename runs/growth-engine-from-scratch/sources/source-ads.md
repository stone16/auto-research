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
- **v2-ai**: FastAPI backend that processes requests, manages sessions, and provid

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-ads.md ...]


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
git clone <repository-

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-ads-data.md ...]


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
confi

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-ads-sdk.md ...]


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
|----------|-----|--------|-

[... truncated to 2500 bytes; full extract at sources/_raw/getu_ads_v2.md ...]


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
               │ M

[... truncated to 2500 bytes; full extract at sources/_raw/attribution_v2.md ...]


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


[... truncated to 2500 bytes; full extract at sources/_raw/facebook-ads-library-api-demo.md ...]

