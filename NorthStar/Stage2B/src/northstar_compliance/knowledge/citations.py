from __future__ import annotations

from hashlib import sha256

from .schemas import EvidenceCitation, RankedEvidence, RetrievalCandidate


def build_citation(candidate: RetrievalCandidate) -> EvidenceCitation:
    chunk=candidate.chunk
    material=f"{chunk.chunk_id}|{chunk.line_start}|{chunk.line_end}|{chunk.text}".encode("utf-8")
    return EvidenceCitation(
        citation_id="CIT-"+sha256(material).hexdigest()[:20].upper(),
        source_id=chunk.source_id,
        source_version_id=chunk.source_version_id,
        chunk_id=chunk.chunk_id,
        title=chunk.title,
        version_label=chunk.version_label,
        line_start=chunk.line_start,
        line_end=chunk.line_end,
        normalized_source_sha256=chunk.normalized_source_sha256,
        excerpt=chunk.text,
    )


def to_ranked_evidence(candidates: list[RetrievalCandidate]) -> tuple[RankedEvidence,...]:
    evidence=[]
    for rank,candidate in enumerate(candidates,start=1):
        chunk=candidate.chunk
        evidence.append(RankedEvidence(
            rank=rank,
            score=candidate.rerank_score,
            citation=build_citation(candidate),
            source_type=chunk.source_type,
            authoritative=chunk.authoritative,
            business_domains=chunk.business_domains,
            jurisdictions=chunk.jurisdictions,
            risk_flags=chunk.risk_flags,
            ranking_reasons=candidate.reasons,
        ))
    return tuple(evidence)
