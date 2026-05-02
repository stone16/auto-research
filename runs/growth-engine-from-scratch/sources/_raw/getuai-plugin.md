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
GOOGLE_ADS_CONFIG_PATH=google_ads.yml
```

## Testing

### Run All Tests
```bash
# Basic API validation tests
python tests/test_basic_api.py

# Specific plugin tests
python -m pytest tests/test_google_search_api.py -v
python -m pytest tests/test_competitor_discovery_api.py -v
python -m pytest tests/test_keyword_ideas_api.py -v

# Integration workflow tests
python -m pytest tests/test_integration_workflows.py -v
```


```
