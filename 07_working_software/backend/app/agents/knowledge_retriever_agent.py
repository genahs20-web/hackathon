"""Knowledge Retriever Agent: retrieves and formats relevant chunks with citations (FR-2.x)."""

from dataclasses import dataclass

from app.rag.retriever import RetrievalResult, retrieve_relevant_chunks


@dataclass
class RetrievedContext:
    chunks: list[RetrievalResult]
    formatted_context: str
    has_results: bool


def retrieve(query: str, customer_id: str) -> RetrievedContext:
    """Retrieve top-K chunks for a query and format them into an LLM-ready context block."""
    chunks = retrieve_relevant_chunks(query, customer_id)

    if not chunks:
        return RetrievedContext(chunks=[], formatted_context="", has_results=False)

    formatted = "\n\n".join(
        f"[Source: {c.document_name}, relevance={c.relevance_score}]\n{c.snippet}" for c in chunks
    )
    return RetrievedContext(chunks=chunks, formatted_context=formatted, has_results=True)
