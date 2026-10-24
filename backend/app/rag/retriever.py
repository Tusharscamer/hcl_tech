from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from .vector_store import vector_store
from ..utils.logger import logger

def format_docs(docs: List[Document]) -> str:
    """
    LangChain pipeline helper: Formats retrieved Document objects into a clean prompt context string.
    """
    formatted_chunks = []
    for d in docs:
        src = d.metadata.get("source", "Policy Document")
        formatted_chunks.append(f"[{src}]: {d.page_content.strip()}")
    return "\n\n---\n\n".join(formatted_chunks)

def create_langchain_rag_chain():
    """
    Constructs a LangChain LCEL (LangChain Expression Language) pipeline:
    Query -> LangChain VectorStoreRetriever -> Document Formatter
    """
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    rag_pipeline = (
        {"query": RunnablePassthrough()}
        | RunnableLambda(lambda x: base_retriever.invoke(x["query"]))
        | RunnableLambda(format_docs)
    )
    return rag_pipeline

# Pre-compiled LangChain RAG pipeline
langchain_rag_pipeline = create_langchain_rag_chain()

def retrieve_policy_context(query: str, top_k: int = 2) -> Dict[str, Any]:
    """
    LangChain RAG Pipeline execution:
    Executes semantic similarity search on LangChain VectorStore,
    returning structured passage metadata and formatted context text.
    """
    logger.info(f"[LangChain RAG Pipeline] Executing retrieval for: '{query}'")
    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
    matched_docs: List[Document] = retriever.invoke(query)

    passages = []
    sources = set()

    for doc in matched_docs:
        src = doc.metadata.get("source", "unknown")
        passages.append({
            "source": src,
            "text": doc.page_content,
            "metadata": doc.metadata
        })
        sources.add(src)

    context_text = format_docs(matched_docs)

    return {
        "passages": passages,
        "sources": list(sources),
        "context_text": context_text,
        "total_matches": len(matched_docs),
        "pipeline": "LangChain LCEL VectorStoreRetriever"
    }
