# Repo: Business-Intelligent

## README.md
```markdown
# Business-Intelligent

A multi-agent business intelligence platform for attribution analysis, competitor research, and market insights.

## Development Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3104 | React + Vite dev server |
| Backend API | 8029 | FastAPI server |
| Multi-agent | 8042 | Agent orchestration |
| MySQL | 3306 | Database |

## Quick Start

```bash
# Frontend
cd frontend && pnpm dev  # http://localhost:3104

# Backend
cd backend && python -m uvicorn main:app --reload --port 8029
```

## Project Structure

```
Business-Intelligent/
├── frontend/          # React + TypeScript + Vite
├── backend/           # FastAPI + LangGraph agents
└── docs/              # Documentation
```
```
