from pathlib import Path
from northstar_compliance.graph.factory import build_runtime, build_state
from northstar_compliance.tools.gateway import ToolGateway

ROOT=Path(__file__).resolve().parents[2]

def test_132_path_coverage_and_efficiency_metrics():
    gw=ToolGateway({'TOOL-004':'ambiguous_after_commit'}); runtime,_=build_runtime(ROOT,gateway=gw); s=runtime.run(build_state(run_id='RUN-T132'))
    nodes={t['source_node'] for t in s.transitions}
    assert {'N00_VALIDATE_CONTEXT','N10_GUARD_CHECK','N20_MODEL_DECIDE','N30_POLICY_GATE','N40_TOOL_EXECUTE','N50_RECOVERY','N60_OBSERVE','N70_COMPLETION_CHECK','N90_TERMINATE'} <= nodes
    assert s.run_state.ledger.model_calls==7 and s.run_state.ledger.tool_calls==6
