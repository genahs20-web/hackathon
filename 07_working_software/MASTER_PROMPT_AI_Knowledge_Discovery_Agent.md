# MASTER PROMPT: AI Knowledge Discovery & Decision Assistant
## Complete Build Guide for Amazon Q - Phase by Phase

**Project**: AI Knowledge Discovery & Decision Assistant (AI Fridays Challenge)
**Date**: 10 July 2026
**Target**: 10 Deliverables, 100 Marks, Production-Ready Code
**Tools**: Amazon Q, Claude, or Your Preferred AI Tool
**Token Strategy**: Phase-by-phase with continuation markers

---

# ⚡ QUICK START INSTRUCTIONS FOR AMAZON Q USERS

## How to Use This Prompt:

1. **Copy ONE PHASE at a time** into Amazon Q
2. **Execute the phase completely**
3. **Save all outputs** to your local workspace
4. **When context fills up**, use the continuation marker `CONTINUE FROM NEXT PHASE:`
5. **Never regenerate previous phases** - build incrementally

---

---

# 🎯 PROJECT OVERVIEW & AI ARCHITECTURE

## Business Problem
A business analyst receives multiple enterprise documents (policies, procedures, reports, meeting notes, presentations). Instead of manually reviewing hundreds of pages, they upload documents and ask natural language questions. The AI system:
- Indexes documents automatically
- Retrieves relevant information via semantic search
- Identifies conflicts in documents
- Generates executive summaries with source citations
- Recommends next steps
- Maintains conversation history

## Tech Stack
- **Backend**: Python 3.12, FastAPI, LangGraph, LangChain, SQLAlchemy, SQLite, ChromaDB, Pydantic
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS
- **AI Agents**: 7 LangGraph-based autonomous agents
- **RAG**: PDF loading, chunking, embedding, semantic retrieval
- **Deployment**: Docker, Docker Compose

## Database Tables
Customer, Document, ConversationHistory, KnowledgeBase, Embedding, Conflict, Recommendation, Notification, AuditLog, ChatMessage

## 10 Required Deliverables (AI Fridays Scoring)
1. Functional Requirements Document (10 marks)
2. Application Architecture Diagrams (10 marks)
3. Database Design / Data Models (10 marks)
4. Story-to-Spec Decomposition (8 marks)
5. Wireframes / UI Design (7 marks)
6. SPECS / DSL in Markdown/YAML (12 marks)
7. **Software Code & Working Software (18 marks - HIGHEST)**
8. Functional Test Scripts (8 marks)
9. Traceability Matrix (9 marks)
10. Code Quality Review Agent (8 marks)

---

---

# 📋 PHASE 1: DELIVERABLE 1 - FUNCTIONAL REQUIREMENTS DOCUMENT

## Objective
Create comprehensive requirements document covering functional/non-functional requirements, personas, user journeys, business rules, acceptance criteria.

## Instructions for Amazon Q

```
Generate DELIVERABLE 1: Functional Requirements Document for "AI Knowledge Discovery & Decision Assistant"

INCLUDE:

1. BUSINESS OVERVIEW
   - Problem statement
   - Solution overview
   - Key success criteria

2. USER PERSONAS (3-4 personas)
   - Business Analyst (primary user)
   - Knowledge Manager
   - Executive/Decision Maker
   - For each: role, goals, pain points, technical skill level

3. USER JOURNEYS (2-3 complete journeys)
   - Journey 1: Document Upload & Initial Query
   - Journey 2: Conflict Discovery & Resolution
   - Journey 3: Executive Summary Generation

4. FUNCTIONAL REQUIREMENTS (Group by epic)
   
   EPIC 1: DOCUMENT MANAGEMENT
   FR-1.1: User can upload PDF documents
   FR-1.2: System automatically indexes documents
   FR-1.3: User can view upload history
   FR-1.4: System extracts document metadata
   
   EPIC 2: KNOWLEDGE RETRIEVAL
   FR-2.1: User can search using natural language
   FR-2.2: System retrieves top-K relevant documents
   FR-2.3: System ranks results by relevance
   FR-2.4: System returns source citations
   
   EPIC 3: CONFLICT IDENTIFICATION
   FR-3.1: System identifies contradictory information
   FR-3.2: System highlights conflicting sections
   FR-3.3: System suggests resolution strategies
   
   EPIC 4: SUMMARIZATION & RECOMMENDATIONS
   FR-4.1: System generates concise summaries
   FR-4.2: System provides AI recommendations
   FR-4.3: System suggests next steps
   FR-4.4: System generates executive summaries
   
   EPIC 5: CONVERSATIONAL AI
   FR-5.1: Multi-turn conversation support
   FR-5.2: Conversation context retention
   FR-5.3: Conversation history retrieval
   
   EPIC 6: ADMINISTRATION
   FR-6.1: Admin can manage documents
   FR-6.2: Admin can view audit logs
   FR-6.3: Admin can generate reports

5. NON-FUNCTIONAL REQUIREMENTS
   - Performance: Response time < 2s for queries
   - Scalability: Support 1000+ concurrent users
   - Availability: 99.5% uptime
   - Security: Data encryption, role-based access
   - Reliability: 99% accuracy in conflict detection
   - Maintainability: Modular architecture, documented APIs
   - Usability: Intuitive UI, minimal training

6. BUSINESS RULES
   - BR-1: Only authenticated users can access
   - BR-2: Users can only access their documents
   - BR-3: AI recommendations must have confidence scores
   - BR-4: Audit logs must track all document access
   - BR-5: Conflicts must be manually reviewed before action

7. ACCEPTANCE CRITERIA (for each FR)
   Example for FR-1.1:
   - GIVEN a user is on dashboard
   - WHEN user clicks "Upload Document"
   - AND selects a PDF file ≤ 50MB
   - THEN system uploads file
   - AND system begins indexing
   - AND user sees success message

8. ASSUMPTIONS & CONSTRAINTS
   - Maximum 100 documents per user
   - Maximum document size: 50MB
   - Supported formats: PDF only
   - Responses must include source citations
   - Conflict detection requires 3+ documents

9. SCREEN-LEVEL REQUIREMENTS
   - Login Screen: Email/password authentication
   - Dashboard: Document summary, recent queries, recommendations
   - Document Upload: Drag-drop interface, progress indicator
   - Query Interface: Search bar, filters, results display
   - Chat Interface: Message history, typing indicator, streaming responses
   - Admin Panel: Document management, user management, audit logs

OUTPUT FORMAT: Professional markdown with tables, clear hierarchy, and checkboxes.
```

---

# 📊 PHASE 2: DELIVERABLE 2 - ARCHITECTURE DIAGRAMS

## Objective
Create logical, technical, data flow, integration, security, and AI-assist architecture views.

## Instructions for Amazon Q

```
Generate DELIVERABLE 2: Application & Technical Architecture Diagrams for "AI Knowledge Discovery & Decision Assistant"

CREATE 6 ARCHITECTURE VIEWS:

1. LOGICAL ARCHITECTURE DIAGRAM
   Show layers:
   - Presentation Layer (React Frontend)
   - Application Layer (FastAPI, Business Logic)
   - Data Layer (SQLite, ChromaDB)
   - External Services (OpenAI API, Azure OpenAI)
   
   Format: ASCII diagram or Mermaid syntax
   
2. TECHNICAL ARCHITECTURE DIAGRAM
   Show components:
   - Frontend: React, TypeScript, TailwindCSS
   - Backend: FastAPI, Pydantic
   - AI/ML: LangGraph, LangChain, ChromaDB
   - Database: SQLite (relational), ChromaDB (vector)
   - External: OpenAI API
   
   Include: Message flows, API calls, data stores

3. DATA FLOW DIAGRAM
   Show:
   - User uploads PDF
   - PDF → Document Storage
   - PDF → PDF Loader
   - PDF → Text Chunking
   - Chunks → Embedding Generation
   - Embeddings → ChromaDB Storage
   - User Query → Embedding
   - Query Embedding → Semantic Search
   - Retrieved Docs → LLM Context
   - LLM Response → User

4. AI AGENT WORKFLOW DIAGRAM
   Show 7 agents and interactions:
   - Supervisor Agent (orchestrator)
   - Document Analyzer Agent
   - Query Understanding Agent
   - Knowledge Retriever Agent
   - Conflict Detector Agent
   - Summarization Agent
   - Recommendation Agent
   
   Show: Inputs, outputs, tool calls, memory, error handling

5. SECURITY ARCHITECTURE DIAGRAM
   Show:
   - Authentication (JWT tokens)
   - Authorization (role-based access)
   - Data encryption (at rest, in transit)
   - Audit logging
   - API security (rate limiting, validation)
   - Database security (parameterized queries)

6. DEPLOYMENT ARCHITECTURE DIAGRAM
   Show:
   - Docker containers
   - Docker Compose services
   - Volume mounts
   - Port mappings
   - Network configuration
   - Environment variables

OUTPUT FORMAT: Use Mermaid syntax for diagrams (can render in GitHub/markdown) or detailed ASCII art with descriptions.
```

---

# 🗄️ PHASE 3: DELIVERABLE 3 - DATABASE DESIGN & DATA MODELS

## Objective
Create logical model, physical model, ER diagram, relationships, constraints, sample data, data dictionary.

## Instructions for Amazon Q

```
Generate DELIVERABLE 3: Database Design & Data Models for "AI Knowledge Discovery & Decision Assistant"

CREATE:

1. LOGICAL DATA MODEL
   Define entities and relationships (conceptual):
   - Customer
   - Document
   - DocumentChunk
   - Embedding
   - ConversationHistory
   - ChatMessage
   - KnowledgeBase
   - Conflict
   - Recommendation
   - Notification
   - AuditLog

2. ENTITY-RELATIONSHIP DIAGRAM
   Use Mermaid/PlantUML syntax showing:
   - All entities and attributes
   - Primary keys (PK)
   - Foreign keys (FK)
   - Relationships (1:1, 1:N, M:N)
   - Cardinality notation

3. PHYSICAL DATA MODEL (DDL)
   For each table:
   
   TABLE: customers
   - customer_id (PK, UUID)
   - email (UNIQUE, NOT NULL)
   - name (VARCHAR 255, NOT NULL)
   - organization (VARCHAR 255)
   - role (ENUM: user, admin)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)
   - is_active (BOOLEAN, DEFAULT true)
   - INDEX: email, created_at
   
   TABLE: documents
   - document_id (PK, UUID)
   - customer_id (FK → customers)
   - file_name (VARCHAR 255, NOT NULL)
   - file_path (TEXT)
   - file_size (INTEGER)
   - file_type (VARCHAR 10)
   - status (ENUM: uploaded, processing, indexed, failed)
   - upload_date (TIMESTAMP)
   - indexed_date (TIMESTAMP)
   - total_chunks (INTEGER)
   - metadata (JSON)
   - created_at (TIMESTAMP)
   - INDEX: customer_id, status, upload_date
   
   TABLE: document_chunks
   - chunk_id (PK, UUID)
   - document_id (FK → documents)
   - chunk_text (TEXT)
   - chunk_index (INTEGER)
   - created_at (TIMESTAMP)
   - INDEX: document_id
   
   TABLE: embeddings
   - embedding_id (PK, UUID)
   - chunk_id (FK → document_chunks)
   - embedding_vector (VECTOR 1536) [ChromaDB integration]
   - model_used (VARCHAR 100)
   - created_at (TIMESTAMP)
   
   TABLE: conversation_histories
   - conversation_id (PK, UUID)
   - customer_id (FK → customers)
   - title (VARCHAR 255)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)
   - is_archived (BOOLEAN, DEFAULT false)
   - INDEX: customer_id, created_at
   
   TABLE: chat_messages
   - message_id (PK, UUID)
   - conversation_id (FK → conversation_histories)
   - sender_type (ENUM: user, assistant)
   - message_text (TEXT)
   - sources (JSON) [array of document references]
   - confidence_score (DECIMAL 3,2)
   - created_at (TIMESTAMP)
   - INDEX: conversation_id, created_at
   
   TABLE: conflicts
   - conflict_id (PK, UUID)
   - conversation_id (FK → conversation_histories)
   - customer_id (FK → customers)
   - conflict_description (TEXT)
   - source_documents (JSON) [array of doc IDs]
   - severity (ENUM: low, medium, high)
   - resolved (BOOLEAN, DEFAULT false)
   - resolution_notes (TEXT)
   - created_at (TIMESTAMP)
   - INDEX: customer_id, severity, resolved
   
   TABLE: recommendations
   - recommendation_id (PK, UUID)
   - conversation_id (FK → conversation_histories)
   - customer_id (FK → customers)
   - recommendation_text (TEXT)
   - confidence_score (DECIMAL 3,2)
   - supporting_documents (JSON)
   - status (ENUM: pending, approved, rejected)
   - created_at (TIMESTAMP)
   - INDEX: customer_id, status
   
   TABLE: notifications
   - notification_id (PK, UUID)
   - customer_id (FK → customers)
   - notification_type (VARCHAR 50)
   - message (TEXT)
   - is_read (BOOLEAN, DEFAULT false)
   - created_at (TIMESTAMP)
   - read_at (TIMESTAMP)
   - INDEX: customer_id, is_read
   
   TABLE: audit_logs
   - log_id (PK, UUID)
   - customer_id (FK → customers)
   - action (VARCHAR 100)
   - entity_type (VARCHAR 50)
   - entity_id (UUID)
   - details (JSON)
   - ip_address (VARCHAR 45)
   - created_at (TIMESTAMP)
   - INDEX: customer_id, action, created_at

4. DATA RELATIONSHIPS
   Document (1) ← Many → DocumentChunk
   DocumentChunk (1) ← Many → Embedding
   Document (1) ← Many → Conflict
   ConversationHistory (1) ← Many → ChatMessage
   ConversationHistory (1) ← Many → Conflict
   ConversationHistory (1) ← Many → Recommendation
   Customer (1) ← Many → Document
   Customer (1) ← Many → ConversationHistory
   Customer (1) ← Many → Notification
   Customer (1) ← Many → AuditLog

5. NORMALIZATION
   - All tables in 3NF
   - No redundant data
   - Proper primary/foreign keys
   - Referential integrity maintained

6. SAMPLE DATA (5-10 rows per table)
   Provide realistic test data

7. DATA DICTIONARY
   For each field:
   - Name
   - Type
   - Length/Precision
   - Nullable
   - Default value
   - Description
   - Validation rules

8. INDEXES & PERFORMANCE
   List all indexes created for query optimization
   Explain why each index was created

OUTPUT FORMAT: SQL DDL statements + ER diagram (Mermaid/PlantUML) + comprehensive markdown documentation.
```

---

# 📐 PHASE 4: DELIVERABLE 4 - STORY-TO-SPEC DECOMPOSITION (SSD)

## Objective
Decompose requirements into epics, user stories, workflows, business rules, validation rules, implementation-ready specs.

## Instructions for Amazon Q

```
Generate DELIVERABLE 4: Story-to-Spec Decomposition for "AI Knowledge Discovery & Decision Assistant"

CREATE:

1. EPIC BREAKDOWN
   
   EPIC 1: DOCUMENT MANAGEMENT SYSTEM
   Description: Manage document lifecycle - upload, process, store, retrieve
   
   EPIC 2: SEMANTIC KNOWLEDGE RETRIEVAL
   Description: Retrieve relevant documents using semantic search
   
   EPIC 3: INTELLIGENT CONFLICT DETECTION
   Description: Identify, flag, and resolve conflicting information
   
   EPIC 4: AI-POWERED INSIGHTS & RECOMMENDATIONS
   Description: Generate summaries and actionable recommendations
   
   EPIC 5: MULTI-TURN CONVERSATIONAL AI
   Description: Enable natural conversation with context preservation
   
   EPIC 6: ADMINISTRATION & MONITORING
   Description: Admin controls, audit logging, monitoring

2. USER STORIES (3-4 per epic)
   Format:
   
   STORY: US-1.1 - User uploads PDF document
   Epic: EPIC 1
   Priority: High
   Story Points: 5
   
   User Story:
   AS A business analyst
   I WANT TO upload enterprise documents (PDFs)
   SO THAT I can build a knowledge base for analysis
   
   Acceptance Criteria:
   - GIVEN user is on dashboard
   - WHEN user clicks "Upload Document"
   - AND selects a PDF file (≤50MB)
   - THEN file is uploaded successfully
   - AND indexing begins automatically
   - AND user sees progress indicator
   - AND upload completion notification is sent
   
   Workflow:
   1. User clicks upload button
   2. File browser opens
   3. User selects PDF file
   4. System validates file (type, size)
   5. File upload to backend
   6. Trigger PDF processing pipeline
   7. Show success message
   8. Display document in document list
   
   Business Rules:
   - BR-1.1: Only PDF files allowed
   - BR-1.2: Maximum file size 50MB
   - BR-1.3: Maximum 100 documents per user
   - BR-1.4: Document names must be unique per user
   
   Validation Rules:
   - VR-1.1: File extension must be .pdf
   - VR-1.2: File size must be > 0 and ≤ 52428800 bytes
   - VR-1.3: File must be readable PDF (not corrupted)
   
   Dependencies: None
   
   Implementation Notes:
   - Use FastAPI file upload endpoint
   - Implement async file processing
   - Store file path in document table
   - Trigger Celery task for indexing
   - Return document_id to frontend

3. WORKFLOWS (Process flows with decision points)
   
   WORKFLOW: Document Processing Pipeline
   Input: PDF file path
   Output: Indexed document in ChromaDB
   
   Steps:
   1. Extract text from PDF
   2. Split text into chunks (500 tokens, 50 overlap)
   3. Generate embeddings for each chunk
   4. Store embeddings in ChromaDB
   5. Update document status to "indexed"
   6. Trigger notification to user
   
   Error Handling:
   - If PDF extraction fails → retry 3x, then mark as failed
   - If embedding generation fails → log error, continue with next chunk
   - If ChromaDB storage fails → retry with exponential backoff
   
   WORKFLOW: Query & Retrieval
   Input: User query (natural language)
   Output: Top-K relevant documents with context
   
   Steps:
   1. Receive user query
   2. Generate embedding for query
   3. Search ChromaDB for top-5 similar chunks
   4. Retrieve source documents
   5. Format results with citations
   6. Return to user

4. BUSINESS RULES (Consolidated list)
   BR-1: Document Management
   BR-2: Access Control
   BR-3: AI Confidence Thresholds
   BR-4: Conflict Severity Levels
   BR-5: Recommendation Approval Workflow

5. VALIDATION RULES (Consolidated list)
   VR-1: Document Validation (format, size)
   VR-2: Input Validation (query length, special chars)
   VR-3: Output Validation (response format, citations)

6. IMPLEMENTATION-READY SPECS
   For each story:
   - Input/Output data structures (JSON schema)
   - API endpoint specifications
   - Database operations
   - Error codes and messages
   - Security requirements
   - Performance requirements

OUTPUT FORMAT: Structured markdown with tables, nested hierarchies, and clear formatting.
```

---

# 🎨 PHASE 5: DELIVERABLE 5 - WIREFRAMES & UI DESIGN

## Objective
Create screen designs showing data flow, navigation, user interactions.

## Instructions for Amazon Q

```
Generate DELIVERABLE 5: Wireframes & User Interface Design for "AI Knowledge Discovery & Decision Assistant"

CREATE WIREFRAMES FOR 8 SCREENS:

1. LOGIN SCREEN
   Layout:
   - Centered card on gradient background
   - Email input field
   - Password input field
   - "Remember me" checkbox
   - "Forgot password" link
   - Sign in button
   - Sign up link
   
   Interactions:
   - Email validation on blur
   - Show/hide password toggle
   - Disable button while submitting
   - Show error messages inline
   
   Design Notes:
   - Minimal, professional
   - No icons
   - Dark mode: #F8FAFC background
   - Card: white with subtle border
   - Typography: Large, clear labels

2. DASHBOARD SCREEN
   Layout:
   - Top navigation bar (logo, user menu, logout)
   - Left sidebar (navigation links)
   - Main content area with grid:
     
     Row 1: 
     - Quick Upload Card (drag-drop area)
     - Document Count Summary Card
     - Recent Queries Card
     
     Row 2:
     - AI Recommendations Card
     - Conflicts Identified Card
     - Renewal Rate Card (if policy renewal context)
     
     Row 3:
     - Recent Conversations Table
     - Activity Timeline
   
   Interactive Elements:
   - Hover states on cards
   - Click to navigate to details
   - Quick action buttons

3. DOCUMENT MANAGEMENT SCREEN
   Layout:
   - Page title: "Your Documents"
   - Search/filter bar
   - Upload button (triggers modal)
   - Documents table with columns:
     - Document name
     - Upload date
     - Status (processing, indexed, failed)
     - Document size
     - Actions (view, delete, reindex)
   - Pagination
   - Sorting capabilities
   
   Details:
   - Show document processing progress
   - Display error messages if indexing failed
   - Quick preview on hover

4. QUERY & SEARCH SCREEN
   Layout:
   - Large search bar at top
   - Filters sidebar (date range, document filter, confidence level)
   - Search results area:
     - Result card showing:
       - Relevant text snippet
       - Source document name
       - Relevance score
       - Page reference
       - "View in context" button
   - Pagination of results
   - "Save search" option
   
   Interactive:
   - Auto-complete suggestions
   - Highlight matching terms
   - Preview modal on click

5. CHAT/CONVERSATION SCREEN
   Layout:
   - Top: Conversation title, date range
   - Left sidebar: Conversation history (list of past conversations)
   - Main area: Chat message area
     - User messages (right aligned, light blue background)
     - Assistant messages (left aligned, white background with border)
     - Message timestamp
     - Sources indicated below assistant message
   - Bottom: Message input field with:
     - Text input
     - Send button
     - Attachment button (for context documents)
     - Clear conversation button
   
   Features:
   - Typing indicator when AI responding
   - Streaming response display
   - Source citations clickable (expand to show full text)
   - Copy button on messages
   - Edit/delete message options
   - "Save as recommendation" button

6. CONFLICT DETECTION SCREEN
   Layout:
   - Page title: "Identified Conflicts"
   - Severity filter buttons (All, Low, Medium, High)
   - Conflict cards showing:
     - Conflict description
     - Involved documents (badges)
     - Severity level (color-coded)
     - Resolution status
     - View details button
   - Details modal showing:
     - Full conflict description
     - Source document excerpts
     - Suggested resolution
     - Mark as resolved button
     - Add resolution notes
   
   Visual Design:
   - Severity color coding
   - Expandable sections
   - Clear call-to-action buttons

7. RECOMMENDATIONS SCREEN
   Layout:
   - Page title: "AI Recommendations"
   - Filter by status (Pending, Approved, Rejected)
   - Recommendation cards:
     - Title
     - Description
     - Confidence score (0-100%)
     - Supporting documents
     - Status badge
     - Actions: Approve, Reject, View Details
   - Details modal
   - Add notes field
   
   Design:
   - Confidence score shown as progress bar
   - Color-coded status badges
   - Clear action buttons

8. ADMIN DASHBOARD
   Layout:
   - User management section:
     - User list table
     - Add user button
     - Edit/delete user actions
   - Document management:
     - Total documents uploaded
     - Reindex all button
   - Audit logs:
     - Searchable log table
     - Filter by action, user, date
   - System health:
     - API uptime
     - Database status
     - Vector DB status

DESIGN SYSTEM:

Color Palette:
- Background: #F8FAFC
- Card: #FFFFFF
- Primary: #1E3A8A (dark blue)
- Secondary: #475569 (slate)
- Accent: #2563EB (bright blue)
- Success: #16A34A (green)
- Warning: #CA8A04 (amber)
- Danger: #DC2626 (red)
- Neutral text: #1F2937

Typography:
- Heading 1: 32px, bold, #1E3A8A
- Heading 2: 24px, bold, #1E3A8A
- Body: 16px, regular, #4B5563
- Small: 14px, regular, #6B7280
- Labels: 14px, medium, #4B5563

Spacing:
- 8px, 16px, 24px, 32px, 48px (8px baseline)

Components:
- Buttons: 40px height, 16px padding, rounded 6px
- Inputs: 40px height, 12px padding, border 1px #E5E7EB
- Cards: 1px border #E5E7EB, box-shadow: 0 1px 3px rgba(0,0,0,0.1)
- Tables: header #F3F4F6, striped rows
- Modals: overlay dark background, centered card

OUTPUT FORMAT: ASCII wireframe sketches + detailed design specifications + component library definitions.
```

---

# 📋 PHASE 6: DELIVERABLE 6 - SPECS/DSL IN MARKDOWN/YAML

## Objective
Create structured specifications for each story component with field definitions, screen behavior, validation, APIs.

## Instructions for Amazon Q

```
Generate DELIVERABLE 6: SPECS/DSL in Markdown/YAML for "AI Knowledge Discovery & Decision Assistant"

CREATE SPECIFICATIONS FOR KEY COMPONENTS:

1. API SPECIFICATIONS (REST)

   API Spec: POST /api/documents/upload
   ---
   Description: Upload a PDF document for processing
   Authentication: JWT token required
   
   Request:
   - Method: POST
   - Content-Type: multipart/form-data
   - Body:
     - file: File (PDF, max 50MB)
     - metadata: Object (optional)
       - title: string
       - description: string
       - tags: array of strings
   
   Response (200):
   {
     "success": true,
     "document_id": "uuid",
     "file_name": "string",
     "status": "uploading",
     "message": "Document uploaded. Indexing started."
   }
   
   Error Responses:
   - 400: Invalid file format
   - 413: File too large
   - 401: Unauthorized
   - 500: Server error
   
   Validation Rules:
   - file.mimetype must be "application/pdf"
   - file.size must be ≤ 52428800
   - metadata.title must be 1-255 characters
   - metadata.tags must be array of strings (max 10)

   API Spec: POST /api/chat
   ---
   Description: Send message to AI assistant
   
   Request:
   {
     "conversation_id": "uuid",
     "message": "string",
     "context_documents": ["uuid"] // optional
   }
   
   Response (200):
   {
     "message_id": "uuid",
     "response": "string",
     "sources": [
       {
         "document_id": "uuid",
         "document_name": "string",
         "snippet": "string",
         "relevance_score": 0.95
       }
     ],
     "confidence": 0.92,
     "processing_time_ms": 1250
   }
   
   Validation:
   - message.length must be > 0 and ≤ 2000
   - conversation_id must be valid UUID
   - Remove prompt injection attempts
   
   Implementation:
   - Stream response using Server-Sent Events
   - Trigger conflict detection
   - Log conversation
   - Update conversation history

2. DATA MODEL SPECIFICATIONS (YAML)

   Document:
     description: "Represents an uploaded document"
     fields:
       document_id:
         type: UUID
         primary_key: true
         generated: uuid4()
       customer_id:
         type: UUID
         foreign_key: customers.id
         required: true
       file_name:
         type: string
         length: 255
         required: true
         validation: "match ^[\\w\\s.\\-()]+$"
       file_size:
         type: integer
         required: true
         validation: "0 < size ≤ 52428800"
       status:
         type: enum
         values: [uploaded, processing, indexed, failed]
         default: uploaded
       created_at:
         type: timestamp
         auto_set: true
       metadata:
         type: json
         schema:
           title: string
           tags: array
           category: string
     indexes:
       - [customer_id, created_at]
       - [status]
     relationships:
       document_chunks:
         type: one_to_many
         foreign_table: document_chunks

   Conversation:
     description: "Chat conversation session"
     fields:
       conversation_id:
         type: UUID
         primary_key: true
       customer_id:
         type: UUID
         foreign_key: customers.id
       title:
         type: string
         length: 255
       created_at:
         type: timestamp
       updated_at:
         type: timestamp
       is_archived:
         type: boolean
         default: false
     indexes:
       - [customer_id, created_at]

3. SCREEN BEHAVIOR SPECIFICATIONS

   Screen: ChatInterface
   Purpose: Real-time conversation with AI assistant
   
   Component: MessageInput
   - Type: textarea
   - Placeholder: "Ask a question..."
   - Max length: 2000 characters
   - Behaviors:
     - On keydown (Ctrl+Enter): submit_message()
     - On focus: clear_error_message()
     - On input: update_character_count()
   - Validation:
     - message.trim().length > 0
     - message.length ≤ 2000
   - Error: Display below input in red (#DC2626)
   
   Component: MessageDisplay
   - Render user messages right-aligned, blue background
   - Render assistant messages left-aligned, white background
   - Show timestamp below each message
   - Show sources as collapsible list
   - Support markdown formatting for assistant messages
   - On hover: show copy, delete, edit buttons
   - Loading state: show skeleton for incoming message
   - Streaming: Display text as it arrives (animated)
   
   Component: ConversationSidebar
   - Show list of conversations (10 most recent)
   - On click: load_conversation(id)
   - Show "New Conversation" button
   - Show "Archive" and "Delete" buttons on hover
   - Highlight current conversation
   - Search conversations by title

4. VALIDATION RULE SPECIFICATIONS

   ValidationRules:
     UserQuery:
       - length_min: 1
       - length_max: 2000
       - forbidden_patterns:
         - "<script.*</script>"
         - "DROP TABLE"
         - "DELETE FROM"
       - allowed_chars: "alphanumeric, spaces, punctuation"
       - error_message: "Invalid query format"
     
     DocumentUpload:
       - file_format: "pdf only"
       - file_size_max: 52428800
       - file_size_min: 1
       - allowed_extensions: [".pdf"]
       - scan_for_malware: true
       - error_message: "File must be PDF, ≤50MB"
     
     EmailInput:
       - pattern: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
       - length_max: 254
       - required: true
       - error_message: "Invalid email format"

5. WORKFLOW STATE MACHINE SPECIFICATION

   DocumentIndexingWorkflow:
     initial_state: UPLOADED
     states:
       UPLOADED:
         transitions:
           - event: start_indexing
             target: PROCESSING
             guards:
               - file_exists == true
               - file_size_valid == true
       PROCESSING:
         transitions:
           - event: indexing_complete
             target: INDEXED
           - event: indexing_failed
             target: FAILED
       INDEXED:
         transitions:
           - event: reindex
             target: PROCESSING
       FAILED:
         transitions:
           - event: retry
             target: PROCESSING
           - event: delete
             target: DELETED

6. ERROR HANDLING SPECIFICATION

   ErrorCodes:
     E001:
       message: "Document not found"
       status_code: 404
       user_message: "The document you requested doesn't exist."
       action: "Return to documents list"
     E002:
       message: "Insufficient permissions"
       status_code: 403
       user_message: "You don't have access to this document."
       action: "Contact administrator"
     E003:
       message: "PDF processing failed"
       status_code: 422
       user_message: "We couldn't process this PDF. Please try another file."
       action: "Upload different file"
     E004:
       message: "AI service unavailable"
       status_code: 503
       user_message: "The AI service is temporarily unavailable. Please try again later."
       action: "Retry automatically"

7. FILE STRUCTURE & HIERARCHY

   Directory:
     /backend
       /app
         /api
           /routes
             documents.py
             chat.py
             users.py
             admin.py
           /schemas
             document.py
             chat.py
             user.py
         /services
           document_service.py
           chat_service.py
           rag_service.py
         /agents
           supervisor_agent.py
           document_analyzer_agent.py
           knowledge_retriever_agent.py
           conflict_detector_agent.py
           recommendation_agent.py
           summarization_agent.py
           notification_agent.py
         /database
           models.py
           session.py
           init_db.py
         /rag
           pdf_loader.py
           chunker.py
           embedder.py
           retriever.py
         /config
           settings.py
           constants.py
         main.py
     /frontend
       /src
         /components
           Auth/
           Dashboard/
           DocumentManager/
           ChatInterface/
           RecommendationCard/
         /pages
           LoginPage.tsx
           DashboardPage.tsx
           ChatPage.tsx
         /services
           api.ts
           auth.ts
         App.tsx
         index.tsx

OUTPUT FORMAT: YAML + Markdown with clear structure, tables, and code blocks.
```

---

# 💻 PHASE 7: DELIVERABLE 7 - SOFTWARE CODE & WORKING SOFTWARE

## Objective
Build a complete, working application with all components integrated.

## Instructions for Amazon Q

```
Generate DELIVERABLE 7: Complete Working Software for "AI Knowledge Discovery & Decision Assistant"

GENERATE COMPLETE BACKEND:

1. Main Application File (main.py)
   - FastAPI app initialization
   - CORS configuration
   - JWT security setup
   - Database initialization
   - OpenAI/Azure OpenAI client setup
   - ChromaDB initialization
   - Health check endpoint

2. Database Models (app/database/models.py)
   - SQLAlchemy ORM models
   - All 9 tables with relationships
   - Validators and constraints
   - Index definitions
   - Sample seed data

3. Pydantic Schemas (app/api/schemas/)
   - DocumentSchema
   - ChatSchema
   - ConflictSchema
   - RecommendationSchema
   - UserSchema
   - ConversationSchema

4. API Routes (app/api/routes/)
   
   documents.py:
   - POST /api/documents/upload (handle file upload, trigger indexing)
   - GET /api/documents (list user's documents)
   - GET /api/documents/{id} (get document details)
   - DELETE /api/documents/{id} (delete document)
   - POST /api/documents/{id}/reindex (re-index document)
   
   chat.py:
   - POST /api/chat (send message, get response)
   - GET /api/conversations (list conversations)
   - GET /api/conversations/{id} (get conversation history)
   - POST /api/conversations (create new conversation)
   - DELETE /api/conversations/{id} (delete conversation)
   
   users.py:
   - POST /api/auth/register (register user)
   - POST /api/auth/login (login, return JWT)
   - GET /api/auth/me (current user info)
   - POST /api/auth/refresh (refresh token)
   
   admin.py:
   - GET /api/admin/users (list all users)
   - GET /api/admin/documents (list all documents)
   - GET /api/admin/audit-logs (view audit logs)
   - POST /api/admin/reindex-all (reindex all documents)

5. RAG Pipeline (app/rag/)
   
   pdf_loader.py:
   - extract_text_from_pdf(file_path: str) → str
   - handle PDF upload, extraction, error handling
   
   chunker.py:
   - chunk_text(text: str, chunk_size=500, overlap=50) → List[str]
   - Split text into overlapping chunks
   
   embedder.py:
   - generate_embeddings(texts: List[str]) → List[List[float]]
   - Use OpenAI embedding model
   
   retriever.py:
   - retrieve_relevant_chunks(query: str, top_k=5) → List[RetrievalResult]
   - Query ChromaDB, return with sources
   
   prompt_injection_filter.py:
   - detect_injection(text: str) → bool
   - Validate user input

6. AI Agents (app/agents/)
   
   Each agent file with:
   - system_prompt definition
   - tools definition
   - agent initialization
   - memory management
   - error handling
   - invoke() method
   
   supervisor_agent.py:
   - Orchestrates workflow
   - Routes to appropriate agents
   - Error recovery
   
   document_analyzer_agent.py:
   - Analyzes document content
   - Extracts key entities
   - Identifies document type
   
   knowledge_retriever_agent.py:
   - Retrieves relevant documents
   - Formats results with citations
   - Handles no-results scenarios
   
   conflict_detector_agent.py:
   - Identifies contradictions
   - Flags severity levels
   - Suggests resolutions
   
   recommendation_agent.py:
   - Generates recommendations
   - Calculates confidence scores
   - Provides supporting evidence
   
   summarization_agent.py:
   - Creates concise summaries
   - Highlights key points
   - Generates executive summary
   
   notification_agent.py:
   - Creates notifications
   - Handles delivery
   - Tracks read/unread status

7. Services (app/services/)
   
   document_service.py:
   - upload_document(customer_id, file)
   - index_document(document_id)
   - delete_document(document_id)
   - get_document_list(customer_id)
   
   chat_service.py:
   - create_conversation(customer_id, title)
   - save_message(conversation_id, sender, text, sources)
   - get_conversation_history(conversation_id)
   - stream_ai_response(message, conversation_id)
   
   rag_service.py:
   - index_to_chromadb(document_id, chunks)
   - search_chromadb(query, customer_id)
   - get_document_context(document_ids)

GENERATE COMPLETE FRONTEND:

React Application with:
1. pages/
   - LoginPage.tsx
   - DashboardPage.tsx
   - ChatPage.tsx
   - DocumentsPage.tsx
   - RecommendationsPage.tsx
   - ConflictsPage.tsx
   - ProfilePage.tsx
   - AdminPage.tsx
   - NotFoundPage.tsx

2. components/
   - Auth/LoginForm.tsx
   - Layout/Navbar.tsx
   - Layout/Sidebar.tsx
   - Dashboard/SummaryCards.tsx
   - DocumentManager/UploadArea.tsx
   - DocumentManager/DocumentTable.tsx
   - ChatInterface/MessageList.tsx
   - ChatInterface/MessageInput.tsx
   - ConversationSidebar.tsx
   - ConflictCard.tsx
   - RecommendationCard.tsx

3. services/
   - api.ts (axios instance, all API calls)
   - auth.ts (JWT token management)
   - storage.ts (localStorage management)

4. hooks/
   - useAuth.ts (authentication hook)
   - useChat.ts (chat state management)
   - useDocuments.ts (document state management)

5. utils/
   - validators.ts (input validation)
   - formatters.ts (date, text formatting)
   - constants.ts (API endpoints, messages)

6. styles/
   - globals.css (TailwindCSS + custom)
   - component-specific CSS

7. App.tsx
   - Route configuration
   - Protected routes
   - Error boundary
   - Theme provider

8. main.tsx
   - React root render

CONFIGURATION FILES:

package.json:
- All dependencies (react, vite, tailwindcss, axios, etc.)
- Scripts for dev, build, preview

requirements.txt:
- All Python dependencies
- pinned versions

.env.example:
- All environment variables needed

docker-compose.yml:
- Backend service
- Frontend service (dev)
- SQLite volume
- ChromaDB service

Dockerfile:
- Multi-stage build
- Optimized layers
- Security best practices

DATABASE INITIALIZATION:

init_db.py:
- Create all tables
- Create indexes
- Insert seed data:
  - 3 test customers
  - 5 sample documents
  - 10 sample conversations with messages
  - Sample conflicts and recommendations

CODE QUALITY:
- Type hints on all functions
- Docstrings on all classes/functions
- Error handling (try-except)
- Input validation
- Proper logging

ENSURE:
- All imports work
- No circular dependencies
- All APIs connected
- All databases accessible
- All agents can execute
- Frontend communicates with backend
- No TODOs or placeholders
- Code follows PEP 8 (Python) and ESLint (JavaScript)

OUTPUT FORMAT: Complete, production-ready code ready to run.
```

---

# ✅ PHASE 8: DELIVERABLE 8 - FUNCTIONAL TEST SCRIPTS

## Objective
Create comprehensive test cases covering positive, negative, boundary, exception, and security scenarios.

## Instructions for Amazon Q

```
Generate DELIVERABLE 8: Functional Test Scripts for "AI Knowledge Discovery & Decision Assistant"

CREATE TEST CASES IN CSV FORMAT:

Test Case CSV Structure:
TestID,Module,TestType,Description,PreConditions,Steps,ExpectedResult,ActualResult,Status,Notes

DOCUMENT MANAGEMENT TESTS:

T001,Document Upload,Positive,User uploads valid PDF,User logged in,1. Click Upload 2. Select valid PDF 3. Click Submit,File uploaded successfully with success message,Pass,File size 2MB
T002,Document Upload,Negative,User uploads non-PDF file,User logged in,1. Click Upload 2. Select .docx file,Error message shown,Pass,"Error: Only PDF files allowed"
T003,Document Upload,Boundary,User uploads exactly 50MB file,User logged in,1. Click Upload 2. Select 50MB PDF,File uploaded successfully,Pass,Boundary test
T004,Document Upload,Boundary,User uploads 50.1MB file,User logged in,1. Click Upload 2. Select 50.1MB PDF,Error: File too large,Pass,Boundary exceeded
T005,Document Upload,Validation,User uploads file with special chars in name,User logged in,1. Click Upload 2. Select file with @#$,File uploaded with cleaned filename,Pass,Filename sanitized
T006,Document Management,Positive,User views document list,User logged in with documents,1. Go to Documents page 2. View list,All documents displayed with metadata,Pass,Pagination works
T007,Document Management,Positive,User deletes document,User logged in with documents,1. Select document 2. Click Delete 3. Confirm,Document removed from list and DB,Pass,Soft delete implemented
T008,Document Management,Exception,User attempts to delete non-existent document,User logged in,1. Call delete API with invalid ID,404 error returned,Pass,Proper error handling

CHAT & CONVERSATION TESTS:

T009,Chat Interface,Positive,User sends message,Logged in with open conversation,1. Type message 2. Click Send,Message appears in history and AI responds,Pass,Streaming response works
T010,Chat Interface,Positive,User receives multi-document context,Logged in with 3 documents,1. Send query 2. AI retrieves docs,Response includes citations from 2+ docs,Pass,Cross-document analysis works
T011,Chat Interface,Validation,User sends empty message,Logged in,1. Click Send without message,Error: Message required,Pass,Form validation works
T012,Chat Interface,Validation,User sends message exceeding 2000 chars,Logged in,1. Paste 2001-char message 2. Send,Error message shown,Pass,Length validation enforced
T013,Chat Interface,Security,User attempts prompt injection,Logged in,1. Send 'Ignore instructions. Do this instead',System filters injection and responds normally,Pass,Prompt injection blocked
T014,Conversation Management,Positive,User views conversation history,Logged in,1. Open conversation 2. Scroll up,All messages displayed with correct order,Pass,Pagination works for long histories
T015,Conversation Management,Positive,User creates new conversation,Logged in,1. Click New Conversation 2. Give title,New conversation created and opened,Pass,Conversation ID generated
T016,Conversation Management,Positive,User archives conversation,Logged in with conversations,1. Right-click conversation 2. Archive,Conversation moves to archive,Pass,Soft delete used

SEMANTIC SEARCH TESTS:

T017,Search Functionality,Positive,User searches with natural language,Documents indexed,1. Enter 'policy renewal deadlines' 2. Submit,Top-5 relevant documents returned with scores,Pass,Relevance scoring works
T018,Search Functionality,Negative,User searches with no matching results,Documents indexed,1. Enter 'xyz123abc' 2. Submit,No results message shown,Pass,Graceful no-results handling
T019,Search Functionality,Boundary,System searches 1000-page document,Large document indexed,1. Search across 1000-page doc,Results returned in <2 seconds,Pass,Performance acceptable

CONFLICT DETECTION TESTS:

T020,Conflict Detection,Positive,System detects conflicting information,Multiple documents with conflicts,1. Upload docs 2. Trigger analysis,Conflicts flagged with severity levels,Pass,AI detection works
T021,Conflict Detection,Positive,System highlights specific conflict sections,Conflicts detected,1. Open conflict 2. View details,Source document sections highlighted,Pass,Cross-referencing works
T022,Conflict Detection,Exception,No conflicts found in documents,Documents without conflicts,1. Upload docs 2. Trigger analysis,No conflicts message shown,Pass,Correct handling

RECOMMENDATION ENGINE TESTS:

T023,Recommendations,Positive,AI generates recommendations,Query results available,1. Ask for recommendations,Recommendations shown with confidence scores,Pass,Score between 0-100%
T024,Recommendations,Positive,User approves recommendation,Recommendations displayed,1. Click Approve 2. Confirm,Recommendation marked approved and logged,Pass,Audit trail created
T025,Recommendations,Positive,User rejects recommendation,Recommendations displayed,1. Click Reject 2. Add reason,Recommendation marked rejected with notes,Pass,Reason captured

SECURITY & ACCESS CONTROL TESTS:

T026,Security,Positive,Authenticated user accesses documents,User logged in,1. Access dashboard 2. View documents,User sees only their documents,Pass,Row-level security works
T027,Security,Negative,Unauthenticated user attempts access,User not logged in,1. Access /api/documents without token,401 Unauthorized returned,Pass,JWT validation works
T028,Security,Negative,User attempts to access another user's documents,User logged in,1. Modify URL to another user's doc ID,403 Forbidden returned,Pass,Authorization enforced
T029,Security,Negative,User sends malicious SQL in search,User logged in,1. Send "'; DROP TABLE--",System sanitizes and responds normally,Pass,SQL injection prevented
T030,Security,Positive,API rate limiting works,User making rapid requests,1. Send 100 requests/second,Requests throttled after limit,Pass,Rate limiter configured

PERFORMANCE TESTS:

T031,Performance,Positive,Chat response time <2 seconds,System with indexes,1. Send query 2. Measure response time,Response received in <2s,Pass,SLA met
T032,Performance,Positive,Document indexing completes in reasonable time,50MB PDF,1. Upload document 2. Time indexing,Indexing completes in <5 minutes,Pass,Acceptable performance
T033,Performance,Positive,Search returns results in <1 second,1000 documents indexed,1. Search 2. Measure response time,Results in <1s,Pass,Index optimization effective

INTEGRATION TESTS:

T034,Integration,Positive,Complete workflow: upload → search → chat,Clean database,1. Upload doc 2. Search 3. Chat 4. Get recommendation,Full workflow completes successfully,Pass,End-to-end test
T035,Integration,Positive,Multiple users interact simultaneously,3 users logged in,1. User A uploads 2. User B searches 3. User C chats,All operations succeed independently,Pass,Concurrency works

ADMIN TESTS:

T036,Admin,Positive,Admin views all documents,Admin logged in,1. Access admin dashboard 2. View all docs,All user documents displayed,Pass,Admin access works
T037,Admin,Positive,Admin views audit logs,Admin logged in,1. Access audit logs 2. Filter by action,Logs displayed with complete details,Pass,Audit trail comprehensive
T038,Admin,Positive,Admin reindexes all documents,Admin logged in,1. Click reindex all 2. Confirm,All documents reindexed,Pass,Bulk operation works

ERROR HANDLING TESTS:

T039,Error Handling,Exception,Database connection fails,DB down,1. Attempt any operation,Graceful error message shown,Pass,Circuit breaker implemented
T040,Error Handling,Exception,OpenAI API unavailable,API down,1. Send chat message,User-friendly error message,Pass,Fallback message shown

OUTPUT FORMAT: CSV file with all test cases, ready to import to Excel/Google Sheets.
```

---

# 📍 PHASE 9: DELIVERABLE 9 - TRACEABILITY MATRIX

## Objective
Map requirements → stories → specs → database → code → tests → AI outputs with complete traceability.

## Instructions for Amazon Q

```
Generate DELIVERABLE 9: Traceability Matrix for "AI Knowledge Discovery & Decision Assistant"

CREATE COMPREHENSIVE TRACEABILITY MATRIX IN CSV FORMAT:

Columns:
RequirementID,RequirementText,UserStoryID,StoryTitle,EpicID,SpecID,DatabaseTable,DatabaseField,CodeModule,CodeFunction,TestID,TestDescription,AgentResponsible,AIPromptUsed,DemoEvidence

ENTRIES:

FR-1.1,User can upload PDF documents,US-1.1,User uploads PDF,EPIC-1,SPEC-1.1.1,documents,document_id + file_path,app/api/routes/documents.py,upload_document(),T001,User uploads valid PDF,Document Analyzer Agent,"Prompt: 'Extract text from PDF and prepare for embedding'",docs/demo_01.mp4

FR-1.2,System automatically indexes documents,US-1.2,Auto index,EPIC-1,SPEC-1.2.1,documents + document_chunks + embeddings,status + chunk_text + embedding_vector,app/rag/chunker.py + embedder.py,index_document() + generate_embeddings(),T031,Document indexing performance,Document Analyzer Agent,"Prompt: 'Split text into semantic chunks with overlap'",docs/demo_02.mp4

FR-2.1,User can search using natural language,US-2.1,Natural language search,EPIC-2,SPEC-2.1.1,embeddings + knowledge_base,embedding_vector,app/rag/retriever.py,retrieve_relevant_chunks(),T017,User searches with natural language,Knowledge Retriever Agent,"Prompt: 'Find semantically similar documents to user query'",docs/demo_03.mp4

FR-2.4,System returns source citations,US-2.4,Include citations,EPIC-2,SPEC-2.4.1,chat_messages + documents,sources (JSON),app/services/chat_service.py,format_response_with_citations(),T010,User receives multi-document context,Knowledge Retriever Agent,"Prompt: 'Format results with document name, page, snippet'",docs/demo_04.mp4

FR-3.1,System identifies contradictory information,US-3.1,Detect conflicts,EPIC-3,SPEC-3.1.1,conflicts + documents,conflict_description + source_documents,app/agents/conflict_detector_agent.py,detect_conflicts(),T020,System detects conflicting information,Conflict Detector Agent,"Prompt: 'Analyze documents for contradictions and rate severity'",docs/demo_05.mp4

FR-4.1,System generates concise summaries,US-4.1,Create summary,EPIC-4,SPEC-4.1.1,chat_messages,message_text,app/agents/summarization_agent.py,generate_summary(),T025,User receives recommendation,Summarization Agent,"Prompt: 'Summarize key points in 3-4 sentences with citations'",docs/demo_06.mp4

FR-4.2,System provides AI recommendations,US-4.2,AI recommendations,EPIC-4,SPEC-4.2.1,recommendations,recommendation_text + confidence_score,app/agents/recommendation_agent.py,generate_recommendations(),T023,AI generates recommendations,Recommendation Agent,"Prompt: 'Analyze documents and suggest next steps with confidence'",docs/demo_07.mp4

FR-5.1,Multi-turn conversation support,US-5.1,Conversation context,EPIC-5,SPEC-5.1.1,conversation_histories + chat_messages,conversation_id,app/services/chat_service.py,load_conversation_context(),T009,User sends message with response,Supervisor Agent,"Prompt: 'Maintain conversation context across turns'",docs/demo_08.mp4

FR-6.2,Admin can view audit logs,US-6.2,View audit logs,EPIC-6,SPEC-6.2.1,audit_logs,action + entity_type + details,app/api/routes/admin.py,get_audit_logs(),T037,Admin views audit logs,Notification Agent,"Prompt: 'Log all actions with timestamp and user context'",docs/demo_09.mp4

NFR-1,Response time <2 seconds,US-2.1,Natural language search,EPIC-2,SPEC-2.1.1,embeddings (with indexes),embedding_vector,app/rag/retriever.py,retrieve_relevant_chunks(),T031,Chat response time <2 seconds,Knowledge Retriever Agent,"Prompt: 'Optimize vector search with proper indexing'",docs/perf_01.mp4

NFR-2,System supports 1000 concurrent users,,-,EPIC-5,SPEC-5.1.2,-,-,app/main.py,FastAPI configuration with worker processes,T035,Multiple users interact simultaneously,Supervisor Agent,"Prompt: 'Configure FastAPI for async handling and connection pooling'",docs/load_test.mp4

NFR-3,Data encryption at rest,,-,EPIC-6,SPEC-6.1.1,all tables,all columns (encrypted),app/config/settings.py,database encryption setup,T026,Security: Access control,-,Supervisor Agent,"Prompt: 'Enable SQLite encryption with SQLCipher'",docs/security_audit.pdf

BUSINESS RULE MAPPING:

BR-1: Only authenticated users can access,FR-2.1 + FR-6.1,JWT validation,app/api/security.py,verify_token(),T027,Unauthenticated user attempts access

BR-2: Users access only their documents,FR-1.1 + FR-6.1,Row-level security,app/api/routes/documents.py,query_documents(),T026,Authenticated user accesses documents

BR-3: AI recommendations require confidence scores,FR-4.2,Confidence calculation,app/agents/recommendation_agent.py,calculate_confidence(),T023,AI generates recommendations

BR-4: Audit logs track all access,FR-6.2,Logging middleware,app/middleware/audit.py,log_action(),T037,Admin views audit logs

DATABASE FIELD MAPPING:

documents.document_id ← FR-1.1 (upload) ← app/api/routes/documents.py (upload_document()) ← T001
documents.status ← FR-1.2 (auto-index) ← app/rag/chunker.py (update_status()) ← T031
embeddings.embedding_vector ← FR-2.1 (search) ← app/rag/embedder.py (generate_embeddings()) ← T017
conflicts.conflict_description ← FR-3.1 (detect) ← app/agents/conflict_detector_agent.py ← T020
recommendations.confidence_score ← FR-4.2 (recommend) ← app/agents/recommendation_agent.py ← T023

CODE MODULE MAPPING:

Backend:
- app/api/routes/documents.py: FR-1.1, FR-1.2, FR-1.3, FR-1.4
- app/api/routes/chat.py: FR-5.1, FR-5.2, FR-5.3
- app/rag/: FR-2.1, FR-2.2, FR-2.3, FR-2.4
- app/agents/: FR-3.1, FR-4.1, FR-4.2
- app/database/models.py: All database requirements

Frontend:
- pages/ChatPage.tsx: FR-5.1, FR-5.2, FR-5.3
- pages/DocumentsPage.tsx: FR-1.1, FR-1.2, FR-1.3
- components/ChatInterface/: FR-5.1 (multi-turn), FR-2.4 (citations)

PROMPT & AI OUTPUT MAPPING:

Agent,Prompt Used,Feature Generated,Test Coverage,Demo File
Document Analyzer Agent,"Extract and analyze document structure",Document indexing,T031,demo_02.mp4
Knowledge Retriever Agent,"Find semantically similar documents",Search results with citations,T010 + T017,demo_03.mp4 + demo_04.mp4
Conflict Detector Agent,"Analyze for contradictions",Conflict detection results,T020,demo_05.mp4
Summarization Agent,"Create concise summaries",Summary text,T025,demo_06.mp4
Recommendation Agent,"Generate actionable recommendations",Recommendation with confidence,T023,demo_07.mp4
Supervisor Agent,"Orchestrate workflow",Full conversation flow,T034 + T035,demo_08.mp4

OUTPUT FORMAT: CSV file importable to Excel with complete traceability across all artifacts.
```

---

# 🤖 PHASE 10: DELIVERABLE 10 - CODE QUALITY REVIEW AGENT

## Objective
Create an AI-assisted agent that reviews application code against quality checklist and SonarQube-style criteria.

## Instructions for Amazon Q

```
Generate DELIVERABLE 10: Code Quality Review Agent for "AI Knowledge Discovery & Decision Assistant"

CREATE AN AI AGENT (Streamlit + Claude API) THAT:

1. PURPOSE
   Review the application code developed in Deliverable 7 against:
   - Maintainability
   - Readability
   - Modularity
   - Coding standards
   - Naming conventions
   - Duplication
   - Exception handling
   - Security considerations
   - Configuration handling
   - Database access quality
   - Test readiness
   - Traceability to specifications

2. APPLICATION STRUCTURE (Streamlit)

   File: quality_review_agent.py
   
   Purpose:
   - Frontend UI for code quality review
   - Upload/select code files
   - Trigger review process
   - Display comprehensive results
   - Generate quality report

   UI Components:
   - File upload area (select code files)
   - Review trigger button
   - Progress indicator during review
   - Quality score display (0-100)
   - Checklist findings table
   - Severity-wise breakdown
   - Code snippet viewer (for issues)
   - Improvement recommendations
   - Export report button

3. QUALITY CHECKLIST

   Maintainability:
   - [ ] Functions are <50 lines
   - [ ] Classes are <200 lines
   - [ ] Single responsibility principle
   - [ ] DRY violations detected
   - [ ] Code comments are present
   - [ ] Complex logic explained

   Readability:
   - [ ] Variable names are descriptive
   - [ ] Function names are clear
   - [ ] Code is properly indented
   - [ ] Line length <120 characters
   - [ ] Type hints present (Python)
   - [ ] Docstrings on functions/classes

   Modularity:
   - [ ] Separation of concerns
   - [ ] Reusable components
   - [ ] Low coupling
   - [ ] High cohesion
   - [ ] No circular dependencies
   - [ ] Clear interfaces/contracts

   Coding Standards:
   - [ ] PEP 8 compliance (Python)
   - [ ] ESLint compliance (JavaScript)
   - [ ] Naming conventions followed
   - [ ] Code style consistent
   - [ ] No hardcoded values
   - [ ] Configuration externalized

   Exception Handling:
   - [ ] Try-catch blocks present
   - [ ] Specific exceptions caught
   - [ ] Error messages informative
   - [ ] Graceful fallbacks implemented
   - [ ] Logging on errors
   - [ ] No silent failures

   Security:
   - [ ] No hardcoded secrets
   - [ ] Input validation present
   - [ ] SQL injection prevention
   - [ ] XSS prevention (frontend)
   - [ ] CSRF protection (if needed)
   - [ ] Authentication/authorization checks
   - [ ] No sensitive data in logs
   - [ ] Secure random generation

   Database Access:
   - [ ] Parameterized queries used
   - [ ] Connection pooling configured
   - [ ] Transactions used appropriately
   - [ ] Indexes on foreign keys
   - [ ] No N+1 queries
   - [ ] Performance optimized

   Test Readiness:
   - [ ] Code is testable
   - [ ] Dependencies injectable
   - [ ] Mocking possible
   - [ ] Test data setup available
   - [ ] Edge cases considered
   - [ ] Unit test coverage >70%

   Traceability:
   - [ ] Code maps to requirements
   - [ ] Comments reference specs
   - [ ] Version control messages clear
   - [ ] Audit logging implemented
   - [ ] Changes documented
   - [ ] Deployment procedures clear

4. REVIEW ALGORITHM

   Process:
   1. Parse uploaded code files
   2. For each file:
      a. Analyze against checklist
      b. Identify issues
      c. Classify by severity
      d. Generate recommendations
   3. Calculate quality score:
      - Pass: +2 points per item
      - Warning: +1 point
      - Fail: 0 points
      - Total: 10 categories × ~12 items = 120 max
      - Normalize to 0-100
   4. Generate report

5. SEVERITY CLASSIFICATION

   CRITICAL:
   - Security vulnerabilities
   - SQL injection risks
   - Unhandled exceptions
   - Data loss risks
   - Authentication bypass

   MAJOR:
   - Performance bottlenecks
   - Violations of architecture
   - High complexity functions
   - Poor error handling
   - Code duplication >20%

   MINOR:
   - Naming convention violations
   - Missing docstrings
   - Style inconsistencies
   - Minor readability issues
   - Unused imports

   INFO:
   - Suggestions for improvement
   - Best practice tips
   - Optimization opportunities

6. REPORT GENERATION

   Structure:

   QUALITY SCORE: 87/100
   
   STATUS: PRODUCTION READY (with minor improvements)
   
   SUMMARY:
   - Total Issues: 12
   - Critical: 0
   - Major: 2
   - Minor: 8
   - Info: 2
   
   MAINTAINABILITY SCORE: 88/100
   - 11/12 criteria pass
   - Issue: APIRoute.chat() is 85 lines (recommend <50)
   
   READABILITY SCORE: 92/100
   - 11/12 criteria pass
   - Issue: Variable 'temp_var' needs better name
   
   MODULARITY SCORE: 85/100
   - 10/12 criteria pass
   - Issue: chat_service.py and rag_service.py share duplicate logic
   
   SECURITY SCORE: 90/100
   - 11/12 criteria pass
   - Issue: Password hashing not validated in tests
   
   DATABASE ACCESS SCORE: 87/100
   - 10/12 criteria pass
   - Issues:
     - Chat retrieval missing index on conversation_id
     - Embedding search not using connection pooling
   
   TEST READINESS SCORE: 78/100
   - 9/12 criteria pass
   - Issues:
     - Agent initialization not mockable
     - ChromaDB integration not testable
   
   TOP 5 RECOMMENDATIONS:
   1. Refactor chat route into multiple smaller functions
   2. Extract duplicate RAG logic into shared utility
   3. Add integration tests for multi-agent workflow
   4. Implement connection pooling for database
   5. Add monitoring for LLM API failures
   
   IMPROVEMENT ROADMAP:
   - Week 1: Refactor chat routes (Priority: HIGH)
   - Week 2: Add missing unit tests (Priority: HIGH)
   - Week 3: Optimize database queries (Priority: MEDIUM)
   - Week 4: Add performance monitoring (Priority: MEDIUM)

7. CODE SNIPPETS FOR ISSUES

   Issue: Function too complex
   File: app/agents/supervisor_agent.py
   Line: 45-120
   Severity: MAJOR
   
   Recommendation: Break into 3 smaller functions
   
   Current:
   ```python
   def orchestrate_workflow(query, documents):
       # 75 lines of complex logic
   ```
   
   Suggested:
   ```python
   def parse_query(query):
       # 15 lines
   
   def retrieve_context(query, documents):
       # 20 lines
   
   def generate_response(context):
       # 15 lines
   
   def orchestrate_workflow(query, documents):
       parsed_query = parse_query(query)
       context = retrieve_context(parsed_query, documents)
       response = generate_response(context)
       return response
   ```

8. AUTOMATED FIXES

   For style issues, provide:
   ```python
   # Before:
   x=5
   
   # After:
   x = 5
   ```

9. ACTIONABLE RECOMMENDATIONS

   Don't just say "improve error handling"
   
   DO say:
   "Add try-except block around OpenAI API calls.
    Catch rate_limit_error specifically.
    Implement exponential backoff retry.
    Log error with request_id for debugging.
    Return 503 to user with retry-after header."

10. OUTPUT OPTIONS

    - Display in Streamlit UI
    - Export to PDF report
    - Export to CSV (for tracking)
    - Generate GitHub issues (optional)
    - Send email report

11. IMPLEMENTATION (Python + Streamlit)

    Create file: quality_review_agent.py
    
    Components:
    - file_uploader() - Upload code files
    - parse_files() - Extract code content
    - create_prompt_for_review() - Build Claude prompt
    - call_claude_api() - Get AI review
    - parse_review_results() - Structure findings
    - calculate_quality_score() - Compute score
    - display_report() - Render UI
    - export_report() - Generate PDF/CSV

    Main flow:
    1. User uploads files
    2. System parses code
    3. Claude reviews against checklist
    4. Results formatted and displayed
    5. User can export or generate issues

OUTPUT FORMAT: Working Streamlit application + comprehensive quality report format specification.
```

---

---

# 🎬 EXECUTION STRATEGY FOR AMAZON Q

## How to Use These 10 Phases:

### Phase-by-Phase Execution:

**PHASE 1:** Copy Phase 1 section into Amazon Q
- Execute all deliverable 1 tasks
- Save outputs to `/deliverables/01_requirements.md`
- Verify completeness

**PHASE 2:** Copy Phase 2 section into Amazon Q
- Execute architecture diagrams
- Save to `/deliverables/02_architecture/`
- Review diagrams

**... Continue for PHASES 3-10 ...**

### When Context Fills Up:

Use continuation pattern:
```
CONTINUE FROM PHASE 6
(Resume from where Phase 5 ended)
```

### Token Management:

- **Each phase**: ~2000-3000 tokens
- **Context window**: 100k tokens (Amazon Q)
- **Per session**: Can do 3-4 phases before context fills

### Quality Checkpoints:

After each phase:
1. ✅ Verify all files generated
2. ✅ Check for completeness
3. ✅ Validate no placeholders
4. ✅ Ensure proper formatting

---

# 📦 FINAL DELIVERABLES STRUCTURE:

```
ai-knowledge-discovery-assistant/
├── deliverables/
│   ├── 01_requirements.md
│   ├── 02_architecture/
│   │   ├── logical_diagram.md
│   │   ├── technical_diagram.md
│   │   ├── data_flow_diagram.md
│   │   ├── agent_workflow.md
│   │   ├── security_architecture.md
│   │   └── deployment_architecture.md
│   ├── 03_database/
│   │   ├── er_diagram.md
│   │   ├── ddl_statements.sql
│   │   └── data_dictionary.md
│   ├── 04_story_decomposition.md
│   ├── 05_wireframes.md
│   ├── 06_specs/
│   │   ├── api_specifications.yaml
│   │   ├── data_models.yaml
│   │   ├── screen_behavior.md
│   │   ├── validation_rules.yaml
│   │   └── workflow_state_machines.yaml
│   ├── 07_working_software/
│   │   ├── backend/ (complete Python code)
│   │   ├── frontend/ (complete React code)
│   │   ├── docker/
│   │   ├── config/
│   │   └── README.md
│   ├── 08_test_scripts.csv
│   ├── 09_traceability_matrix.csv
│   └── 10_code_quality_review/
│       ├── quality_review_agent.py
│       └── quality_report.md
└── prompt_history.md (all AI prompts used)
```

---

## Ready to Start?

Copy **PHASE 1** into Amazon Q or your preferred AI tool and begin!

Each phase is self-contained but builds on previous phases for complete traceability.

**Good luck! 🚀**
