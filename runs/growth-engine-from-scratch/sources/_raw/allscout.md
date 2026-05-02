# Repo: allscout

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
- `POST /api/analyze` - Analyze a URL with web search + generate search keywords
- `GET /api/health` - Health check

### Discovery Endpoints (Find Real Reddit Opportunities)
- `POST /api/discover` - Find Reddit posts using one keyword from analysis
- `POST /api/discover/batch` - Run multiple keyword searches, get aggregated posts
- `POST /api/discover/competitors` - Find discussions about competitors
- `POST /api/discover/keywords` - Get info about available keywords

### Reddit Endpoints (Low-level)
- `POST /api/reddit/search` - Direct Reddit search
- `POST /api/reddit/post` - Get post with comments
- `GET /api/reddit/health` - Reddit service health check

## Complete Workflow: Find Reddit Opportunities

### Step 1: Analyze Company URL

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://linear.app"}'
```

Response includes:
- Company info (name, description, target audience)
- **search_keywords**: 15-20 search terms for finding relevant posts
- **pain_points**: User frustrations to look for
- **competitor_names**: Competitors for comparison searches
- **target_subreddits**: Where target users hang out

### Step 2: Discover Reddit Opportunities

Use the analysis to find real Reddit posts:

```bash
# Single keyword search (use keyword_index to rotate through keywords)
curl -X POST http://localhost:8000/api/discover \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": { ... response from /api/analyze ... },
    "keyword_index": 0,
    "limit": 10
  }'

# Batch search (multiple keywords, deduplicated results)
curl -X POST http://localhost:8000/api/discover/batch \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": { ... },
    "num_keywords": 3,
    "posts_per_keyword": 5
  }'

# Find competitor discussions
curl -X POST http://localhost:8000/api/discover/competitors \
  -H "Content-Type: application/json" \
  -d '{
    "analysis": { ... },
    "competitor_index": 0,
    "limit": 10
  }'
```

### Step 3: Get Post Details with Comments

```bash
curl -X POST http://localhost:8000/api/reddit/post \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.reddit.com/r/SaaS/comments/xxxxx/title/",
    "sort": "top",
    "limit": 50
  }'
```

### Keyword Rotation

Each call to `/api/discover` uses one keyword. Increment `keyword_index` to use different keywords:

```python
# Frontend can track current index and rotate
for i in range(total_keywords):
    results = await fetch('/api/discover', {
        "analysis": analysis,
        "keyword_index": i,
        "limit": 5
    })
```

Check available keywords:
```bash
curl -X POST http://localhost:8000/api/discover/keywords \
  -H "Content-Type: application/json" \
  -d '{"analysis": {...}, "keyword_index": 0}'
```

## LLM Service Usage

```python
from src.services import LLMService
from src.core import AvailableModels
from pydantic import BaseModel

# Plain text response
response = await LLMService.chat_completion(
    model=AvailableModels.GPT_4O_MINI,
    system_prompt="You are a helpful assistant.",
    user_prompt="What is Python?",
)

# Structured response with Pydantic
class Summary(BaseModel):
    title: str
    points: list[str]

result = await LLMService.chat_completion(
    model=AvailableModels.GPT_4O,
    system_prompt="Summarize the text.",
    user_prompt="...",
    output=Summary,
)

# Web Search with citations (Responses API)
class CompanyInfo(BaseModel):
    name: str
    description: str
    industry: str

result = await LLMService.websearch_completion(
    model=AvailableModels.GPT_4O,
    system_prompt="Analyze the company website.",
    user_prompt="https://linear.app",
    output=CompanyInfo,
)
print(result.content)     # CompanyInfo instance
print(result.citations)   # List of source URLs
```

## Reddit Service Usage

The Reddit service uses SteadyAPI to search posts and retrieve comments.

```python
from src.services import RedditService

# Search for posts
results = await RedditService.search_posts(
    query="project management tools",
    subreddit="SaaS",  # Optional: limit to specific subreddit
    sort="top",        # relevance, hot, top, new, comments
    time_filter="month",  # hour, day, week, month, year, all
    limit=20,
)

for post in results.posts:
    print(f"[r/{post.subreddit}] {post.title}")
    print(f"  Score: {post.score}, Comments: {post.num_comments}")
    print(f"  URL: {post.full_permalink}")

# Get a post with comments
post = await RedditService.get_post_with_comments(
    post_url="https://www.reddit.com/r/SaaS/comments/xxxxx/title/",
    comment_sort="top",
    comment_limit=50,
)

print(f"Post: {post.title}")
print(f"Content: {post.selftext}")

for comment in post.comments:
    print(f"  {comment.author}: {comment.body[:100]}...")
    print(f"  Score: {comment.score}")
    
    # Nested replies
    for reply in comment.replies:
        print(f"    └─ {reply.author}: {reply.body[:50]}...")
```

### Reddit API via HTTP

```bash
# Search posts
curl -X POST http://localhost:8000/api/reddit/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best CRM software",
    "subreddit": "smallbusiness",
    "sort": "top",
    "time": "month",
    "limit": 10
  }'

# Get post with comments
curl -X POST http://localhost:8000/api/reddit/post \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.reddit.com/r/SaaS/comments/xxxxx/title/",
    "sort": "top",
    "limit": 50
  }'

# Check Reddit service health
curl http://localhost:8000/api/reddit/health
```

```
