from __future__ import annotations

class SentenceTransformerAdapter:
    """Optional production-oriented adapter; not exercised in offline acceptance."""
    def __init__(self, embedding_model: str, reranker_model: str | None = None):
        try:
            from sentence_transformers import CrossEncoder, SentenceTransformer
        except ImportError as exc:
            raise RuntimeError("install the semantic-transformer extra") from exc
        self.encoder=SentenceTransformer(embedding_model)
        self.reranker=CrossEncoder(reranker_model) if reranker_model else None

    def encode(self, texts: list[str]):
        return self.encoder.encode(texts,normalize_embeddings=True)

    def rerank(self, query: str, texts: list[str]):
        if self.reranker is None:
            raise RuntimeError("reranker model not configured")
        return self.reranker.predict([(query,text) for text in texts])
