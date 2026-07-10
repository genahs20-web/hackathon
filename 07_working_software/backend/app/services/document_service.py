"""Document lifecycle service: upload, index, delete, list (EPIC 1)."""

import json
import logging
import os
import uuid
from datetime import datetime

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.agents import document_analyzer_agent, notification_agent
from app.config.constants import ALLOWED_FILE_EXTENSIONS, MAX_DOCUMENTS_PER_USER, MAX_FILE_SIZE_BYTES
from app.config.settings import get_settings
from app.database.models import Document, DocumentChunk, Embedding
from app.database.session import SessionLocal
from app.middleware.audit import log_action
from app.rag.chunker import chunk_text
from app.rag.loaders import extract_text
from app.rag.retriever import index_chunk

logger = logging.getLogger(__name__)
settings = get_settings()


def _validate_upload(file: UploadFile, file_size: int) -> str:
    extension = os.path.splitext(file.filename or "")[1].lower()
    if extension not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format")
    if not (0 < file_size <= MAX_FILE_SIZE_BYTES):
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")
    return extension.lstrip(".")


async def upload_document(
    db: Session, customer_id: str, file: UploadFile, title: str | None, tags: list[str]
) -> Document:
    """Validate, store, and register a new document, then kick off background indexing (FR-1.1)."""
    existing_count = db.query(Document).filter(Document.customer_id == customer_id).count()
    if existing_count >= MAX_DOCUMENTS_PER_USER:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document limit reached")

    contents = await file.read()
    file_type = _validate_upload(file, len(contents))

    os.makedirs(settings.storage_path, exist_ok=True)
    document_id = str(uuid.uuid4())
    stored_path = os.path.join(settings.storage_path, f"{document_id}.{file_type}")
    with open(stored_path, "wb") as f:
        f.write(contents)

    document = Document(
        document_id=document_id,
        customer_id=customer_id,
        file_name=file.filename or f"document.{file_type}",
        file_path=stored_path,
        file_size=len(contents),
        file_type=file_type,
        status="uploaded",
        doc_metadata=json.dumps({"title": title, "tags": tags}),
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    log_action(db, customer_id, action="document.upload", entity_type="document", entity_id=document_id)
    return document


def index_document_task(document_id: str) -> None:
    """Background-task entry point: opens its own DB session since the request session
    is closed before a BackgroundTask runs."""
    db = SessionLocal()
    try:
        index_document(db, document_id)
    finally:
        db.close()


def index_document(db: Session, document_id: str) -> Document:
    """Run the extraction -> chunk -> embed -> store pipeline for a document (FR-1.2)."""
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    document.status = "processing"
    db.commit()

    try:
        text = extract_text(document.file_path, document.file_type)
        document_analyzer_agent.analyze_document(text)  # entity/type extraction (FR-1.4)
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            chunk_row = DocumentChunk(
                document_id=document.document_id, chunk_text=chunk, chunk_index=index
            )
            db.add(chunk_row)
            db.flush()

            vector_id = index_chunk(chunk_row.chunk_id, document.document_id, document.file_name, chunk, document.customer_id)
            db.add(Embedding(chunk_id=chunk_row.chunk_id, chroma_vector_id=vector_id))

        document.status = "indexed"
        document.indexed_date = datetime.utcnow()
        document.total_chunks = len(chunks)
        db.commit()

        notification_agent.create_notification(
            db, document.customer_id, "document_indexed", f"'{document.file_name}' is ready to query."
        )
    except Exception:
        logger.exception("Indexing failed for document_id=%s", document_id)
        document.status = "failed"
        db.commit()

    return document


def get_document_list(db: Session, customer_id: str, status_filter: str | None = None) -> list[Document]:
    """List documents owned by the customer (BR-2), optionally filtered by status."""
    query = db.query(Document).filter(Document.customer_id == customer_id)
    if status_filter:
        query = query.filter(Document.status == status_filter)
    return query.order_by(Document.upload_date.desc()).all()


def get_document(db: Session, document_id: str, customer_id: str) -> Document:
    """Fetch a single document, enforcing ownership (BR-2)."""
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if document.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the document owner")
    return document


def delete_document(db: Session, document_id: str, customer_id: str) -> None:
    """Delete a document and its cascaded chunks/embeddings (FR-1.x)."""
    document = get_document(db, document_id, customer_id)
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    db.delete(document)
    db.commit()
    log_action(db, customer_id, action="document.delete", entity_type="document", entity_id=document_id)
