from __future__ import annotations

from .authorization import authorize_chunks
from .citations import to_ranked_evidence
from .corpus import PreparedCorpus
from .fusion import reciprocal_rank_fusion
from .index import validate_index_manifest
from .lexical import BM25Index
from .reranker import MetadataAwareReranker, deduplicate_overlapping
from .schemas import RetrievalContext, RetrievalIndexManifest, RetrievalPrincipalContext, RetrievalQuery, SCHEMA_VERSION
from .semantic import LatentSemanticIndex


class AuthorizedRetrievalService:
    def __init__(self, corpus: PreparedCorpus, index_manifest: RetrievalIndexManifest):
        validate_index_manifest(corpus,index_manifest)
        self.corpus=corpus
        self.index_manifest=index_manifest
        self.reranker=MetadataAwareReranker()
        self.last_authorized_chunk_ids: tuple[str,...] = ()
        self.last_scored_chunk_ids: tuple[str,...] = ()

    def retrieve(self, query: RetrievalQuery, principal: RetrievalPrincipalContext) -> RetrievalContext:
        authorized=authorize_chunks(self.corpus.chunks,principal,query)
        self.last_authorized_chunk_ids=tuple(c.chunk_id for c in authorized)
        # Security boundary: scorers are constructed only from the authorized subset.
        lexical=BM25Index(authorized).score(query.text)
        semantic=LatentSemanticIndex(authorized,dimensions=self.index_manifest.semantic_dimensions).score(query.text)
        self.last_scored_chunk_ids=tuple(sorted({c.chunk_id for c,_ in lexical}|{c.chunk_id for c,_ in semantic}))
        fused=reciprocal_rank_fusion(
            lexical,semantic,query.lexical_k,query.semantic_k,
        )
        reranked=self.reranker.rerank(query,fused)
        selected=deduplicate_overlapping(reranked,query.top_k)
        evidence=to_ranked_evidence(selected)
        context_parts=[]
        for item in evidence:
            c=item.citation
            context_parts.append(
                f"[{c.citation_id}] {c.title} v{c.version_label} "
                f"({c.source_id}/{c.source_version_id}, lines {c.line_start}-{c.line_end})\n{c.excerpt}"
            )
        return RetrievalContext(
            schema_version=SCHEMA_VERSION,
            query_id=query.query_id,
            principal_id=principal.principal_id,
            index_id=self.index_manifest.index_id,
            evidence=evidence,
            context_text="\n\n".join(context_parts),
        )
