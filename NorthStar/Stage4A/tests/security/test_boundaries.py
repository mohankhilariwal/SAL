from pathlib import Path
from northstar_compliance.graph.factory import build_runtime, build_state

ROOT=Path(__file__).resolve().parents[2]

def test_129_exactly_one_agent_and_no_future_stage_modules():
    state=build_state(); assert state.run_state.agent_id=='AGT-001'
    assert not (ROOT/'src/northstar_compliance/memory').exists()
    assert not (ROOT/'src/northstar_compliance/harness').exists()
    assert not (ROOT/'src/northstar_compliance/agents').exists()

def test_130_every_tool_action_uses_gateway():
    runtime,gw=build_runtime(ROOT); state=runtime.run(build_state(run_id='RUN-T130'))
    assert state.run_state.ledger.tool_calls==6 and len(gw.calls)==6

def test_131_maya_restricted_evidence_not_present():
    runtime,_=build_runtime(ROOT); state=runtime.run(build_state(run_id='RUN-T131'))
    text=str(state.to_dict()); assert 'Borealis' not in text and 'RESTRICTED' not in text
