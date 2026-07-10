# Data Dictionary

## customers
| Field | Type | Length | Nullable | Default | Description | Validation |
|---|---|---|---|---|---|---|
| customer_id | UUID (TEXT) | 36 | No | — | Primary key | Generated via `uuid4()` |
| email | TEXT | 254 | No | — | Login identifier, unique | RFC 5322 email pattern |
| name | TEXT | 255 | No | — | Display name | 1–255 chars |
| organization | TEXT | 255 | Yes | NULL | Company/org name | — |
| role | ENUM | — | No | `user` | Access level | `user` \| `admin` |
| hashed_password | TEXT | — | No | — | bcrypt hash | Never stored/logged in plaintext |
| is_active | BOOLEAN | — | No | true | Account enabled flag | — |
| created_at | TIMESTAMP | — | No | now() | Record creation time | ISO-8601 |
| updated_at | TIMESTAMP | — | No | now() | Last modified time | ISO-8601 |

## documents
| Field | Type | Length | Nullable | Default | Description | Validation |
|---|---|---|---|---|---|---|
| document_id | UUID | 36 | No | — | Primary key | — |
| customer_id | UUID (FK) | 36 | No | — | Owner reference | Must exist in `customers` |
| file_name | TEXT | 255 | No | — | Original filename | Sanitized, `^[\w\s.\-()]+$` |
| file_path | TEXT | — | No | — | Storage path | — |
| file_size | INTEGER | — | No | — | Size in bytes | `0 < size ≤ 52428800` |
| file_type | TEXT | 10 | No | `pdf` | File extension | One of `pdf`\|`docx`\|`pptx`\|`xlsx`\|`eml` |
| status | ENUM | — | No | `uploaded` | Processing lifecycle state | `uploaded`\|`processing`\|`indexed`\|`failed` |
| upload_date | TIMESTAMP | — | No | now() | When uploaded | — |
| indexed_date | TIMESTAMP | — | Yes | NULL | When indexing completed | — |
| total_chunks | INTEGER | — | No | 0 | Count of chunks generated | ≥ 0 |
| metadata | JSON | — | Yes | NULL | Title/tags/category | — |
| created_at | TIMESTAMP | — | No | now() | Row creation time | — |

## document_chunks
| Field | Type | Nullable | Description |
|---|---|---|---|
| chunk_id | UUID | No | Primary key |
| document_id | UUID (FK) | No | Parent document |
| chunk_text | TEXT | No | ~500-token chunk of extracted text |
| chunk_index | INTEGER | No | Order within document (0-based) |
| created_at | TIMESTAMP | No | Creation time |

## embeddings
| Field | Type | Nullable | Description |
|---|---|---|---|
| embedding_id | UUID | No | Primary key |
| chunk_id | UUID (FK) | No | Source chunk |
| chroma_vector_id | TEXT | No | Pointer to vector stored in ChromaDB |
| model_used | TEXT | No | Embedding model identifier |
| created_at | TIMESTAMP | No | Creation time |

## conversation_histories
| Field | Type | Nullable | Description |
|---|---|---|---|
| conversation_id | UUID | No | Primary key |
| customer_id | UUID (FK) | No | Owner |
| title | TEXT | No | User-facing conversation title |
| is_archived | BOOLEAN | No | Soft-hide flag |
| created_at / updated_at | TIMESTAMP | No | Lifecycle timestamps |

## chat_messages
| Field | Type | Nullable | Description | Validation |
|---|---|---|---|---|
| message_id | UUID | No | Primary key | — |
| conversation_id | UUID (FK) | No | Parent conversation | — |
| sender_type | ENUM | No | `user` or `assistant` | — |
| message_text | TEXT | No | Message body | ≤ 2000 chars for user messages |
| sources | JSON | Yes | Array of `{document_id, document_name, snippet, relevance_score}` | — |
| confidence_score | DECIMAL(3,2) | Yes | AI confidence for assistant messages | 0.00–1.00 |
| created_at | TIMESTAMP | No | Sent time | — |

## conflicts
| Field | Type | Nullable | Description | Validation |
|---|---|---|---|---|
| conflict_id | UUID | No | Primary key | — |
| conversation_id | UUID (FK) | Yes | Conversation that surfaced it | — |
| customer_id | UUID (FK) | No | Owner | — |
| conflict_description | TEXT | No | Human-readable contradiction summary | — |
| source_documents | JSON | No | Array of document_ids involved | Min 2 entries |
| severity | ENUM | No | `low`\|`medium`\|`high` | — |
| resolved | BOOLEAN | No | Resolution status | default false |
| resolution_notes | TEXT | Yes | Analyst notes on resolution | — |
| created_at | TIMESTAMP | No | Detection time | — |

## recommendations
| Field | Type | Nullable | Description | Validation |
|---|---|---|---|---|
| recommendation_id | UUID | No | Primary key | — |
| conversation_id | UUID (FK) | Yes | Source conversation | — |
| customer_id | UUID (FK) | No | Owner | — |
| recommendation_text | TEXT | No | Suggested action | — |
| confidence_score | DECIMAL(3,2) | No | AI confidence | 0.00–1.00, BR-3 |
| supporting_documents | JSON | Yes | Array of document_ids | — |
| status | ENUM | No | `pending`\|`approved`\|`rejected` | — |
| created_at | TIMESTAMP | No | Creation time | — |

## notifications
| Field | Type | Nullable | Description |
|---|---|---|---|
| notification_id | UUID | No | Primary key |
| customer_id | UUID (FK) | No | Recipient |
| notification_type | TEXT | No | e.g. `document_indexed`, `conflict_detected` |
| message | TEXT | No | Notification body |
| is_read | BOOLEAN | No | Read status |
| created_at / read_at | TIMESTAMP | No/Yes | Lifecycle timestamps |

## audit_logs
| Field | Type | Nullable | Description |
|---|---|---|---|
| log_id | UUID | No | Primary key |
| customer_id | UUID (FK) | Yes | Actor (nullable for system actions) |
| action | TEXT | No | e.g. `document.upload`, `conflict.resolve` |
| entity_type | TEXT | No | e.g. `document`, `conversation` |
| entity_id | UUID | Yes | Affected entity |
| details | JSON | Yes | Additional structured context |
| ip_address | TEXT | Yes | Client IP (IPv4/IPv6) |
| created_at | TIMESTAMP | No | Event time |

---

## Indexes & Rationale

| Index | Reason |
|---|---|
| `idx_customers_email` | Fast login lookup by email |
| `idx_documents_customer_id` | Row-level scoping (BR-2) on every document list query |
| `idx_documents_status` | Dashboard filters by processing status |
| `idx_document_chunks_document_id` | Retrieve all chunks for a document during reindex |
| `idx_embeddings_chunk_id` | Join back from ChromaDB result to source chunk |
| `idx_conversations_customer_id` | List conversations per user |
| `idx_chat_messages_conversation_id` | Load message history in order |
| `idx_conflicts_customer_id` / `severity` / `resolved` | Conflicts screen filters |
| `idx_recommendations_customer_id` / `status` | Recommendations screen filters |
| `idx_notifications_customer_id` / `is_read` | Unread-notification badge queries |
| `idx_audit_logs_customer_id` / `action` / `created_at` | Admin audit log search/filter |

---

## Sample Data

```sql
-- customers
INSERT INTO customers (customer_id, email, name, organization, role, hashed_password) VALUES
 ('c1a1...', 'analyst@acme.com', 'Priya Sharma', 'Acme Corp', 'user', '$2b$12$...'),
 ('c2b2...', 'kmanager@acme.com', 'Raj Mehta', 'Acme Corp', 'user', '$2b$12$...'),
 ('c3c3...', 'exec@acme.com', 'Lena Ortiz', 'Acme Corp', 'user', '$2b$12$...'),
 ('c4d4...', 'admin@acme.com', 'System Admin', 'Acme Corp', 'admin', '$2b$12$...');

-- documents
INSERT INTO documents (document_id, customer_id, file_name, file_path, file_size, status, total_chunks) VALUES
 ('d1...', 'c1a1...', 'remote_work_policy_2024.pdf', '/data/docs/d1.pdf', 204800, 'indexed', 12),
 ('d2...', 'c1a1...', 'remote_work_policy_2025.pdf', '/data/docs/d2.pdf', 215040, 'indexed', 13),
 ('d3...', 'c1a1...', 'q2_vendor_risk_report.pdf', '/data/docs/d3.pdf', 512000, 'indexed', 28);

-- conflicts
INSERT INTO conflicts (conflict_id, customer_id, conflict_description, source_documents, severity, resolved) VALUES
 ('cf1...', 'c1a1...', 'Remote work days differ: 2024 policy allows 2 days/week, 2025 policy allows 3 days/week.',
  '["d1...","d2..."]', 'medium', 0);

-- recommendations
INSERT INTO recommendations (recommendation_id, customer_id, recommendation_text, confidence_score, status) VALUES
 ('r1...', 'c3c3...', 'Schedule a review with Procurement — 2 vendors flagged as high-risk in Q2 report.', 0.87, 'pending');
```

## Normalization Notes
- All tables are in **3NF**: no repeating groups, no partial or transitive dependencies on non-key attributes.
- `sources`, `metadata`, `source_documents`, `supporting_documents`, and `details` are stored as JSON blobs by design — they represent variable-shape denormalized references (document lists, arbitrary metadata) that would otherwise require excessive join tables for data that is always read as a unit, never queried by internal field.
- Referential integrity is enforced via `FOREIGN KEY` constraints with `ON DELETE CASCADE` (dependent child data) or `ON DELETE SET NULL` (historical references that should survive parent deletion, e.g. conflicts/recommendations outliving an archived conversation).
