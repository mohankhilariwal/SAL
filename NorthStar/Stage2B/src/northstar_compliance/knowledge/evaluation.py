from __future__ import annotations

from time import perf_counter

from .corpus import PreparedCorpus
from .retrieval import AuthorizedRetrievalService
from .schemas import RetrievalEvaluationCase, RetrievalEvaluationResult
from .validation import validate_citation


def evaluate_case(
    service: AuthorizedRetrievalService,
    corpus: PreparedCorpus,
    case: RetrievalEvaluationCase,
) -> RetrievalEvaluationResult:
    start=perf_counter()
    context=service.retrieve(case.query,case.principal)
    latency=(perf_counter()-start)*1000
    retrieved=tuple(item.citation.chunk_id for item in context.evidence)
    relevant=set(case.relevant_chunk_ids)
    hits=[x for x in retrieved if x in relevant]
    precision=len(hits)/len(retrieved) if retrieved else 0.0
    recall=len(hits)/len(relevant) if relevant else 1.0
    rr=0.0
    for i,x in enumerate(retrieved,start=1):
        if x in relevant:
            rr=1/i
            break
    citation_correct=sum(validate_citation(corpus,item.citation) for item in context.evidence)
    citation_correctness=citation_correct/len(context.evidence) if context.evidence else 1.0
    forbidden_hits=len(set(retrieved).intersection(case.forbidden_chunk_ids))
    duplicate_spans=0
    seen=[]
    for item in context.evidence:
        c=item.citation
        key=(c.source_version_id,c.line_start,c.line_end)
        if key in seen:
            duplicate_spans+=1
        seen.append(key)
    return RetrievalEvaluationResult(
        case_id=case.case_id,
        precision_at_k=precision,
        recall_at_k=recall,
        reciprocal_rank=rr,
        citation_correctness=citation_correctness,
        forbidden_hits=forbidden_hits,
        duplicate_source_spans=duplicate_spans,
        latency_ms=latency,
        retrieved_chunk_ids=retrieved,
    )
