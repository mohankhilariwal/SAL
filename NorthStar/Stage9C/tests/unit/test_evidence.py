from northstar_compliance.guardrails.evidence import minimized_evidence
from northstar_compliance.guardrails.models import GuardrailRequest, GuardrailStage

def test_869_evidence_is_minimized(engine):
    req=GuardrailRequest('R',GuardrailStage.INPUT,'T','C','RUN','TASK',payload={'text':'normal'},metadata={'content_type':'text/plain','malware_status':'clean','token':'secret'})
    d=engine.evaluate(req); e=minimized_evidence(req,d)
    assert 'token' not in e and e['authority_effect']=='none' and len(e['payload_digest'])==64

def test_870_decision_cannot_create_authority(engine):
    req=GuardrailRequest('R',GuardrailStage.INPUT,'T','C','RUN','TASK',payload={'text':'normal'},metadata={'content_type':'text/plain','malware_status':'clean'})
    assert engine.evaluate(req).authority_effect=='none'
