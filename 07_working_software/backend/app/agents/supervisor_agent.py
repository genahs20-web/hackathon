"""Supervisor Agent: orchestrates the retrieval -> conflict -> summary -> recommendation pipeline
using a LangGraph StateGraph (FR-5.x)."""

import logging
from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents import (
    conflict_detector_agent,
    knowledge_retriever_agent,
    recommendation_agent,
    summarization_agent,
)
from app.rag.retriever import RetrievalResult

logger = logging.getLogger(__name__)


class WorkflowState(TypedDict, total=False):
    query: str
    customer_id: str
    formatted_context: str
    retrieved_chunks: list[RetrievalResult]
    sources: list[dict]
    has_results: bool
    conflicts: list[dict]
    summary: str
    recommendation: dict


def _retrieve_node(state: WorkflowState) -> WorkflowState:
    result = knowledge_retriever_agent.retrieve(state["query"], state["customer_id"])
    return {
        "formatted_context": result.formatted_context,
        "has_results": result.has_results,
        "retrieved_chunks": result.chunks,
        "sources": [
            {
                "document_id": c.document_id,
                "document_name": c.document_name,
                "snippet": c.snippet,
                "relevance_score": c.relevance_score,
            }
            for c in result.chunks
        ],
    }


def _detect_conflicts_node(state: WorkflowState) -> WorkflowState:
    if not state.get("has_results"):
        return {"conflicts": []}
    return {"conflicts": conflict_detector_agent.detect_conflicts(state["retrieved_chunks"])}


def _summarize_node(state: WorkflowState) -> WorkflowState:
    if not state.get("has_results"):
        return {"summary": "No relevant documents were found for this question."}
    summary = summarization_agent.generate_summary(state["query"], state["formatted_context"])
    return {"summary": summary}


def _recommend_node(state: WorkflowState) -> WorkflowState:
    recommendation = recommendation_agent.generate_recommendation(state["summary"], state.get("conflicts"))
    return {"recommendation": recommendation}


def _build_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("retrieve", _retrieve_node)
    graph.add_node("detect_conflicts", _detect_conflicts_node)
    graph.add_node("summarize", _summarize_node)
    graph.add_node("recommend", _recommend_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "detect_conflicts")
    graph.add_edge("detect_conflicts", "summarize")
    graph.add_edge("summarize", "recommend")
    graph.add_edge("recommend", END)

    return graph.compile()


_compiled_graph = _build_graph()


def run_query(query: str, customer_id: str) -> WorkflowState:
    """Run the full agent workflow for a user query and return the aggregated state."""
    try:
        return _compiled_graph.invoke({"query": query, "customer_id": customer_id})
    except Exception:
        logger.exception("Supervisor Agent: workflow failed for customer_id=%s", customer_id)
        return {
            "summary": "Something went wrong while processing your request. Please try again.",
            "sources": [],
            "conflicts": [],
            "recommendation": {"recommendation_text": "", "confidence_score": 0.0},
        }
