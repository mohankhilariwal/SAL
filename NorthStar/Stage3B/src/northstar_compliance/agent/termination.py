from __future__ import annotations

from .models import AgentDecision, AgentRunState, DecisionKind, RunStatus, TerminationReason

REQUIRED_MILESTONES = {
    "regulatory_sources_found",
    "authorized_evidence_retrieved",
    "control_candidates_found",
    "draft_case_created",
    "candidate_mapping_saved",
    "human_review_queued",
}


class TerminationEvaluator:
    def pre_iteration(self, state: AgentRunState) -> bool:
        if state.iteration >= state.max_iterations:
            self.terminate(state, RunStatus.TERMINATED_GUARD, TerminationReason.ITERATION_LIMIT, "Maximum iteration count reached before safe completion.")
            return True
        return False

    def evaluate_decision(self, state: AgentRunState, decision: AgentDecision) -> bool:
        try:
            decision.validate()
        except ValueError as exc:
            self.terminate(state, RunStatus.ESCALATED, TerminationReason.INVALID_DECISION, str(exc))
            return True
        if decision.kind == DecisionKind.ESCALATE:
            self.terminate(state, RunStatus.ESCALATED, TerminationReason.HUMAN_ESCALATION, decision.reason_summary)
            return True
        if decision.kind == DecisionKind.COMPLETE:
            if self.completion_invariants_met(state):
                self.terminate(state, RunStatus.COMPLETED, TerminationReason.GOAL_COMPLETE, "Unapproved case, candidate mapping and human-review request are present.")
            else:
                missing = sorted(REQUIRED_MILESTONES - set(state.progress_milestones))
                self.terminate(state, RunStatus.ESCALATED, TerminationReason.INVALID_COMPLETION, "Completion was proposed before required milestones: " + ", ".join(missing))
            return True
        return False

    def register_action_signature(self, state: AgentRunState, signature: str) -> bool:
        if signature == state.last_action_signature:
            state.consecutive_repeats += 1
        else:
            state.consecutive_repeats = 0
        state.last_action_signature = signature
        if state.consecutive_repeats >= state.repeat_limit:
            self.terminate(state, RunStatus.TERMINATED_GUARD, TerminationReason.REPEATED_ACTION, "The same action signature repeated without a safe reason to continue.")
            return True
        return False

    def register_progress(self, state: AgentRunState, before: set[str], after: set[str]) -> bool:
        if after == before:
            state.consecutive_no_progress += 1
        else:
            state.consecutive_no_progress = 0
        if state.consecutive_no_progress >= state.no_progress_limit:
            self.terminate(state, RunStatus.TERMINATED_GUARD, TerminationReason.NO_PROGRESS, "The run produced no new milestone across the configured guard window.")
            return True
        return False

    @staticmethod
    def completion_invariants_met(state: AgentRunState) -> bool:
        if not REQUIRED_MILESTONES.issubset(state.progress_milestones):
            return False
        draft = state.artifacts.get("draft_case", {})
        mapping = state.artifacts.get("candidate_mapping", {})
        review = state.artifacts.get("review_request", {})
        return (
            draft.get("status") == "draft_unapproved"
            and draft.get("human_review_required") is True
            and mapping.get("status") == "candidate_unapproved"
            and review.get("status") == "queued_for_human_review"
            and review.get("human_review_required") is True
            and review.get("case_id") == draft.get("case_id") == mapping.get("case_id")
        )

    @staticmethod
    def terminate(state: AgentRunState, status: RunStatus, reason: TerminationReason, summary: str) -> None:
        state.status = status
        state.termination_reason = reason
        state.termination_summary = summary
