from datetime import timedelta
from pathlib import Path
import pytest

from northstar_compliance.approval.service import ApprovalServiceError
from northstar_compliance.approval.token import ApprovalTokenError
from northstar_compliance.evaluation.stage4c import trace_contains_sensitive_material


def test_178_self_approval_remains_blocked(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    with pytest.raises(ApprovalServiceError, match="separation_of_duties_violation"):
        harness.submit_decision(session_id=started.session_id, token=started.approval_token, reviewer_id="maya.chen", reviewer_roles=["compliance_approver"], decision="approved", reason="", now=now+timedelta(seconds=1))


def test_179_tampered_token_fails_before_decision(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    token = started.approval_token[:-1] + ("A" if started.approval_token[-1] != "A" else "B")
    with pytest.raises(ApprovalTokenError, match="invalid_signature"):
        harness.submit_decision(session_id=started.session_id, token=token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision="approved", reason="", now=now+timedelta(seconds=1))


def test_180_trace_contains_no_sensitive_material(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    session = harness.graph.store.load_session(started.session_id)
    assert trace_contains_sensitive_material(session["workspace_path"]) is False
