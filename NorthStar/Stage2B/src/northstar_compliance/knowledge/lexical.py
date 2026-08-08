from __future__ import annotations

from collections import Counter
import math

from .schemas import KnowledgeChunk
from .tokenization import tokenize


class BM25Index:
    def __init__(self, chunks: tuple[KnowledgeChunk, ...], k1: float = 1.5, b: float = 0.75):
        self.chunks=chunks
        self.k1=k1
        self.b=b
        self.tokens=[tokenize(c.text + " " + " ".join(c.heading_path)) for c in chunks]
        self.term_counts=[Counter(x) for x in self.tokens]
        self.doc_lengths=[len(x) for x in self.tokens]
        self.avgdl=sum(self.doc_lengths)/len(self.doc_lengths) if self.doc_lengths else 0.0
        df=Counter()
        for terms in self.term_counts:
            df.update(terms.keys())
        self.df=df
        self.n=len(chunks)

    def score(self, query: str) -> list[tuple[KnowledgeChunk,float]]:
        qterms=tokenize(query)
        results=[]
        for chunk, counts, dl in zip(self.chunks, self.term_counts, self.doc_lengths):
            score=0.0
            for term in qterms:
                freq=counts.get(term,0)
                if not freq:
                    continue
                n_q=self.df.get(term,0)
                idf=math.log(1 + (self.n - n_q + 0.5)/(n_q + 0.5))
                denom=freq + self.k1*(1-self.b + self.b*(dl/self.avgdl if self.avgdl else 0.0))
                score += idf * (freq*(self.k1+1))/denom
            results.append((chunk,score))
        return sorted(results, key=lambda x:(-x[1],x[0].chunk_id))
