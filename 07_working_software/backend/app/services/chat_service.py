"""Conversation and chat message service (EPIC 5)."""

import json
import time
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.agents.supervisor_agent import run_query
from app.database.models import ChatMessage, Conflict, ConversationHistory, Recommendation
from app.rag.prompt_injection_filter import detect_injection


def create_conversation(db: Session, customer_id: str, title: str | None) -> ConversationHistory:
    """Create a new conversation for a customer (FR-5.x)."""
    conversation = ConversationHistory(
        conversation_id=str(uuid.uuid4()), customer_id=customer_id, title=title or "New Conversation"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: str, customer_id: str) -> ConversationHistory:
    conversation = db.get(ConversationHistory, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    if conversation.customer_id != customer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not the conversation owner")
    return conversation


def list_conversations(db: Session, customer_id: str) -> list[ConversationHistory]:
    return (
        db.query(ConversationHistory)
        .filter(ConversationHistory.customer_id == customer_id, ConversationHistory.is_archived.is_(False))
        .order_by(ConversationHistory.updated_at.desc())
        .limit(10)
        .all()
    )


def archive_conversation(db: Session, conversation_id: str, customer_id: str) -> None:
    conversation = get_conversation(db, conversation_id, customer_id)
    conversation.is_archived = True
    db.commit()


def save_message(
    db: Session, conversation_id: str, sender_type: str, text: str, sources: list[dict] | None = None,
    confidence_score: float | None = None,
) -> ChatMessage:
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        sender_type=sender_type,
        message_text=text,
        sources=json.dumps(sources) if sources else None,
        confidence_score=confidence_score,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_conversation_history(db: Session, conversation_id: str, customer_id: str) -> list[ChatMessage]:
    conversation = get_conversation(db, conversation_id, customer_id)
    return conversation.messages


def send_message(db: Session, customer_id: str, conversation_id: str, message_text: str) -> dict:
    """Validate, run the agent workflow, and persist both sides of the exchange (FR-5.1/2, VR-2.x)."""
    get_conversation(db, conversation_id, customer_id)  # ownership check

    if detect_injection(message_text):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message could not be processed")

    save_message(db, conversation_id, "user", message_text)

    start = time.perf_counter()
    result = run_query(message_text, customer_id)
    elapsed_ms = int((time.perf_counter() - start) * 1000)

    sources = result.get("sources", [])
    summary = result.get("summary", "")
    confidence = float(result.get("recommendation", {}).get("confidence_score", 0.0))

    assistant_message = save_message(db, conversation_id, "assistant", summary, sources, confidence)

    _persist_conflicts(db, customer_id, conversation_id, result.get("conflicts", []))
    _persist_recommendation(db, customer_id, conversation_id, result.get("recommendation", {}))

    return {
        "message_id": assistant_message.message_id,
        "response": summary,
        "sources": sources,
        "confidence": confidence,
        "processing_time_ms": elapsed_ms,
    }


def _persist_conflicts(db: Session, customer_id: str, conversation_id: str, conflicts: list[dict]) -> None:
    for conflict in conflicts:
        db.add(
            Conflict(
                conflict_id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                customer_id=customer_id,
                conflict_description=conflict.get("description", ""),
                source_documents=json.dumps(conflict.get("source_documents", [])),
                severity=conflict.get("severity", "medium"),
            )
        )
    if conflicts:
        db.commit()


def _persist_recommendation(db: Session, customer_id: str, conversation_id: str, recommendation: dict) -> None:
    if not recommendation.get("recommendation_text"):
        return
    db.add(
        Recommendation(
            recommendation_id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            customer_id=customer_id,
            recommendation_text=recommendation["recommendation_text"],
            confidence_score=recommendation.get("confidence_score", 0.0),
        )
    )
    db.commit()
