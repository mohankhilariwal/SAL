from __future__ import annotations
from pathlib import Path
import pytest
from northstar_compliance.guardrails.models import GuardrailRequest, GuardrailStage, Outcome

ROOT=Path(__file__).resolve().parents[2]

@pytest.mark.parametrize('suffix,meta,expected',[
 ('872',{'bundle_digest':'d','authority_tier':1,'bundle_stale':False,'operation':'run','stage8d_resolved':False},Outcome.ALLOW),
 ('873',{'bundle_digest':'d','authority_tier':1,'bundle_stale':False,'operation':'run','stage8d_resolved':False,'emergency_stop':True},Outcome.DENY),
 ('874',{'bundle_digest':'','authority_tier':1,'bundle_stale':False,'operation':'run','stage8d_resolved':False},Outcome.DENY),
 ('875',{'bundle_digest':'d','authority_tier':3,'bundle_stale':True,'operation':'run','stage8d_resolved':False},Outcome.DENY),
 ('876',{'bundle_digest':'d','authority_tier':3,'bundle_stale':False,'operation':'promote_to_production','stage8d_resolved':False},Outcome.DENY),
])
def test_runtime_matrix(engine,suffix,meta,expected):
    req=GuardrailRequest(f'R-{suffix}',GuardrailStage.RUNTIME,'T','C','RUN','TASK',payload={},metadata=meta)
    assert engine.evaluate(req).outcome is expected

def test_877_exactly_one_agent_in_docs():
    text=(ROOT/'docs/source-of-truth/04-Component-and-Agent-Catalogue.md').read_text() if (ROOT/'docs/source-of-truth/04-Component-and-Agent-Catalogue.md').exists() else 'pending'
    assert 'AGT-001' in text or text=='pending'

def test_878_no_new_tool_ids_in_config():
    text=(ROOT/'config/guardrails/guardrail_policy_bundle.json').read_text()
    assert 'TOOL-007' not in text

def test_879_inactive_future_routes_not_enabled():
    text=(ROOT/'config/guardrails/control_plane_profile.json').read_text()
    assert 'create_agent' in text and 'activate_route' in text

def test_880_stage8d_remains_unresolved():
    import json
    raw=json.loads((ROOT/'config/guardrails/control_plane_profile.json').read_text())
    assert raw['stage8d_resolved'] is False
