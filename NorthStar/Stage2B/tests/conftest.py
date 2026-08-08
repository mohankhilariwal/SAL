from pathlib import Path
import pytest

from northstar_compliance.knowledge.corpus import load_prepared_corpus
from northstar_compliance.knowledge.index import build_index_manifest
from northstar_compliance.knowledge.retrieval import AuthorizedRetrievalService
from northstar_compliance.knowledge.schemas import Classification, RetrievalPrincipalContext
from northstar_compliance.knowledge.service import KnowledgePreparationService

@pytest.fixture()
def stage(tmp_path: Path):
    root=Path(__file__).resolve().parents[1]
    prepared=tmp_path/"prepared"
    KnowledgePreparationService().prepare(root/"datasets/stage2a/input/manifest.json",root/"datasets/stage2a/input",prepared)
    corpus=load_prepared_corpus(prepared)
    manifest=build_index_manifest(corpus,tmp_path/"index-manifest.json")
    service=AuthorizedRetrievalService(corpus,manifest)
    maya=RetrievalPrincipalContext("PER-001-MAYA",("COMPLIANCE_ANALYST",),Classification.CONFIDENTIAL,"REGULATORY_CHANGE_ANALYSIS","CA","2026-07-31",("CA","US","EU"))
    sofia=RetrievalPrincipalContext("PER-006-SOFIA",("MODEL_RISK",),Classification.RESTRICTED,"REGULATORY_CHANGE_ANALYSIS","CA","2026-07-31",("CA",))
    return root,corpus,manifest,service,maya,sofia
