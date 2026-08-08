from __future__ import annotations

from dataclasses import replace

from .schemas import RetrievalCandidate


def reciprocal_rank_fusion(
    lexical: list[tuple[object,float]],
    semantic: list[tuple[object,float]],
    lexical_k: int,
    semantic_k: int,
    rrf_k: int = 60,
    lexical_weight: float = 1.0,
    semantic_weight: float = 1.0,
) -> list[RetrievalCandidate]:
    by_id={}
    for rank,(chunk,score) in enumerate(lexical[:lexical_k],start=1):
        by_id[chunk.chunk_id]=RetrievalCandidate(
            chunk=chunk, lexical_rank=rank, lexical_score=score,
            fused_score=lexical_weight/(rrf_k+rank),
            reasons=("lexical_candidate",),
        )
    for rank,(chunk,score) in enumerate(semantic[:semantic_k],start=1):
        current=by_id.get(chunk.chunk_id)
        contribution=semantic_weight/(rrf_k+rank)
        if current:
            by_id[chunk.chunk_id]=replace(
                current,
                semantic_rank=rank,
                semantic_score=score,
                fused_score=current.fused_score+contribution,
                reasons=current.reasons+("semantic_candidate",),
            )
        else:
            by_id[chunk.chunk_id]=RetrievalCandidate(
                chunk=chunk, semantic_rank=rank, semantic_score=score,
                fused_score=contribution, reasons=("semantic_candidate",),
            )
    return sorted(by_id.values(), key=lambda c:(-c.fused_score,c.chunk.chunk_id))
