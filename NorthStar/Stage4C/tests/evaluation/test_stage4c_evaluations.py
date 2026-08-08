from datetime import timedelta
from pathlib import Path

from northstar_compliance.evaluation.stage4c import count_trace_events, read_trace


def test_181_lifecycle_trace_is_correlated(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    harness.submit_decision(session_id=started.session_id, token=started.approval_token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision="approved", reason="ok", now=now+timedelta(seconds=2))
    final = harness.resume(session_id=started.session_id, run_id=started.run_id, worker_id="worker", now=now+timedelta(seconds=3))
    session = harness.graph.store.load_session(started.session_id)
    events = read_trace(session["workspace_path"])
    event_types = {e["event_type"] for e in events}
    assert {"harness.start", "harness.suspended", "approval.accepted", "harness.resume", "harness.completed"}.issubset(event_types)
    assert all(e["session_id"] == started.session_id for e in events)
    assert {e["trace_id"] for e in events} == {started.trace_id}
    assert final.trace_id == started.trace_id
    assert count_trace_events(session["workspace_path"]) >= 5


def test_182_no_memory_multiagent_or_concurrent_branch_modules(harness, repo_root):
    assert harness.manifest.memory_enabled is False
    assert harness.manifest.multiple_agents_enabled is False
    assert harness.manifest.concurrent_graph_branches is False
    assert not (repo_root / "src/northstar_compliance/memory").exists()
    assert not (repo_root / "src/northstar_compliance/agents").exists()
