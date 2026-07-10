"""Pydantic schemas for conflict detection endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class ConflictResponse(BaseModel):
    conflict_id: str
    conflict_description: str
    source_documents: list[str]
    severity: str
    resolved: bool
    resolution_notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConflictResolveRequest(BaseModel):
    resolution_notes: str = Field(min_length=1, max_length=2000)


class ConflictListResponse(BaseModel):
    conflicts: list[ConflictResponse]
