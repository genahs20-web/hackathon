"""Recommendation Agent: generates actionable recommendations with confidence scores (FR-4.2, BR-3)."""

import json
import logging

from app.agents.llm_client import LLMUnavailableError, complete

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a recommendation assistant for business decision makers. Given a summary of findings "
    "and any detected conflicts, suggest ONE concrete, actionable next step. Respond as JSON: "
    "{\"recommendation_text\": str, \"confidence_score\": float (0.0-1.0)}. Confidence should reflect "
    "how strongly the provided context supports the recommendation."
)


def generate_recommendation(summary: str, conflicts: list[dict] | None = None) -> dict:
    """Generate a recommendation with a mandatory confidence score (BR-3)."""
    conflict_note = f"\n\nDetected conflicts: {json.dumps(conflicts)}" if conflicts else ""
    user_prompt = f"Summary: {summary}{conflict_note}"

    try:
        raw_response = complete(SYSTEM_PROMPT, user_prompt)
        parsed = json.loads(raw_response)
    except (LLMUnavailableError, json.JSONDecodeError):
        logger.error("Recommendation Agent: generation failed, returning fallback")
        return {"recommendation_text": "Unable to generate a recommendation at this time.", "confidence_score": 0.0}

    parsed["confidence_score"] = max(0.0, min(1.0, float(parsed.get("confidence_score", 0.0))))
    return parsed
