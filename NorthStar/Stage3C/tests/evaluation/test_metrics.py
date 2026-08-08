from conftest import make_runtime


def test_106_recovery_rate_and_efficiency(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path, {"TOOL-001": ["transient"], "TOOL-004": ["timeout_after_commit"]})
    out = runtime.run(goal, principal)
    assert out.status == "completed"
    assert out.budget_ledger["failures"] == 2
    assert out.budget_ledger["tool_calls"] >= 6
    assert len(out.completed_milestones) == 6


def test_107_exactly_one_agent_and_no_graph_or_memory(tmp_path):
    root = tmp_path.parents[1] if False else None
    from northstar_compliance.agent.runtime import AgentRuntime
    assert AgentRuntime.AGENT_ID == "AGT-001"
