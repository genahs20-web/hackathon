"""Shared LLM chat-completion helper with retry/backoff for all agents (E004)."""

import logging
import time

import httpx
from openai import APIError, AzureOpenAI, OpenAI, RateLimitError

from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

MAX_RETRIES = 3
BASE_BACKOFF_SECONDS = 1.0


class LLMUnavailableError(Exception):
    """Raised when the LLM provider fails after all retry attempts (maps to E004)."""


def _get_client() -> OpenAI | AzureOpenAI:
    if settings.use_azure_openai:
        return AzureOpenAI(
            api_key=settings.openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )
    http_client = httpx.Client(verify=settings.openai_verify_ssl)
    return OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url or None,
        http_client=http_client,
    )


def complete(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Call the chat completion API with exponential-backoff retry, raising LLMUnavailableError on exhaustion."""
    client = _get_client()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=settings.openai_chat_model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content or ""
        except (RateLimitError, APIError) as exc:
            logger.warning("LLM call failed (attempt %d/%d): %s", attempt, MAX_RETRIES, exc)
            if attempt == MAX_RETRIES:
                raise LLMUnavailableError("LLM service unavailable after retries") from exc
            time.sleep(BASE_BACKOFF_SECONDS * (2 ** (attempt - 1)))

    raise LLMUnavailableError("LLM service unavailable after retries")
