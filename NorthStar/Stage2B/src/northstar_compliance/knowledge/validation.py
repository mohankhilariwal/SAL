from __future__ import annotations

from hashlib import sha256
from .corpus import PreparedCorpus
from .schemas import EvidenceCitation


def validate_prepared_corpus(corpus: PreparedCorpus) -> dict:
    ids=set()
    errors=[]
    for chunk in corpus.chunks:
        if chunk.chunk_id in ids:
            errors.append(f"duplicate chunk id: {chunk.chunk_id}")
        ids.add(chunk.chunk_id)
        if sha256(chunk.text.encode("utf-8")).hexdigest() != chunk.text_sha256:
            errors.append(f"chunk hash mismatch: {chunk.chunk_id}")
        path=corpus.normalized_source_path(chunk)
        lines=path.read_text(encoding="utf-8").splitlines()
        reconstructed="\n".join(lines[chunk.line_start-1:chunk.line_end])
        if reconstructed != chunk.text:
            errors.append(f"coordinate mismatch: {chunk.chunk_id}")
        chunk.access.validate()
    return {"passed": not errors, "errors": errors, "chunk_count": len(corpus.chunks)}


def validate_citation(corpus: PreparedCorpus, citation: EvidenceCitation) -> bool:
    matches=[c for c in corpus.chunks if c.chunk_id == citation.chunk_id]
    if len(matches) != 1:
        return False
    chunk=matches[0]
    if (
        chunk.source_id != citation.source_id
        or chunk.source_version_id != citation.source_version_id
        or chunk.line_start != citation.line_start
        or chunk.line_end != citation.line_end
        or chunk.normalized_source_sha256 != citation.normalized_source_sha256
        or chunk.text != citation.excerpt
    ):
        return False
    path=corpus.normalized_source_path(chunk)
    lines=path.read_text(encoding="utf-8").splitlines()
    reconstructed="\n".join(lines[citation.line_start-1:citation.line_end])
    return reconstructed == citation.excerpt
