"""Generates text embeddings via OpenAI/Azure OpenAI."""

import httpx
from openai import AzureOpenAI, OpenAI

from app.config.settings import get_settings

settings = get_settings()


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


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate an embedding vector for each input text, batched in a single API call."""
    if not texts:
        return []

    client = _get_client()
    response = client.embeddings.create(model=settings.openai_embedding_model, input=texts)
    return [item.embedding for item in response.data]
