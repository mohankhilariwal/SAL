from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from .models import AgentDecision, AgentGoal, AgentRunState, DecisionKind


class DecisionProvider(Protocol):
    def decide(self, goal: AgentGoal, state: AgentRunState, tool_view: list[dict]) -> AgentDecision: ...


class RuleBasedDecisionProvider:
    """Deterministic test oracle; not evidence of managed-model planning quality."""

    def decide(self, goal: AgentGoal, state: AgentRunState, tool_view: list[dict]) -> AgentDecision:
        milestones = set(state.progress_milestones)
        if "regulatory_sources_found" not in milestones:
            return AgentDecision(
                DecisionKind.CALL_TOOL,
                "The run has no regulatory catalogue observation.",
                "Populate regulatory source candidates.",
                "TOOL-001", "1.0.0",
                {"query": goal.title, "jurisdictions": list(goal.jurisdictions), "max_results": 5},
            )
        if "authorized_evidence_retrieved" not in milestones:
            return AgentDecision(
                DecisionKind.CALL_TOOL,
                "The run needs authorized internal evidence before proposing impact.",
                "Populate exact cited evidence without widening access.",
                "TOOL-003", "1.0.0",
                {"query": goal.evidence_query, "top_k": 5},
            )
        if "control_candidates_found" not in milestones:
            return AgentDecision(
                DecisionKind.CALL_TOOL,
                "The run has no affected control candidates.",
                "Populate candidate controls for the affected domains.",
                "TOOL-002", "1.0.0",
                {"query": goal.evidence_query, "business_domains": list(goal.business_domains), "max_results": 8},
            )
        if "draft_case_created" not in milestones:
            evidence_ids = [c["citation_id"] for c in state.artifacts["retrieval_context"]["citations"]]
            return AgentDecision(
                DecisionKind.CALL_TOOL,
                "Evidence and control candidates are present; an unapproved draft case is missing.",
                "Create the reversible draft case.",
                "TOOL-004", "1.0.0",
                {"publication_id": goal.publication_id, "title": goal.title, "evidence_ids": evidence_ids},
            )
        if "candidate_mapping_saved" not in milestones:
            return AgentDecision(
                DecisionKind.CALL_TOOL,
                "The draft case has no candidate control mapping.",
                "Save an unapproved candidate mapping.",
                "TOOL-005", "1.0.0",
                {
                    "case_id": state.artifacts["draft_case"]["case_id"],
                    "control_ids": [c["control_id"] for c in state.artifacts["controls"]],
                    "evidence_ids": [c["citation_id"] for c in state.artifacts["retrieval_context"]["citations"]],
                },
            )
        if "human_review_queued" not in milestones:
            return AgentDecision(
                DecisionKind.CALL_TOOL,
                "The unapproved package has not been routed to an accountable human.",
                "Queue the case and mapping for human review.",
                "TOOL-006", "1.0.0",
                {
                    "case_id": state.artifacts["draft_case"]["case_id"],
                    "mapping_id": state.artifacts["candidate_mapping"]["mapping_id"],
                    "reviewer_group": "ComplianceReview",
                    "priority": "high",
                },
            )
        return AgentDecision(
            DecisionKind.COMPLETE,
            "All deterministic completion invariants are present.",
            "Terminate with an unapproved, human-review-required outcome.",
        )


class ScriptedDecisionProvider:
    def __init__(self, decisions: Iterable[AgentDecision]):
        self._decisions = iter(decisions)

    def decide(self, goal: AgentGoal, state: AgentRunState, tool_view: list[dict]) -> AgentDecision:
        try:
            return next(self._decisions)
        except StopIteration:
            return AgentDecision(DecisionKind.ESCALATE, "The scripted provider has no further safe decision.", "Return control to a human.")
