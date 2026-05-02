# source-social

Source digest auto-composed from 4 per-repo raw extracts under `runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections using `source-*.md§Repo: <name>` per §6.3.

## Table of Contents
- reddit-scount
- x-api-credit-monitor
- youtube-api-demo
- openclaw-marketing

---

# Repo: reddit-scount

## README.md
```markdown
# Reddit Scout

Find marketing opportunities on Reddit for your product.

## Project Structure

```
reddit_scout/
├── frontend/          # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── data/
│   │   └── styles/
│   └── package.json
├── backend/           # Python + FastAPI
│   ├── src/
│   │   ├── api/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── llm_config.py      # Azure OpenAI config
│   │   │   └── reddit_config.py   # SteadyAPI config
│   │   ├── models/
│   │   │   ├── opportunity.py
│   │   │   └── reddit.py          # Reddit data models
│   │   └── services/
│   │       ├── opportunity_service.py
│   │       ├── llm_service.py     # Azure OpenAI service
│   │       └── reddit_service.py  # Reddit/SteadyAPI service
│   ├── main.py
│   └── pyproject.toml
└── prototype.html     # Original prototype
```

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

### Backend (使用 uv)

```bash
cd backend

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# 安装依赖
uv sync

# 启动服务
uv run python main.py
```

Backend runs at http://localhost:8000

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# MySQL Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=reddit_scout
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=10

# SteadyAPI (for Reddit integration)
# Get your API key at: https://steadyapi.com/register
STEADY_API_KEY=your-steadyapi-key
```

## Database Setup

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE reddit_scout CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Initialize tables (auto-runs on app startup)
cd backend
python scripts/init_db.py
```

## API Endpoints

### Core Endpoints
- `GET /api/opportunities` - Get initial opportunities (mock data)
- `GET /api/opportunities/extra` - Get extra opportunities (mock data)
- `POS

[... truncated to 2500 bytes; full extract at sources/_raw/reddit-scount.md ...]


# Repo: x-api-credit-monitor

## README.md
```markdown
# x-api-credit-monitor

> Daily heartbeat + low-balance alert for X Developer Console credits,
> delivered to Lark.

## What this does

Every day at 09:00 local time this tool logs into `console.x.com` using your
Chrome session cookies, reads the current credit balance and last-7-day
spend, and posts a Lark message to the "Getu Ops Alerts" channel showing
balance, average daily burn, and days remaining. When the balance drops
below `LOW_BALANCE_THRESHOLD` it also posts a low-balance alert. When the
Chrome session has expired, it posts a "please re-login" alert so the next
day's run recovers automatically once you sign in again.

It runs as a macOS **launchd user agent**; no extra server or supervisor
is involved.

## Requirements

- macOS (launchd + `plutil` are used)
- Google Chrome with a logged-in profile at `console.x.com`
- Python 3.11 or newer
- A Lark **custom bot** webhook in the destination channel, with
  signature verification enabled

## Lark custom bot setup

One-time setup inside the Lark channel that should receive heartbeats:

1. Open the channel → **Settings (⋯)** → **Bots** → **Add bot** →
   **Custom Bot**.
2. Give it a name (e.g. `x-credit-monitor`) and description, then
   **Add**.
3. On the generated webhook page: **enable Signature verification** (this
   is mandatory for this tool — the code always signs requests).
4. Copy the **Webhook URL** → `LARK_WEBHOOK_URL` in `.env`.
5. Copy the **Sign secret** → `LARK_SIGN_SECRET` in `.env`.

The sign secret is never logged at any level — not at DEBUG, INFO,
WARNING, or ERROR — and never written to the stdout/stderr log files.

## Configuration (.env)

Copy `.env.example` to `.env` and fill in each field. The five required
variables are:

| Variable                      | Purpose                                                                                                                                       | Example                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `X_ACCOUNT_ID`                | X Developer Console account id — visible in the `console.x.com` URL once you are logged in.                                                   | `1234567890`                                  

[... truncated to 2500 bytes; full extract at sources/_raw/x-api-credit-monitor.md ...]


# Repo: youtube-api-demo

## README.md
```markdown
# YouTube API Demo

A simple web application that demonstrates how to use the YouTube Data API v3 to search for videos based on keywords.

## Features

- Search for YouTube videos using keywords
- Adjust the number of search results (5, 10, 25, or 50)
- View video thumbnails, titles, channel names, and descriptions
- Click to watch videos on YouTube

## Technologies Used

- Node.js and Express for the backend
- Vanilla JavaScript, HTML, and CSS for the frontend
- YouTube Data API v3 for fetching video data

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file in the root directory with your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   PORT=3000
   ```
4. Start the server:
   ```
   node src/server.js
   ```
5. Open your browser and navigate to `http://localhost:3000`

## How to Get a YouTube API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key and add it to your `.env` file

## API Endpoint

The application exposes the following API endpoint:

- `GET /api/search?query=SEARCH_TERM&maxResults=NUMBER_OF_RESULTS`
  - `query`: The search term (required)
  - `maxResults`: The number of results to return (optional, default: 10, max: 50)

## License

This project is licensed under the MIT License. 
```


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

