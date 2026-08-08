from __future__ import annotations

from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import json

from northstar_compliance.knowledge.corpus import load_prepared_corpus
from northstar_compliance.knowledge.index import build_index_manifest
from northstar_compliance.knowledge.retrieval import AuthorizedRetrievalService
from northstar_compliance.knowledge.schemas import Classification, RetrievalPrincipalContext, RetrievalQuery
from northstar_compliance.knowledge.service import KnowledgePreparationService
from northstar_compliance.knowledge.store import atomic_write_json

prepared=ROOT/"examples/stage2b-output/prepared-corpus"
index_root=ROOT/"examples/stage2b-output/index"
report_root=ROOT/"reports"

KnowledgePreparationService().prepare(
    ROOT/"datasets/stage2a/input/manifest.json",
    ROOT/"datasets/stage2a/input",
    prepared,
)
corpus=load_prepared_corpus(prepared)
manifest=build_index_manifest(corpus,index_root/"retrieval-index-manifest.json")
service=AuthorizedRetrievalService(corpus,manifest)
principal=RetrievalPrincipalContext(
    principal_id="PER-001-MAYA",
    groups=("COMPLIANCE_ANALYST",),
    clearance=Classification.CONFIDENTIAL,
    purpose="REGULATORY_CHANGE_ANALYSIS",
    residency="CA",
    as_of_date="2026-07-31",
    jurisdictions=("CA","US","EU"),
)
queries=[
    RetrievalQuery(query_id="RQ-001",text="borrower affordability and ability to repay evidence",top_k=4),
    RetrievalQuery(query_id="RQ-002",text="sanctions screening restricted parties transaction monitoring escalation",top_k=4),
    RetrievalQuery(query_id="RQ-003",text="third-party customer personal data cross-border transfer controls",top_k=4),
    RetrievalQuery(query_id="RQ-004",text="Project Borealis delayed sanctions screening incident",top_k=4),
]
results=[]
for query in queries:
    context=service.retrieve(query,principal)
    results.append(context.to_dict())
atomic_write_json(report_root/"demo-output.json",{"index":manifest.to_dict(),"results":results})
print(json.dumps({"index_id":manifest.index_id,"queries":len(results),"top_sources":[[e["citation"]["source_id"] for e in r["evidence"]] for r in results]},indent=2))
