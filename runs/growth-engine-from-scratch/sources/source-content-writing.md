# source-content-writing

Source digest auto-composed from 7 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- geowriter
- seo-poster
- getuai-email-2.0
- openclaw-marketing
- OpenBox-Marketing
- Vibe-marketing
- LLMRush

---

# Repo: geowriter

## README.md
```markdown
# geo-seo-v2
pr test

```


# Repo: seo-poster


# Repo: getuai-email-2.0

## README.md
```markdown
# Email Marketing Tool - Full Stack

生产级全栈项目，基于原型完全还原：FastAPI + MySQL + Azure OpenAI + SMTP (后端) 和 Next.js + TypeScript + Tailwind (前端)。

## ✨ 特性

- 📊 **Campaign 管理**：创建、编辑、删除营销活动
- 📧 **SMTP 账号管理**：添加、测试、管理多个 SMTP 发件账号
- 👥 **Recipients 管理**：批量导入、编辑收件人信息
- 🤖 **AI 个性化生成**：使用 Azure OpenAI (gpt5-mini) 为每个收件人生成个性化邮件
- 📮 **批量发送**：创建 Batch，智能选择收件人，随机使用 SMTP 账号发送
- 🎨 **Excel 风格界面**：完全还原原型的交互和视觉设计

## 📋 前置要求

- Docker (可选，用于 MySQL)
- Python 3.10+
- Node 18+
- Azure OpenAI 资源 (deployment: gpt5-mini)

## 🚀 快速开始

### 1️⃣ 数据库 (MySQL)

使用 Docker 启动 MySQL (推荐):

```bash
docker compose up -d mysql
```

默认凭证：
- host: localhost
- port: 3306
- user: root
- pass: Bobliew0119!
- db: email

如果不使用 Docker，手动创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS email CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2️⃣ 后端 (FastAPI)

```bash
cd backend

# 复制环境变量文件并填写 Azure OpenAI 配置
cp .env.example .env

# 安装依赖
poetry install

# 启动服务 (开发模式，自动重载)
./bin/uv

# 或使用 poetry 直接运行
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

健康检查: http://localhost:8000/health

**后端 API 端点：**

- `/api/campaigns` - Campaign CRUD
- `/api/recipients` - Recipients CRUD + CSV 导入
- `/api/smtp` - SMTP 账号 CRUD + 测试
- `/api/batches` - Batch 创建、AI 生成、发送

### 3️⃣ 前端 (Next.js)

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

打开浏览器: http://localhost:3000

## 🎯 核心流程

1. **创建 Campaign**
   - 点击 "New Campaign"
   - 输入名称、描述、AI Prompt Template
   - Template 中可使用 `{email}`, `{first_name}`, `{last_name}`, `{company}`, `{position}` 占位符

2. **配置 SMTP 账号**
   - 切换到 "SMTP Accounts" 标签
   - 添加 SMTP 账号信息
   - 点击 "Test" 验证连接（必须通过才能使用）

3. **导入 Recipients**
   - 切换到 "Recipients" 标签
   - 点击 "Import CSV" 上传 CSV 文件
   - CSV 格式: `email,first_name,last_n

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-email-2.0.md ...]


# Repo: openclaw-marketing

## README.md
```markdown
# 🦞 OpenClaw — Personal AI Assistant

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text-dark.png">
        <img src="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text.png" alt="OpenClaw" width="500">
    </picture>
</p>

<p align="center">
  <strong>EXFOLIATE! EXFOLIATE!</strong>
</p>

<p align="center">
  <a href="https://github.com/openclaw/openclaw/actions/workflows/ci.yml?branch=main"><img src="https://img.shields.io/github/actions/workflow/status/openclaw/openclaw/ci.yml?branch=main&style=for-the-badge" alt="CI status"></a>
  <a href="https://github.com/openclaw/openclaw/releases"><img src="https://img.shields.io/github/v/release/openclaw/openclaw?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="https://discord.gg/clawd"><img src="https://img.shields.io/discord/1456350064065904867?label=Discord&logo=discord&logoColor=white&color=5865F2&style=for-the-badge" alt="Discord"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
</p>

**OpenClaw** is a _personal AI assistant_ you run on your own devices.
It answers you on the channels you already use (WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, BlueBubbles, IRC, Microsoft Teams, Matrix, Feishu, LINE, Mattermost, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch, Zalo, Zalo Personal, WebChat). It can speak and listen on macOS/iOS/Android, and can render a live Canvas you control. The Gateway is just the control plane — the product is the assistant.

If you want a personal, single-user assistant that feels local, fast, and always-on, this is it.

[Website](https://openclaw.ai) · [Docs](https://docs.openclaw.ai) · [Vision](VISION.md) · [DeepWiki](https://deepwiki.com/openclaw/openclaw) · [Getting Started](https://docs.openclaw.ai/start/getting-started) · [Updating](https://docs.openclaw.ai/install/updating) · [Showcase](https://docs.openclaw.ai/start/showcase) · [FAQ](https://docs.openclaw.ai/help/faq) · [Wizard](https://docs.openclaw.ai/start/wizard) · [Nix](https://github.com/openclaw/nix-openclaw) · [Docker](https://docs.openclaw.ai/install/docker) · [Discord](https://discord.gg/clawd)

Preferred setup: run the onboarding wizard (`openclaw onbo

[... truncated to 2500 bytes; full extract at sources/_raw/openclaw-marketing.md ...]


# Repo: OpenBox-Marketing

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
docker push gcr.io/<PROJEC

[... truncated to 2500 bytes; full extract at sources/_raw/OpenBox-Marketing.md ...]


# Repo: Vibe-marketing


# Repo: LLMRush

## README.md
```markdown
# LLMRush Website

LLMRush is a modern web application that helps users find ranking information and sentiment scores for their search terms (company URLs or product names) across various LLM models (OpenAI ChatGPT, Deepseek, Anthropic Claude, Google Gemini, etc.).

## Features

- **Multi-model comparison** across major LLM providers
- **Ranking analysis** showing where a product/company ranks in relevant queries
- **Sentiment analysis** on a scale from -10 to 10
- **Aggregated positive and negative reviews** for each model
- **Token usage tracking** for cost management
- **User authentication** with JWT tokens and session management
- **Search history** with floating widget UI
- **Remember Me** functionality for extended sessions
- **Comprehensive security** including CSRF protection and security headers
- **Structured logging** with request IDs for debugging
- **Error tracking** with Sentry integration (optional)
- **Database connection retry** logic for reliability
- **Auto token refresh** for seamless user experience

## Tech Stack

### Frontend
- React 18 with Vite
- Tailwind CSS for styling
- React Query for data fetching
- Axios with interceptors for API calls
- Automatic token refresh handling

### Backend
- FastAPI (Python 3.11+)
- MySQL with aiomysql (async)
- Redis for caching
- SQLAlchemy ORM with Alembic migrations
- JWT authentication with bcrypt
- Structured logging with request tracking

## Security Features

- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS, CSP
- **CSRF Protection**: Token-based CSRF protection for state-changing operations
- **Rate Limiting**: Implemented on authentication endpoints
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Protection**: Using parameterized queries via SQLAlchemy
- **XSS Protection**: Content Security Policy and output encoding
- **Request ID Tracking**: Every request gets a unique ID for debugging

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python 3.11+
- MySQL 5.7+ or MariaDB 10.3+
- Redis 6.0+ (optional but recommended)
- npm or yarn

### Quick Start

The easiest way to run LLMRush is using the provided script:

```bash
# Make the script executable
chmod +x run.sh

# Run the application
./run.sh
```

This will:
1. Install frontend dependencies
2. Build the frontend
3. Copy the built files to the backend's static directory
4. Install backend dependencies
5. Start the bac

[... truncated to 2500 bytes; full extract at sources/_raw/LLMRush.md ...]

