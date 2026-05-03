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
   - Configurable retention period

## Storage System

### Image Storage

#### Upload Image
```http
POST /api/v1/images/upload
Headers: 
  X-Session-Id: uuid-v4
Form Data:
  file: image_file
  name: image_name
  form_name: string (optional, defaults to "default")
Response: {
    "filename": "stored_image_name.ext"
}
```

#### List Session Images
```http
GET /api/v1/images
Headers: X-Session-Id: uuid-v4
Query Parameters:
  form_name: string (optional)
Response: {
    "images": [
        "image1.jpg",
        "image2.png"
    ]
}
```

#### Get Image
```http
GET /api/v1/images/{filename}
Headers: X-Session-Id: uuid-v4
Response: Image file
```

#### Delete Image
```http
DELETE /api/v1/images/{filename}
Headers: X-Session-Id: uuid-v4
```

#### Cleanup Form Images
```http
DELETE /api/v1/images
Headers: X-Session-Id: uuid-v4
Query Parameters:
  form_name: string (required)
```

### Text Storage

#### Save Company Info
```http
POST /api/v1/texts/save/companyInfo
Headers: 
  X-Session-Id: uuid-v4
Body: {
    "company_name": string,
    "company_description": string,
    "company_logo": string,
    "product_images": [
        {
            "title": string,
            "description": string,
            "filename": string
        }
    ],
    "promotional_images": [
        {
            "title": string,
            "description": string,
            "filename": string
        }
    ]
}
Response: {
    "status": "success"
}
```

#### List Session Texts
```http
GET /api/v1/texts
Headers: X-Session-Id: uuid-v4
Response: {
    "texts": [
        {
            "id": string,
            "content": string,
            "created_at": string
        }
    ]
}
```

#### Delete Session Texts
```http
DELETE /api/v1/texts
Headers: X-Session-Id: uuid-v4
```

All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (missing session ID)
- 404: Not Found (resource doesn't exist)
- 413: Payload Too Large (file size exceeds limit)
- 500: Internal Server Error

## Configuration

Required environment variables:
```bash
# Server Configuration
PORT=8000
API_V1_STR=/api/v1

# Storage Configuration
TEMP_IMAGE_STORAGE_DIR=storage
MAX_IMAGE_SIZE_MB=5
IMAGE_RETENTION_MINUTES=60

# Session Configuration
SESSION_RETENTION_MINUTES=30
```

## Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r re

[... truncated to 5000 bytes; full extract at sources/_raw/getuai-api.md ...]


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
│   │   └── schemas/     # Pydantic schemas
│   └── requirements.txt
├── frontend/            # Next.js frontend application
│   ├── app/            # Next.js app router pages
│   ├── components/     # React components
│   ├── lib/           # Utilities and API client
│   └── package.json
└── docker-compose.yml  # Docker configuration
```

## Development

### Backend Development

- FastAPI auto-reloads on file changes
- Async SQLAlchemy ORM with AsyncMy MySQL driver
- Environment-based configuration (.env.development)
- JWT authentication with configurable security
- Connection pooling optimized for performance
- CORS configured for frontend access

### Frontend Development

- Next.js with App Router
- TypeScript for type safety
- TanStack Query for data fetching
- Tailwind CSS for styling
- Recharts for data visualization

## Deployment

For production deployment:

1. Update environment variables in `.env` files
2. Build Docker images: `docker-compose build`
3. Run with Docker: `docker-compose up -d`
4. Configure reverse proxy (nginx/caddy) for production domains

## Security Notes

- Backend requires JWT authentication for all endpoints
- Database connection is read-only for user data
- CORS is configured to only allow specific origins
- Sensitive data (Stripe IDs, etc.) are masked in UI
```


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
- `npm format`: Format code

## Application Routes

### /chat
Chat interface for AI interactions:
- Initializes session if none exists
- Connects to AI service for message streaming
- Displays message history
- Handles errors and reconnection

### /company-info
Company information form:
- Collects company details
- Handles image uploads
- Validates form data
- Submits to API layer
- Redirects to chat on success

## Session Management

The session service (`src/services/session.ts`) handles:
- Session initialization
- Session ID storage
- Adding session headers to requests
- Session validation and retry logic
- Session expiration handling

### Session Flow

1. Initial Access:
   - Session service checks for existing session
   - If none exists, requests new session from API
   - Stores session ID for future requests

2. API Requests:
   - Session ID added to request headers
   - Automatic retry on session expiration
   - New session creation if needed

3. AI Service Requests:
   - Same session ID used for AI requests
   - Handles session validation failures
   - Maintains session consistency

## API Integration

### API Service (`src/services/api.ts`)
- Base URL: http://localhost:8000
- Handles form submissions
- Manages image uploads
- Stores company information

### AI Service (`src/services/ai.ts`)
- Base URL: http://localhost:8001
- Manages chat messages
- Handles streaming responses
- Maintains chat context

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License

MIT License - see LICENSE file for details

```


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

## Troubleshooting

### API Routing Issues

If you're experiencing API routing issues:

1. Check the environment setting - `process.env.NODE_ENV` should be `development` for local development
2. Verify your `API_PREFIX` environment variable is correctly set
3. For production, ensure your proxy server is properly configured to route `/api/*` requests to the backend

### Session Storage

Session IDs are stored in localStorage. If you experience session issues, try clearing localStorage in your browser. 
```


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

**Required for full functionality:**
- Azure OpenAI credentials for AI-powered analysis
- Google Ads Customer ID for keyword research  
- Google Search API key for search analysis
- All configuration files: `google_ads1.yml`, `service_account_credentials.json`

### 3. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

### 4. Test the API

```bash
# Test health endpoint
curl http://localhost:8010/health

# View all available endpoints
curl http://localhost:8010/

# Run test suite
python tests/test_basic_api.py
```

## API Endpoints

### SEO Analysis Tools
- `POST /api/v1/site-structure/analyze` - Website structure and link analysis
- `POST /api/v1/meta-tags/analyze` - Meta tags and social media optimization

### Competitor Analysis & Keyword Research Tools
- `POST /api/v1/google-search/analyze` - Google search results analysis
- `POST /api/v1/competitor-discovery/analyze` - AI-powered competitor identification
- `POST /api/v1/keyword-ideas/generate` - Keyword research with Google Ads API
- `POST /api/v1/url-content/analyze` - Content extraction and keyword analysis
- `POST /api/v1/keyword-clustering/analyze` - Semantic keyword clustering

### API Documentation
Complete OpenAPI 3.0.3 schemas available in `docs/schemas/`:
- `site_structure.analyze.schema.json`
- `meta_tags.analyze.schema.json`
- `google_search.analyze.schema.json`
- `competitor_discovery.analyze.schema.json`
- `keyword_ideas.generate.schema.json`
- `url_content.analyze.schema.json`
- `keyword_clustering.analyze.schema.json`

## Configuration

### Environment Variables

All configuration is managed through environment variables. See `.env.example` for complete configuration options.

#### Required API Keys
```bash
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_API_VERSION=2025-03-01-preview
COMPETITOR_DISCOVERY_MODEL=gpt-5
URL_CONTENT_ANALYSIS_MODEL=gpt-4.1
KEYWORD_CLUSTERING_MODEL=gpt-4.1-mini
KEYWORD_EXTRACTION_MODEL=gpt-4o
GOOGLE_ADS_CUSTOMER_ID=your-customer-id
GOOGLE_SEARCH_API_KEY=your-search-api-key
GOOGLE_SEARCH_CX=your-search-engine-id
```

#### Optional Configuration
```bash
LOG_LEVEL=INFO
REQUEST_TIMEOUT_SECONDS=30
DEBUG_MODE=false
```

### Google Ads API Setup

1. Create `google_ads.yml` configuration file:
```yaml
developer_token: "your-developer-token"
client_id: "your-client-id"
client_secret: "your-client-secret"
refresh_token: "your-refresh-token"
```

2. Set the config path:
```bash
GOOGLE_AD

[... truncated to 5000 bytes; full extract at sources/_raw/getuai-plugin.md ...]


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

- Focus: connections + the firm's core info. No activity items, no "first N articles published"-style milestones, no shipped-work history. Activity belongs on the agent pages.
- Pi-managed vs user-editable must be visible at a glance. Pi-managed = set during onboarding, locked in the dashboard, "message your partner to change". User-editable = anything the user should be able to update without us.
- User data fields default to **read-only**. An explicit `Edit` button unlocks them; `Save` commits, `Cancel` reverts. Never leave editable inputs always-hot — it invites accidental edits.

# Always read CLAUDE.md first

Every task: read `CLAUDE.md` and any files it imports (e.g. this `AGENTS.md`) before writing or editing code. The harness auto-loads them, but read them anyway — the principles override defaults.

```

## agents.md
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

- Focus: connections + the firm's core info. No activity items, no "first N articles published"-style milestones, no shipped-work history. Activity belongs on the agent pages.
- Pi-managed vs user-editable must be visible at a glance. Pi-managed = set during onboarding, locked in the dashboard, "message your partner to change". User-editable = anything the user should be able to update without us.
- User data fields default to **read-only**. An explicit `Edit` button unlocks them; `Save` commits, `Cancel` reverts. Never leave editable inputs always-hot — it invites accidental edits.

# Always read CLAUDE.md first

Every task: read `CLAUDE.md` and any files it imports (e.g. this `AGENTS.md`) before writing or editing code. The harness auto-loads them, but read them anyway — the principles override defaults.

```


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

Wait for the Codespace to initialize. Python 3.12, Node.js 19, and dependencies will be automatically installed.

Now you can continue with [Step 2: Configure Resources.](#step-2-configure-resources)

### Option B: Local Installation on your device

#### 1. Clone the Repository

```bash
git clone https://github.com/Azure-Samples/visionary-lab
```

#### 2. Backend Setup

##### 2.1 Install UV Package Manager

UV is a fast Python package installer and resolver that we use for managing dependencies.

Mac/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (using PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

##### 2.2 Copy environment file template

```bash
cp .env.example .env
```

The environment variables will be defined below.

#### 3. Frontend Setup

```bash
cd frontend
npm install --legacy-peer-deps
```

## Step 2: Configure Resources

1. Configure Azure credentials using a code or text editor:

   ```bash
   code .env
   ```

   Replace the placeholders with your actual Azure values:

   | Service / Model   | Variables                                                                                                                                                                                                                                                                                                                                                                      |
   | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | **Sora 2**        | - `SORA_AOAI_RESOURCE`: name of the Azure OpenAI resource used for Sora 2 <br> - `SORA_DEPLOYMENT`: deployment name for the Sora 2 model (typically `sora-2`) <br> - `SORA_AOAI_API_KEY`: API key for the Azure OpenAI Sora 2 resource                                                                  |
   | **GPT-Image-1**   | - `IMAGEGEN_AOAI_RESOURCE`: name of the Azure OpenAI resource used for gpt-image-1 <br> - `IMAGEGEN_DEPLOYMENT`: deployment name for the gpt-image-1 model <br> - `IMAGEGEN_AOAI_API_KEY`: API key for the gpt-image-1 resource                                                                              

[... truncated to 5000 bytes; full extract at sources/_raw/Visionary.md ...]


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
- Resolve gallery image version `latest` to the actual latest version name before VM or VMSS creation.
- Keep the builder VM separate from the image-build VM lifecycle.
- Use LF line endings for scripts uploaded to Linux.
- Treat `8444` and `18789` as first-class deployment ports, not optional debug ports.

## Windows Execution Guidance

- On Windows, prefer `powershell.exe -NoProfile -Command "& 'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd' ..."` for Azure CLI automation.
- Avoid mixing Git Bash quoting rules with long `az.cmd` command lines.
- If a backend or script needs Azure CLI from Python, call the executable directly with argument arrays instead of shell-joined strings.
- For SSH and SCP on Windows, rely on executable argument arrays and explicit key paths.

## KasmVNC Rules

- `claw-kasmvnc.service` must start KasmVNC with `-disableBasicAuth` for iframe embedding in the workbench.
- A `401 Unauthorized` on `8444` means basic auth is still enabled and the right-side desktop pane will not embed cleanly.
- After patching the service unit, run:
  - `systemctl daemon-reload`
  - `systemctl restart claw-kasmvnc.service`
- For quick verification, external reachability matters more than local process state.

## OpenClaw Rules

- Gateway default port is `18789`.
- Remote runtime config must enable HTTP responses and chat completions endpoints.
- Backend startup should inject runtime config and env files into `/home/claw/.openclaw/`.
- Backend task dispatch should use the remote gateway only after `/health` is reachable.
- If the desktop is ready but the gateway is not, machine state should not become fully ready.

## Troubleshooting Checklist

- Gallery version stuck in `Creating`:
  - Check Azure activity log.
  - Confirm source managed image succeeded.
  - Continue with the managed image if gallery replication is the only blocker.
- VM or VMSS has public IP but `8444` times out:
  - Check subnet NSG.
  - Check NIC-level auto-created NSG.
  - Confirm the instance inherited or attached the intended NSG.
- `8444` returns `401`:
  - KasmVNC basic auth is still active.
- `18789` is unreachable:
  - NSG rule is missing, or OpenClaw gateway is not healthy.
- Backend can start the machine but chat still behaves like mock:
  - Confirm `CLOUD_MACHINE_PROVIDER=azure_vmss`.
  - Confirm the remote runtime config was pushed successfully.
  - Confirm `/v1/responses` is enabled on the gateway.
- Bash command works badly with Azure CLI on Windows:
  - Move the command to PowerShell or Python subprocess arrays.

## Known Pitfalls To Remember

- CRLF line

[... truncated to 5000 bytes; full extract at sources/_raw/clawcloud.md ...]


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
- **Others**: More agents are in planning...

## Flexible Integrations
- **Multiple LLM Providers**: Support OpenRouter, OpenAI, Anthropic, Google and Ollama 
- **Popular Market Data**: Cover US market, Crypto market, Hong Kong market, China market and more
- **Multi-Agent Framework Compatible**: Support Langchain, Agno by A2A Protocol

# Quick Start

ValueCell is a Python-based application featuring a comprehensive web interface. Follow this guide to set up and run the application efficiently.

## Prerequisites

For optimal performance and streamlined development, we recommend installing the following tools:

**[uv](https://docs.astral.sh/uv/getting-started/installation/)** - Ultra-fast Python package and project manager built in Rust  
**[bun](https://github.com/oven-sh/bun#install)** - High-performance JavaScript/TypeScript toolkit with runtime, bundler, test runner, and package manager

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ValueCell-ai/valuecell.git
   cd valuecell
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your API keys and preferences. This configuration file is shared across all agents.

## Configuration

### Model Providers
Configure your preferred model providers by editing the ⁠`.env` file:

- **Primary Support**: [OpenRouter](https://openrouter.ai) - Currently the main supported provider for most agents
- **TradingAgents** requires the use of Memory. If you use OpenRouter as API key, configuring the Embedding model parameters will be needed (since OpenRouter does not support Embedding models). Please refer to the TradingAgents/.env.example file and copy its configuration into the .env file located in the root directory.
  

Choose your preferred models and providers based on your requirements and preferences.

## Running the Application

Launch the complete application stack (frontend, backend, and agents):

### Linux / Macos
```bash
bash start.sh
```

### Windows (PowerShell)
```powershell
.\start.ps1
```

## Accessing the Interface

- **Web UI**: Navigate to [http://localhost:1420](http://localhost:1420) in your browser
- **Logs**: Monitor application logs at `logs/{timestamp}/*.log` for detailed runtime information of backend services and individual agents

## Next Steps

Once the application is running, you can explore the web interface to interact with ValueCell's features and capabilities.

---

**Note**: E

[... truncated to 5000 bytes; full extract at sources/_raw/valuecell.md ...]


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
docker push gcr.io/<PROJECT_ID>/openbox-sandbox:latest
docker push gcr.io/<PROJECT_ID>/openbox-backend:latest
docker push gcr.io/<PROJECT_ID>/openbox-frontend:latest
```

### Step 5: 创建 K8s Secret

**重要**：Redis 密码中的特殊字符 `!@#$%` 等必须 URL 编码。

```bash
kubectl create secret generic openbox-secrets -n openbox \
  --from-literal=DATABASE_URL='<ASYNCPG_URL>' \
  --from-literal=REDIS_URL='<REDIS_URL_ENCODED>' \
  --from-literal=JWT_SECRET='<JWT_SECRET>' \
  --from-literal=SANDBOX_IMAGE='gcr.io/<PROJECT_ID>/openbox-sandbox:latest' \
  --from-literal=OPENBOX_API_KEY='<API_KEY>' \
  --from-literal=BLOB_AZURE_CONNECTION_STRING='<BLOB_CONN>' \
  --from-literal=BLOB_AZURE_CONTAINER='<CONTAINER_NAME>' \
  --from-literal=TAVILY_API_KEY='<TAVILY_KEY>' \
  --from-literal=OPENAI_API_KEY='<OPENAI_KEY>'
```

### Step 6: 创建镜像拉取凭证

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
for NS in openbox openbox-sandbox; do
  kubectl create secret docker-registry gcr-pull-secret -n $NS \
    --docker-server=gcr.io --docker-username=oauth2accesstoken \
    --docker-password="$ACCESS_TOKEN" --docker-email=<EMAIL>
done

# 绑定到 ServiceAccount
kubectl patch serviceaccount default -n openbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
```

### Step 7: 部署 K8s 资源

`k8s/base.yaml` 包含所有资源定义。部署前需：

1. 确认 `BLOB_PROVIDER` 值（azure 或 gcs）
2. 确认环境变量与 Secret key 匹配

```bash
sed "s/PROJECT_ID/<PROJECT_ID>/g" k8s/base.yaml | kubectl apply -f -
```

部署后绑定 imagePullSecret 到创建的 ServiceAccount：

```bash
kubectl patch serviceaccount openbox-backend -n openbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
kubectl patch serviceaccount sandbox-pods -n openbox-sandbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
```

### Step 8: 运行数据库 Migration

```bash
kubectl exec -n openbox deployment/openbox-backend -- uv run alembic upgrade head
```

**注意**：检查 migration 中的列长度是否与 ORM 模型一致（常见问题：`VARCHAR(26)` vs `String(64)`）。如不一致需手动 ALTER。

### Step 9: 配置外部访问（Ingress + HTTPS）

#### 预留静态 IP

```bash
gcloud compute addresses create <APP>-static-ip --global --project=<PROJECT_ID>
gcloud compute addresses describe <APP>-static-ip --global --format='get(address)'
```

#### 创建 ManagedCertificate + Ingress

参考 `.claude/gke-ingress-setup/SKILL.md` 中的完整流�

[... truncated to 5000 bytes; full extract at sources/_raw/project-base.md ...]


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
export WORKER_URL="https://github-pr-to-lark.<your-subdomain>.workers.dev"
export GITHUB_WEBHOOK_SECRET="<same value you set on the Worker>"
scripts/apply-webhook.sh webhooks/pr-to-lark.json
```

## Workflow

1. Edit the JSON file (e.g. `rulesets/main-protection.json`)
2. Open a PR against this repo so the change gets reviewed
3. After merge, run `scripts/apply-ruleset.sh <file>` to push the change to GitHub
4. Verify in the GitHub UI: `Organization settings → Repository rulesets`

## Future additions

- `settings/` — org-level settings snapshots (via `gh api /orgs/{org}`)
- `.github/workflows/apply.yml` — auto-apply on merge to `main`
- Terraform migration if ruleset count exceeds ~5 or we expand to multiple orgs

```


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
~/.optiminds/scripts/apply.sh --check ~/dev/my-repo
```

Sample up-to-date output:

```
==> Fetching latest template version...
==> Current applied:  0.4.1
==> Template latest:  0.4.1  (up-to-date)
```

Strict mode for CI exits non-zero when the consumer is behind, so a
pipeline step can surface the drift:

```bash
~/.optiminds/scripts/apply.sh --check --strict ~/dev/my-repo
```

Sample behind output:

```
==> Fetching latest template version...
==> Current applied:  0.3.0
==> Template latest:  0.4.1  (behind 1 minor, 1 patch)

Files that would change if you re-apply:
  M  .github/workflows/codex-review.yml         (template updated)
  !  AGENTS.md                                   (consumer modified — would skip without --force)
  +  docs/runbooks/cost-monitoring.template.md   (new in template)

Run: ~/.optiminds/scripts/apply.sh ~/dev/my-repo
```

Exit codes follow the `grep`/`diff` convention: `0` for up-to-date,
`2` for behind (under `--strict` only; default always exits 0), `1` for
real errors (missing metadata, malformed JSON, target not a git repo).

A compact push-mode banner fires automatically on `apply.sh <target>`
when the consumer's `template_version` is behind the template's current
version — no separate command needed. Sample banner when the consumer is
one minor + one patch behind:

```
==> Template metadata upgrade: 0.3.0 → 0.4.1 (1 minor + 1 patch)
==>   Run `apply.sh --check ~/dev/my-repo` for file-level diff before re-applying.
```

Set `OPTIMINDS_QUIET_VERSION=1` to silence the push-mode banner for
CI/scripted consumers that have already acknowledged the drift and don't
want log noise:

```bash
OPTIMINDS_QUIET_VERSION=1 ~/.optiminds/scripts/apply.sh ~/dev/my-repo
```

- Suppresses the minor / patch / ahead / first-tracking banners.
- Does **not** suppress the BREAKING banner for major version jumps — by
  design. Silently crossing a major boundary is the exact failure mode
  SemVer's major signal exists to prevent, so the BREAKING line is the
  one guard rail you cannot disable.

**Known limitation** — `--check` relies on the template clone's local
`origin/main` ref. A stale clone (corporate proxy that caches DNS, an
offline laptop, or a long-lived checkout) can report a false "up-to-date".
Run `git -C ~/.optiminds pull` periodically — or before a `--check` run
you care about — to refresh the local ref.

## What's in Layer 0 (the always-applies set)

| File | Purpose |
|---|---|
| `.github/workflows/codex-review.yml` | 3-pass Codex AI review

[... truncated to 5000 bytes; full extract at sources/_raw/optiminds-repo-template.md ...]

