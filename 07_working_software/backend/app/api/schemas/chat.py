"""Pydantic schemas for chat and conversation endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    document_id: str
    document_name: str
    snippet: str
    relevance_score: float


class ChatRequest(BaseModel):
    conversation_id: str
    message: str = Field(min_length=1, max_length=2000)
    context_documents: list[str] | None = None


class ChatResponse(BaseModel):
    message_id: str
    response: str
    sources: list[SourceCitation]
    confidence: float
    processing_time_ms: int


class ConversationCreateRequest(BaseModel):
    title: str | None = None


class ConversationResponse(BaseModel):
    conversation_id: str
    title: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    message_id: str
    sender_type: str
    message_text: str
    sources: list[SourceCitation] | None
    confidence_score: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    conversation_id: str
    title: str
    messages: list[ChatMessageResponse]
