# Repo: ads-library

## README.md
```markdown
# AdScope — AI-Powered Ad Intelligence

Enter any company URL and let AI analyze their ad strategy across Meta and Google platforms.

## Project Structure

```
ads-library/
├── frontend/    # Next.js frontend (TypeScript, Tailwind, shadcn/ui)
├── server/      # FastAPI backend  (Python, SQLAlchemy, Azure OpenAI)
└── README.md
```

## Getting Started

### Backend

```bash
cd server
cp .env.example .env   # fill in your keys
pip install -e .
python -m src.main
```

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open [http://localhost:3103](http://localhost:3103) in your browser.

```
