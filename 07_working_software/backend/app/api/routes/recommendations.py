"""Recommendation review endpoints (EPIC 4)."""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.recommendation import RecommendationPatchRequest, RecommendationResponse
from app.api.security import get_current_user
from app.database.models import Customer, Recommendation
from app.database.session import get_db
from app.middleware.audit import log_action

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


def _to_response(recommendation: Recommendation) -> RecommendationResponse:
    return RecommendationResponse(
        recommendation_id=recommendation.recommendation_id,
        recommendation_text=recommendation.recommendation_text,
        confidence_score=float(recommendation.confidence_score),
        supporting_documents=json.loads(recommendation.supporting_documents or "[]"),
        status=recommendation.status,
        created_at=recommendation.created_at,
    )


@router.get("", response_model=list[RecommendationResponse])
def list_recommendations(
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> list[RecommendationResponse]:
    query = db.query(Recommendation).filter(Recommendation.customer_id == current_user.customer_id)
    if status_filter:
        query = query.filter(Recommendation.status == status_filter)
    return [_to_response(r) for r in query.order_by(Recommendation.created_at.desc()).all()]


@router.patch("/{recommendation_id}", response_model=RecommendationResponse)
def patch_recommendation(
    recommendation_id: str,
    request: RecommendationPatchRequest,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> RecommendationResponse:
    recommendation = db.get(Recommendation, recommendation_id)
    if recommendation is None or recommendation.customer_id != current_user.customer_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if request.status == "rejected" and not request.notes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A rejection reason is required")

    recommendation.status = request.status
    db.commit()
    log_action(
        db,
        current_user.customer_id,
        action=f"recommendation.{request.status}",
        entity_type="recommendation",
        entity_id=recommendation_id,
        details={"notes": request.notes} if request.notes else None,
    )
    return _to_response(recommendation)
