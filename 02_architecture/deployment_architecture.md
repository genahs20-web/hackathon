# Deployment Architecture Diagram

```mermaid
flowchart TB
    subgraph HOST["Docker Host"]
        subgraph FEC["frontend container"]
            F1[nginx serving Vite build]
        end
        subgraph BEC["backend container"]
            B1[uvicorn + FastAPI]
        end
        subgraph CHC["chromadb container"]
            C1[ChromaDB server]
        end
        V1[(sqlite_data volume)]
        V2[(chroma_data volume)]
    end

    CLIENT([Browser]) -->|:80| F1
    F1 -->|/api proxy :8000| B1
    B1 -->|:8001| C1
    B1 --- V1
    C1 --- V2
```

## docker-compose Service Map

| Service | Image/Build | Ports | Volumes | Depends On |
|---|---|---|---|---|
| frontend | `./frontend` (multi-stage Dockerfile) | `80:80` | — | backend |
| backend | `./backend` (Dockerfile) | `8000:8000` | `sqlite_data:/app/data` | chromadb |
| chromadb | `chromadb/chroma` | `8001:8000` | `chroma_data:/chroma/chroma` | — |

## Environment Variables (per service)

| Variable | Service | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | backend | LLM/embedding API access |
| `DATABASE_URL` | backend | SQLite connection string |
| `CHROMA_HOST` / `CHROMA_PORT` | backend | ChromaDB connection |
| `JWT_SECRET_KEY` | backend | Token signing secret |
| `VITE_API_BASE_URL` | frontend | Backend API base URL |

## Network
- All services share a Docker bridge network `app-network`.
- Only `frontend` port 80 is exposed externally in production; `backend` and `chromadb` are internal-only behind the frontend/reverse proxy.
