from __future__ import annotations

from collections.abc import Iterable

from .models import Blocker, EvidenceItem, FinalAssessment


class FinalReadinessAssessor:
    """Deterministic, non-authorizing final readiness assessment."""

    def evaluate(
        self,
        evidence: Iterable[EvidenceItem],
        blocker_catalogue: Iterable[Blocker],
    ) -> FinalAssessment:
        evidence_by_id = {item.evidence_id: item for item in evidence}
        hard: list[Blocker] = []
        soft: list[Blocker] = []

        for blocker in blocker_catalogue:
            item = evidence_by_id.get(blocker.evidence_id)
            unresolved = item is None or not item.production_sufficient
            if not unresolved:
                continue
            if blocker.severity == "hard":
                hard.append(blocker)
            else:
                soft.append(blocker)

        # Stage 11 is intentionally unable to activate production. Even a future
        # evidence-complete result must be consumed by an external deployment authority.
        rationale = [
            "Production route activation is outside PRR-001 and CAPSTONE-001 authority.",
            "Exactly one active AGT-001 and the accepted authority boundaries are preserved.",
            "Hard blockers are conjunctive and cannot be averaged away by a score.",
        ]
        if hard:
            rationale.append(f"{len(hard)} hard production blockers remain unresolved.")
        if soft:
            rationale.append(f"{len(soft)} soft gaps remain open.")

        return FinalAssessment(
            assessment_id="PRA-FINAL-001",
            decision="denied" if hard else "conditional_preproduction_only",
            production_route_enabled=False,
            active_agent_count=1,
            selected_topology="one_agent_specialized_graph_profiles",
            hard_blockers=tuple(hard),
            soft_gaps=tuple(soft),
            rationale=tuple(rationale),
        )
