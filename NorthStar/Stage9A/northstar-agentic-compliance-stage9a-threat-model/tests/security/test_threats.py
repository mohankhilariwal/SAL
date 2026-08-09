from northstar_compliance.security.threat_model.catalogue import by_risk_id
from northstar_compliance.security.threat_model.fixtures import MALICIOUS_PUBLICATION, POISONED_POLICY, FOREIGN_AUDIENCE_TOKEN, SPOOFED_AGENT_CARD
from .helpers import make_engine

def cat(): return make_engine().catalogue

def test_712_direct_injection_present(): assert by_risk_id(cat(),'RSK-310')['owasp_agentic_top10']=='ASI01'
def test_713_indirect_injection_present(): assert 'DF-002' in by_risk_id(cat(),'RSK-311')['entry_flows']
def test_714_retrieval_poisoning_present(): assert by_risk_id(cat(),'RSK-313')['threat_family']=='memory_context_poisoning'
def test_715_tool_poisoning_present(): assert by_risk_id(cat(),'RSK-315')['owasp_agentic_top10']=='ASI02'
def test_716_confused_deputy_controls():
    c=' '.join(by_risk_id(cat(),'RSK-317')['controls']).lower(); assert 'consent' in c and 'passthrough' in c
def test_717_token_replay_present(): assert by_risk_id(cat(),'RSK-318')['residual_impact']==4
def test_718_cross_tenant_residual_critical():
    e=make_engine(); t=next(t for t in e.threats if t.risk_id=='RSK-320'); assert e.risk_band(t.residual.value)=='high'
def test_719_secret_leak_present(): assert by_risk_id(cat(),'RSK-321')['inherent_impact']==5
def test_720_supply_chain_present(): assert by_risk_id(cat(),'RSK-322')['owasp_agentic_top10']=='ASI04'
def test_721_code_exec_present(): assert by_risk_id(cat(),'RSK-324')['owasp_agentic_top10']=='ASI05'
def test_722_memory_poisoning_present(): assert by_risk_id(cat(),'RSK-326')['owasp_agentic_top10']=='ASI06'
def test_723_replay_idempotency_present(): assert 'Idempotency keys' in by_risk_id(cat(),'RSK-329')['controls'][0]
def test_724_audit_tampering_present(): assert 'Repudiation' in by_risk_id(cat(),'RSK-330')['stride']
def test_725_judge_manipulation_present(): assert by_risk_id(cat(),'RSK-331')['inherent_impact']==5
def test_726_dos_present(): assert 'Denial of Service' in by_risk_id(cat(),'RSK-333')['stride']
def test_727_human_trust_present(): assert by_risk_id(cat(),'RSK-337')['owasp_agentic_top10']=='ASI09'
def test_728_future_agent_card_inactive(): assert by_risk_id(cat(),'RSK-339')['scope']=='future'
def test_729_future_rogue_agent_inactive(): assert by_risk_id(cat(),'RSK-344')['status']=='future_not_active'
def test_730_malicious_publication_fixture(): assert 'TOOL-006' in MALICIOUS_PUBLICATION['text'] and 'no_approval' in MALICIOUS_PUBLICATION['expected']
def test_731_poisoned_policy_fixture(): assert POISONED_POLICY['source_version']=='superseded'
def test_732_foreign_token_fixture(): assert FOREIGN_AUDIENCE_TOKEN['aud'] != FOREIGN_AUDIENCE_TOKEN['resource']
def test_733_spoofed_card_fixture(): assert 'approve_case' in SPOOFED_AGENT_CARD['skills']
def test_734_no_route_activation(): assert 'no_model_provider_or_route_activated' in make_engine().snapshot['invariants']
