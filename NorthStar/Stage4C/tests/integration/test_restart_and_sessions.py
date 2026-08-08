from datetime import timedelta
import pytest

from northstar_compliance.harness.factory import build_harness
from northstar_compliance.graph.runtime import GraphRuntimeError


def test_175_restart_recreates_harness_and_resumes(harness, harness_request, now, repo_root, tmp_path):
    started = harness.start(harness_request, now=now)
    harness.submit_decision(session_id=started.session_id, token=started.approval_token, reviewer_id="daniel.brooks", reviewer_roles=["compliance_approver"], decision="approved", reason="ok", now=now+timedelta(seconds=4))
    restarted = build_harness(repository_root=repo_root, runtime_root=tmp_path/"runtime", approval_secret=b"stage4c-test-secret-material-32-bytes-minimum", approval_ttl_seconds=60)
    final = restarted.resume(session_id=started.session_id, run_id=started.run_id, worker_id="worker-restart", now=now+timedelta(seconds=5))
    assert final.review_outcome == "approved"
    assert restarted.graph.store.count_tool_effects("TOOL-006") == 1


def test_176_session_mismatch_fails_closed(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    with pytest.raises(Exception, match="session_not_found"):
        harness.resume(session_id="SESSION-NOTREAL", run_id=started.run_id, worker_id="worker", now=now)


def test_177_graph_version_mismatch_fails_closed(harness, harness_request, now):
    started = harness.start(harness_request, now=now)
    state, revision = harness.graph.store.load_workflow(started.run_id)
    state.graph_version = "9.9.9"
    harness.graph.store.save_workflow(state, expected_revision=revision)
    with pytest.raises(GraphRuntimeError, match="graph_version_mismatch"):
        harness.resume(session_id=started.session_id, run_id=started.run_id, worker_id="worker", now=now)
