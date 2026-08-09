import pytest
from northstar_compliance.capstone import compare_topologies


@pytest.mark.parametrize("quality,handoff,representative", [
    (None,None,False),
    (0.0,0.0,False),
    (0.09,0.01,True),
    (0.20,0.03,True),
])
def test_current_topology_remains_single(quality, handoff, representative):
    result = compare_topologies(
        measured_quality_gain=quality,
        handoff_error_rate=handoff,
        representative_evidence=representative,
        independent_authority_boundary=False,
        independent_fault_domain=False,
    )
    assert result.selected_topology == "one_agent_specialized_graph_profiles"


def test_independent_boundary_only_triggers_review_evidence():
    result = compare_topologies(
        measured_quality_gain=None,
        handoff_error_rate=None,
        representative_evidence=False,
        independent_authority_boundary=True,
        independent_fault_domain=False,
    )
    assert result.multi_agent_score > 55
    assert result.selected_topology == "one_agent_specialized_graph_profiles"


def test_fault_domain_only_does_not_activate_agent():
    result = compare_topologies(
        measured_quality_gain=None,
        handoff_error_rate=None,
        representative_evidence=False,
        independent_authority_boundary=False,
        independent_fault_domain=True,
    )
    assert result.selected_topology == "one_agent_specialized_graph_profiles"


def test_topology_output_has_no_authority():
    result = compare_topologies(
        measured_quality_gain=0.2,
        handoff_error_rate=0.0,
        representative_evidence=True,
        independent_authority_boundary=True,
        independent_fault_domain=True,
    )
    assert result.authority_effect == "none"
