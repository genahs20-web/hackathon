"""Document Analyzer Agent: extracts entities, document type, and structure from a new upload."""

import json
import logging

from app.agents.llm_client import LLMUnavailableError, complete

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a document analysis assistant. Given an excerpt of an enterprise document, "
    "identify: (1) the likely document type (policy, report, meeting notes, presentation, "
    "contract, or other), (2) up to 8 key entities or topics mentioned, and (3) a one-sentence "
    "structural summary. Respond as JSON with keys: document_type, key_entities, structure_summary."
)


def analyze_document(document_text: str) -> dict:
    """Run entity/type extraction over the first ~3000 characters of a document's text."""
    excerpt = document_text[:3000]
    try:
        raw_response = complete(SYSTEM_PROMPT, excerpt)
        return json.loads(raw_response)
    except LLMUnavailableError:
        logger.error("Document Analyzer Agent: LLM unavailable, returning fallback analysis")
        return {"document_type": "unknown", "key_entities": [], "structure_summary": ""}
    except json.JSONDecodeError:
        logger.error("Document Analyzer Agent: could not parse LLM response as JSON")
        return {"document_type": "unknown", "key_entities": [], "structure_summary": ""}
