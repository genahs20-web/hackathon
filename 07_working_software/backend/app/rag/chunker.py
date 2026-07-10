"""Splits extracted document text into overlapping chunks for embedding."""

import tiktoken

from app.config.constants import CHUNK_OVERLAP_TOKENS, CHUNK_SIZE_TOKENS

_encoding = tiktoken.get_encoding("cl100k_base")


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE_TOKENS, overlap: int = CHUNK_OVERLAP_TOKENS
) -> list[str]:
    """Split text into token-bounded chunks with overlap between consecutive chunks."""
    if not text.strip():
        return []

    tokens = _encoding.encode(text)
    chunks: list[str] = []
    start = 0

    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(_encoding.decode(tokens[start:end]))
        if end == len(tokens):
            break
        start = end - overlap

    return chunks
