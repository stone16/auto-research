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
