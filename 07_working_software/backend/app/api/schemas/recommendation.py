"""Pydantic schemas for recommendation endpoints."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RecommendationResponse(BaseModel):
    recommendation_id: str
    recommendation_text: str
    confidence_score: float
    supporting_documents: list[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationPatchRequest(BaseModel):
    status: Literal["approved", "rejected"]
    notes: str | None = Field(default=None, max_length=500)


class RecommendationListResponse(BaseModel):
    recommendations: list[RecommendationResponse]
