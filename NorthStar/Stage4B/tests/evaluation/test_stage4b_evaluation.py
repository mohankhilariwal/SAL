from datetime import timedelta
from pathlib import Path

def test_155_decision_latency_excludes_model_tool_replay(runtime,t0):
    w=runtime.start(now=t0); state,_=runtime.store.load_run(w.run_id); before=(state.run_state.model_calls,state.run_state.tool_calls)
    runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=5))
    runtime.resume(w.run_id,now=t0+timedelta(seconds=5)); state,_=runtime.store.load_run(w.run_id)
    assert (state.run_state.model_calls,state.run_state.tool_calls)==before==(1,1)

def test_156_transition_evidence_has_wait_and_decision_routes(runtime,t0):
    w=runtime.start(now=t0);runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=2));runtime.resume(w.run_id,now=t0+timedelta(seconds=2))
    state,_=runtime.store.load_run(w.run_id); routes=[x.route for x in state.transitions]
    assert 'wait' in routes and 'approved' in routes and 'complete' in routes

def test_157_one_agent_no_future_modules():
    root=Path(__file__).resolve().parents[2]
    assert not (root/'src/northstar_compliance/memory').exists()
    assert not (root/'src/northstar_compliance/harness').exists()
    assert not (root/'src/northstar_compliance/agents').exists()

def test_158_disposition_never_claims_final_compliance(runtime,t0):
    w=runtime.start(now=t0);runtime.approvals.submit(token=w.approval_token,reviewer_id='daniel',reviewer_roles=['compliance_approver'],decision='approved',reason='ok',now=t0+timedelta(seconds=2));f=runtime.resume(w.run_id,now=t0+timedelta(seconds=2))
    assert 'final_compliance' not in f.final_disposition and f.final_disposition.startswith('preliminary_grounded_')
