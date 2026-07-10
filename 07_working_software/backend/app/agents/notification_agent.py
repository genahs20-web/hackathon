"""Notification Agent: creates and tracks in-app notifications (FR-6.x)."""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import Notification


def create_notification(db: Session, customer_id: str, notification_type: str, message: str) -> Notification:
    """Persist a notification for a customer."""
    notification = Notification(
        notification_id=str(uuid.uuid4()),
        customer_id=customer_id,
        notification_type=notification_type,
        message=message,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def mark_read(db: Session, notification_id: str) -> None:
    """Mark a notification as read."""
    notification = db.get(Notification, notification_id)
    if notification is not None:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.commit()
