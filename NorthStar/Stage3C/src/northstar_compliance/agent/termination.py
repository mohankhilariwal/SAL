from __future__ import annotations

from .models import AgentRunState, REQUIRED_MILESTONES

class TerminationEvaluator:
    @staticmethod
    def completion_valid(state: AgentRunState) -> bool:
        if not set(REQUIRED_MILESTONES).issubset(state.milestones):
            return False
        draft = state.artifacts.get("draft_case", {})
        mapping = state.artifacts.get("candidate_mapping", {})
        review = state.artifacts.get("review_request", {})
        case_id = draft.get("case_id")
        return bool(
            case_id
            and draft.get("status") == "draft_unapproved"
            and draft.get("human_review_required") is True
            and mapping.get("status") == "candidate_unapproved"
            and mapping.get("case_id") == case_id
            and review.get("status") == "queued_for_human_review"
            and review.get("human_review_required") is True
            and review.get("case_id") == case_id
        )
