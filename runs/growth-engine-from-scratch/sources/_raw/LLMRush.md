# Repo: LLMRush

## README.md
```markdown
# LLMRush Website

LLMRush is a modern web application that helps users find ranking information and sentiment scores for their search terms (company URLs or product names) across various LLM models (OpenAI ChatGPT, Deepseek, Anthropic Claude, Google Gemini, etc.).

## Features

- **Multi-model comparison** across major LLM providers
- **Ranking analysis** showing where a product/company ranks in relevant queries
- **Sentiment analysis** on a scale from -10 to 10
- **Aggregated positive and negative reviews** for each model
- **Token usage tracking** for cost management
- **User authentication** with JWT tokens and session management
- **Search history** with floating widget UI
- **Remember Me** functionality for extended sessions
- **Comprehensive security** including CSRF protection and security headers
- **Structured logging** with request IDs for debugging
- **Error tracking** with Sentry integration (optional)
- **Database connection retry** logic for reliability
- **Auto token refresh** for seamless user experience

## Tech Stack

### Frontend
- React 18 with Vite
- Tailwind CSS for styling
- React Query for data fetching
- Axios with interceptors for API calls
- Automatic token refresh handling

### Backend
- FastAPI (Python 3.11+)
- MySQL with aiomysql (async)
- Redis for caching
- SQLAlchemy ORM with Alembic migrations
- JWT authentication with bcrypt
- Structured logging with request tracking

## Security Features

- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS, CSP
- **CSRF Protection**: Token-based CSRF protection for state-changing operations
- **Rate Limiting**: Implemented on authentication endpoints
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Protection**: Using parameterized queries via SQLAlchemy
- **XSS Protection**: Content Security Policy and output encoding
- **Request ID Tracking**: Every request gets a unique ID for debugging

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python 3.11+
- MySQL 5.7+ or MariaDB 10.3+
- Redis 6.0+ (optional but recommended)
- npm or yarn

### Quick Start

The easiest way to run LLMRush is using the provided script:

```bash
# Make the script executable
chmod +x run.sh

# Run the application
./run.sh
```

This will:
1. Install frontend dependencies
2. Build the frontend
3. Copy the built files to the backend's static directory
4. Install backend dependencies
5. Start the backend server which will also serve the frontend

Once running, access the application at http://localhost:8000

### Development Mode

For development, you can run the frontend and backend separately:

#### Frontend:

```bash
cd frontend
npm install
npm run dev
```

This will start the frontend development server at http://localhost:5173

#### Backend:

```bash
cd backend
python -m pip install -r requirements.txt
cd app
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at http://localhost:8000/api

## Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration (Required)
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=llm_rush_db
DB_ECHO=false

# Redis Configuration (Optional but recommended)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=1
REDIS_PASSWORD=your_redis_password
REDIS_PREFIX=llmrush

# Security (Required - change these!)
JWT_SECRET_KEY=your-secret-key-change-in-production
CSRF_SECRET_KEY=your-csrf-secret-key-change-in-production

# Error Tracking (Optional)
SENTRY_DSN=your_sentry_dsn_here
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
JSON_LOGS=true

# LLM API Keys (At least one required)
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
XAI_API_KEY=your_xai_api_key_here
GROK_API_KEY=your_grok_api_key_here

# For development without API keys
ENABLE_MOCK_RESPONSES=false

# Web Search Fallback
GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
GOOGLE_SEARCH_CX=your_google_search_cx_here
ENABLE_WEB_SEARCH=true
MAX_WEB_RESULTS=5

# Application Settings
PROMOTE_GETU=false
MARKETING_TEAM_URL=/about#contact
MAX_MODELS=3
NUM_QUERIES_TO_GENERATE=10
```

## Database Setup

1. Create the database:
```sql
CREATE DATABASE llm_rush_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Run migrations:
```bash
cd backend
alembic upgrade head
```

## Project Structure

```
LLMRush/
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── context/      # React contexts
│   │   └── hooks/        # Custom hooks
│   └── public/           # Static assets
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality (auth, security, logging)
│   │   ├── db/           # Database models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   ├── alembic/          # Database migrations
│   └── scripts/          # Utility scripts
└── tests/                # Test suite
```

## Database Maintenance

LLMRush includes automatic maintenance for database cleanup:

- Expired access tokens are automatically marked as expired (not deleted) for safety
- Inactive sessions are automatically marked as ended after 24 hours
- Search history and user data are preserved indefinitely to prevent data loss
- Cleanup operations are designed to be safe and never delete user-generated content

The application includes built-in cleanup services that run automatically and safely handle:
- Token expiration management
- Session lifecycle management  
- Database integrity protection

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite:

```bash
cd tests
python run_tests.py
```

## Production Deployment

### Security Checklist

- [ ] Change all default secret keys (JWT_SECRET_KEY, CSRF_SECRET_KEY)
- [ ] Enable HTTPS and set secure cookies
- [ ] Configure proper CORS origins
- [ ] Set up database backups
- [ ] Enable Sentry for error tracking
- [ ] Configure rate limiting on all endpoints
- [ ] Set up monitoring and alerting
- [ ] Review and adjust security headers

### Performance Optimization

- Enable Redis for caching
- Use a production WSGI server (Gunicorn/uWSGI)
- Set up a reverse proxy (Nginx/Apache)
- Enable gzip compression
- Optimize database queries with proper indexes
- Use a CDN for static assets

### Monitoring

The application includes:
- Structured JSON logging with request IDs
- Health check endpoints at `/health` and `/api/health/detailed`
- Optional Sentry integration for error tracking
- Database connection monitoring with retry logic
- Redis circuit breaker for graceful degradation

## Recent Updates

### Security Enhancements
- Added comprehensive security headers middleware
- Implemented CSRF protection for all state-changing operations
- Added request ID tracking for better debugging
- Implemented structured logging with JSON output

### Authentication Improvements
- Added "Remember Me" functionality with extended token expiration
- Implemented automatic token refresh on the frontend
- Added token expiry handling with seamless retry

### Infrastructure Improvements
- Added database connection retry logic
- Implemented comprehensive error tracking with Sentry
- Added circuit breaker pattern for Redis connections
- Improved error handling and user feedback

### Data Safety Improvements
- Fixed dangerous cascade deletion relationships that could cause data loss
- Improved logout and password reset processes to preserve user data
- Enhanced cleanup services to be safe and non-destructive
- Removed potentially dangerous maintenance scripts

## License

This project is proprietary and confidential. 
```
