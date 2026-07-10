"""Conflict review endpoints (EPIC 3)."""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.conflict import ConflictResolveRequest, ConflictResponse
from app.api.security import get_current_user
from app.database.models import Conflict, Customer
from app.database.session import get_db
from app.middleware.audit import log_action

router = APIRouter(prefix="/api/conflicts", tags=["conflicts"])


def _to_response(conflict: Conflict) -> ConflictResponse:
    return ConflictResponse(
        conflict_id=conflict.conflict_id,
        conflict_description=conflict.conflict_description,
        source_documents=json.loads(conflict.source_documents),
        severity=conflict.severity,
        resolved=conflict.resolved,
        resolution_notes=conflict.resolution_notes,
        created_at=conflict.created_at,
    )


@router.get("", response_model=list[ConflictResponse])
def list_conflicts(
    severity: str | None = None,
    resolved: bool | None = None,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> list[ConflictResponse]:
    query = db.query(Conflict).filter(Conflict.customer_id == current_user.customer_id)
    if severity:
        query = query.filter(Conflict.severity == severity)
    if resolved is not None:
        query = query.filter(Conflict.resolved == resolved)
    return [_to_response(c) for c in query.order_by(Conflict.created_at.desc()).all()]


@router.post("/{conflict_id}/resolve", response_model=ConflictResponse)
def resolve_conflict(
    conflict_id: str,
    request: ConflictResolveRequest,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> ConflictResponse:
    conflict = db.get(Conflict, conflict_id)
    if conflict is None or conflict.customer_id != current_user.customer_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conflict not found")
    if conflict.resolved:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict already resolved")

    conflict.resolved = True
    conflict.resolution_notes = request.resolution_notes
    db.commit()
    log_action(db, current_user.customer_id, action="conflict.resolve", entity_type="conflict", entity_id=conflict_id)
    return _to_response(conflict)
