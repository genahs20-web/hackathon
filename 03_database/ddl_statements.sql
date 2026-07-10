-- =====================================================================
-- Deliverable 3: Physical Data Model (DDL)
-- AI Knowledge Discovery & Decision Assistant
-- Target: SQLite 3 (application layer generates UUIDs as TEXT)
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- customers
-- ---------------------------------------------------------------------
CREATE TABLE customers (
    customer_id     TEXT PRIMARY KEY,                  -- UUID
    email           TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    organization    TEXT,
    role            TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    hashed_password TEXT NOT NULL,
    is_active       INTEGER NOT NULL DEFAULT 1,        -- boolean
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_created_at ON customers(created_at);

-- ---------------------------------------------------------------------
-- documents
-- ---------------------------------------------------------------------
CREATE TABLE documents (
    document_id     TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    file_name       TEXT NOT NULL,
    file_path       TEXT NOT NULL,
    file_size       INTEGER NOT NULL CHECK (file_size > 0 AND file_size <= 52428800),
    file_type       TEXT NOT NULL DEFAULT 'pdf'
                        CHECK (file_type IN ('pdf', 'docx', 'pptx', 'xlsx', 'eml')),
    status          TEXT NOT NULL DEFAULT 'uploaded'
                        CHECK (status IN ('uploaded', 'processing', 'indexed', 'failed')),
    upload_date     TEXT NOT NULL DEFAULT (datetime('now')),
    indexed_date    TEXT,
    total_chunks    INTEGER NOT NULL DEFAULT 0,
    metadata        TEXT,                              -- JSON
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_documents_customer_id ON documents(customer_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_upload_date ON documents(upload_date);

-- ---------------------------------------------------------------------
-- document_chunks
-- ---------------------------------------------------------------------
CREATE TABLE document_chunks (
    chunk_id        TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_text      TEXT NOT NULL,
    chunk_index     INTEGER NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_document_chunks_document_id ON document_chunks(document_id);

-- ---------------------------------------------------------------------
-- embeddings
-- Note: the actual vector lives in ChromaDB; this table stores the
-- pointer/metadata so relational queries can join back to source chunks.
-- ---------------------------------------------------------------------
CREATE TABLE embeddings (
    embedding_id    TEXT PRIMARY KEY,
    chunk_id        TEXT NOT NULL REFERENCES document_chunks(chunk_id) ON DELETE CASCADE,
    chroma_vector_id TEXT NOT NULL,                    -- ID of vector in ChromaDB collection
    model_used      TEXT NOT NULL DEFAULT 'text-embedding-3-small',
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_embeddings_chunk_id ON embeddings(chunk_id);

-- ---------------------------------------------------------------------
-- conversation_histories
-- ---------------------------------------------------------------------
CREATE TABLE conversation_histories (
    conversation_id TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    title           TEXT NOT NULL DEFAULT 'New Conversation',
    is_archived     INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_conversations_customer_id ON conversation_histories(customer_id);
CREATE INDEX idx_conversations_created_at ON conversation_histories(created_at);

-- ---------------------------------------------------------------------
-- chat_messages
-- ---------------------------------------------------------------------
CREATE TABLE chat_messages (
    message_id      TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversation_histories(conversation_id) ON DELETE CASCADE,
    sender_type     TEXT NOT NULL CHECK (sender_type IN ('user', 'assistant')),
    message_text    TEXT NOT NULL,
    sources         TEXT,                              -- JSON array of {document_id, snippet, relevance_score}
    confidence_score REAL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_chat_messages_conversation_id ON chat_messages(conversation_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);

-- ---------------------------------------------------------------------
-- conflicts
-- ---------------------------------------------------------------------
CREATE TABLE conflicts (
    conflict_id         TEXT PRIMARY KEY,
    conversation_id     TEXT REFERENCES conversation_histories(conversation_id) ON DELETE SET NULL,
    customer_id         TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    conflict_description TEXT NOT NULL,
    source_documents    TEXT NOT NULL,                 -- JSON array of document_ids
    severity            TEXT NOT NULL DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high')),
    resolved            INTEGER NOT NULL DEFAULT 0,
    resolution_notes    TEXT,
    created_at          TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_conflicts_customer_id ON conflicts(customer_id);
CREATE INDEX idx_conflicts_severity ON conflicts(severity);
CREATE INDEX idx_conflicts_resolved ON conflicts(resolved);

-- ---------------------------------------------------------------------
-- recommendations
-- ---------------------------------------------------------------------
CREATE TABLE recommendations (
    recommendation_id   TEXT PRIMARY KEY,
    conversation_id     TEXT REFERENCES conversation_histories(conversation_id) ON DELETE SET NULL,
    customer_id         TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    recommendation_text TEXT NOT NULL,
    confidence_score    REAL NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    supporting_documents TEXT,                         -- JSON array of document_ids
    status               TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at           TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_recommendations_customer_id ON recommendations(customer_id);
CREATE INDEX idx_recommendations_status ON recommendations(status);

-- ---------------------------------------------------------------------
-- notifications
-- ---------------------------------------------------------------------
CREATE TABLE notifications (
    notification_id     TEXT PRIMARY KEY,
    customer_id         TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    notification_type   TEXT NOT NULL,
    message              TEXT NOT NULL,
    is_read              INTEGER NOT NULL DEFAULT 0,
    created_at           TEXT NOT NULL DEFAULT (datetime('now')),
    read_at              TEXT
);
CREATE INDEX idx_notifications_customer_id ON notifications(customer_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);

-- ---------------------------------------------------------------------
-- audit_logs
-- ---------------------------------------------------------------------
CREATE TABLE audit_logs (
    log_id          TEXT PRIMARY KEY,
    customer_id     TEXT REFERENCES customers(customer_id) ON DELETE SET NULL,
    action          TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT,
    details          TEXT,                              -- JSON
    ip_address       TEXT,
    created_at       TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_audit_logs_customer_id ON audit_logs(customer_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
