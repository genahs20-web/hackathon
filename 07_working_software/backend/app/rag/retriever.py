"""Semantic retrieval against ChromaDB, scoped per-customer (BR-2)."""

from dataclasses import dataclass
from functools import lru_cache

import chromadb

from app.config.constants import RETRIEVAL_SIMILARITY_FLOOR, RETRIEVAL_TOP_K
from app.config.settings import get_settings
from app.rag.embedder import generate_embeddings

settings = get_settings()


@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    document_name: str
    snippet: str
    relevance_score: float


@lru_cache
def _get_client() -> chromadb.HttpClient:
    """Lazily construct the ChromaDB client on first use so importing this module
    (e.g. in unit tests) doesn't require a live ChromaDB connection."""
    return chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)


def _get_collection():
    return _get_client().get_or_create_collection(name=settings.chroma_collection_name)


def index_chunk(chunk_id: str, document_id: str, document_name: str, chunk_text: str, customer_id: str) -> str:
    """Embed and store a single chunk in ChromaDB. Returns the ChromaDB vector id."""
    collection = _get_collection()
    [embedding] = generate_embeddings([chunk_text])
    vector_id = f"chunk-{chunk_id}"
    collection.add(
        ids=[vector_id],
        embeddings=[embedding],
        documents=[chunk_text],
        metadatas=[{"document_id": document_id, "document_name": document_name, "customer_id": customer_id}],
    )
    return vector_id


def retrieve_relevant_chunks(query: str, customer_id: str, top_k: int = RETRIEVAL_TOP_K) -> list[RetrievalResult]:
    """Retrieve the top-K most relevant chunks for a query, scoped to the requesting customer."""
    collection = _get_collection()
    [query_embedding] = generate_embeddings([query])

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"customer_id": customer_id},
    )

    matches: list[RetrievalResult] = []
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for vector_id, doc_text, metadata, distance in zip(ids, documents, metadatas, distances):
        similarity = 1 - distance
        if similarity < RETRIEVAL_SIMILARITY_FLOOR:
            continue
        matches.append(
            RetrievalResult(
                chunk_id=vector_id.removeprefix("chunk-"),
                document_id=metadata["document_id"],
                document_name=metadata["document_name"],
                snippet=doc_text[:500],
                relevance_score=round(similarity, 4),
            )
        )

    return sorted(matches, key=lambda r: r.relevance_score, reverse=True)
