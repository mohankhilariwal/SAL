from __future__ import annotations

from .models import TopologyComparison


def compare_topologies(
    *,
    measured_quality_gain: float | None,
    handoff_error_rate: float | None,
    representative_evidence: bool,
    independent_authority_boundary: bool,
    independent_fault_domain: bool,
) -> TopologyComparison:
    single_score = 90
    multi_score = 55
    reasons: list[str] = [
        "The current workflow shares case state, authority, lifecycle, tools and human approval.",
        "GRAPH-001 already supplies specialized bounded work units without new agent identities.",
        "WP-008, MCP, A2A and additional-agent routes remain inactive_future.",
    ]

    if independent_authority_boundary:
        multi_score += 15
        reasons.append("An independent authority boundary would justify formal multi-agent review.")
    if independent_fault_domain:
        multi_score += 10
        reasons.append("An independent fault domain would increase the value of a separately operated agent.")
    if representative_evidence and measured_quality_gain is not None and measured_quality_gain >= 0.10:
        multi_score += 15
        reasons.append("Representative evidence shows at least the tutorial review trigger for quality gain.")
    else:
        reasons.append("No representative repeated-trial evidence shows a material quality gain.")
    if handoff_error_rate is not None and handoff_error_rate > 0.02:
        multi_score -= 15
        reasons.append("Observed handoff error exceeds the tutorial review parameter.")

    # The current accepted architecture cannot be changed by this advisory comparison.
    return TopologyComparison(
        comparison_id="TOPOLOGY-FINAL-001",
        selected_topology="one_agent_specialized_graph_profiles",
        single_agent_score=single_score,
        multi_agent_score=multi_score,
        measured_quality_gain=measured_quality_gain,
        handoff_error_rate=handoff_error_rate,
        representative_evidence=representative_evidence,
        reasons=tuple(reasons),
    )
