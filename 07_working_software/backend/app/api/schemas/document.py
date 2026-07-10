"""Pydantic schemas for document upload and management."""

from datetime import datetime

from pydantic import BaseModel, Field


class DocumentMetadataRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    tags: list[str] = Field(default_factory=list, max_length=10)
    category: str | None = None


class DocumentUploadResponse(BaseModel):
    success: bool
    document_id: str
    file_name: str
    file_type: str
    status: str
    message: str


class DocumentResponse(BaseModel):
    document_id: str
    customer_id: str
    file_name: str
    file_size: int
    file_type: str
    status: str
    upload_date: datetime
    indexed_date: datetime | None
    total_chunks: int

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
