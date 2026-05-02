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
   - CSV 格式: `email,first_name,last_name,company,position`

4. **创建 Email Batch**
   - 切换到 "Email Batch" 标签
   - 点击 "New Batch"，选择收件人筛选策略和数量
   - 从下拉框选择创建的 Batch

5. **AI 生成邮件内容**
   - 选择 Batch 后，点击 "Generate Content"
   - AI 会根据 Campaign 的 Prompt Template 为每个收件人生成个性化邮件

6. **发送邮件**
   - 检查生成的邮件内容
   - 点击 "Send Emails" 批量发送
   - 系统会随机选择已激活的 SMTP 账号发送

## ⚙️ 配置说明

### 后端环境变量 (.env)

```bash
# MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Bobliew0119!
DB_NAME=email

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt5-mini
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# App
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### 前端配置

后端 API 地址在各个组件中硬编码为 `http://localhost:8000`。如需修改，可以创建环境变量文件：

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

然后在代码中使用 `process.env.NEXT_PUBLIC_API_URL`。

## 🎨 UI/UX 特性

- ✅ Excel 风格表格，支持直接编辑
- ✅ 行号、复选框、多选删除
- ✅ 状态徽章 (Active, Pending, Sent, Failed)
- ✅ 模态框表单，优雅的交互动效
- ✅ 面包屑导航、Tab 切换
- ✅ 右侧边栏统计面板
- ✅ 响应式设计、自定义滚动条
- ✅ 完全还原原型设计系统

## 📦 项目结构

```
email_2.0/
├── backend/                 # FastAPI 后端
│   ├── src/
│   │   ├── core/            # 配置、数据库
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic 数据验证
│   │   ├── routers/         # API 路由
│   │   ├── services/        # 业务逻辑 (AI, Mailer)
│   │   └── main.py          # 应用入口
│   ├── bin/uv               # 启动脚本
│   ├── pyproject.toml       # Poetry 依赖
│   └── .env.example         # 环境变量模板
├── frontend/                # Next.js 前端
│   ├── app/                 # App Router
│   │   ├── layout.tsx       # 根布局
│   │   ├── page.tsx         # 主页面
│   │   └── globals.css      # 全局样式 (原型还原)
│   ├── components/          # React 组件
│   │   ├── views/           # 视图组件
│   │   │   ├── CampaignsView.tsx
│   │   │   ├── SMTPView.tsx
│   │   │   ├── RecipientsView.tsx
│   │   │   └── EmailBatchView.tsx
│   │   ├── Sidebar.tsx      # 侧边栏
│   │   ├── Modal.tsx        # 模态框
│   │   └── Toast.tsx        # 通知
│   ├── lib/                 # 工具函数
│   ├── package.json         # npm 依赖
│   └── tsconfig.json        # TypeScript 配置
├── docker-compose.yml       # Docker 编排 (MySQL)
├── prototype/               # 原始 HTML 原型
└── README.md                # 项目文档
```

## 🔒 安全注意事项

- ⚠️ SMTP 密码存储为明文，生产环境需加密存储
- ⚠️ 前端 API 调用未做认证，需添加 JWT 或 OAuth
- ⚠️ CORS 设置允许所有来源，生产环境需限制
- ⚠️ 数据库密码应使用环境变量，不应提交到代码仓库

## 🐛 故障排查

### 后端无法启动

- 确认 MySQL 运行且凭证正确
- 检查 `.env` 文件配置
- 运行 `poetry install` 重新安装依赖

### 前端报错

- 确认后端已启动在 8000 端口
- 运行 `npm install` 重新安装依赖
- 清除缓存：`rm -rf .next && npm run dev`

### SMTP 发送失败

- 确认 SMTP 账号已通过 "Test" 验证
- 检查 SMTP 服务器设置和凭证
- 某些邮箱（如 Gmail）需要开启"应用专用密码"

### AI 生成失败

- 确认 Azure OpenAI 凭证正确
- 检查 deployment 名称是否为 `gpt5-mini`
- 查看后端日志确认错误信息

## 📄 许可

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Built with ❤️ using FastAPI, Next.js, and Azure OpenAI**

```
