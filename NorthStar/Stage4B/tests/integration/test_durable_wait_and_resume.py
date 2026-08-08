from datetime import timedelta
import pytest
from northstar_compliance.durable.store import LeaseUnavailable
from northstar_compliance.graph.factory import build_runtime

def test_146_start_suspends_and_releases(runtime,t0):
    w=runtime.start(now=t0)
    assert w.status=='waiting_for_human_review' and w.current_node=='N80_REVIEW_DECISION_GATE' and w.approval_token

def test_147_resume_without_event_stays_waiting(runtime,t0):
    w=runtime.start(now=t0); r=runtime.resume(w.run_id,now=t0+timedelta(seconds=5))
    assert r.status=='waiting_for_human_review' and r.review_outcome is None

def test_148_approved_route(runtime,t0):
    w=runtime.start(now=t0)
    runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='accepted',now=t0+timedelta(seconds=5))
    f=runtime.resume(w.run_id,now=t0+timedelta(seconds=5))
    assert f.status=='completed' and f.review_outcome=='approved' and f.final_disposition=='preliminary_grounded_human_approved'

def test_149_rejected_route(runtime,t0):
    w=runtime.start(now=t0)
    runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='rejected',reason='evidence incomplete',now=t0+timedelta(seconds=5))
    f=runtime.resume(w.run_id,now=t0+timedelta(seconds=5))
    assert f.review_outcome=='rejected' and f.final_disposition=='preliminary_grounded_human_rejected'

def test_150_timeout_escalates(runtime,t0):
    w=runtime.start(now=t0); f=runtime.resume(w.run_id,now=t0+timedelta(seconds=61))
    assert f.status=='escalated' and f.review_outcome=='expired_escalated' and f.termination_reason=='approval_timeout'

def test_151_restart_resume_no_repeated_tool(tmp_path,t0):
    db=tmp_path/'restart.db'; r1=build_runtime(db,wait_timeout_seconds=60); w=r1.start(now=t0)
    assert r1.store.tool_effect_count('TOOL-006')==1
    r2=build_runtime(db,wait_timeout_seconds=60)
    r2.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=5))
    f=r2.resume(w.run_id,now=t0+timedelta(seconds=5))
    assert f.review_outcome=='approved' and r2.store.tool_effect_count('TOOL-006')==1

def test_152_resume_lease_blocks_second_worker(runtime,t0):
    w=runtime.start(now=t0); runtime.store.acquire_lease(w.run_id,'worker-a',t0+timedelta(seconds=1),10)
    with pytest.raises(LeaseUnavailable): runtime.resume(w.run_id,worker_id='worker-b',now=t0+timedelta(seconds=2))
    runtime.store.release_lease(w.run_id,'worker-a')

def test_153_expired_lease_can_be_taken(runtime,t0):
    w=runtime.start(now=t0); runtime.store.acquire_lease(w.run_id,'dead-worker',t0,1)
    r=runtime.resume(w.run_id,worker_id='worker-b',now=t0+timedelta(seconds=2))
    assert r.status=='waiting_for_human_review'

def test_154_graph_version_mismatch_fails(tmp_path,t0):
    db=tmp_path/'mismatch.db'; r1=build_runtime(db); w=r1.start(now=t0)
    import sqlite3
    with sqlite3.connect(db) as c:
        row=c.execute('select state_json from workflow_runs where run_id=?',(w.run_id,)).fetchone()[0]
        import json,hashlib
        d=json.loads(row);d['graph_version']='9.9.9';s=json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False);h=hashlib.sha256(s.encode()).hexdigest()
        c.execute('update workflow_runs set graph_version=?,state_json=?,state_sha256=? where run_id=?',('9.9.9',s,h,w.run_id));c.commit()
    with pytest.raises(Exception, match='state_graph_version_mismatch'): r1.resume(w.run_id,now=t0+timedelta(seconds=1))
