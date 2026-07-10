# Entity-Relationship Diagram

```mermaid
erDiagram
    CUSTOMERS ||--o{ DOCUMENTS : uploads
    CUSTOMERS ||--o{ CONVERSATION_HISTORIES : owns
    CUSTOMERS ||--o{ NOTIFICATIONS : receives
    CUSTOMERS ||--o{ AUDIT_LOGS : generates
    CUSTOMERS ||--o{ CONFLICTS : owns
    CUSTOMERS ||--o{ RECOMMENDATIONS : owns

    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : "split into"
    DOCUMENT_CHUNKS ||--o{ EMBEDDINGS : "embedded as"

    CONVERSATION_HISTORIES ||--o{ CHAT_MESSAGES : contains
    CONVERSATION_HISTORIES ||--o{ CONFLICTS : surfaces
    CONVERSATION_HISTORIES ||--o{ RECOMMENDATIONS : surfaces

    CUSTOMERS {
        uuid customer_id PK
        string email UK
        string name
        string organization
        enum role
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }
    DOCUMENTS {
        uuid document_id PK
        uuid customer_id FK
        string file_name
        text file_path
        int file_size
        string file_type
        enum status
        timestamp upload_date
        timestamp indexed_date
        int total_chunks
        json metadata
        timestamp created_at
    }
    DOCUMENT_CHUNKS {
        uuid chunk_id PK
        uuid document_id FK
        text chunk_text
        int chunk_index
        timestamp created_at
    }
    EMBEDDINGS {
        uuid embedding_id PK
        uuid chunk_id FK
        vector embedding_vector
        string model_used
        timestamp created_at
    }
    CONVERSATION_HISTORIES {
        uuid conversation_id PK
        uuid customer_id FK
        string title
        boolean is_archived
        timestamp created_at
        timestamp updated_at
    }
    CHAT_MESSAGES {
        uuid message_id PK
        uuid conversation_id FK
        enum sender_type
        text message_text
        json sources
        decimal confidence_score
        timestamp created_at
    }
    CONFLICTS {
        uuid conflict_id PK
        uuid conversation_id FK
        uuid customer_id FK
        text conflict_description
        json source_documents
        enum severity
        boolean resolved
        text resolution_notes
        timestamp created_at
    }
    RECOMMENDATIONS {
        uuid recommendation_id PK
        uuid conversation_id FK
        uuid customer_id FK
        text recommendation_text
        decimal confidence_score
        json supporting_documents
        enum status
        timestamp created_at
    }
    NOTIFICATIONS {
        uuid notification_id PK
        uuid customer_id FK
        string notification_type
        text message
        boolean is_read
        timestamp created_at
        timestamp read_at
    }
    AUDIT_LOGS {
        uuid log_id PK
        uuid customer_id FK
        string action
        string entity_type
        uuid entity_id
        json details
        string ip_address
        timestamp created_at
    }
```

## Cardinality Summary

| Relationship | Cardinality |
|---|---|
| Customer → Document | 1 : N |
| Customer → ConversationHistory | 1 : N |
| Customer → Notification | 1 : N |
| Customer → AuditLog | 1 : N |
| Customer → Conflict | 1 : N |
| Customer → Recommendation | 1 : N |
| Document → DocumentChunk | 1 : N |
| DocumentChunk → Embedding | 1 : 1 |
| ConversationHistory → ChatMessage | 1 : N |
| ConversationHistory → Conflict | 1 : N |
| ConversationHistory → Recommendation | 1 : N |
