import os
from typing import List, Dict, Any, Tuple, Optional
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from .loader import load_policy_documents
from .splitter import split_text_into_chunks
from .embeddings import embedding_engine, GeminiLangChainEmbeddings
from ..config.settings import settings
from ..utils.logger import logger

class ChromaBankingVectorStore:
    """
    LangChain Chroma VectorStore integration for Apex Bank Policy RAG.
    Stores and indexes neural embeddings in ChromaDB without writing files to local disk.
    Supports LangChain LCEL retriever pipelines and similarity search.
    """
    _instance = None

    def __init__(self):
        self.collection_name = "apex_daily_banking_policies"
        self.embedding = embedding_engine

        # Configure Chroma client (Ephemeral In-Memory without local disk persistence)
        # Supports remote Chroma server if CHROMA_HOST is set
        chroma_host = os.getenv("CHROMA_HOST")
        chroma_port = int(os.getenv("CHROMA_PORT", 8000))

        if chroma_host:
            logger.info(f"[ChromaDB] Connecting to remote Chroma Vector Database at {chroma_host}:{chroma_port}...")
            self.client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        else:
            logger.info("[ChromaDB] Initializing Chroma Vector Database Engine (Non-disk Ephemeral Client)...")
            self.client = chromadb.EphemeralClient()

        # Initialize LangChain Chroma VectorStore wrapper
        self.vector_store: Chroma = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding
        )

        self._initialize_store()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ChromaBankingVectorStore()
        return cls._instance

    def _initialize_store(self):
        """
        Loads PDF policies via LangChain Loader, splits via RecursiveCharacterTextSplitter,
        and indexes documents into Chroma VectorStore using Gemini embeddings.
        """
        logger.info("[ChromaDB] Ingesting policy documents through LangChain pipeline...")
        raw_docs: List[Document] = load_policy_documents()
        chunked_docs: List[Document] = split_text_into_chunks(raw_docs)

        if chunked_docs:
            self.vector_store.add_documents(chunked_docs)
            logger.info(f"[ChromaDB] Successfully indexed {len(chunked_docs)} Document chunks into Chroma VectorStore.")

    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Returns official LangChain VectorStoreRetriever.
        """
        kwargs = search_kwargs or {"k": 2}
        return self.vector_store.as_retriever(search_kwargs=kwargs)

    def similarity_search(self, query: str, k: int = 3, **kwargs) -> List[Document]:
        """
        LangChain similarity search.
        """
        return self.vector_store.similarity_search(query, k=k, **kwargs)

    def similarity_search_with_score(self, query: str, k: int = 3, **kwargs) -> List[Tuple[Document, float]]:
        """
        LangChain similarity search with distance score.
        """
        return self.vector_store.similarity_search_with_score(query, k=k, **kwargs)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """
        Backwards-compatible search method returning formatted metadata and content.
        """
        matches = self.vector_store.similarity_search_with_score(query, k=top_k)
        return [
            (
                {
                    "source": doc.metadata.get("source", "unknown"),
                    "text": doc.page_content,
                    "metadata": doc.metadata
                },
                float(score)
            )
            for doc, score in matches
        ]

# Global singleton instance
chroma_store = ChromaBankingVectorStore.get_instance()
vector_store = chroma_store
