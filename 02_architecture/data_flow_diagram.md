# Data Flow Diagram

## 1. Document Ingestion Flow

```mermaid
flowchart TD
    U1([User uploads PDF/DOCX/PPTX/XLSX/EML]) --> S1[Document Storage - filesystem/blob]
    S1 --> L1[Format-Aware Loader - extract text, tables, OCR images]
    L1 --> C1[Text Chunker - 500 tokens, 50 overlap]
    C1 --> E1[Embedding Generator - OpenAI embeddings]
    E1 --> V1[(ChromaDB - store vectors)]
    E1 --> R1[(SQLite - document_chunks table)]
    V1 --> N1([Notify user: indexing complete])
```

## 2. Query & Retrieval Flow

```mermaid
flowchart TD
    Q1([User submits query]) --> Q2[Generate query embedding]
    Q2 --> Q3[(ChromaDB semantic search - top K)]
    Q3 --> Q4[Retrieve source document metadata]
    Q4 --> Q5[Build LLM context window]
    Q5 --> Q6[LLM generates response]
    Q6 --> Q7([Response + citations returned to user])
    Q7 --> Q8[(Persist chat_messages)]
```

## Data Elements at Each Stage

| Stage | Input | Output |
|---|---|---|
| Upload | Raw file bytes (PDF/DOCX/PPTX/XLSX/EML) | Stored file + `document` row (status=uploaded) |
| Extraction | File path + file_type | Raw text string (text, table rows flattened to text, OCR'd image text) |
| Chunking | Raw text | List of text chunks (500 tokens, 50 overlap) |
| Embedding | Text chunks | Vector embeddings (1536-dim) |
| Storage | Vectors + chunk metadata | ChromaDB collection entries + `document_chunks` rows |
| Query embedding | User query string | Query vector |
| Semantic search | Query vector | Top-K chunk matches with similarity scores |
| Context assembly | Matched chunks | Formatted LLM prompt context |
| Generation | Prompt + context | Natural language answer + source list |
| Persistence | Answer + sources | `chat_messages` row |
