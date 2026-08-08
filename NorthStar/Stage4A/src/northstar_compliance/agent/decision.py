from __future__ import annotations

from .models import AgentDecision, AgentRunState, REQUIRED_MILESTONES

MILESTONE_TO_TOOL = {
    "regulatory_sources_found": "TOOL-001",
    "authorized_evidence_retrieved": "TOOL-003",
    "control_candidates_found": "TOOL-002",
    "draft_case_created": "TOOL-004",
    "candidate_mapping_saved": "TOOL-005",
    "human_review_queued": "TOOL-006",
}


class DeterministicDecisionProvider:
    """Offline provider that proves graph mechanics without claiming model quality."""

    def decide(self, state: AgentRunState) -> tuple[AgentDecision, tuple[int, int]]:
        for milestone in REQUIRED_MILESTONES:
            if milestone not in state.milestones:
                tool_id = MILESTONE_TO_TOOL[milestone]
                case_id = state.artifacts.get("case", {}).get("case_id", f"CASE-{state.run_id[-8:]}")
                args = {
                    "publication_id": state.principal.publication_scope,
                    "case_id": case_id,
                    "purpose": state.principal.purpose,
                }
                return (
                    AgentDecision(
                        kind="tool",
                        tool_id=tool_id,
                        arguments=args,
                        reason_summary=f"Acquire the next required milestone: {milestone}.",
                    ),
                    (86, 20),
                )
        return AgentDecision(kind="complete", reason_summary="All six required unapproved milestones exist."), (64, 12)
