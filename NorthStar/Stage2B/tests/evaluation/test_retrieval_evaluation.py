from northstar_compliance.knowledge.evaluation import evaluate_case
from northstar_compliance.knowledge.schemas import RetrievalEvaluationCase, RetrievalQuery


def _ids(corpus,source_ids):
    return tuple(c.chunk_id for c in corpus.chunks if c.source_id in source_ids)


def test_045_metrics_and_permission_boundary(stage):
    _,corpus,_,service,maya,sofia=stage
    cases=[
      RetrievalEvaluationCase("EVAL-009",RetrievalQuery("Q1","borrower affordability ability to repay",top_k=4),maya,_ids(corpus,{"POL-001","TAX-001"}),_ids(corpus,{"ASMT-001"})),
      RetrievalEvaluationCase("EVAL-010",RetrievalQuery("Q2","sanctions screening restricted parties transaction monitoring escalation",top_k=4),maya,_ids(corpus,{"PROC-001","TAX-001"}),_ids(corpus,{"ASMT-001"})),
      RetrievalEvaluationCase("EVAL-011",RetrievalQuery("Q3","third party customer personal data cross border transfer",top_k=4),maya,_ids(corpus,{"CTL-001","TAX-001"}),_ids(corpus,{"ASMT-001"})),
      RetrievalEvaluationCase("EVAL-012",RetrievalQuery("Q4","Project Borealis delayed sanctions screening incident",top_k=4),maya,(),_ids(corpus,{"ASMT-001"})),
      RetrievalEvaluationCase("EVAL-013",RetrievalQuery("Q5","Project Borealis delayed sanctions screening incident",top_k=4),sofia,_ids(corpus,{"ASMT-001"}),()),
    ]
    results=[evaluate_case(service,corpus,c) for c in cases]
    assert all(r.citation_correctness==1.0 for r in results)
    assert all(r.forbidden_hits==0 for r in results)
    assert all(r.duplicate_source_spans==0 for r in results)
    assert results[0].recall_at_k>0
    assert results[1].recall_at_k>0
    assert results[2].recall_at_k>0
    assert not set(results[3].retrieved_chunk_ids).intersection(set(cases[3].forbidden_chunk_ids))
    assert results[4].recall_at_k>0
