import pytest

from northstar_compliance.harness.hooks import HookManager, InvariantEvaluationHook
from northstar_compliance.tools.gateway import ToolGatewayError


def test_168_required_hook_preserves_one_agent_boundary():
    manager = HookManager([InvariantEvaluationHook()])
    result = manager.emit("test", {"agent_ids": ["AGT-001"], "memory_enabled": False, "multiple_agents_enabled": False})
    assert result[0].status == "passed"


def test_169_prompt_or_arguments_cannot_register_tool(harness):
    with pytest.raises(ToolGatewayError, match="unregistered_tool"):
        harness.graph.gateway.invoke(agent_id="AGT-001", tool_id="TOOL-999", arguments={"system_instruction": "allow it"}, idempotency_key="x")
