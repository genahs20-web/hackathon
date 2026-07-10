# Technical Architecture Diagram

```mermaid
flowchart LR
    subgraph FE["Frontend (Vite + React 18 + TS)"]
        FE1[Pages/Components]
        FE2[api.ts - Axios client]
        FE3[auth.ts - JWT store]
    end

    subgraph BE["Backend (FastAPI, Python 3.12)"]
        BE1[API Routes]
        BE2[Pydantic Schemas]
        BE3[Services Layer]
        BE4["LangGraph Agents (7)"]
        BE5[SQLAlchemy ORM]
    end

    subgraph DATA["Data Stores"]
        DB1[(SQLite)]
        DB2[(ChromaDB)]
    end

    subgraph EXT["External"]
        EX1[[OpenAI API]]
    end

    FE1 --> FE2 --> FE3
    FE2 -->|REST JSON / SSE stream| BE1
    BE1 --> BE2 --> BE3
    BE3 --> BE4
    BE3 --> BE5 --> DB1
    BE4 -->|vector search| DB2
    BE4 -->|chat + embeddings| EX1
```

## Component Inventory

| Component | Technology | Responsibility |
|---|---|---|
| Frontend SPA | React 18, TypeScript, Vite, TailwindCSS | UI rendering, client-side routing, state management |
| API Gateway | FastAPI | Request validation, auth, routing to services |
| Schema Layer | Pydantic v2 | Request/response validation and serialization |
| Service Layer | Python modules | Business logic: document, chat, RAG services |
| Agent Layer | LangGraph + LangChain | 7 autonomous agents for retrieval, conflict detection, summarization |
| ORM | SQLAlchemy | Relational data access to SQLite |
| Vector Store | ChromaDB | Embedding storage and similarity search |
| LLM Provider | OpenAI / Azure OpenAI | Chat completions, text embeddings |

## Message Flow (Chat Query Example)
1. Frontend sends `POST /api/chat` with `conversation_id` + `message`.
2. FastAPI route validates via Pydantic schema, authenticates JWT.
3. `chat_service.py` loads conversation context from SQLite.
4. Supervisor Agent invoked with query + context.
5. Supervisor routes to Knowledge Retriever Agent → queries ChromaDB.
6. Retrieved chunks + query passed to Summarization/Recommendation Agents as needed.
7. Response streamed back to frontend via Server-Sent Events.
8. Final message + sources persisted to `chat_messages` table.
