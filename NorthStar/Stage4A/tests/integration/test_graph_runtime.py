from pathlib import Path
import tempfile
from northstar_compliance.agent.models import PrincipalContext, RuntimeBudget
from northstar_compliance.graph.factory import build_runtime, build_state
from northstar_compliance.tools.gateway import ToolGateway

ROOT=Path(__file__).resolve().parents[2]

def test_118_happy_path_and_completion_invariants():
    with tempfile.TemporaryDirectory() as td:
        runtime,gateway=build_runtime(ROOT,checkpoint_dir=Path(td)); s=runtime.run(build_state(run_id='RUN-T118'))
        assert s.run_state.status=='completed'; assert len(s.run_state.milestones)==6
        assert s.run_state.final_disposition=='preliminary_grounded_unapproved'; assert s.run_state.human_review_required
        assert s.transitions[-1]['target_node']=='__END__'

def test_119_conditional_path_has_all_node_types():
    runtime,_=build_runtime(ROOT); s=runtime.run(build_state(run_id='RUN-T119'))
    types={t['node_type'] for t in s.transitions}
    assert {'deterministic','model','policy','tool','termination'} <= types

def test_120_policy_denial_precedes_write_gateway_call():
    runtime,gateway=build_runtime(ROOT); s=runtime.run(build_state(run_id='RUN-T120',principal=PrincipalContext(allow_writes=False)))
    assert s.run_state.status=='escalated' and s.run_state.termination_reason=='write_scope_denied'
    assert not any(tool in {'TOOL-004','TOOL-005','TOOL-006'} for tool,_ in gateway.calls)

def test_121_transient_read_uses_registered_fallback():
    gw=ToolGateway({'TOOL-003':'transient_read'}); runtime,_=build_runtime(ROOT,gateway=gw); s=runtime.run(build_state(run_id='RUN-T121'))
    assert s.run_state.status=='completed'; assert ('TOOL-003','fallback') in gw.calls
    assert any(r['action']=='read_fallback' for r in s.run_state.recovery_records)

def test_122_ambiguous_write_reconciles_without_duplicate():
    gw=ToolGateway({'TOOL-004':'ambiguous_after_commit'}); runtime,_=build_runtime(ROOT,gateway=gw); s=runtime.run(build_state(run_id='RUN-T122'))
    assert s.run_state.status=='completed'
    assert len([1 for (tool,_key) in gw.store if tool=='TOOL-004'])==1
    assert any(r['action']=='reconcile_write' for r in s.run_state.recovery_records)

def test_123_cancellation_is_non_success():
    runtime,_=build_runtime(ROOT,cancelled=lambda: True); s=runtime.run(build_state(run_id='RUN-T123'))
    assert s.run_state.status=='cancelled'; assert s.run_state.final_disposition=='preliminary_grounded_unapproved'

def test_124_graph_transition_budget_stops():
    b=RuntimeBudget(max_graph_transitions=3); runtime,_=build_runtime(ROOT); s=runtime.run(build_state(run_id='RUN-T124',budget=b))
    assert s.run_state.status=='terminated_guard'; assert s.run_state.termination_reason=='graph_transition_budget_exhausted'


def test_133_wall_time_budget_is_run_scoped():
    b=RuntimeBudget(max_wall_seconds=0.0); runtime,_=build_runtime(ROOT); s=runtime.run(build_state(run_id='RUN-T133',budget=b))
    assert s.run_state.status=='terminated_guard'; assert s.run_state.termination_reason=='wall_time_budget_exhausted'
