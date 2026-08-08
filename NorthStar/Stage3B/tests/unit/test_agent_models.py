import pytest

from northstar_compliance.agent.models import AgentDecision, DecisionKind


def test_test074_decision_schema_rejects_missing_tool_fields():
    decision = AgentDecision(DecisionKind.CALL_TOOL, "Need evidence.", "Retrieve evidence.")
    with pytest.raises(ValueError):
        decision.validate()


def test_test075_terminal_decision_rejects_tool_fields():
    decision = AgentDecision(DecisionKind.COMPLETE, "Done.", "Stop.", "TOOL-001", "1.0.0", {})
    with pytest.raises(ValueError):
        decision.validate()
