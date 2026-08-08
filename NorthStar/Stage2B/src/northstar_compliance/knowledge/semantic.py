from __future__ import annotations

from collections import Counter
import math
import numpy as np

from .schemas import KnowledgeChunk
from .tokenization import tokenize


class LatentSemanticIndex:
    """Deterministic local LSA: TF-IDF followed by truncated SVD."""
    def __init__(self, chunks: tuple[KnowledgeChunk, ...], dimensions: int = 8):
        self.chunks=chunks
        docs=[tokenize(c.text + " " + " ".join(c.heading_path) + " " + " ".join(c.business_domains)) for c in chunks]
        vocab=sorted({t for d in docs for t in d})
        self.vocab={t:i for i,t in enumerate(vocab)}
        n=len(docs)
        df=Counter()
        for d in docs:
            df.update(set(d))
        self.idf=np.array([math.log((1+n)/(1+df[t]))+1 for t in vocab],dtype=float)
        matrix=np.zeros((n,len(vocab)),dtype=float)
        for i,d in enumerate(docs):
            counts=Counter(d)
            if not d:
                continue
            for t,c in counts.items():
                matrix[i,self.vocab[t]]=(c/len(d))*self.idf[self.vocab[t]]
        self.dimensions=max(1,min(dimensions, min(matrix.shape) if matrix.size else 1))
        if n and len(vocab):
            _,_,vt=np.linalg.svd(matrix,full_matrices=False)
            self.components=vt[:self.dimensions].T
            vectors=matrix @ self.components
        else:
            self.components=np.zeros((len(vocab),self.dimensions))
            vectors=np.zeros((n,self.dimensions))
        self.doc_vectors=self._normalize(vectors)

    @staticmethod
    def _normalize(matrix: np.ndarray) -> np.ndarray:
        if matrix.size == 0:
            return matrix
        norms=np.linalg.norm(matrix,axis=1,keepdims=True)
        norms[norms==0]=1.0
        return matrix/norms

    def _query_vector(self, text: str) -> np.ndarray:
        tokens=tokenize(text)
        v=np.zeros((1,len(self.vocab)),dtype=float)
        counts=Counter(tokens)
        if tokens:
            for t,c in counts.items():
                idx=self.vocab.get(t)
                if idx is not None:
                    v[0,idx]=(c/len(tokens))*self.idf[idx]
        latent=v@self.components
        return self._normalize(latent)

    def score(self, query: str) -> list[tuple[KnowledgeChunk,float]]:
        q=self._query_vector(query)
        scores=(self.doc_vectors@q.T).reshape(-1) if len(self.chunks) else np.array([])
        results=[(chunk,float(score)) for chunk,score in zip(self.chunks,scores)]
        return sorted(results,key=lambda x:(-x[1],x[0].chunk_id))
