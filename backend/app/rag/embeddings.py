import re
import math
import time
import json
import urllib.request
from typing import List, Dict, Any
from langchain_core.embeddings import Embeddings
from ..config.settings import settings
from ..utils.logger import logger

class GeminiLangChainEmbeddings(Embeddings):
    """
    LangChain Embeddings implementation powered by Google Gemini (models/gemini-embedding-001).
    Produces consistent 3072-dimensional semantic vectors compliant with ChromaDB & LangChain.
    Includes automatic rate-limit backoff and guaranteed dimensional consistency.
    """
    def __init__(self, model_name: str = "gemini-embedding-001"):
        self.model_name = model_name
        self.api_key = settings.GEMINI_API_KEY
        self.cache: Dict[str, List[float]] = {}
        self.vector_dim = 3072

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        LangChain Interface: Embeds a list of document strings with rate-limiting & retries.
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
            batch_success = False

            # Try up to 3 times with exponential backoff on 429
            for attempt in range(3):
                try:
                    req = urllib.request.Request(
                        url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        raw_embeddings = data.get("embeddings", [])
                        for idx, emb_obj in enumerate(raw_embeddings):
                            vec = emb_obj.get("values", [])
                            if vec and len(vec) == self.vector_dim:
                                self.cache[chunk_slice[idx].strip()] = vec
                                results.append(vec)
                            else:
                                results.append(self._offline_fallback_vector(chunk_slice[idx]))
                    batch_success = True
                    logger.info(f"[LangChain Embeddings] Embedded batch {i // batch_size + 1} ({len(chunk_slice)} docs) via {self.model_name} (dim: {self.vector_dim}).")
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt < 2:
                        wait_sec = (attempt + 1) * 2.5
                        logger.warning(f"[LangChain Embeddings] Rate limit (429) hit. Backing off for {wait_sec}s...")
                        time.sleep(wait_sec)
                    else:
                        logger.warning(f"[LangChain Embeddings] Batch embed error ({e}).")
                        break
                except Exception as e:
                    logger.warning(f"[LangChain Embeddings] Request error: {e}")
                    break

            if not batch_success:
                logger.warning(f"[LangChain Embeddings] Generating {self.vector_dim}-dim fallback vectors for batch.")
                for t in chunk_slice:
                    results.append(self._offline_fallback_vector(t))

            # Polite spacing between batches
            time.sleep(0.4)

        return results

    def embed_query(self, text: str) -> List[float]:
        """
        LangChain Interface: Embeds a single query string.
        """
        cleaned = text.strip()
        if not cleaned:
            return [0.0] * self.vector_dim

        if cleaned in self.cache:
            return self.cache[cleaned]

        if self.api_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:embedContent?key={self.api_key}"
            payload = {
                "model": f"models/{self.model_name}",
                "content": {"parts": [{"text": cleaned[:2000]}]}
            }
            for attempt in range(2):
                try:
                    req = urllib.request.Request(
                        url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        vec = data.get("embedding", {}).get("values", [])
                        if vec and len(vec) == self.vector_dim:
                            self.cache[cleaned] = vec
                            return vec
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt == 0:
                        time.sleep(1.5)
                    else:
                        break
                except Exception:
                    break

        fallback = self._offline_fallback_vector(cleaned)
        self.cache[cleaned] = fallback
        return fallback

    def _offline_fallback_vector(self, text: str) -> List[float]:
        """
        Guarantees deterministic vector with EXACT self.vector_dim (3072) length for Chroma compatibility.
        """
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 2]
        dim = self.vector_dim
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
