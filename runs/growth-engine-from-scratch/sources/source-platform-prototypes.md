# source-platform-prototypes

Source digest auto-composed from 7 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- 0407-prototype
- 0408-prototype
- getuai-2.0
- getuai-mvp
- gmi-prototype
- getuai-comp-analysis-demo
- getuai-competitor-analysis

---

# Repo: 0407-prototype


# Repo: 0408-prototype


# Repo: getuai-2.0

## README.md
```markdown
<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1r8qvoChH2STCNMPBQkBPOes_lWmE1ewi

## Project Structure

```
.
├── frontend/          # React + Vite frontend application
│   ├── components/    # React UI components
│   ├── services/      # API service layer (Gemini AI)
│   ├── App.tsx        # Main application component
│   ├── index.tsx      # React DOM entry point
│   ├── index.html     # HTML template
│   ├── types.ts       # TypeScript type definitions
│   ├── vite.config.ts # Vite build configuration
│   ├── tsconfig.json  # TypeScript configuration
│   └── package.json   # Dependencies and scripts
├── .gitignore
└── README.md
```

## Run Locally

**Prerequisites:** Node.js

1. Navigate to the frontend directory:
   `cd frontend`
2. Install dependencies:
   `npm install`
3. Set the `GEMINI_API_KEY` in [frontend/.env.local](frontend/.env.local) to your Gemini API key
4. Run the app:
   `npm run dev`

```


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


# Repo: gmi-prototype

## README.md
```markdown
# GMI Cloud Video Generation Prototype

A simple Python prototype for generating videos using GMI Cloud's VideoGen API with an interactive interface.

## ✅ Features

- **Interactive video generation** with model selection
- **18+ GMI Cloud models** (Veo3, WAN-AI, Kling, Luma)
- **Batch video generation** (1-10 videos per session)
- **Automatic local storage** in `./generated_videos/`
- **Real-time progress monitoring**
- **Robust error handling**

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config.yaml and add your GMI Cloud API key
   ```

3. **Run video generation:**
   ```bash
   python generate_videos.py
   ```

## 🎬 Interactive Experience

The script guides you through:

1. **📋 Model Selection**: Choose from available models
   - Google Veo (Veo3, Veo3-Fast)
   - WAN-AI models (2.1, 2.2 variants)
   - Kling models (Text2Video, Image2Video)
   - Luma Ray2

2. **🔢 Video Count**: Specify 1-10 videos to generate

3. **✍️ Custom Prompt**: Enter your video description

4. **🎬 Automatic Generation**: Videos saved to `./generated_videos/`

## ⚙️ Configuration

Edit `config/config.yaml` with your GMI Cloud credentials:

```yaml
gmi_cloud:
  videogen:
    api_key: "your-gmi-api-key-here"
    base_url: "https://console.gmicloud.ai/api/v1"
```

## 📋 Sample Usage

```bash
$ python generate_videos.py

🎬============================================================🎬
       GMI CLOUD VIDEO GENERATION
🎬============================================================🎬

📋 Step 1: Loading Available Models
✅ Found 18 available models

📋 Step 2: Select Video Generation Model
🎬 Google Veo:
  1. Veo3-Fast
  2. Veo3
🎬 WAN-AI:
  3. Wan-AI_Wan2.2-T2V-A14B
  ...

Select model (1-18): 1
✅ Selected: Veo3-Fast

📋 Step 3: Number of Videos
Enter number of videos (1-10): 2
✅ Will generate 2 videos

📋 Step 4: Video Description  
Your prompt: A cat playing in a sunny garden
✅ Prompt: A cat playing in a sunny garden

📋 Step 5: Video Generation
🎬 Generating videos...
✅ Videos saved to ./generated_videos/
```

## 📁 Project Structure

```
gmi-prototype/
├── generate_videos.py              # 🎬 Main interactive script
├── README.md                       # 📖 This file
├── requirements.txt            

[... truncated to 2500 bytes; full extract at sources/_raw/gmi-prototype.md ...]


# Repo: getuai-comp-analysis-demo

## README.md
```markdown
# getuai-comp-analysis-demo
getuai competitor analysis demo

```


# Repo: getuai-competitor-analysis

## README.md
```markdown
# Keyword Research Tool

A powerful keyword research tool that combines Google Search and Google Ads API to generate keyword ideas and analyze search results.

## Features

- Search content using Google Custom Search API
- Generate keyword ideas using Google Ads API
- AI-powered keyword extraction from search results
- Simple web interface for easy interaction

## Prerequisites

- Python 3.9 or higher
- Google Ads API credentials (`google_ads1.yml`)
- Google Custom Search API key
- Google Custom Search Engine ID

## Setup

### 1. Create and Activate Virtual Environment

#### Windows

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

#### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

1. Ensure your `google_ads1.yml` is placed in the `api/` directory
2. Update the following credentials in `api/utils/google_search.py`:
   - `api_key`: Your Google Custom Search API key
   - `cx`: Your Custom Search Engine ID

### 4. Proxy Configuration (if needed)

If you need to use a proxy for API httpx:

1. Set system-wide proxy:

   ```bash
   # Windows (Command Prompt)
   set HTTP_PROXY=http://127.0.0.1:7890
   set HTTPS_PROXY=http://127.0.0.1:7890
   set NO_PROXY=127.0.0.1,127.0.0.1,::1 # local calls without proxy

   # macOS/Linux
   export HTTP_PROXY="http://127.0.0.1:7890"
   export HTTPS_PROXY="http://127.0.0.1:7890"
   ```

2. Add proxy configuration to `google_ads1.yml`:
   ```yaml
   http_proxy: http://127.0.0.1:7890
   ```
   For Python httpx library (if used):
   ```python
   os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
   os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
   ```

## Running the Application

1. Make sure your virtual environment is activated
2. Start the server with uvicorn:

#### Development mode (with auto-reload)

start keyword research mcp

```bash
cd mcp_server/keyword_research
python -m main
```

start competitor analysis mcp

```bash
cd mcp_server/competitor_analysis
python -m main
```

start a simple test UI

```bash
uvicorn main:app --host 127.0.0.1 --port 8006 --reload
```

#### Production mode

```bash
uvicorn main:app --host 127.0.0.1 --port 8006 --workers 4
```

3. Access the web interface at: http://127.0.0.1:800

[... truncated to 2500 bytes; full extract at sources/_raw/getuai-competitor-analysis.md ...]

