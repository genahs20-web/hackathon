"""Summarization Agent: produces concise, cited summaries (FR-4.1, FR-4.4)."""

import logging

from app.agents.llm_client import LLMUnavailableError, complete

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a summarization assistant for business analysts. Given a user's question and a set "
    "of retrieved document excerpts, write a concise 3-4 sentence answer. Every factual claim must "
    "be traceable to the provided excerpts; do not invent information not present in the context. "
    "If the context is insufficient to answer, say so plainly."
)

EXECUTIVE_SYSTEM_PROMPT = (
    "You are an executive briefing assistant. Given retrieved document excerpts, write a concise "
    "executive summary (3-4 sentences) suitable for a senior decision maker: lead with the key "
    "finding, then supporting detail, in plain business language."
)


def generate_summary(question: str, context: str) -> str:
    """Generate a concise, context-grounded answer to the user's question."""
    user_prompt = f"Question: {question}\n\nContext:\n{context}"
    try:
        return complete(SYSTEM_PROMPT, user_prompt)
    except LLMUnavailableError:
        logger.error("Summarization Agent: LLM unavailable")
        return "The AI service is temporarily unavailable. Please try again shortly."


def generate_executive_summary(context: str) -> str:
    """Generate an executive-level summary of the given context (FR-4.4)."""
    try:
        return complete(EXECUTIVE_SYSTEM_PROMPT, context)
    except LLMUnavailableError:
        logger.error("Summarization Agent: LLM unavailable for executive summary")
        return "The AI service is temporarily unavailable. Please try again shortly."
