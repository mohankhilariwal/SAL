import pytest
from northstar_compliance.capstone import Blocker, EvidenceItem, FinalReadinessAssessor


def evidence(status):
    return EvidenceItem("E", "evidence", status, "test")


def blocker(severity="hard"):
    return Blocker("B", "blocker", severity, "E", "owner", "reason")


@pytest.mark.parametrize("status", ["missing", "proposed", "local_only", "unapproved", "unexercised"])
def test_nonproduction_evidence_denies(status):
    result = FinalReadinessAssessor().evaluate([evidence(status)], [blocker()])
    assert result.decision == "denied"
    assert result.production_route_enabled is False


def test_present_hard_evidence_is_conditional_preproduction_only():
    result = FinalReadinessAssessor().evaluate([evidence("present")], [blocker()])
    assert result.decision == "conditional_preproduction_only"
    assert result.production_route_enabled is False


def test_soft_gap_does_not_enable_production():
    result = FinalReadinessAssessor().evaluate([evidence("missing")], [blocker("soft")])
    assert result.decision == "conditional_preproduction_only"
    assert result.production_route_enabled is False


def test_assessment_preserves_one_agent():
    result = FinalReadinessAssessor().evaluate([], [])
    assert result.active_agent_count == 1
    assert result.selected_topology == "one_agent_specialized_graph_profiles"
