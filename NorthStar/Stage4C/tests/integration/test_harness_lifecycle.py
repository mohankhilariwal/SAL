from datetime import timedelta
from pathlib import Path


def test_170_start_runs_through_harness_and_suspends(harness, harness_request, now):
    result = harness.start(harness_request, now=now)
    assert result.status == "waiting_for_human_review"
    assert result.current_node == "N80_REVIEW_DECISION_GATE"
    assert result.disposition == "preliminary_grounded_unapproved"
    assert result.approval_token
    assert harness.graph.store.count_tool_effects("TOOL-006") == 1


def test_171_workspace_never_persists_raw_approval_token(harness, harness_request, now):
    result = harness.start(harness_request, now=now)
    session = harness.graph.store.load_session(result.session_id)
    text = "\n".join(p.read_text(encoding="utf-8") for p in Path(session["workspace_path"]).rglob("*") if p.is_file())
    assert result.approval_token not in text
    assert "approval_token" not in text


def test_172_approved_resume_preserves_single_tool_effect(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    harness.submit_decision(session_id=started.session_id, token=started.approval_token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision="approved", reason="sufficient", now=now+timedelta(seconds=10))
    final = harness.resume(session_id=started.session_id, run_id=started.run_id, worker_id="worker-1", now=now+timedelta(seconds=11))
    assert final.status == "completed"
    assert final.review_outcome == "approved"
    assert final.disposition == "preliminary_grounded_human_approved"
    assert harness.graph.store.count_tool_effects("TOOL-006") == 1


def test_173_rejected_route(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    harness.submit_decision(session_id=started.session_id, token=started.approval_token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision="rejected", reason="evidence gap", now=now+timedelta(seconds=5))
    final = harness.resume(session_id=started.session_id, run_id=started.run_id, worker_id="worker-1", now=now+timedelta(seconds=6))
    assert final.review_outcome == "rejected"
    assert final.disposition == "preliminary_grounded_human_rejected"


def test_174_timeout_never_approves(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    final = harness.resume(session_id=started.session_id, run_id=started.run_id, worker_id="worker-1", now=now+timedelta(seconds=61))
    assert final.status == "escalated"
    assert final.review_outcome == "expired_escalated"
    assert final.disposition == "preliminary_grounded_unapproved"
