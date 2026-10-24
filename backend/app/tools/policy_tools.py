from typing import Dict, Any, List
from ..rag.retriever import retrieve_policy_context
from ..utils.logger import logger

def retrieve_policy_tool(query: str, top_k: int = 2) -> Dict[str, Any]:
    """
    RAG Tool: Retrieves relevant clauses, limits, FAQs, and regulatory rules
    from official Apex Bank policy PDFs (banking_faq.pdf, card_policy.pdf, 
    loan_policy.pdf, payment_policy.pdf) using vector similarity search.
    """
    logger.info(f"[PolicyTool] Executing RAG semantic retrieval for query: '{query}' (top_k={top_k})")
    rag_result = retrieve_policy_context(query, top_k=top_k)
    return {
        "tool": "retrieve_policy_tool",
        "query": query,
        "passages": rag_result.get("passages", []),
        "sources": rag_result.get("sources", []),
        "context_text": rag_result.get("context_text", "")
    }

def get_faq_answer(topic: str) -> Dict[str, Any]:
    """
    RAG Tool: Queries the banking FAQ policy document for verified guidelines.
    """
    return retrieve_policy_tool(f"FAQ guidelines on {topic}", top_k=2)

def search_card_policy(query: str) -> Dict[str, Any]:
    """
    RAG Tool: Searches card replacement, dispute, and international limit policies.
    """
    return retrieve_policy_tool(f"card policy {query}", top_k=2)
