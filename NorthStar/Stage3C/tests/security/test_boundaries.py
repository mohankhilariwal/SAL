from northstar_compliance.agent.decision import ScriptedDecisionProvider
from northstar_compliance.agent.models import AgentDecision
from northstar_compliance.tools.gateway import Principal
from conftest import make_runtime


def test_102_authority_like_argument_rejected(tmp_path, goal, principal):
    provider = ScriptedDecisionProvider([AgentDecision(
        "call_tool", "attempt authority", "none", "TOOL-004", "1.0.0",
        {"publication_id": goal.publication_id, "write_scope": ["admin"]},
    )])
    runtime, primary, _ = make_runtime(tmp_path, providers=[provider])
    out = runtime.run(goal, principal)
    assert out.status == "escalated"
    assert not primary.stores.drafts


def test_103_non_allowlisted_tool_never_invoked(tmp_path, goal, principal):
    provider = ScriptedDecisionProvider([AgentDecision(
        "call_tool", "bad tool", "none", "TOOL-999", "1.0.0", {},
    )])
    runtime, primary, _ = make_runtime(tmp_path, providers=[provider])
    out = runtime.run(goal, principal)
    assert out.termination_reason == "invalid_decision"
    assert sum(primary.call_counts.values()) == 0


def test_104_restricted_borealis_evidence_absent(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path)
    out = runtime.run(goal, principal)
    evidence = str(out.artifacts.get("evidence", []))
    assert "Borealis" not in evidence


def test_105_write_scope_denial(tmp_path, goal):
    runtime, primary, _ = make_runtime(tmp_path)
    principal = Principal("maya.chen", write_scope=())
    out = runtime.run(goal, principal)
    assert out.status == "escalated"
    assert out.termination_reason == "invalid_decision"
    assert not primary.stores.drafts
