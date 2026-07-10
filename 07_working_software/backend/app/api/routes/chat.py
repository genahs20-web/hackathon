"""Chat and conversation endpoints (EPIC 5)."""

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationCreateRequest,
    ConversationDetailResponse,
    ConversationResponse,
)
from app.api.security import get_current_user
from app.database.models import Customer
from app.database.session import get_db
from app.services import chat_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def send_chat_message(
    request: ChatRequest, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)
) -> ChatResponse:
    result = chat_service.send_message(db, current_user.customer_id, request.conversation_id, request.message)
    return ChatResponse(**result)


@router.get("/conversations", response_model=list[ConversationResponse])
def list_conversations(
    db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)
) -> list[ConversationResponse]:
    conversations = chat_service.list_conversations(db, current_user.customer_id)
    return [ConversationResponse.model_validate(c) for c in conversations]


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> ConversationResponse:
    conversation = chat_service.create_conversation(db, current_user.customer_id, request.title)
    return ConversationResponse.model_validate(conversation)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation_detail(
    conversation_id: str, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)
) -> ConversationDetailResponse:
    conversation = chat_service.get_conversation(db, conversation_id, current_user.customer_id)
    messages = chat_service.get_conversation_history(db, conversation_id, current_user.customer_id)
    return ConversationDetailResponse(
        conversation_id=conversation.conversation_id,
        title=conversation.title,
        messages=[
            {
                "message_id": m.message_id,
                "sender_type": m.sender_type,
                "message_text": m.message_text,
                "sources": json.loads(m.sources) if m.sources else None,
                "confidence_score": m.confidence_score,
                "created_at": m.created_at,
            }
            for m in messages
        ],
    )


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)
) -> dict:
    chat_service.archive_conversation(db, conversation_id, current_user.customer_id)
    return {"success": True}
