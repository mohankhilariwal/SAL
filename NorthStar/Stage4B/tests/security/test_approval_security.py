from datetime import timedelta
import pytest
from northstar_compliance.approval.token import TokenValidationError
from northstar_compliance.durable.store import DurableStoreError

def waiting(runtime,t0): return runtime.start(now=t0)

def test_139_tampered_token_rejected(runtime,t0):
    w=waiting(runtime,t0); bad=w.approval_token[:-1]+('A' if w.approval_token[-1]!='A' else 'B')
    with pytest.raises(TokenValidationError): runtime.approvals.submit(token=bad,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=1))

def test_140_expired_token_rejected(runtime,t0):
    w=waiting(runtime,t0)
    with pytest.raises(TokenValidationError): runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=61))

def test_141_wrong_role_rejected(runtime,t0):
    w=waiting(runtime,t0)
    with pytest.raises(DurableStoreError, match='reviewer_role_missing'):
        runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['analyst'],decision='approved',reason='ok',now=t0+timedelta(seconds=1))

def test_142_separation_of_duties(runtime,t0):
    w=waiting(runtime,t0)
    with pytest.raises(DurableStoreError, match='separation_of_duties'):
        runtime.approvals.submit(token=w.approval_token,reviewer_id='maya.chen',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=1))

def test_143_reject_requires_reason(runtime,t0):
    w=waiting(runtime,t0)
    with pytest.raises(DurableStoreError, match='rejection_reason_required'):
        runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='rejected',reason='',now=t0+timedelta(seconds=1))

def test_144_invalid_decision_rejected(runtime,t0):
    w=waiting(runtime,t0)
    with pytest.raises(DurableStoreError, match='invalid_decision'):
        runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='edited',reason='x',now=t0+timedelta(seconds=1))

def test_145_token_single_use(runtime,t0):
    w=waiting(runtime,t0)
    runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=1))
    with pytest.raises(DurableStoreError, match='decision_already_recorded'):
        runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=2))
