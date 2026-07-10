# Deliverable 4: Story-to-Spec Decomposition (SSD)
## AI Knowledge Discovery & Decision Assistant

---

## 1. Epic Breakdown

| Epic | Description |
|---|---|
| EPIC 1: Document Management System | Manage document lifecycle — upload (multi-format), process, store, retrieve |
| EPIC 2: Semantic Knowledge Retrieval | Retrieve relevant documents using semantic search |
| EPIC 3: Intelligent Conflict Detection | Identify, flag, and resolve conflicting information |
| EPIC 4: AI-Powered Insights & Recommendations | Generate summaries and actionable recommendations |
| EPIC 5: Multi-Turn Conversational AI | Enable natural conversation with context preservation |
| EPIC 6: Administration & Monitoring | Admin controls, audit logging, monitoring |

---

## 2. User Stories

### EPIC 1: Document Management System

#### US-1.1 — User uploads an enterprise document
- **Priority:** High · **Story Points:** 5

**User Story:**
AS A business analyst
I WANT TO upload enterprise documents (PDF, DOCX, PPTX, XLSX, EML)
SO THAT I can build a knowledge base for analysis

**Acceptance Criteria:**
- GIVEN user is on dashboard
- WHEN user clicks "Upload Document"
- AND selects a file (≤50MB) in a supported format
- THEN file is uploaded successfully
- AND format-appropriate indexing begins automatically
- AND user sees a progress indicator
- AND an upload-completion notification is sent

**Workflow:**
1. User clicks upload button
2. File browser opens
3. User selects a file
4. System validates file (extension, size, not corrupted)
5. File uploaded to backend storage
6. System selects the loader matching `file_type` (pdf/docx/pptx/xlsx/eml)
7. Trigger document processing pipeline
8. Show success message
9. Display document in document list with status `processing`

**Business Rules:** BR-1.1 (allowed formats only) · BR-1.2 (max 50MB) · BR-1.3 (max 100 docs/user) · BR-1.4 (unique doc names per user)

**Validation Rules:** VR-1.1 (extension in allow-list) · VR-1.2 (0 < size ≤ 52428800 bytes) · VR-1.3 (file must parse without corruption errors)

**Dependencies:** None

**Implementation Notes:**
- FastAPI multipart upload endpoint.
- Loader dispatch table: `{pdf: PyPDFLoader, docx: DocxLoader, pptx: PptxLoader, xlsx: XlsxLoader, eml: EmlLoader}`.
- Async background task for processing (indexing pipeline).
- Return `document_id` immediately; status transitions tracked via polling or SSE.

---

#### US-1.2 — System automatically indexes an uploaded document
- **Priority:** High · **Story Points:** 8

**User Story:** AS the system, I WANT TO automatically extract, chunk, and embed document content SO THAT it becomes searchable immediately after upload.

**Acceptance Criteria:**
- GIVEN a document with status `uploaded`
- WHEN the indexing pipeline runs
- THEN text (and table/OCR content where applicable) is extracted
- AND text is split into ~500-token chunks with 50-token overlap
- AND each chunk is embedded and stored in ChromaDB
- AND document status transitions to `indexed`

**Workflow:** Extract → Chunk → Embed → Store in ChromaDB → Update `documents.status` → Notify user

**Business Rules:** BR-1.1 · BR-1.3

**Validation Rules:** VR-1.3

**Dependencies:** US-1.1

**Implementation Notes:** Retry up to 3x on extraction failure; on repeated failure set status `failed` with error detail in `metadata`.

---

#### US-1.3 — User views document list and status
- **Priority:** Medium · **Story Points:** 3

**User Story:** AS A business analyst, I WANT TO see all my uploaded documents and their processing status SO THAT I know what's ready to query.

**Acceptance Criteria:** GIVEN user is logged in, WHEN user opens Documents screen, THEN all owned documents are listed with name, format, size, status, and upload date.

**Business Rules:** BR-2 (row-level scoping)

**Dependencies:** US-1.1

---

#### US-1.4 — User deletes a document
- **Priority:** Medium · **Story Points:** 3

**User Story:** AS A business analyst, I WANT TO delete a document I no longer need SO THAT my knowledge base stays relevant.

**Acceptance Criteria:** GIVEN a document owned by the user, WHEN user clicks Delete and confirms, THEN the document, its chunks, and its embeddings are removed (cascade) and an audit log entry is created.

**Business Rules:** BR-2 · BR-4

---

### EPIC 2: Semantic Knowledge Retrieval

#### US-2.1 — User searches using natural language
- **Priority:** High · **Story Points:** 5

**User Story:** AS A business analyst, I WANT TO ask a natural-language question SO THAT I get relevant document excerpts without manual searching.

**Acceptance Criteria:** GIVEN indexed documents exist, WHEN user submits a query, THEN top-5 relevant chunks are returned ranked by similarity score, each with a source citation.

**Business Rules:** BR-2

**Validation Rules:** VR-2.1 (query length 1–2000 chars) · VR-2.2 (no injection patterns)

**Dependencies:** US-1.2

**Implementation Notes:** Embed query via same model as ingestion; query ChromaDB collection scoped by `customer_id` metadata filter.

---

#### US-2.2 — System ranks results by relevance
- **Priority:** Medium · **Story Points:** 2

**Acceptance Criteria:** GIVEN a search is executed, WHEN results are returned, THEN they are sorted descending by cosine similarity score, and any result below 0.5 similarity is excluded.

---

#### US-2.3 — System returns source citations
- **Priority:** High · **Story Points:** 3

**Acceptance Criteria:** GIVEN an AI response is generated, WHEN it references document content, THEN each factual claim links to a `{document_id, document_name, page/slide/row, snippet}` citation object.

**Dependencies:** US-2.1

---

### EPIC 3: Intelligent Conflict Detection

#### US-3.1 — System detects contradictions across documents
- **Priority:** High · **Story Points:** 8

**User Story:** AS A knowledge manager, I WANT TO be automatically alerted to contradictory statements across documents SO THAT I can resolve them before they cause confusion.

**Acceptance Criteria:** GIVEN 3+ indexed documents share overlapping topics, WHEN the Conflict Detector Agent runs, THEN contradictions are flagged with a severity level (low/medium/high) and the involved document IDs.

**Business Rules:** BR-5 (manual review required before action)

**Dependencies:** US-1.2, US-2.1

**Implementation Notes:** LLM comparison prompt over co-retrieved chunks; confidence threshold 0.6 before surfacing (below threshold is discarded, not shown).

---

#### US-3.2 — User reviews and resolves a conflict
- **Priority:** Medium · **Story Points:** 5

**Acceptance Criteria:** GIVEN a flagged conflict, WHEN user opens conflict details, THEN both source excerpts are shown side by side; user can mark it resolved with notes, which are persisted and audit-logged.

**Dependencies:** US-3.1

---

### EPIC 4: AI-Powered Insights & Recommendations

#### US-4.1 — System generates a concise summary
- **Priority:** High · **Story Points:** 5

**Acceptance Criteria:** GIVEN retrieved content, WHEN summarization is requested, THEN a 3–4 sentence summary is generated with citations.

**Dependencies:** US-2.1

---

#### US-4.2 — System provides AI recommendations with confidence scores
- **Priority:** High · **Story Points:** 5

**Acceptance Criteria:** GIVEN a summary or conflict analysis, WHEN recommendation generation runs, THEN a recommendation is produced with a confidence score (0.0–1.0, BR-3) and supporting document references.

**Dependencies:** US-4.1

---

#### US-4.3 — User approves or rejects a recommendation
- **Priority:** Medium · **Story Points:** 3

**Acceptance Criteria:** GIVEN a pending recommendation, WHEN user clicks Approve/Reject, THEN status updates accordingly and (if rejected) a reason is captured.

**Dependencies:** US-4.2

---

### EPIC 5: Multi-Turn Conversational AI

#### US-5.1 — User carries on a multi-turn conversation
- **Priority:** High · **Story Points:** 8

**Acceptance Criteria:** GIVEN an open conversation, WHEN user sends a follow-up referencing prior context (e.g., pronouns), THEN the system resolves the reference correctly using conversation history.

**Business Rules:** BR-1 (auth required)

**Dependencies:** US-2.1

---

#### US-5.2 — User retrieves conversation history
- **Priority:** Medium · **Story Points:** 3

**Acceptance Criteria:** GIVEN past conversations exist, WHEN user opens the sidebar, THEN the 10 most recent conversations are listed and clicking one loads its full message history in order.

---

### EPIC 6: Administration & Monitoring

#### US-6.1 — Admin manages all documents
- **Priority:** Medium · **Story Points:** 5

**Acceptance Criteria:** GIVEN an admin user, WHEN admin opens the admin panel, THEN all users' documents are visible with reindex/delete actions available.

**Business Rules:** BR-2 (admin override), BR-4

---

#### US-6.2 — Admin views audit logs
- **Priority:** Medium · **Story Points:** 3

**Acceptance Criteria:** GIVEN admin is logged in, WHEN admin opens audit logs, THEN logs are searchable/filterable by action, user, and date range.

**Business Rules:** BR-4

---

## 3. Workflows

### Workflow: Document Processing Pipeline
- **Input:** Uploaded file path + `file_type`
- **Output:** Indexed document in ChromaDB
- **Steps:** Select loader by `file_type` → Extract text/tables/OCR → Chunk (500 tokens, 50 overlap) → Generate embeddings → Store in ChromaDB → Update `documents.status = indexed` → Notify user
- **Error Handling:** Extraction failure → retry 3x → mark `failed`. Embedding failure on one chunk → log and continue with remaining chunks. ChromaDB write failure → retry with exponential backoff.

### Workflow: Query & Retrieval
- **Input:** User query (natural language)
- **Output:** Top-K relevant chunks with citations
- **Steps:** Receive query → embed query → search ChromaDB (top-5, scoped by `customer_id`) → retrieve source metadata → format with citations → return to user

---

## 4. Business Rules (Consolidated)

| ID | Rule |
|---|---|
| BR-1 | Only authenticated users can access the system |
| BR-2 | Users can only access their own documents (row-level security); admins can access all |
| BR-3 | AI recommendations must include a confidence score |
| BR-4 | Audit logs must track all document access and mutation |
| BR-5 | Conflicts must be manually reviewed before any downstream action |

## 5. Validation Rules (Consolidated)

| ID | Rule |
|---|---|
| VR-1.1 | File extension must be one of: pdf, docx, pptx, xlsx, eml |
| VR-1.2 | File size: 0 < size ≤ 52,428,800 bytes |
| VR-1.3 | File must parse without corruption errors |
| VR-2.1 | Query length: 1–2000 characters |
| VR-2.2 | Query must not contain prompt-injection or SQL-injection patterns |

## 6. Implementation-Ready Specs Summary

Each story above maps to: an API endpoint (Deliverable 6), a database table/field (Deliverable 3), a code module/function (Deliverable 7), and at least one test case (Deliverable 8) — full cross-references in the Traceability Matrix (Deliverable 9).

*End of Deliverable 4.*
