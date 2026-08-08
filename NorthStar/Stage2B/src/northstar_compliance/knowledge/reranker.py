from __future__ import annotations

from dataclasses import replace

from .schemas import RetrievalCandidate, RetrievalQuery
from .tokenization import tokenize


def _overlap_ratio(a_start:int,a_end:int,b_start:int,b_end:int)->float:
    overlap=max(0,min(a_end,b_end)-max(a_start,b_start)+1)
    base=min(a_end-a_start+1,b_end-b_start+1)
    return overlap/base if base else 0.0


class MetadataAwareReranker:
    def rerank(self, query: RetrievalQuery, candidates: list[RetrievalCandidate]) -> list[RetrievalCandidate]:
        qtokens=set(tokenize(query.text))
        scored=[]
        for c in candidates:
            ctokens=set(tokenize(c.chunk.text))
            coverage=len(qtokens & ctokens)/max(1,len(qtokens))
            score=c.fused_score + 0.05*coverage
            reasons=list(c.reasons)
            if coverage:
                reasons.append(f"query_term_coverage={coverage:.3f}")
            if query.text.lower() in c.chunk.text.lower():
                score += 0.02
                reasons.append("exact_query_phrase")
            if c.chunk.authoritative:
                score += 0.01
                reasons.append("authoritative_source")
            if query.business_domains and set(query.business_domains).intersection(c.chunk.business_domains):
                score += 0.015
                reasons.append("business_domain_match")
            if query.jurisdictions and set(query.jurisdictions).intersection(c.chunk.jurisdictions):
                score += 0.01
                reasons.append("jurisdiction_match")
            scored.append(replace(c,rerank_score=score,reasons=tuple(reasons)))
        return sorted(scored,key=lambda x:(-x.rerank_score,x.chunk.chunk_id))


def deduplicate_overlapping(candidates: list[RetrievalCandidate], top_k: int, overlap_threshold: float = 0.50) -> list[RetrievalCandidate]:
    selected=[]
    for candidate in candidates:
        duplicate=False
        for kept in selected:
            if candidate.chunk.source_version_id != kept.chunk.source_version_id:
                continue
            if _overlap_ratio(
                candidate.chunk.line_start,candidate.chunk.line_end,
                kept.chunk.line_start,kept.chunk.line_end,
            ) >= overlap_threshold:
                duplicate=True
                break
        if not duplicate:
            selected.append(candidate)
        if len(selected)>=top_k:
            break
    return selected
