from dataclasses import replace

from northstar_compliance.knowledge.schemas import RetrievalQuery
from northstar_compliance.knowledge.validation import validate_citation


def test_040_exact_citations_validate(stage):
    _,corpus,_,service,maya,_=stage
    ctx=service.retrieve(RetrievalQuery("Q","customer personal data cross-border transfer",top_k=5),maya)
    assert ctx.evidence
    assert all(validate_citation(corpus,e.citation) for e in ctx.evidence)


def test_041_tampered_citation_rejected(stage):
    _,corpus,_,service,maya,_=stage
    ctx=service.retrieve(RetrievalQuery("Q","affordability ability repay",top_k=3),maya)
    bad=replace(ctx.evidence[0].citation,excerpt=ctx.evidence[0].citation.excerpt+" tampered")
    assert not validate_citation(corpus,bad)


def test_042_expired_source_filtered(stage):
    _,corpus,_,service,maya,_=stage
    # Fixture sources are current on 2026-07-31. A pre-effective query must yield no authorized chunks.
    old=replace(maya,as_of_date="2024-01-01")
    ctx=service.retrieve(RetrievalQuery("Q","affordability"),old)
    assert not ctx.evidence


def test_043_purpose_residency_and_clearance_fail_closed(stage):
    _,_,_,service,maya,_=stage
    wrong=replace(maya,purpose="MARKETING")
    assert not service.retrieve(RetrievalQuery("Q","customer data"),wrong).evidence
    wrong=replace(maya,residency="US")
    assert not service.retrieve(RetrievalQuery("Q","customer data"),wrong).evidence


def test_046_no_agent_tool_or_generation_contract():
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]
    code="\n".join(p.read_text(encoding="utf-8") for p in (root/"src").rglob("*.py"))
    assert "AGT-" not in code and "TOOL-" not in code
    assert "generate_answer" not in code and "agent_loop" not in code
