"""Audit logging helper, invoked by services on every mutating action (BR-4)."""

import json
import uuid

from sqlalchemy.orm import Session

from app.database.models import AuditLog


def log_action(
    db: Session,
    customer_id: str | None,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    details: dict | None = None,
    ip_address: str | None = None,
) -> None:
    """Write an immutable audit log entry for a mutating action."""
    entry = AuditLog(
        log_id=str(uuid.uuid4()),
        customer_id=customer_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=json.dumps(details) if details else None,
        ip_address=ip_address,
    )
    db.add(entry)
    db.commit()
