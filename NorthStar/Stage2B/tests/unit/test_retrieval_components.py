from dataclasses import replace
import pytest

from northstar_compliance.knowledge.authorization import authorize_chunks
from northstar_compliance.knowledge.fusion import reciprocal_rank_fusion
from northstar_compliance.knowledge.index import validate_index_manifest
from northstar_compliance.knowledge.lexical import BM25Index
from northstar_compliance.knowledge.reranker import MetadataAwareReranker, deduplicate_overlapping
from northstar_compliance.knowledge.schemas import RetrievalQuery
from northstar_compliance.knowledge.semantic import LatentSemanticIndex


def test_033_index_manifest_matches_corpus(stage):
    _,corpus,manifest,_,_,_=stage
    validate_index_manifest(corpus,manifest)
    assert manifest.chunk_count==len(corpus.chunks)


def test_034_authorization_before_scoring(stage):
    _,_,_,service,maya,_=stage
    service.retrieve(RetrievalQuery("Q","Project Borealis sanctions incident"),maya)
    assert set(service.last_scored_chunk_ids)==set(service.last_authorized_chunk_ids)
    assert not any(c.startswith("CHK-") and c not in service.last_authorized_chunk_ids for c in service.last_scored_chunk_ids)
    restricted={c.chunk_id for c in service.corpus.chunks if c.source_id=="ASMT-001"}
    assert restricted.isdisjoint(service.last_scored_chunk_ids)


def test_035_bm25_exact_term_retrieval(stage):
    _,corpus,_,_,maya,_=stage
    q=RetrievalQuery("Q","affordability ability repay")
    allowed=authorize_chunks(corpus.chunks,maya,q)
    ranked=BM25Index(allowed).score(q.text)
    assert ranked[0][0].source_id in {"POL-001","TAX-001"}


def test_036_lsa_semantic_retrieval(stage):
    _,corpus,_,_,maya,_=stage
    q=RetrievalQuery("Q","personal information overseas disclosure")
    allowed=authorize_chunks(corpus.chunks,maya,q)
    ranked=LatentSemanticIndex(allowed).score(q.text)
    assert any(chunk.source_id=="CTL-001" for chunk,_ in ranked[:5])


def test_037_rrf_is_deterministic(stage):
    _,corpus,_,_,maya,_=stage
    q=RetrievalQuery("Q","sanctions screening")
    allowed=authorize_chunks(corpus.chunks,maya,q)
    l=BM25Index(allowed).score(q.text); s=LatentSemanticIndex(allowed).score(q.text)
    a=reciprocal_rank_fusion(l,s,10,10); b=reciprocal_rank_fusion(l,s,10,10)
    assert [(x.chunk.chunk_id,x.fused_score) for x in a]==[(x.chunk.chunk_id,x.fused_score) for x in b]


def test_038_reranker_prioritizes_authoritative_exact_evidence(stage):
    _,corpus,_,_,maya,_=stage
    q=RetrievalQuery("Q","sanctions screening restricted parties",business_domains=("PAYMENTS",))
    allowed=authorize_chunks(corpus.chunks,maya,q)
    l=BM25Index(allowed).score(q.text); s=LatentSemanticIndex(allowed).score(q.text)
    fused=reciprocal_rank_fusion(l,s,12,12)
    reranked=MetadataAwareReranker().rerank(q,fused)
    assert reranked[0].chunk.source_id in {"PROC-001","TAX-001"}
    assert reranked[0].rerank_score>=reranked[-1].rerank_score


def test_039_overlap_deduplication(stage):
    _,corpus,_,_,maya,_=stage
    q=RetrievalQuery("Q","customer data third party cross border",top_k=10)
    allowed=authorize_chunks(corpus.chunks,maya,q)
    l=BM25Index(allowed).score(q.text); s=LatentSemanticIndex(allowed).score(q.text)
    reranked=MetadataAwareReranker().rerank(q,reciprocal_rank_fusion(l,s,20,20))
    selected=deduplicate_overlapping(reranked,10)
    spans=[(x.chunk.source_version_id,x.chunk.line_start,x.chunk.line_end) for x in selected]
    assert len(spans)==len(set(spans))


def test_044_index_config_mismatch_fails(stage):
    _,corpus,manifest,_,_,_=stage
    with pytest.raises(ValueError): validate_index_manifest(corpus,replace(manifest,config_hash="bad"))
