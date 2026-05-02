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
- `in`, `not_in`: 包含/不包含
- `like`: 模糊匹配
- `between`: 范围查询

## 🖥️ 快速启动
pip install -r requirements.txt
python start_unified_dashboard.py
python start_server.py
访问 `http://localhost:3010` 打开Web管理界面，功能包括：

### 主要功能模块

1. **任务管理**
   - 查看系统状态和统计信息
   - 管理定时任务
   - 监控任务执行状态

2. **API测试工具**
   - 在线测试所有API接口
   - GetUI-Ads一键登录认证
   - 实时查看请求和响应
   - 支持自定义查询参数

3. **API文档**
   - 完整的接口文档
   - 示例代码和参数说明
   - 支持中英文切换

### 特色功能

- 🎨 **现代化UI**: 基于现代设计规范的响应式界面
- 🔧 **参数编辑器**: 可视化的查询参数选择和编辑
- 🌐 **多语言支持**: 中文/英文界面切换
- 📊 **实时预览**: 查询结果实时显示和格式化
- 🔍 **智能提示**: 参数选择时的智能提示和验证

## 📊 数据模型

### 主要数据表

#### google_ads_campaigns
```sql
- campaign_id: 广告系列ID
- campaign_name: 广告系列名称
- campaign_status: 广告系列状态
- ads_user_id: 用户ID
- date: 日期
- impressions: 展示次数
- clicks: 点击次数
- cost_micros: 费用(微分)
- conversions: 转化次数
```

#### meta_ads_campaigns
```sql
- campaign_id: 广告系列ID
- campaign_name: 广告系列名称
- ads_user_id: 用户ID
- date: 日期
- impressions: 展示次数
- clicks: 点击次数
- spend: 花费
- conversions: 转化次数
```

#### tiktok_ads_campaigns
```sql
- campaign_id: 广告系列ID
- campaign_name: 广告系列名称
- ads_user_id: 用户ID
- date: 日期
- impressions: 展示次数
- clicks: 点击次数
- cost: 费用
- conversions: 转化次数
```

## 🔧 开发指南

### 项目结构

```
data/
├── app/                    # 应用核心代码
│   ├── api/               # API路由
│   │   └── v1/           # API v1版本
│   │       ├── platforms/ # 平台特定接口
│   │       ├── multi_level_query.py  # 多级查询
│   │       └── query_builder.py      # 查询构建器
│   ├── core/              # 核心模块
│   ├── models/            # 数据模型
│   └── utils/             # 工具函数
├── ui/                    # Web界面
│   ├── index.html        # 主页面
│   └── app.js            # 前端逻辑
├── alembic/              # 数据库迁移
├── scripts/              # 脚本文件
└── requirements.txt      # Python依赖
```

### 添加新的查询功能

1. **定义数据模型** (在 `app/models/` 中)
2. **创建API路由** (在 `app/api/v1/` 中)
3. **实现查询逻辑** (使用Query Builder模式)
4. **添加前端界面** (在 `ui/` 中)
5. **编写测试** (创建测试脚本)

### 扩展新平台支持

1. **创建平台模块** (在 `app/api/v1/platforms/` 中)
2. **定义数据表结构** (创建Alembic迁移)
3. **实现数据同步逻辑**
4. **添加到Query Builder数据源**
5. **更新前端界面选项**

## 🧪 测试

### 运行测试

```bash
# 测试API接口
python test_api_integration.py

# 测试查询构建器
python test_query_builder_fix.py

# 测试特定查询
python test_user_query_direct.py

# 检查数据库数据
python check_database_data.py
```

### 调试工具

项目包含多个调试脚本：

- `debug_query_issue.py`: 查询问题诊断
- `test_specific_query.py`: 特定查询测试
- `check_database_data.py`: 数据库数据检查

## 🚀 部署

### 生产环境部署

1. **配置生产环境变量**
```bash
export DATABASE_URL=postgresql://prod_user:password@prod_host/prod_db
export GETUAI_ADS_API_URL=https://api.getuai.com
export JWT_SECRET=production_secret_key
```

2. **使用Gunicorn启动**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8011
```

3. **配置Nginx反向代理**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8011;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8011

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8011"]
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 代码规范

- 遵循PEP 8 Python代码规范
- 使用类型提示 (Type Hints)
- 编写清晰的文档字符串
- 保持函数单一职责
- 添加适当的错误处理

## 📝 更新日志

### v1.2.0 (2024-12-12)
- ✅ 修复Query Builder日期条件SQL生成问题
- ✅ 增强Web界面参数选择功能
- ✅ 添加实时查询调试信息
- ✅ 优化前端UI交互体验

### v1.1.0 (2024-12-01)
- ✅ 实现灵活查询构建器 (Query Builder)
- ✅ 添加多平台数据统一查询
- ✅ 集成GetUI-Ads认证系统
- ✅ 完善Web管理界面

### v1.0.0 (2024-11-01)
- ✅ 基础数据平台架构
- ✅ 多平台API集成
- ✅ 数据存储和查询功能
- ✅ 基础Web界面

## 📞 支持

如有问题或建议，请通过以下方式联系：

- 📧 Email: support@getuai.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 文档: [在线文档](https://docs.getuai.com)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**Data Platform** - 让广告数据管理更简单、更高效 🚀 
```


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

The SDK provides custom exceptions for different error types:

```python
from getuai_ads_sdk.exceptions import (
    SDKError, AuthenticationError, CredentialsError,
    ProjectError, NetworkError, CacheError
)

try:
    user = await sdk.get_user_by_token(access_token)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except SDKError as e:
    print(f"SDK error: {e}")
```

## Configuration

### Environment Variables

| Variable                 | Default                 | Description            |
| ------------------------ | ----------------------- | ---------------------- |
| `REDIS_HOST`             | `localhost`             | Redis server host      |
| `REDIS_PORT`             | `6379`                  | Redis server port      |
| `REDIS_DB`               | `0`                     | Redis database number  |
| `REDIS_PASSWORD`         | `None`                  | Redis password         |
| `REDIS_SSL`              | `false`                 | Enable SSL for Redis   |
| `GETUAI_API_BASE_URL`    | `http://localhost:8001` | API base URL           |
| `GETUAI_API_TIMEOUT`     | `30`                    | API request timeout    |
| `GETUAI_API_MAX_RETRIES` | `3`                     | Maximum retry attempts |
| `GETUAI_LOG_LEVEL`       | `INFO`                  | Logging level          |
| `GETUAI_CACHE_TTL`       | `10`                    | Cache TTL in seconds   |

### Configuration Object

```python
config = SDKConfig(
    # Redis settings
    redis_host="localhost",
    redis_port=6379,
    redis_db=0,
    redis_password=None,
    redis_ssl=False,
    redis_timeout=30,
    redis_max_connections=10,

    # API settings
    api_base_url="http://localhost:8001",
    api_timeout=30,
    api_max_retries=3,
    api_key=None,

    # General settings
    log_level="INFO",
    cache_ttl=10
)
```

## Examples

See the `examples/` directory for complete usage examples:

- `basic_usage.py`: Basic SDK usage
- `advanced_usage.py`: Advanced features and error handling

## Development

### Setup Development Environment

```bash
git clone <repository-url>
cd ads-sdk
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sdk.py

# Run with coverage
pytest --cov=getuai_ads_sdk
```

### Building and Publishing

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Publish to PyPI
twine upload dist/*
```

## API Endpoints

The SDK connects to the following API endpoints (based on v2-ai project):

### Authentication

- `GET /auth/me` - Get current user information

### Third-party Credentials

- `POST /auth/refresh_third_party_auth` - Refresh third-party credentials

### Projects

- `GET /project/get/{project_id}` - Get project configuration
- `POST /project/paginate` - Get paginated user projects

## License

MIT License - see LICENSE file for details.

## Support

For support and questions, please contact the GetU AI team.

```


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
echo '{"resource":"campaign"}' | \
  python -m google_ads_cli exec run --operation gaql.fields --stdin --compact -c config.yaml
```

### Validate GAQL before executing

```bash
echo '{"query":"SELECT campaign.id, campaign.name FROM campaign"}' | \
  python -m google_ads_cli exec run --operation gaql.validate --stdin --compact -c config.yaml
```

## Configuration

The CLI reads credentials from a YAML config file:

```yaml
google_ads:
  client_id: "YOUR_CLIENT_ID.apps.googleusercontent.com"
  client_secret: "YOUR_CLIENT_SECRET"
  refresh_token: "YOUR_REFRESH_TOKEN"
  developer_token: "YOUR_DEVELOPER_TOKEN"
  customer_id: "1234567890"
  # login_customer_id: "0987654321"  # MCC account (optional)
  # api_version: "v23"               # defaults to v23
```

Credentials can also be overridden via CLI flags: `--customer_id`, `--login_customer_id`, `--developer_token`.

## Workflow Patterns

### Pattern 1: Incremental Build

1. `search.campaign.create` - Create campaign
2. `search.ad_group.create` - Add ad groups (can include keywords inline)
3. `search.ad.create_rsa` - Add RSA ads
4. `search.criteria.add` - Add location/language targeting
5. `search.criteria.add_negatives` - Add campaign negative keywords

### Pattern 2: One-Shot Full Build (Recommended)

Use `search.composite.create_full` with a single payload containing campaign config,
ad groups (with keywords), and ads. Handles all steps automatically with partial
failure tolerance.

### Pattern 3: Expand Existing Campaign

Use `search.composite.create_groups` to add new ad groups + ads to an existing campaign.

### Pattern 4: Monitor and Optimize

1. `report.campaign` - Check campaign-level metrics
2. `report.ad` - Check ad-level performance
3. `report.search_terms` - Discover search terms
4. `search.keyword.add` - Add winning search terms as keywords
5. `search.criteria.add_negatives` - Negate irrelevant terms
6. `search.campaign.update_bidding` - Adjust bidding strategy

### Pattern 5: GAQL Discovery and Execution

1. `gaql.resources` - List all available GAQL resources
2. `gaql.fields` - Discover selectable/filterable fields for a resource
3. `gaql.field` - Inspect a single field's metadata (type, compatibility)
4. `gaql.build` - Programmatically construct a GAQL query with static validation
5. `gaql.validate` - Validate query (static rules + API dry-run) before execution
6. `gaql.run` - Execute GAQL and get flattened results

This pattern is ideal for agents that need to dynamically construct queries based on
user intent rather than using predefined report operations.

```

## skills/google-ads-cli/references/ad.md
```markdown
# Ad / RSA Operations (7)

## search.ad.create_rsa

Create Responsive Search Ads.

```json
{
  "campaign_id": "23219624121",
  "ads": [
    {
      "ad_group_id": "189105408658",
      "ad_name": "Brand RSA v1",
      "headlines": [
        "Buy Running Shoes",
        "Free Shipping Today",
        "Top Rated Athletic Gear"
      ],
      "descriptions": [
        "Shop our collection of premium running shoes. Free returns.",
        "Discover top-rated footwear for every activity."
      ],
      "final_url": "https://www.example.com/shoes",
      "path1": "shoes",
      "path2": "running"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ads | array | yes | 1-50 RSA items |
| ads[].ad_group_id | string | yes | Target ad group ID |
| ads[].ad_name | string | yes | Ad name (1-100 chars) |
| ads[].headlines | string[] | yes | 3-15 headlines (each max 30 chars) |
| ads[].descriptions | string[] | yes | 2-4 descriptions (each max 90 chars) |
| ads[].final_url | string | yes | Landing page URL (max 255) |
| ads[].path1 | string | no | Display URL path 1 (max 25 chars) |
| ads[].path2 | string | no | Display URL path 2 (max 25 chars) |

## search.ad.get_rsa

Get RSA details by ad IDs.

```json
{
  "campaign_id": "23219624121",
  "ad_ids": ["741457938700", "741457938701"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_ids | string[] | yes | 1-50 ad IDs |

## search.ad.update_rsa

Update RSA content (headlines, descriptions, URLs, paths).

```json
{
  "campaign_id": "23219624121",
  "updates": [
    {
      "ad_id": "741457938700",
      "headlines": ["New Headline 1", "New Headline 2", "New Headline 3"],
      "descriptions": ["Updated description one.", "Updated description two."],
      "final_url": "https://www.example.com/new-landing",
      "path1": "new",
      "path2": "page"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| updates | array | yes | 1-50 update items |
| updates[].ad_id | string | yes | Ad ID |
| updates[].headlines | string[] | no | 3-15 new headlines (replaces all) |
| updates[].descriptions | string[] | no | 2-4 new descriptions (replaces all) |
| updates[].final_url | string | no | New landing URL |
| updates[].path1 | string | no | New path1 |
| updates[].path2 | string | no | New path2 |

## search.ad.update_status

Change ad status.

```json
{
  "ad_group_ad_ids": ["189105408658~741457938700"],
  "status": "PAUSED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_ad_ids | string[] | yes | 1-100 IDs in `ad_group_id~ad_id` format |
| status | enum | yes | `ENABLED` or `PAUSED` |

## search.ad.list

List ads in a campaign.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_id | string | no | Filter by ad group |
| status_filter | string | no | `ENABLED`, `PAUSED`, or null |

## search.ad.remove

Remove ads.

```json
{
  "ad_group_ad_ids": ["189105408658~741457938700"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_ad_ids | string[] | yes | 1-100 IDs in `ad_group_id~ad_id` format |

## search.ad.copy_rsa

Copy RSA ads to a different ad group. Fetches source ad content automatically.

```json
{
  "source_campaign_id": "23219624121",
  "source_ad_ids": ["741457938700"],
  "target_ad_group_id": "189105408698",
  "target_campaign_id": "23219624121"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| source_campaign_id | string | yes | Source campaign ID |
| source_ad_ids | string[] | yes | 1-50 source ad IDs |
| target_ad_group_id | string | yes | Destination ad group |
| target_campaign_id | string | yes | Destination campaign |

```

## skills/google-ads-cli/references/ad_group.md
```markdown
# Ad Group Operations (5)

## search.ad_group.create

Create ad groups in a campaign. Can include keywords inline.

```json
{
  "campaign_id": "23219624121",
  "ad_groups": [
    {
      "ad_group_name": "Brand Terms",
      "target_cpa": 5.0,
      "keywords": [
        { "text": "buy shoes online", "match_type": ["EXACT", "PHRASE"] }
      ],
      "negative_keywords": [
        { "text": "free", "match_type": ["BROAD"] }
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_groups | array | yes | 1-100 ad groups |
| ad_groups[].ad_group_name | string | yes | Name (1-100 chars) |
| ad_groups[].target_cpa | float | no | Target CPA (0.01-100) |
| ad_groups[].keywords | array | no | Keywords (max 100). See keyword format below |
| ad_groups[].negative_keywords | array | no | Negative keywords (max 100) |

**Keyword format**: `{ "text": "keyword text", "match_type": ["EXACT", "PHRASE", "BROAD"] }`
Each keyword can have multiple match types; a separate criterion is created for each.

## search.ad_group.list

List ad groups in a campaign.

```json
{
  "campaign_id": "23219624121",
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| status_filter | string | no | `ENABLED`, `PAUSED`, or null (all) |

## search.ad_group.find

Find ad groups by name.

```json
{
  "campaign_id": "23219624121",
  "ad_group_names": ["Brand Terms", "Generic SEO"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_names | string[] | yes | 1-50 ad group names |

## search.ad_group.update_status

Change ad group status.

```json
{
  "campaign_id": "23219624121",
  "ad_group_ids": ["189105408658", "189105408698"],
  "status": "PAUSED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_ids | string[] | yes | 1-100 ad group IDs |
| status | enum | yes | `ENABLED` or `PAUSED` |

## search.ad_group.remove

Remove ad groups.

```json
{
  "campaign_id": "23219624121",
  "ad_group_ids": ["189105408658"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_ids | string[] | yes | 1-100 ad group IDs |

```

## skills/google-ads-cli/references/campaign.md
```markdown
# Campaign Operations (6)

## search.campaign.create

Create a new Search campaign with budget.

```json
{
  "campaign_name": "My Campaign",
  "budget_amount": 10.0,
  "status": "PAUSED",
  "start_days_from_now": 0,
  "end_days_from_now": 30,
  "bidding_strategy": "MAXIMIZE_CONVERSIONS",
  "maximize_conversions": { "target_cpa": 5.0 }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_name | string | yes | 1-255 chars |
| budget_amount | float | no | Daily budget (default 1.0, range 0.01-100000) |
| status | enum | no | `ENABLED` or `PAUSED` (default) |
| start_days_from_now | int | no | Start date offset (default 0, range 0-365) |
| end_days_from_now | int | no | End date offset (range 10-3650, null = indefinite) |
| bidding_strategy | enum | no | See bidding strategies below (default `MAXIMIZE_CONVERSIONS`) |
| maximize_conversions | object | no | `{ "target_cpa": float }` (0.1-100) |
| maximize_conversion_value | object | conditional | `{ "target_roas": float }` (0.1-1000). Required when strategy is `MAXIMIZE_CONVERSION_VALUE` |
| target_impression_share | object | conditional | Required when strategy is `TARGET_IMPRESSION_SHARE` |
| target_spend | object | conditional | `{ "cpc_bid_ceiling": float }` (0.1-1000). Required when strategy is `TARGET_SPEND` |

**Bidding strategies**: `MAXIMIZE_CONVERSIONS`, `MAXIMIZE_CONVERSION_VALUE`, `TARGET_IMPRESSION_SHARE`, `TARGET_SPEND`

**target_impression_share object**:
```json
{
  "location": "ABSOLUTE_TOP_OF_PAGE",
  "location_fraction": 0.9,
  "cpc_bid_ceiling": 2.0
}
```
Location options: `ANYWHERE_ON_PAGE`, `TOP_OF_PAGE`, `ABSOLUTE_TOP_OF_PAGE`

## search.campaign.list

List campaigns by type and status.

```json
{
  "campaign_type": "SEARCH",
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_type | string | no | `SEARCH` (default), `DISPLAY`, `DEMAND_GEN`, `APP` |
| status_filter | string | no | `ENABLED`, `PAUSED`, or null (all) |

## search.campaign.find

Find campaigns by IDs or names.

```json
{
  "campaign_ids_or_names": ["23219624121", "My Campaign Name"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_ids_or_names | string[] | yes | 1-50 campaign IDs or names |

## search.campaign.update

Update campaign name, status, or end date.

```json
{
  "campaigns": [
    {
      "campaign_id": "23219624121",
      "campaign_name": "New Name",
      "status": "PAUSED",
      "end_days_from_now": 60
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaigns | array | yes | 1-20 update items |
| campaigns[].campaign_id | string | yes | Campaign ID |
| campaigns[].campaign_name | string | no | New name (max 255) |
| campaigns[].status | enum | no | `ENABLED` or `PAUSED` |
| campaigns[].end_days_from_now | int | no | New end date (1-3650 days) |

## search.campaign.update_bidding

Change bidding strategy for campaigns.

```json
{
  "campaigns": [
    {
      "campaign_id": "23219624121",
      "bidding_strategy": "TARGET_SPEND",
      "target_spend": { "cpc_bid_ceiling": 1.5 }
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaigns | array | yes | 1-20 bidding update items |
| campaigns[].campaign_id | string | yes | Campaign ID |
| campaigns[].bidding_strategy | enum | yes | New bidding strategy |
| campaigns[].maximize_conversions | object | no | Strategy-specific params |
| campaigns[].maximize_conversion_value | object | no | Strategy-specific params |
| campaigns[].target_impression_share | object | no | Strategy-specific params |
| campaigns[].target_spend | object | no | Strategy-specific params |

## search.campaign.copy

Copy a campaign (optionally with ad groups).

```json
{
  "source_campaign_id": "23219624121",
  "copy_with_groups": false,
  "campaigns": [
    { "campaign_name": "Copy of Campaign", "budget_amount": 10.0 }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| source_campaign_id | string | yes | Source campaign ID |
| copy_with_groups | bool | no | Copy ad groups too (default false) |
| campaigns | array | yes | 1-20 target campaigns |
| campaigns[].campaign_name | string | yes | New campaign name (max 255) |
| campaigns[].budget_amount | float | no | Override budget (default: source budget) |

```

## skills/google-ads-cli/references/composite.md
```markdown
# Composite Operations (2)

One-shot creation of full campaign structures. Recommended for building new campaigns from scratch.

## search.composite.create_full

Create a complete campaign structure in one shot: campaign + targeting + ad groups (with keywords) + RSA ads.

```json
{
  "campaign": {
    "campaign_name": "Full Campaign Test",
    "budget_amount": 10.0,
    "status": "PAUSED",
    "bidding_strategy": "MAXIMIZE_CONVERSIONS",
    "locations": ["2840"],
    "languages": ["1000"],
    "negative_keywords": [
      { "text": "free", "match_type": "BROAD" }
    ]
  },
  "ad_groups": [
    {
      "ad_group_name": "Brand Terms",
      "keywords": [
        { "text": "brand shoes", "match_type": ["EXACT", "PHRASE"] }
      ]
    },
    {
      "ad_group_name": "Generic Terms",
      "keywords": [
        { "text": "running shoes", "match_type": ["BROAD"] }
      ]
    }
  ],
  "ads": [
    {
      "ad_group_name": "Brand Terms",
      "ad_name": "Brand RSA",
      "headlines": ["Buy Brand Shoes", "Official Store", "Free Shipping"],
      "descriptions": ["Shop the official brand store.", "Premium quality guaranteed."],
      "final_url": "https://www.example.com/brand"
    },
    {
      "ad_group_name": "Generic Terms",
      "ad_name": "Generic RSA",
      "headlines": ["Best Running Shoes", "Top Rated Footwear", "Shop Now"],
      "descriptions": ["Find your perfect pair today.", "Free returns on all orders."],
      "final_url": "https://www.example.com/running"
    }
  ]
}
```

**Campaign config fields**: Same as `search.campaign.create` (see [campaign.md](campaign.md)) plus:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| locations | string[] | no | Geo target constant IDs |
| languages | string[] | no | Language constant IDs |
| negative_keywords | array | no | Campaign-level negatives `[{text, match_type}]` |

**Ad groups**: Same as `search.ad_group.create` items (name, target_cpa, keywords, negative_keywords).

**Ads**: Reference ad groups by `ad_group_name` (must match an entry in `ad_groups`).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_name | string | yes | Must match an ad_group in the ad_groups array |
| ad_name | string | yes | Ad name (1-100 chars) |
| headlines | string[] | yes | 3-15 headlines (each max 30 chars) |
| descriptions | string[] | yes | 2-4 descriptions (each max 90 chars) |
| final_url | string | yes | Landing page URL |
| path1 | string | no | Display URL path 1 |
| path2 | string | no | Display URL path 2 |

The operation is fault-tolerant: if ad creation fails (e.g. policy violation), the campaign and ad groups are still preserved.

## search.composite.create_groups

Add ad groups + ads to an existing campaign.

```json
{
  "campaign_id": "23219624121",
  "ad_groups": [
    {
      "ad_group_name": "New Group",
      "keywords": [
        { "text": "new keyword", "match_type": ["EXACT"] }
      ]
    }
  ],
  "ads": [
    {
      "ad_group_name": "New Group",
      "ad_name": "New RSA",
      "headlines": ["Headline 1", "Headline 2", "Headline 3"],
      "descriptions": ["Description one.", "Description two."],
      "final_url": "https://www.example.com/new"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Existing campaign ID |
| ad_groups | array | yes | 1-100 ad group configs |
| ads | array | yes | 1-100 ad configs (reference ad_group_name) |

```

## skills/google-ads-cli/references/gaql.md
```markdown
# GAQL Operations (6)

Field/resource discovery, programmatic query building, validation, and enhanced execution.
Adapted from the [google-ads-api-developer-assistant](https://github.com/googleads/google-ads-api-developer-assistant) design patterns.

## gaql.resources

List all available GAQL resources (tables).

```json
{}
```

No payload fields required.

**Response example**:
```json
{
  "total": 120,
  "resources": [
    { "name": "ad_group", "category": "RESOURCE", "data_type": "MESSAGE" },
    { "name": "campaign", "category": "RESOURCE", "data_type": "MESSAGE" }
  ]
}
```

## gaql.fields

Discover all selectable fields for a resource.

```json
{
  "resource": "campaign"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource | string | yes | Resource name (e.g. `campaign`, `ad_group`, `ad_group_ad`) |

**Response**: Returns each field with `name`, `category`, `data_type`, `selectable`, `filterable`, `sortable`, `is_repeated`, `selectable_with`, `metrics`, `segments`, `attribute_resources`.

## gaql.field

Get detailed metadata for a single field.

```json
{
  "field_name": "metrics.clicks"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| field_name | string | yes | Full field name (e.g. `metrics.clicks`, `campaign.status`) |

**Response**: Detailed field info including `data_type`, `selectable`, `filterable`, `sortable`, `selectable_with` (list of compatible resources/segments), `enum_values` (for ENUM types).

## gaql.build

Programmatically construct a GAQL query from parameters. Runs static validation rules automatically.

```json
{
  "resource": "campaign",
  "fields": ["campaign.id", "campaign.name", "metrics.clicks", "metrics.impressions"],
  "conditions": ["campaign.status = 'ENABLED'"],
  "order_by": "metrics.clicks DESC",
  "limit": 10,
  "date_range": "LAST_30_DAYS"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource | string | yes | GAQL resource name |
| fields | string[] | yes | Fields to SELECT (min 1) |
| conditions | string[] | no | WHERE conditions |
| order_by | string | no | ORDER BY clause (e.g. `metrics.clicks DESC`) |
| limit | int | no | LIMIT rows (1-10000) |
| date_range | string | no | Date range: `LAST_30_DAYS`, `YESTERDAY`, etc., or custom `YYYY-MM-DD,YYYY-MM-DD` |

**Response**:
```json
{
  "query": "SELECT campaign.id, campaign.name, metrics.clicks, metrics.impressions FROM campaign WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS ORDER BY metrics.clicks DESC LIMIT 10",
  "validation": {
    "valid": true,
    "error_count": 0,
    "warning_count": 0,
    "issues": []
  }
}
```

**Static validation rules**:
- GAQL `OR` operator is forbidden (use `IN(...)` instead)
- Date segments in SELECT require `DURING` or `BETWEEN` in WHERE
- `ORDER BY` fields should appear in SELECT
- `click_view` resource requires single-day date filter (TODAY, YESTERDAY, or same-day BETWEEN)
- `change_status` resource requires `BETWEEN` on `last_change_date_time` + LIMIT

## gaql.validate

Validate a GAQL query without executing it. Runs static rules first, then API dry-run (`validateOnly=true`).

```json
{
  "query": "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | GAQL query to validate (min 10 chars) |

**Response**:
```json
{
  "query": "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'",
  "static_validation": {
    "valid": true,
    "error_count": 0,
    "warning_count": 0,
    "issues": []
  },
  "dry_run": {
    "executed": true,
    "valid": true,
    "error": null
  },
  "valid": true
}
```

If static validation fails, dry-run is skipped. If dry-run fails, `dry_run.error` contains the API error message.

## gaql.run

Execute a GAQL query and return results. Supports flattening nested JSON to dot-notation keys.

```json
{
  "query": "SELECT campaign.id, campaign.name, campaign.status, metrics.clicks FROM campaign WHERE campaign.status != 'REMOVED' LIMIT 5",
  "flatten": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | GAQL query to execute (min 10 chars) |
| flatten | bool | no | Flatten nested response (default `true`) |

**Response (flatten=true)**:
```json
{
  "query": "SELECT campaign.id, campaign.name ...",
  "total": 5,
  "rows": [
    {
      "campaign.resourceName": "customers/123/campaigns/456",
      "campaign.id": "456",
      "campaign.name": "My Campaign",
      "campaign.status": "ENABLED",
      "metrics.clicks": "142"
    }
  ]
}
```

**Response (flatten=false)**: Returns raw nested API response structure.

**Difference from `report.gaql`**: `gaql.run` provides `flatten` option for cleaner output and includes the original query in the response. `report.gaql` returns raw API results for backward compatibility.

```

## skills/google-ads-cli/references/keyword.md
```markdown
# Keyword Operations (3)

## search.keyword.add

Add keywords and/or negative keywords to an ad group.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "keywords": [
    { "text": "running shoes", "match_type": ["EXACT", "PHRASE"] },
    { "text": "athletic footwear", "match_type": ["BROAD"] }
  ],
  "negative_keywords": [
    { "text": "cheap", "match_type": ["BROAD"] }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_id | string | yes | Ad group ID |
| keywords | array | no | Positive keywords (max 100) |
| negative_keywords | array | no | Negative keywords (max 100) |

At least one of `keywords` or `negative_keywords` must be provided.

## search.keyword.list

List keywords in ad groups.

```json
{
  "ad_group_ids": ["189105408658", "189105408698"],
  "status": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_ids | string[] | yes | 1-20 ad group IDs |
| status | string | no | `ENABLED` (default) or `PAUSED` |

## search.keyword.remove

Remove keywords by criterion ID.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "criterion_ids": ["123456789", "987654321"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_id | string | yes | Ad group ID |
| criterion_ids | string[] | yes | Criterion IDs to remove |

```

## skills/google-ads-cli/references/operations.md
```markdown
# Operations Reference

38 operations organized by usage scenario. Each operation is invoked via:

```bash
echo '<payload>' | python -m google_ads_cli exec run --operation <name> --stdin --compact -c config.yaml
```

All operations return a `ResultEnvelope`:

```json
{ "success": true, "command": "exec <operation>", "result": { ... }, "elapsed_ms": 1234.5 }
```

On failure: `success: false`, `errors: [...]`, exit code `1`.

---

## Operations by Scenario

| Scenario | File | Operations | When to use |
|----------|------|------------|-------------|
| Campaign Management | [campaign.md](campaign.md) | `search.campaign.create`, `list`, `find`, `update`, `update_bidding`, `copy` (6) | Create, list, find, update, or copy campaigns |
| Ad Group Management | [ad_group.md](ad_group.md) | `search.ad_group.create`, `list`, `find`, `update_status`, `remove` (5) | Manage ad groups within a campaign |
| Keyword Management | [keyword.md](keyword.md) | `search.keyword.add`, `list`, `remove` (3) | Add, list, or remove keywords in ad groups |
| Ad / RSA Creative | [ad.md](ad.md) | `search.ad.create_rsa`, `get_rsa`, `update_rsa`, `update_status`, `list`, `remove`, `copy_rsa` (7) | Create, edit, or manage Responsive Search Ads |
| Targeting & Budget | [targeting.md](targeting.md) | `search.budget.update`, `search.criteria.add`, `list`, `remove`, `add_negatives` (5) | Set budgets, location/language targeting, campaign negatives |
| Composite Build | [composite.md](composite.md) | `search.composite.create_full`, `create_groups` (2) | Build full campaign structures in one shot |
| Reporting | [report.md](report.md) | `report.campaign`, `ad`, `search_terms`, `gaql` (4) | Run predefined performance reports or raw GAQL |
| GAQL Builder | [gaql.md](gaql.md) | `gaql.resources`, `fields`, `field`, `build`, `validate`, `run` (6) | Discover fields, build/validate/execute GAQL queries |

---

## Quick Decision Guide

**"I need to create a new campaign from scratch"**
→ Use `search.composite.create_full` ([composite.md](composite.md)) for one-shot setup

**"I need to check performance"**
→ Use `report.campaign` or `report.ad` ([report.md](report.md))

**"I need a custom data query"**
→ Use `gaql.build` + `gaql.run` ([gaql.md](gaql.md))

**"I need to know what fields/resources exist"**
→ Use `gaql.resources` or `gaql.fields` ([gaql.md](gaql.md))

**"I need to adjust an existing campaign"**
→ See [campaign.md](campaign.md) for updates, [targeting.md](targeting.md) for budget/criteria

```

## skills/google-ads-cli/references/report.md
```markdown
# Report Operations (4)

Predefined performance reports and raw GAQL execution. For dynamic query building, see [gaql.md](gaql.md).

## report.campaign

Campaign performance report.

```json
{
  "date_range": "LAST_7_DAYS",
  "campaign_ids": ["23219624121"],
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| date_range | string | no | Default `LAST_30_DAYS`. Options: `TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`, `LAST_MONTH`, or custom `YYYY-MM-DD,YYYY-MM-DD` |
| campaign_ids | string[] | no | Filter by campaigns |
| status_filter | string | no | `ENABLED`, `PAUSED` |

Returns: impressions, clicks, cost, conversions, ctr, avg_cpc, cost_per_conversion per campaign per date.

## report.ad

Ad-level performance report.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "date_range": "LAST_30_DAYS",
  "limit": 50
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | no | Filter by campaign |
| ad_group_id | string | no | Filter by ad group |
| date_range | string | no | Default `LAST_30_DAYS` |
| limit | int | no | Max rows (1-500, default 50) |

## report.search_terms

Search terms performance report.

```json
{
  "campaign_id": "23219624121",
  "date_range": "LAST_30_DAYS",
  "limit": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | no | Filter by campaign |
| ad_group_id | string | no | Filter by ad group |
| date_range | string | no | Default `LAST_30_DAYS` |
| limit | int | no | Max rows (1-500, default 100) |

Returns: search_term, keyword_text, keyword_match_type, impressions, clicks, cost, conversions, ctr, avg_cpc, cost_per_conversion.

## report.gaql

Run a custom GAQL query. Returns raw API results.

```json
{
  "query": "SELECT campaign.id, campaign.name, metrics.impressions FROM campaign WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_7_DAYS ORDER BY metrics.impressions DESC LIMIT 10"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | GAQL query (min 10 chars) |

Returns raw API results without parsing. For flattened results and validation, use `gaql.run` instead (see [gaql.md](gaql.md)).

**GAQL reference**: [Google Ads Query Language grammar](https://developers.google.com/google-ads/api/docs/query/grammar)

```

## skills/google-ads-cli/references/targeting.md
```markdown
# Targeting & Budget Operations (5)

Budget updates, location/language targeting, and campaign-level negative keywords.

## search.budget.update

Update daily budget for campaigns.

```json
{
  "budget_updates": [
    { "campaign_id": "23219624121", "amount": 15.0 }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| budget_updates | array | yes | 1-100 budget updates |
| budget_updates[].campaign_id | string | yes | Campaign ID |
| budget_updates[].amount | float | yes | New daily budget (0.01-100000) |

## search.criteria.add

Add location and/or language targeting to a campaign.

```json
{
  "campaign_id": "23219624121",
  "location_ids": ["2840", "2124"],
  "language_ids": ["1000", "1001"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| location_ids | string[] | no | Geo target constant IDs (e.g. 2840 = US, 2124 = CA) |
| language_ids | string[] | no | Language constant IDs (e.g. 1000 = English, 1001 = French) |

## search.criteria.list

List all criteria for campaigns.

```json
{
  "campaign_ids": ["23219624121"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_ids | string[] | yes | 1-20 campaign IDs |

## search.criteria.remove

Remove campaign criteria.

```json
{
  "campaign_id": "23219624121",
  "criterion_ids": ["12345", "67890"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| criterion_ids | string[] | yes | Criterion IDs to remove |

## search.criteria.add_negatives

Add campaign-level negative keywords.

```json
{
  "campaign_id": "23219624121",
  "negative_keywords": [
    { "text": "free download", "match_type": "BROAD" },
    { "text": "open source", "match_type": "PHRASE" }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| negative_keywords | array | yes | 1-1000 negative keywords |
| negative_keywords[].text | string | yes | Keyword text (1-80 chars) |
| negative_keywords[].match_type | string | no | `EXACT`, `PHRASE`, or `BROAD` (default) |

```


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
- **Metrics / Traces**: <!-- TODO: Grafana dashboard URL -->
- **Errors**: <!-- TODO: Sentry project link -->

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| SDK cookies not shared across subdomains | eTLD+1 landed on a public suffix (`.vercel.app`, `.github.io`) | Pass explicit `domain` to the SDK init |
| `alembic upgrade head` hits "multiple heads" | Feature branches added migrations in parallel | `alembic merge heads -m "..."` then upgrade |
| Lead table missing rows for known users | Event extracts `name`/`email` lazily; `setUserId` hasn't fired yet | Check SDK `setUserId` wiring on the customer site |

## Contributing

- Read [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md) before non-trivial changes.
- PR expectations: [.github/pull_request_template.md](.github/pull_request_template.md).
- Architecture decisions: [docs/adr/](docs/adr/).

## Related Repos

- Downstream consumers of the SDK — <!-- TODO: list known integrators -->

---

<sub>Scaffolded from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template).</sub>

```

## CLAUDE.md
```markdown
# CLAUDE.md

<!-- Per-repo identity. Org-wide rules live in AGENTS.md. Keep <~50 lines. -->

@AGENTS.md

## Purpose

GetuAI Attribution v2 — ads attribution and lead tracking. A browser SDK captures UTM-driven user journeys across subdomains; two FastAPI services ingest events and expose a dashboard API; a Next.js app renders analytics and lead management. Current focus: refactor `server/` / `events-track-server/` / `sdk/` to feed `frontend-v2/`'s new UI. Current refactor scope is tracked in `target.md`.

## Architecture (5 landmines)

- **Monorepo, 4 active deployables**: `sdk/` (browser JS), `events-track-server/` (FastAPI ingress + consumer), `server/` (FastAPI dashboard API), `frontend-v2/` (Next.js 14, :3103). `frontend/` is legacy v1 — prefer `frontend-v2/` for anything new.
- **Dual MySQL schemas in `server/`** — `ADS_DB_NAME` (default; alembic migrations target this) + `DATA_DB_NAME`. Writes/reads may land in either depending on the table; check `server/core/database.py` before adding a model.
- **Cross-subdomain session via root-domain cookies** — SDK auto-detects eTLD+1 and writes `_getuai_session` / `_getuai_attrib` / `getuai_user_id` there. Public suffixes (`.vercel.app`, `.github.io`) break auto-detection and need an explicit `domain` config. See `sdk/src/session/`.
- **Event dispatch bifurcates** — `PURCHASE` / `LOGIN` / `SIGNUP` / `FORM_SUBMIT` / `EMAIL_VERIFICATION` / `AUDIT_APPROVED` send **immediately**; all others batch every 2s or at 100 events. Don't silently add a new "conversion-type" event to the batch path — data loss is invisible.
- **`setUserId` session rotation** — anonymous → `setUserId(A)` keeps the same `session_id` (backend backfills). `setUserId(A)` → `setUserId(B)` **rotates** `session_id`. Logout alone does NOT rotate.

## Domain Vocabulary

- **tracking_user_id** — per-company identifier: UUID for anonymous, caller-provided for identified users.
- **lead** — `(company_id, tracking_user_id)` tuple with name/email/phone extracted from form_submit / signup / login events; fields: `score` 0–100, `status` ∈ {new, engaged, qualified, opportunity, customer, churned}, `signal_strength` ∈ {hot, warm, cold}.
- **attribution** — first-touch + last-touch UTM snapshot, one record per session (not per user).
- **session_id** — survives cross-subdomain navigation; rotates only on user-identity change.

## Run Locally

```bash
# SDK
cd sdk && npm install && npm run build

# Dashboard API (server/)
cd server && uv sync && cp env.example .env    # fill DB_HOST / ADS_DB_NAME / DATA_DB_NAME
alembic upgrade head && python start.py         # :8000

# Event ingress + consumer (events-track-server/)
cd events-track-server && uv sync && cp configs/env.example .env
python -m api.main                              # :8019

# Frontend v2 (current UI)
cd frontend-v2 && npm install && npm run dev    # :3103
```

## Common Tasks

- **SDK tests**: `cd sdk && npm test` — cross-subdomain + session-rotation regressions via `npm run test:regression`.
- **SDK version bump**: edit `sdk/package.json` version → `npm run build` (scripts/update-version.js syncs `src/version.ts`).
- **DB migrations**: `alembic upgrade head` — run in `server/` and `events-track-server/` separately (each has its own `alembic/`).
- **Deploy**: `cd deploy && ./deploy.sh -b main -e production -y`; full docs in `deploy/DEPLOYMENT.md`.

## File Ownership (per-repo caution levels)

- **High caution** (ask before editing): `server/alembic/`, `events-track-server/alembic/`, `sdk/src/` public API surface, `nginx.conf` routing.
- **Legacy — prefer `frontend-v2/`**: `frontend/` is v1 React+Vite, only touch for critical bugs.
- **AGENTS.md §Core Principles #3 known exception**: `events-track-server/consumer/dead_letter_service.py` and `events-track-server/service/queue/pubsub_queue_client.py` directly import `google.cloud.pubsub_v1`. See `docs/adr/0001-accept-gcp-pubsub-in-events-tracker.md`.
- **Active security debt**: see `docs/security/known-leaks.md` — a GCP service-account private key is currently tracked in HEAD (`events-track-server/credentials/gcp-pub-sub.json`), rotation deferred. New credentials MUST go through env / Secret Manager, never into a file under `credentials/`.

<!-- Path-based review routing: see .github/CODEOWNERS (pending team setup) -->

每次做spec最终测试，都需要把env和credentials通过worktree-setup.shcp到相关的worktree，来启动浏览器测试环境或者必要的带环境的代码测试

---

<sub>Org-wide rules: [AGENTS.md](AGENTS.md). Deep guides auto-trigger as skills — list via `~/.optiminds/scripts/install-skills.sh list`.</sub>

```

## AGENTS.md
```markdown
# AGENTS.md

<!--
Organization-wide agent instructions for every Optiminds repository. This
file is the single source of truth for cross-repo rules. It is readable by
Claude Code (via `@AGENTS.md` reference in CLAUDE.md), Codex CLI (native),
Cursor, Aider, and Continue (all auto-load AGENTS.md).

Per-repo identity lives in CLAUDE.md, not here. This file should almost
never diverge between repos — if you feel the urge to override a rule
here for one repo, write an ADR instead.

Keep under ~200 lines. When a topic needs more depth, add it as a skill in
`skills/optiminds-<topic>/SKILL.md` — skills auto-trigger on matching
context and don't bloat the always-loaded AGENTS.md.
-->

## Core Principles

<!-- DRAFT: Stometa to finalize. These 7 principles were drafted from the
2026-04-21 CTO brainstorm (rankgale incident, cloud migration, harness
model). Refine the wording / ordering / add-remove as needed before the
first major adoption. -->

1. **Never commit secrets.** Every `.env*`, `credentials/`, `keys/`, token,
   or API key must be in `.gitignore` **before** the file is written.
   If a secret leaks to git history: rotate first in Key Vault, then clean
   history. Never reverse that order.

2. **CI must pass to merge.** No `--no-verify`, no skipping checks, no
   direct-to-main commits. If CI is broken and the fix is unclear, stop
   and ask. Broken CI is a P1.

3. **No cloud-vendor SDK in business code.** No `azure.*`, `@azure/*`,
   `google-cloud-*`, `@aws-sdk/*` imports under `/src/`, `/backend/`, `/api/`,
   `/frontend/`, `/sdk/`, `/cli/`. Secrets, storage, queues all come
   through `os.environ[...]` / `process.env.*`. Cloud migration must cost
   days, not months.

4. **Structured logs + metrics + traces on every production code path.**
   New endpoint / new agent / new background job = three signals emitted.
   No `print()`, no bare `logging.info("...")`. See skill `optiminds-obs`
   for the exact conventions (skill auto-triggers on relevant tasks).

5. **Tests ship with the code.** Same PR, not a follow-up. If a bugfix has
   no regression test, the bug will come back.

6. **Architectural changes need an ADR.** Any decision that's "1+ week of
   work", introduces a new external dependency, or changes a public
   contract goes in `docs/adr/` as a MADR-style record before or with the
   implementation PR.

7. **When in doubt, stop and ask.** Read AGENTS.md first, check relevant
   skill descriptions, consult `docs/adr/`, then ask a human. Never
   fabricate conventions under pressure.

## Git & PR Workflow

- **Branches**: `feature/<slug>` or `fix/<slug>`. Never push to `main`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `perf:`, `ci:`). Short subject, body explains WHY.
- **No `Co-Authored-By:` lines** on AI-assisted commits. Authorship =
  the human who approved the PR.
- **PR template**: see `.github/pull_request_template.md`. All 8 sections
  are required — "rollback" and "observability" especially.
- **Review**: every PR gets (a) Codex 3-pass AI review, (b) at least one
  human reviewer per CODEOWNERS. Strict paths (`billing/`, `auth/`,
  `migrations/`) require human approval to merge.
- **Merge**: squash-merge by default; merge commit for release PRs.

## Security Red Lines

These are non-negotiable. Violation = immediate revert + incident ticket.

| Red line | Enforcement |
|---|---|
| No secrets in git (past or present) | `gitleaks` pre-commit + CI + nightly full-history scan |
| No cloud-SDK in business code | (v0.3) `lint-cloud-sdk-imports.sh` in CI |
| No plaintext PII in logs | observability lint (v0.3) + manual review |
| No dynamic code execution on user input | code review + ruff / eslint rules |
| No disabling CI to merge | branch protection rules |
| No force-push to `main` | branch protection rules |

## Testing

- Minimum coverage: 80% on lines changed in a PR.
- TDD discipline: write the failing test first, implement to green, refactor.
- Unit + integration + at least one E2E per critical user flow.
- Never mock what you can inject (dependency inversion > magic mocks).
- See skill `optiminds-testing` for stack-specific patterns (Python pytest,
  TS vitest, etc.) — skill auto-triggers when you're writing tests.

## Engineering Discipline

Rules distilled from harness retros. Each bullet is a load-bearing
invariant — a past task shipped or nearly shipped a bug because the rule
wasn't followed. Source retros tagged `harness-retro` in the issue tracker.

### Planning discipline

- **SC / CP scope parity** — when a Success Criterion uses a universal-tree
  predicate ("no references in surviving files", "all callers", "nothing
  imports X"), the enforcing Checkpoint acceptance criterion MUST evaluate
  the same scope. If the CP is narrower, require BOTH a CP-local check AND
  a spec-level residual check (whole-tree grep against a sentinel whitelist).
  Narrower-CP-only defers drift detection to E2E. _(retro: v0.3.0 ship)_
- **Tool-behaviour claims need evidence at spec time** — any spec assertion
  about a third-party tool (bats, jq, shellcheck, release-please,
  actions/checkout, etc.) must cite evidence against the repo's **pinned**
  version: a runnable command + literal output (≤20 lines) + ISO-8601 date,
  OR a changelog/docs link for that version. Tool behaviour changes across
  versions; "it should work" is not a spec claim. _(retro: version-check-e2e)_

### Code discipline

- **Git worktree detection** — detect a working tree with
  `git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1`,
  NEVER `[[ -d "$TARGET/.git" ]]` or `[[ -e "$TARGET/.git" ]]`. In worktrees
  and submodules, `.git` is a regular file pointing into the main repo's
  `.git/worktrees/` dir — the directory test fails silently on valid
  setups. Regression-test any such check with `git worktree add`.
  _(retro: v0.3.0 ship)_
- **Atomic file writes require same-filesystem tempfile** — use
  `tmp=$(mktemp "${target}.XXXXXX")` (same dir → same fs), then
  `write_to "$tmp" && mv "$tmp" "$target"`. Naked `mktemp` defaults to
  `$TMPDIR` (typically `/tmp`), which on macOS, CI runners, and most
  Linux distros is a separate filesystem — cross-fs `mv` degrades to
  copy-then-unlink and is NOT atomic. Reviewers: an unadorned `mktemp`
  on an "atomic writer" AC is a finding, not a pass. _(retro: version-check-e2e)_
- **Bash arithmetic on parsed integers needs `10#` base prefix** — any
  `$((expr))` whose operands come from parsed string input (arguments,
  file content, SemVer components, line numbers) MUST prefix each
  operand: `(( 10#$major > 10#$other_major ))`. Bash parses leading-zero
  decimals as octal; `08` and `09` are invalid octal digits → "value
  too great for base". Literal integers written in script source are
  exempt (author controls their form). Every shell lib doing arithmetic
  on parsed integers must include a leading-zero test. _(retro: version-check-e2e)_

### CI discipline

- **Default `GITHUB_TOKEN` does NOT trigger downstream workflows** —
  GitHub intentionally skips downstream workflow triggers for events
  produced by actions running with the default token (security feature
  to prevent action self-escalation). For `workflow-A creates event →
  workflow-B runs` chains, choose one: (a) **inline** the downstream
  work into A (preferred — self-contained, no token management), (b)
  use a PAT or GitHub App token in A, or (c) document explicitly that
  B runs only on human-pushed events. Every cross-workflow handoff
  needs a dry-run or CI test before shipping.
  Ref: <https://docs.github.com/en/actions/security-guides/automatic-token-authentication>
  _(retro: v0.3.0 ship)_

### Documentation discipline

- **Flow-change doc-sync** — when changing a user-visible flow (release,
  deploy, adoption, onboarding), (1) grep the tree for every doc that
  describes the flow BEFORE changing it, (2) update every match in the
  SAME commit/PR as the code change, (3) cross-model review must
  explicitly verify doc-to-code consistency after the change. Three
  docs can describe a single flow; the old description silently outlives
  the code if doc-sync isn't forced. _(retro: v0.3.0 ship — README,
  CONTRIBUTING, CHANGELOG each independently described the broken
  pre-fix release flow and all three survived the first-pass review)_

### Evaluation discipline

- **Malformed-input fault-path probe** — every backend check whose code
  reads or parses external input (files, env vars, stdin, arguments
  that flow into `jq` / `sed` / `awk` / `python` / bash parameter
  expansion) MUST test the malformed-input branch in its evaluation:
  either (a) a test in the CP suite feeding invalid JSON / non-numeric
  version / trailing backslash / embedded newline and asserting a
  well-defined behaviour (error message + exit code, or graceful-
  degrade), OR (b) an evaluator-led simulation documenting
  stdout/stderr/exit code under a `Fault-path probe` heading. Pure-
  computation CPs with no external input must state
  `Fault-path probe: N/A` explicitly so the question is visibly asked
  and answered. Atomic-writer patterns require the same-fs tempfile
  check from Code discipline above. _(retro: version-check-e2e — 3
  malformed-input crashes caught by peer after all internal evaluators
  passed happy-path)_

## Tooling Setup

This repo assumes Optiminds organization-wide AI skills and subagents are
installed — once per developer machine. Skills auto-trigger in your CLI
based on task context. For the exact install / update / troubleshoot
commands, see [`docs/tooling-setup.md`](../docs/tooling-setup.md).

## Cross-Repo Glossary

<!-- Terms that mean the same thing across all Optiminds repos. Resist the
urge to redefine per-repo. Additions to this glossary happen via platform-
owners review. -->

- **Consumer** — a paying end-user of an Optiminds product (e.g., a law firm
  on lawyer_marketing). NOT synonymous with "customer" in billing contexts.
- **Tenant** — a logical isolation boundary in multi-tenant services
  (one customer org = one tenant = one `tenant_id` on every structured log).
- **Service** — a deployable unit (a FastAPI app, a worker, a CLI). Each
  repo may host multiple services under separate directories.
- **Agent** — an LLM-orchestrated workflow (Claude / Codex / in-house).
  NOT a user role.

## References

- Per-repo identity: `CLAUDE.md` (repo root)
- Deep guides: skills auto-trigger from `~/.claude/plugins/optiminds/skills/`
  (or your CLI's equivalent). List them: `~/.optiminds/scripts/install-skills.sh list`
- PR template: `.github/pull_request_template.md`
- CODEOWNERS: `.github/CODEOWNERS`
- Review rules: `.codex.yaml`
- Incident SLA: `SECURITY.md`
- Change governance: `CONTRIBUTING.md`

---

<sub>Structure from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template). Do not edit Core Principles / Security Red Lines without platform-owners review. Domain-specific sections can be added below this line per-repo if strictly necessary — prefer `CLAUDE.md` or a skill first.</sub>

```

## agents.md
```markdown
# AGENTS.md

<!--
Organization-wide agent instructions for every Optiminds repository. This
file is the single source of truth for cross-repo rules. It is readable by
Claude Code (via `@AGENTS.md` reference in CLAUDE.md), Codex CLI (native),
Cursor, Aider, and Continue (all auto-load AGENTS.md).

Per-repo identity lives in CLAUDE.md, not here. This file should almost
never diverge between repos — if you feel the urge to override a rule
here for one repo, write an ADR instead.

Keep under ~200 lines. When a topic needs more depth, add it as a skill in
`skills/optiminds-<topic>/SKILL.md` — skills auto-trigger on matching
context and don't bloat the always-loaded AGENTS.md.
-->

## Core Principles

<!-- DRAFT: Stometa to finalize. These 7 principles were drafted from the
2026-04-21 CTO brainstorm (rankgale incident, cloud migration, harness
model). Refine the wording / ordering / add-remove as needed before the
first major adoption. -->

1. **Never commit secrets.** Every `.env*`, `credentials/`, `keys/`, token,
   or API key must be in `.gitignore` **before** the file is written.
   If a secret leaks to git history: rotate first in Key Vault, then clean
   history. Never reverse that order.

2. **CI must pass to merge.** No `--no-verify`, no skipping checks, no
   direct-to-main commits. If CI is broken and the fix is unclear, stop
   and ask. Broken CI is a P1.

3. **No cloud-vendor SDK in business code.** No `azure.*`, `@azure/*`,
   `google-cloud-*`, `@aws-sdk/*` imports under `/src/`, `/backend/`, `/api/`,
   `/frontend/`, `/sdk/`, `/cli/`. Secrets, storage, queues all come
   through `os.environ[...]` / `process.env.*`. Cloud migration must cost
   days, not months.

4. **Structured logs + metrics + traces on every production code path.**
   New endpoint / new agent / new background job = three signals emitted.
   No `print()`, no bare `logging.info("...")`. See skill `optiminds-obs`
   for the exact conventions (skill auto-triggers on relevant tasks).

5. **Tests ship with the code.** Same PR, not a follow-up. If a bugfix has
   no regression test, the bug will come back.

6. **Architectural changes need an ADR.** Any decision that's "1+ week of
   work", introduces a new external dependency, or changes a public
   contract goes in `docs/adr/` as a MADR-style record before or with the
   implementation PR.

7. **When in doubt, stop and ask.** Read AGENTS.md first, check relevant
   skill descriptions, consult `docs/adr/`, then ask a human. Never
   fabricate conventions under pressure.

## Git & PR Workflow

- **Branches**: `feature/<slug>` or `fix/<slug>`. Never push to `main`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `perf:`, `ci:`). Short subject, body explains WHY.
- **No `Co-Authored-By:` lines** on AI-assisted commits. Authorship =
  the human who approved the PR.
- **PR template**: see `.github/pull_request_template.md`. All 8 sections
  are required — "rollback" and "observability" especially.
- **Review**: every PR gets (a) Codex 3-pass AI review, (b) at least one
  human reviewer per CODEOWNERS. Strict paths (`billing/`, `auth/`,
  `migrations/`) require human approval to merge.
- **Merge**: squash-merge by default; merge commit for release PRs.

## Security Red Lines

These are non-negotiable. Violation = immediate revert + incident ticket.

| Red line | Enforcement |
|---|---|
| No secrets in git (past or present) | `gitleaks` pre-commit + CI + nightly full-history scan |
| No cloud-SDK in business code | (v0.3) `lint-cloud-sdk-imports.sh` in CI |
| No plaintext PII in logs | observability lint (v0.3) + manual review |
| No dynamic code execution on user input | code review + ruff / eslint rules |
| No disabling CI to merge | branch protection rules |
| No force-push to `main` | branch protection rules |

## Testing

- Minimum coverage: 80% on lines changed in a PR.
- TDD discipline: write the failing test first, implement to green, refactor.
- Unit + integration + at least one E2E per critical user flow.
- Never mock what you can inject (dependency inversion > magic mocks).
- See skill `optiminds-testing` for stack-specific patterns (Python pytest,
  TS vitest, etc.) — skill auto-triggers when you're writing tests.

## Engineering Discipline

Rules distilled from harness retros. Each bullet is a load-bearing
invariant — a past task shipped or nearly shipped a bug because the rule
wasn't followed. Source retros tagged `harness-retro` in the issue tracker.

### Planning discipline

- **SC / CP scope parity** — when a Success Criterion uses a universal-tree
  predicate ("no references in surviving files", "all callers", "nothing
  imports X"), the enforcing Checkpoint acceptance criterion MUST evaluate
  the same scope. If the CP is narrower, require BOTH a CP-local check AND
  a spec-level residual check (whole-tree grep against a sentinel whitelist).
  Narrower-CP-only defers drift detection to E2E. _(retro: v0.3.0 ship)_
- **Tool-behaviour claims need evidence at spec time** — any spec assertion
  about a third-party tool (bats, jq, shellcheck, release-please,
  actions/checkout, etc.) must cite evidence against the repo's **pinned**
  version: a runnable command + literal output (≤20 lines) + ISO-8601 date,
  OR a changelog/docs link for that version. Tool behaviour changes across
  versions; "it should work" is not a spec claim. _(retro: version-check-e2e)_

### Code discipline

- **Git worktree detection** — detect a working tree with
  `git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1`,
  NEVER `[[ -d "$TARGET/.git" ]]` or `[[ -e "$TARGET/.git" ]]`. In worktrees
  and submodules, `.git` is a regular file pointing into the main repo's
  `.git/worktrees/` dir — the directory test fails silently on valid
  setups. Regression-test any such check with `git worktree add`.
  _(retro: v0.3.0 ship)_
- **Atomic file writes require same-filesystem tempfile** — use
  `tmp=$(mktemp "${target}.XXXXXX")` (same dir → same fs), then
  `write_to "$tmp" && mv "$tmp" "$target"`. Naked `mktemp` defaults to
  `$TMPDIR` (typically `/tmp`), which on macOS, CI runners, and most
  Linux distros is a separate filesystem — cross-fs `mv` degrades to
  copy-then-unlink and is NOT atomic. Reviewers: an unadorned `mktemp`
  on an "atomic writer" AC is a finding, not a pass. _(retro: version-check-e2e)_
- **Bash arithmetic on parsed integers needs `10#` base prefix** — any
  `$((expr))` whose operands come from parsed string input (arguments,
  file content, SemVer components, line numbers) MUST prefix each
  operand: `(( 10#$major > 10#$other_major ))`. Bash parses leading-zero
  decimals as octal; `08` and `09` are invalid octal digits → "value
  too great for base". Literal integers written in script source are
  exempt (author controls their form). Every shell lib doing arithmetic
  on parsed integers must include a leading-zero test. _(retro: version-check-e2e)_

### CI discipline

- **Default `GITHUB_TOKEN` does NOT trigger downstream workflows** —
  GitHub intentionally skips downstream workflow triggers for events
  produced by actions running with the default token (security feature
  to prevent action self-escalation). For `workflow-A creates event →
  workflow-B runs` chains, choose one: (a) **inline** the downstream
  work into A (preferred — self-contained, no token management), (b)
  use a PAT or GitHub App token in A, or (c) document explicitly that
  B runs only on human-pushed events. Every cross-workflow handoff
  needs a dry-run or CI test before shipping.
  Ref: <https://docs.github.com/en/actions/security-guides/automatic-token-authentication>
  _(retro: v0.3.0 ship)_

### Documentation discipline

- **Flow-change doc-sync** — when changing a user-visible flow (release,
  deploy, adoption, onboarding), (1) grep the tree for every doc that
  describes the flow BEFORE changing it, (2) update every match in the
  SAME commit/PR as the code change, (3) cross-model review must
  explicitly verify doc-to-code consistency after the change. Three
  docs can describe a single flow; the old description silently outlives
  the code if doc-sync isn't forced. _(retro: v0.3.0 ship — README,
  CONTRIBUTING, CHANGELOG each independently described the broken
  pre-fix release flow and all three survived the first-pass review)_

### Evaluation discipline

- **Malformed-input fault-path probe** — every backend check whose code
  reads or parses external input (files, env vars, stdin, arguments
  that flow into `jq` / `sed` / `awk` / `python` / bash parameter
  expansion) MUST test the malformed-input branch in its evaluation:
  either (a) a test in the CP suite feeding invalid JSON / non-numeric
  version / trailing backslash / embedded newline and asserting a
  well-defined behaviour (error message + exit code, or graceful-
  degrade), OR (b) an evaluator-led simulation documenting
  stdout/stderr/exit code under a `Fault-path probe` heading. Pure-
  computation CPs with no external input must state
  `Fault-path probe: N/A` explicitly so the question is visibly asked
  and answered. Atomic-writer patterns require the same-fs tempfile
  check from Code discipline above. _(retro: version-check-e2e — 3
  malformed-input crashes caught by peer after all internal evaluators
  passed happy-path)_

## Tooling Setup

This repo assumes Optiminds organization-wide AI skills and subagents are
installed — once per developer machine. Skills auto-trigger in your CLI
based on task context. For the exact install / update / troubleshoot
commands, see [`docs/tooling-setup.md`](../docs/tooling-setup.md).

## Cross-Repo Glossary

<!-- Terms that mean the same thing across all Optiminds repos. Resist the
urge to redefine per-repo. Additions to this glossary happen via platform-
owners review. -->

- **Consumer** — a paying end-user of an Optiminds product (e.g., a law firm
  on lawyer_marketing). NOT synonymous with "customer" in billing contexts.
- **Tenant** — a logical isolation boundary in multi-tenant services
  (one customer org = one tenant = one `tenant_id` on every structured log).
- **Service** — a deployable unit (a FastAPI app, a worker, a CLI). Each
  repo may host multiple services under separate directories.
- **Agent** — an LLM-orchestrated workflow (Claude / Codex / in-house).
  NOT a user role.

## References

- Per-repo identity: `CLAUDE.md` (repo root)
- Deep guides: skills auto-trigger from `~/.claude/plugins/optiminds/skills/`
  (or your CLI's equivalent). List them: `~/.optiminds/scripts/install-skills.sh list`
- PR template: `.github/pull_request_template.md`
- CODEOWNERS: `.github/CODEOWNERS`
- Review rules: `.codex.yaml`
- Incident SLA: `SECURITY.md`
- Change governance: `CONTRIBUTING.md`

---

<sub>Structure from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template). Do not edit Core Principles / Security Red Lines without platform-owners review. Domain-specific sections can be added below this line per-repo if strictly necessary — prefer `CLAUDE.md` or a skill first.</sub>

```


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

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Facebook Ads Library API Documentation](https://www.facebook.com/ads/library/api/)
- [React Documentation](https://reactjs.org/)
- [Material-UI Documentation](https://mui.com/)
- [Vite Documentation](https://vitejs.dev/)

```

