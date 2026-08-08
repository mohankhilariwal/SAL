from __future__ import annotations

from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import json

from northstar_compliance.knowledge.corpus import load_prepared_corpus
from northstar_compliance.knowledge.index import build_index_manifest
from northstar_compliance.knowledge.schemas import Classification, RetrievalPrincipalContext, RetrievalQuery
from northstar_compliance.knowledge.retrieval import AuthorizedRetrievalService
from northstar_compliance.knowledge.service import KnowledgePreparationService
from northstar_compliance.knowledge.validation import validate_citation, validate_prepared_corpus

prepared=ROOT/"examples/stage2b-output/prepared-corpus"
KnowledgePreparationService().prepare(ROOT/"datasets/stage2a/input/manifest.json",ROOT/"datasets/stage2a/input",prepared)
corpus=load_prepared_corpus(prepared)
report=validate_prepared_corpus(corpus)
manifest=build_index_manifest(corpus,ROOT/"examples/stage2b-output/index/retrieval-index-manifest.json")
service=AuthorizedRetrievalService(corpus,manifest)
principal=RetrievalPrincipalContext("PER-001-MAYA",("COMPLIANCE_ANALYST",),Classification.CONFIDENTIAL,"REGULATORY_CHANGE_ANALYSIS","CA","2026-07-31",("CA","US","EU"))
context=service.retrieve(RetrievalQuery("RQ-VALIDATE","customer personal data third party cross-border transfer",top_k=4),principal)
report.update({
    "index_id":manifest.index_id,
    "evidence_count":len(context.evidence),
    "all_citations_valid":all(validate_citation(corpus,x.citation) for x in context.evidence),
    "unauthorized_asmt_scored":any(c.source_id == "ASMT-001" and c.chunk_id in service.last_scored_chunk_ids for c in corpus.chunks),
})
if not report["passed"] or not report["all_citations_valid"] or report["unauthorized_asmt_scored"]:
    raise SystemExit(json.dumps(report,indent=2))
(ROOT/"reports/validation-output.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
