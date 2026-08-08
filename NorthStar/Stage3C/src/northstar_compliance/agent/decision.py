from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .models import AgentDecision, AgentGoal, AgentRunState, DecisionEnvelope, ModelUsage, REQUIRED_MILESTONES

class DecisionProviderError(RuntimeError):
    def __init__(self, message: str, *, retryable: bool = True):
        super().__init__(message)
        self.retryable = retryable

class DecisionProvider(Protocol):
    name: str
    def decide(self, goal: AgentGoal, state: AgentRunState, recovery_context: dict) -> DecisionEnvelope: ...

TOOL_FOR_MILESTONE = {
    "regulatory_sources_found": "TOOL-001",
    "authorized_evidence_retrieved": "TOOL-003",
    "control_candidates_found": "TOOL-002",
    "draft_case_created": "TOOL-004",
    "candidate_mapping_saved": "TOOL-005",
    "human_review_queued": "TOOL-006",
}

class DeterministicDecisionProvider:
    name = "deterministic-local"

    def decide(self, goal: AgentGoal, state: AgentRunState, recovery_context: dict) -> DecisionEnvelope:
        missing = [m for m in REQUIRED_MILESTONES if m not in state.milestones]
        if not missing:
            decision = AgentDecision(
                kind="complete",
                reason_summary="All deterministic completion milestones are present.",
                expected_progress="Terminate for human review.",
            )
            return DecisionEnvelope(decision, ModelUsage(35, 12, self.name, "rule-provider-v1"))
        milestone = missing[0]
        tool_id = TOOL_FOR_MILESTONE[milestone]
        args = self._arguments(tool_id, goal, state, recovery_context)
        decision = AgentDecision(
            kind="call_tool",
            tool_id=tool_id,
            tool_version="1.0.0",
            arguments=args,
            reason_summary=f"The next missing milestone is {milestone}.",
            expected_progress=milestone,
        )
        decision.validate()
        return DecisionEnvelope(decision, ModelUsage(80 + len(state.observations) * 8, 24, self.name, "rule-provider-v1"))

    def _arguments(self, tool_id: str, goal: AgentGoal, state: AgentRunState, recovery_context: dict) -> dict:
        recovery_attempt = int(recovery_context.get("replan_number", 0))
        if tool_id == "TOOL-001":
            return {"publication_id": goal.publication_id, "query": f"regulatory publication {goal.publication_id}", "recovery_attempt": recovery_attempt}
        if tool_id == "TOOL-003":
            return {"query": "automated credit decision evidence retention", "top_k": 5, "recovery_attempt": recovery_attempt}
        if tool_id == "TOOL-002":
            return {"query": "lending adverse action controls", "top_k": 5, "recovery_attempt": recovery_attempt}
        if tool_id == "TOOL-004":
            return {"publication_id": goal.publication_id, "evidence_ids": ["CIT-NS-001"], "control_ids": ["CTL-LEND-017"]}
        if tool_id == "TOOL-005":
            return {"case_id": state.artifacts["draft_case"]["case_id"], "control_ids": ["CTL-LEND-017"]}
        if tool_id == "TOOL-006":
            return {"case_id": state.artifacts["draft_case"]["case_id"], "reviewer_group": "regulatory-compliance"}
        raise ValueError(tool_id)

class ScriptedDecisionProvider:
    def __init__(self, decisions: list[AgentDecision], name: str = "scripted"):
        self.decisions = list(decisions)
        self.name = name

    def decide(self, goal: AgentGoal, state: AgentRunState, recovery_context: dict) -> DecisionEnvelope:
        if not self.decisions:
            raise DecisionProviderError("script exhausted", retryable=False)
        decision = self.decisions.pop(0)
        decision.validate()
        return DecisionEnvelope(decision, ModelUsage(50, 20, self.name, "script-v1"))

class FlakyDecisionProvider:
    def __init__(self, delegate: DecisionProvider, failures: int = 1, *, retryable: bool = True, name: str = "flaky-primary"):
        self.delegate = delegate
        self.failures = failures
        self.retryable = retryable
        self.name = name

    def decide(self, goal: AgentGoal, state: AgentRunState, recovery_context: dict) -> DecisionEnvelope:
        if self.failures > 0:
            self.failures -= 1
            raise DecisionProviderError("synthetic model timeout", retryable=self.retryable)
        return self.delegate.decide(goal, state, recovery_context)

def action_signature(decision: AgentDecision) -> str:
    canonical = json.dumps(
        {"tool_id": decision.tool_id, "tool_version": decision.tool_version, "arguments": decision.arguments},
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(canonical.encode("utf-8")).hexdigest()
