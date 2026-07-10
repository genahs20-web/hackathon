# Logical Architecture Diagram

```mermaid
flowchart TB
    subgraph PL["Presentation Layer"]
        A1[React 18 + TypeScript SPA]
        A2[TailwindCSS UI Components]
    end

    subgraph APPL["Application Layer"]
        B1[FastAPI REST API]
        B2[Business Logic Services]
        B3[LangGraph Agent Orchestration]
    end

    subgraph DL["Data Layer"]
        C1[(SQLite - Relational Data)]
        C2[(ChromaDB - Vector Store)]
    end

    subgraph EXT["External Services"]
        D1[OpenAI API / Azure OpenAI]
    end

    A1 -->|HTTPS/REST + SSE| B1
    A2 --> A1
    B1 --> B2
    B2 --> B3
    B3 -->|embeddings, completions| D1
    B2 -->|CRUD| C1
    B3 -->|semantic search| C2
```

**Layer responsibilities**

| Layer | Responsibility |
|---|---|
| Presentation | Renders UI, manages client state, streams chat responses to the user |
| Application | Exposes REST/SSE endpoints, enforces business rules, orchestrates the 7 LangGraph agents |
| Data | Persists relational entities (SQLite) and vector embeddings (ChromaDB) |
| External Services | Provides LLM completions and embedding generation via OpenAI/Azure OpenAI |
