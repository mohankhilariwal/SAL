from __future__ import annotations
from datetime import datetime, timedelta, timezone
import pytest
from northstar_compliance.guardrails.control_plane import BoundedControlPlane
from northstar_compliance.guardrails.lifecycle import ExceptionManager, GuardrailException, PolicyChangeSet, PolicyLifecycle
from northstar_compliance.guardrails.models import GuardrailRequest, GuardrailStage, Outcome
from northstar_compliance.guardrails.engine import GuardrailEngine


def release(bundle):
    change=PolicyChangeSet('CHG-001',bundle.bundle_id,'0.9.0',bundle.version,('GR-CTL-016',),'PRIYA','stage 9c')
    return PolicyLifecycle().release(bundle,change,validation_passed=True,tests_passed=True,approvers=('SOFIA','MARCUS'))

def test_863_release_requires_validation(bundle):
    change=PolicyChangeSet('CHG-1',bundle.bundle_id,'0','1',('x',),'PRIYA','x')
    with pytest.raises(ValueError): PolicyLifecycle().release(bundle,change,validation_passed=False,tests_passed=True,approvers=('SOFIA','MARCUS'))

def test_864_release_requires_two_independent_approvers(bundle):
    change=PolicyChangeSet('CHG-1',bundle.bundle_id,'0','1',('x',),'PRIYA','x')
    with pytest.raises(ValueError): PolicyLifecycle().release(bundle,change,validation_passed=True,tests_passed=True,approvers=('SOFIA',))

def test_865_release_and_distribution(bundle):
    cp=BoundedControlPlane(); r=release(bundle); cp.register_release(bundle,r); receipt=cp.distribute('CMP-005',bundle.bundle_id,bundle.version)
    assert receipt.digest==bundle.digest and cp.status()['full_control_plane_implemented'] is False

def test_866_control_plane_evaluation(bundle):
    cp=BoundedControlPlane(); r=release(bundle); cp.register_release(bundle,r); cp.distribute('CMP-005',bundle.bundle_id,bundle.version)
    req=GuardrailRequest('R',GuardrailStage.TOOL,'T','C','RUN','TASK',payload={'tool_id':'TOOL-004'},metadata={'authorization_allowed':True,'blast_radius_allowed':True,'gateway_id':'CMP-005','tool_schema_valid':True,'approval_required':False,'concurrent_protected_writes':1,'tool_result_trusted_as_instruction':False})
    assert cp.evaluate('CMP-005',req).outcome is Outcome.ALLOW

def test_867_hard_control_exception_rejected(bundle):
    now=datetime.now(timezone.utc); e=GuardrailException('EX-1',('GR-CTL-001',),'TENANT-CA-001','CASE-2026-0001','x','REQ',('A','B'),now.isoformat(),(now+timedelta(days=1)).isoformat(),'x',('manual_review',))
    with pytest.raises(ValueError): ExceptionManager().approve(e,bundle.controls)

def test_868_soft_exception_applies(bundle):
    now=datetime.now(timezone.utc); e=GuardrailException('EX-2',('GR-CTL-016',),'TENANT-CA-001','CASE-2026-0001','retrieve','REQ',('A','B'),now.isoformat(),(now+timedelta(days=1)).isoformat(),'legacy corpus',('manual_citation_check',))
    ExceptionManager().approve(e,bundle.controls)
    engine=GuardrailEngine(bundle,(e,))
    req=GuardrailRequest('R',GuardrailStage.RETRIEVAL,'TENANT-CA-001','CASE-2026-0001','RUN','TASK',payload={},metadata={'operation':'retrieve','authorization_allowed':True,'resource_tenant_id':'TENANT-CA-001','records':1,'bytes':100,'citation_count':0,'index_age_hours':1})
    d=engine.evaluate(req)
    assert d.outcome is Outcome.ALLOW and d.exception_id=='EX-2' and 'manual_citation_check' in d.obligations
