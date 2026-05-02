# Repo: getuai-seo

## README.md
```markdown
# GetUAI SEO Assistant

This application provides a comprehensive interface for managing and analyzing SEO campaigns. The system is built with a three-layer architecture:

1. **UI Layer** - Frontend interface for user interaction
2. **MCP Layer** - Middle layer for SEO tools and API integration
3. **AI Layer** - Backend for intelligent processing and recommendations

## System Requirements

- Node.js (v16+)
- Python (v3.9+)
- npm or yarn

## Environment Setup

Before running the application, make sure you have the following environment variables set:

```
DEEPSEEK_API_BASE_URL=<deepseek-api-url>
DEEPSEEK_API_KEY=<your-deepseek-api-key>
```

## Installation

Clone the repository and install dependencies for each component:

```bash
# Clone the repository
git clone <repository-url>
cd getuai-seo

# Install UI dependencies
cd v2-ui
npm install

# Install MCP layer dependencies
cd ../v2-mcp-seo
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

### 2. MCP Layer (SEO Tools Integration)

```bash
cd v2-mcp-seo

# Development 
# You need to create a `.env.development`, otherwise it will read from the default `.env`
python -m main

# Production
python -m main --env=production
```

This starts the MCP (Micro Control Program) layer that interfaces with various SEO tools and APIs, typically running on port 8004.

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
- **v2-mcp-seo**: Python-based middleware that handles SEO tools and API integration
- **v2-ai**: FastAPI backend that processes requests, manages sessions, and provides AI-powered recommendations

## Key Features

- SEO performance metrics and analysis
- Keyword research and tracking
- Content optimization recommendations
- Backlink analysis and management
- Competitor analysis
- AI-powered SEO strategy advisor
- Support for file uploads for enhanced analysis

## Troubleshooting

- If you encounter issues with API access, check your credentials and API keys
- For connection issues between layers, ensure all three components are running
- Check the console logs of each component for specific error messages

## Development

The codebase is organized as follows:

- `v2-ui`: Frontend code
- `v2-mcp`: Google Ads API integration
- `v2-ai`: FastAPI backend and AI processing
  - `api/`: API endpoints and core functionality
  - `features/`: Feature-specific modules, including SEO campaigns
  - `agents/`: AI agent implementations


```
