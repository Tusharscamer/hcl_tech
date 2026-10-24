import re
import math
import json
import urllib.request
from typing import List, Dict, Any
from langchain_core.embeddings import Embeddings
from ..config.settings import settings
from ..utils.logger import logger

class GeminiLangChainEmbeddings(Embeddings):
    """
    LangChain Embeddings implementation powered by Google Gemini
    (models/gemini-embedding-001).
    Produces 3072-dimensional semantic vectors compliant with LangChain VectorStore pipelines.
    """
    def __init__(self, model_name: str = "gemini-embedding-001"):
        self.model_name = model_name
        self.api_key = settings.GEMINI_API_KEY
        self.cache: Dict[str, List[float]] = {}
        self.vector_dim = 3072

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        LangChain Interface: Embeds a list of document strings.
        """
        results: List[List[float]] = []
        if not self.api_key:
            return [self._offline_fallback_vector(t) for t in texts]

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:batchEmbedContents?key={self.api_key}"
        batch_size = 10

        for i in range(0, len(texts), batch_size):
            chunk_slice = texts[i:i + batch_size]
            requests_payload = [
                {
                    "model": f"models/{self.model_name}",
                    "content": {"parts": [{"text": t[:2000]}]}
                }
                for t in chunk_slice
            ]

            payload = {"requests": requests_payload}
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    raw_embeddings = data.get("embeddings", [])
                    for idx, emb_obj in enumerate(raw_embeddings):
                        vec = emb_obj.get("values", [])
                        if vec:
                            self.cache[chunk_slice[idx].strip()] = vec
                            results.append(vec)
                        else:
                            results.append(self._offline_fallback_vector(chunk_slice[idx]))
                logger.info(f"[LangChain Embeddings] Embedded batch of {len(chunk_slice)} docs with {self.model_name} (dim: {self.vector_dim}).")
            except Exception as e:
                logger.warning(f"[LangChain Embeddings] Batch embed error ({e}). Using offline vectorizer.")
                for t in chunk_slice:
                    results.append(self._offline_fallback_vector(t))

        return results

    def embed_query(self, text: str) -> List[float]:
        """
        LangChain Interface: Embeds a single query string.
        """
        cleaned = text.strip()
        if not cleaned:
            return [0.0] * 128

        if cleaned in self.cache:
            return self.cache[cleaned]

        if self.api_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:embedContent?key={self.api_key}"
            payload = {
                "model": f"models/{self.model_name}",
                "content": {"parts": [{"text": cleaned[:2000]}]}
            }
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    vec = data.get("embedding", {}).get("values", [])
                    if vec:
                        self.cache[cleaned] = vec
                        return vec
            except Exception as e:
                logger.warning(f"[LangChain Embeddings] Single query embed error ({e}).")

        fallback = self._offline_fallback_vector(cleaned)
        self.cache[cleaned] = fallback
        return fallback

    # Backwards-compatible aliases
    def embed_text(self, text: str) -> List[float]:
        return self.embed_query(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return self.embed_documents(texts)

    def _offline_fallback_vector(self, text: str) -> List[float]:
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 2]
        dim = 128
        vec = [0.0] * dim
        if not tokens:
            return vec
        for t in tokens:
            idx = hash(t) % dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [round(x / norm, 5) for x in vec]
        return vec

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        if len(v1) != len(v2) or not v1:
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        return round(dot, 5)

embedding_engine = GeminiLangChainEmbeddings()
