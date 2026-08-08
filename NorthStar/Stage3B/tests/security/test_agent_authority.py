from pathlib import Path

from northstar_compliance.agent.decision import ScriptedDecisionProvider
from northstar_compliance.agent.factory import build_agent_runtime, default_goal, default_principal
from northstar_compliance.agent.models import AgentDecision, DecisionKind, RunStatus, TerminationReason
from northstar_compliance.tools.models import ToolPrincipalContext


def test_test083_non_allowlisted_tool_is_never_invoked(tmp_path: Path):
    root = Path(__file__).parents[2]
    provider = ScriptedDecisionProvider([
        AgentDecision(DecisionKind.CALL_TOOL, "Try an undeclared privileged action.", "Modify a control.", "TOOL-999", "1.0.0", {"admin": True})
    ])
    runtime = build_agent_runtime(root, tmp_path, provider)
    _, outcome, _ = runtime.run(default_goal(), default_principal())
    assert outcome.status == RunStatus.ESCALATED
    assert outcome.termination_reason == TerminationReason.INVALID_DECISION
    event_path = tmp_path / "events" / "tool-events.jsonl"
    assert not event_path.exists()


def test_test084_model_arguments_cannot_grant_write_scope(tmp_path: Path):
    root = Path(__file__).parents[2]
    provider = ScriptedDecisionProvider([
        AgentDecision(
            DecisionKind.CALL_TOOL,
            "Attempt a draft write with an authority-like argument.",
            "Create a draft.",
            "TOOL-004", "1.0.0",
            {"publication_id": "REG-CA-2026-071", "title": "Valid title for draft case", "evidence_ids": ["CIT-001"], "write_scope": "TOOL-004"},
        )
    ])
    principal = ToolPrincipalContext(
        principal_id="PER-001-MAYA-CHEN", groups=("RegulatoryCompliance",),
        purpose="regulatory-impact-assessment", residency="CA", clearance="internal",
        write_scopes=(), correlation_id="CORR-NO-WRITE",
    )
    runtime = build_agent_runtime(root, tmp_path, provider)
    _, outcome, _ = runtime.run(default_goal(), principal)
    assert outcome.status == RunStatus.ESCALATED
    assert outcome.termination_reason == TerminationReason.TOOL_FAILURE
    assert not (tmp_path / "cases").exists()


def test_test085_restricted_evidence_remains_hidden_from_maya(tmp_path: Path):
    root = Path(__file__).parents[2]
    runtime = build_agent_runtime(root, tmp_path)
    state, outcome, _ = runtime.run(default_goal(), default_principal())
    assert outcome.status == RunStatus.COMPLETED
    ids = {c["citation_id"] for c in state.artifacts["retrieval_context"]["citations"]}
    assert "CIT-BOREALIS-001" not in ids
