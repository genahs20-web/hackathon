"""Conflict Detector Agent: identifies contradictions across retrieved chunks (FR-3.x, BR-5)."""

import json
import logging

from app.agents.llm_client import LLMUnavailableError, complete
from app.config.constants import CONFLICT_CONFIDENCE_THRESHOLD, CONFLICT_MIN_DOCUMENTS
from app.rag.retriever import RetrievalResult

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a conflict detection assistant. Given excerpts from multiple enterprise documents, "
    "identify any factual contradictions between them. For each contradiction found, provide: "
    "description, severity (low|medium|high), confidence (0.0-1.0), and the source document names "
    "involved. Respond as JSON: {\"conflicts\": [{\"description\": str, \"severity\": str, "
    "\"confidence\": float, \"source_documents\": [str]}]}. If no contradictions exist, return "
    "{\"conflicts\": []}."
)


def detect_conflicts(chunks: list[RetrievalResult]) -> list[dict]:
    """Detect contradictions across chunks from 3+ distinct documents. Below-threshold results are dropped (BR-5)."""
    distinct_documents = {c.document_id for c in chunks}
    if len(distinct_documents) < CONFLICT_MIN_DOCUMENTS:
        return []

    excerpt_block = "\n\n".join(f"[{c.document_name}]\n{c.snippet}" for c in chunks)

    try:
        raw_response = complete(SYSTEM_PROMPT, excerpt_block)
        parsed = json.loads(raw_response)
    except (LLMUnavailableError, json.JSONDecodeError):
        logger.error("Conflict Detector Agent: analysis failed, returning no conflicts")
        return []

    conflicts = parsed.get("conflicts", [])
    return [c for c in conflicts if c.get("confidence", 0) >= CONFLICT_CONFIDENCE_THRESHOLD]
