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
