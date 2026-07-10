"""Admin-only endpoints (EPIC 6)."""

import json

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.api.schemas.document import DocumentResponse
from app.api.schemas.user import UserResponse
from app.api.security import require_admin
from app.database.models import AuditLog, Customer, Document
from app.database.session import get_db
from app.services import document_service

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_all_users(db: Session = Depends(get_db), _: Customer = Depends(require_admin)) -> list[UserResponse]:
    return [UserResponse.model_validate(u) for u in db.query(Customer).all()]


@router.get("/documents", response_model=list[DocumentResponse])
def list_all_documents(
    db: Session = Depends(get_db), _: Customer = Depends(require_admin)
) -> list[DocumentResponse]:
    return [DocumentResponse.model_validate(d) for d in db.query(Document).all()]


@router.get("/audit-logs")
def get_audit_logs(
    action: str | None = None,
    customer_id: str | None = None,
    db: Session = Depends(get_db),
    _: Customer = Depends(require_admin),
) -> dict:
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if customer_id:
        query = query.filter(AuditLog.customer_id == customer_id)
    logs = query.order_by(AuditLog.created_at.desc()).all()

    return {
        "logs": [
            {
                "log_id": log.log_id,
                "customer_id": log.customer_id,
                "action": log.action,
                "entity_type": log.entity_type,
                "entity_id": log.entity_id,
                "details": json.loads(log.details) if log.details else None,
                "created_at": log.created_at,
            }
            for log in logs
        ]
    }


@router.post("/reindex-all")
def reindex_all(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: Customer = Depends(require_admin),
) -> dict:
    documents = db.query(Document).all()
    for document in documents:
        document.status = "processing"
    db.commit()

    for document in documents:
        background_tasks.add_task(document_service.index_document_task, document.document_id)

    return {"success": True, "documents_queued": len(documents)}
