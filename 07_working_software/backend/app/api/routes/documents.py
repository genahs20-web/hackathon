"""Document management endpoints (EPIC 1)."""

import json
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.schemas.document import DocumentListResponse, DocumentResponse, DocumentUploadResponse
from app.api.security import get_current_user
from app.database.models import Customer
from app.database.session import get_db
from app.middleware.audit import log_action
from app.services import document_service

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Annotated[str | None, Form()] = None,
    tags: Annotated[str | None, Form()] = None,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> DocumentUploadResponse:
    try:
        tag_list = json.loads(tags) if tags else []
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tags must be a valid JSON array") from exc
    document = await document_service.upload_document(db, current_user.customer_id, file, title, tag_list)
    background_tasks.add_task(document_service.index_document_task, document.document_id)

    return DocumentUploadResponse(
        success=True,
        document_id=document.document_id,
        file_name=document.file_name,
        file_type=document.file_type,
        status=document.status,
        message="Document uploaded. Indexing started.",
    )


@router.get("", response_model=DocumentListResponse)
def list_documents(
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> DocumentListResponse:
    documents = document_service.get_document_list(db, current_user.customer_id, status_filter)
    return DocumentListResponse(
        documents=[DocumentResponse.model_validate(d) for d in documents], total=len(documents)
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)
) -> DocumentResponse:
    document = document_service.get_document(db, document_id, current_user.customer_id)
    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}")
def delete_document(
    document_id: str, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)
) -> dict:
    document_service.delete_document(db, document_id, current_user.customer_id)
    return {"success": True, "message": "Document deleted"}


@router.post("/{document_id}/reindex")
def reindex_document(
    document_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> dict:
    document = document_service.get_document(db, document_id, current_user.customer_id)
    document.status = "processing"
    db.commit()
    background_tasks.add_task(document_service.index_document_task, document_id)
    log_action(db, current_user.customer_id, action="document.reindex", entity_type="document", entity_id=document_id)
    return {"success": True, "status": "processing"}
