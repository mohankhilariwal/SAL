from __future__ import annotations

from .models import AgentRunState, REQUIRED_MILESTONES


def completion_valid(state: AgentRunState) -> tuple[bool, str]:
    missing = [m for m in REQUIRED_MILESTONES if m not in state.milestones]
    if missing:
        return False, "missing_milestones:" + ",".join(missing)
    case = state.artifacts.get("case", {})
    mapping = state.artifacts.get("mapping", {})
    review = state.artifacts.get("review", {})
    if case.get("status") != "draft_unapproved" or not case.get("human_review_required"):
        return False, "invalid_draft_semantics"
    if mapping.get("status") != "candidate_unapproved":
        return False, "invalid_mapping_semantics"
    if review.get("status") != "queued_for_human_review" or not review.get("human_review_required"):
        return False, "invalid_review_semantics"
    ids = {case.get("case_id"), mapping.get("case_id"), review.get("case_id")}
    if len(ids) != 1 or None in ids:
        return False, "case_linkage_mismatch"
    return True, "goal_complete"
