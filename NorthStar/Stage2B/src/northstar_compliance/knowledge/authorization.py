from __future__ import annotations

from datetime import date

from .schemas import CLASSIFICATION_ORDER, KnowledgeChunk, RetrievalPrincipalContext, RetrievalQuery


def _active(chunk: KnowledgeChunk, as_of: date) -> bool:
    start=date.fromisoformat(chunk.effective_from)
    end=date.fromisoformat(chunk.effective_to) if chunk.effective_to else None
    return start <= as_of and (end is None or as_of <= end)


def authorize_chunks(
    chunks: tuple[KnowledgeChunk, ...],
    principal: RetrievalPrincipalContext,
    query: RetrievalQuery,
) -> tuple[KnowledgeChunk, ...]:
    """Fail-closed, deterministic filter executed before scorer construction."""
    if not principal.principal_id or not principal.groups or not principal.purpose or not principal.residency:
        raise ValueError("incomplete retrieval principal context")
    as_of=date.fromisoformat(principal.as_of_date)
    allowed=[]
    principal_groups=set(principal.groups)
    for chunk in chunks:
        scope=chunk.access
        scope.validate()
        if CLASSIFICATION_ORDER[scope.classification] > CLASSIFICATION_ORDER[principal.clearance]:
            continue
        if "*" not in scope.allowed_groups and not principal_groups.intersection(scope.allowed_groups):
            continue
        if principal.purpose != scope.purpose:
            continue
        if principal.residency != scope.residency:
            continue
        if not _active(chunk, as_of):
            continue
        if query.require_authoritative and not chunk.authoritative:
            continue
        if query.source_types and chunk.source_type not in query.source_types:
            continue
        if query.business_domains and not set(query.business_domains).intersection(chunk.business_domains):
            continue
        requested_jurisdictions=set(query.jurisdictions or principal.jurisdictions)
        if requested_jurisdictions and not requested_jurisdictions.intersection(chunk.jurisdictions):
            continue
        allowed.append(chunk)
    return tuple(allowed)
