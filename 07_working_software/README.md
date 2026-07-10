# AI Knowledge Discovery & Decision Assistant — Working Software

## Prerequisites
- Docker + Docker Compose
- An OpenAI API key (or Azure OpenAI endpoint + key)

## Quick Start (Docker)

```bash
cd deliverables/07_working_software
cp .env.example .env
# edit .env and set OPENAI_API_KEY and JWT_SECRET_KEY
cd docker
docker compose --env-file ../.env up --build
```

- Frontend: http://localhost
- Backend API docs: http://localhost:8000/docs
- ChromaDB: http://localhost:8001

## Local Development (without Docker)

**Backend**
```bash
cd backend
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp ../.env.example .env   # edit values
python -m app.database.init_db   # creates tables + seed data
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## Seed Accounts
Created by `python -m app.database.init_db` (password for all: `Password123`):

| Email | Role |
|---|---|
| analyst@acme.com | user |
| kmanager@acme.com | user |
| admin@acme.com | admin |

## Notes
- ChromaDB must be running before the backend starts, since `app/rag/retriever.py` connects to it on import.
- Document indexing runs as a FastAPI `BackgroundTask` after upload; poll `GET /api/documents/{id}` for status.
- See `deliverables/06_specs/api_specifications.yaml` for the full API contract and `deliverables/09_traceability_matrix.csv` for requirement-to-code mapping.
