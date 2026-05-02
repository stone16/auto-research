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

3. Access the web interface at: http://127.0.0.1:8006/ui/index.html

## Project Structure

```
keyword-research/
├── api/
│   ├── google_ads1.yml              # Google Ads API configuration
│   ├── service_account_credentials.json
│   ├── generate_keyword_ideas.py    # Keyword generation logic
│   └── utils/
│       ├── google_search.py         # Google Search API integration
│       └── keyword_ideas.py         # Keyword processing utilities
├── mcp_server/
│   ├── competitor_analysis/         # Competitor analysis MCP service
│   └── keyword_research/           # Keyword research MCP service
├── ui/
│   └── index.html                  # Web interface
├── ai/
│   └── routers/                    # AI analysis endpoints
├── main.py                         # Main application entry
├── requirements.txt                # Project dependencies
├── .env                           # Environment variables
└── README.md                      # Project documentation
```

## Key Components

- `api/`: Google Ads and Search API integrations
- `mcp_server/`: MCP services for keyword research and competitor analysis
- `ui/`: Web interface for interacting with the services
- `ai/`: AI-powered analysis components

```
