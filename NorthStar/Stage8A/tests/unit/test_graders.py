from copy import deepcopy
import pytest
from northstar_compliance.evaluation.graders import DEFAULT_GRADERS

@pytest.mark.parametrize("grader", DEFAULT_GRADERS, ids=[f"TEST-{i}" for i in range(524,536)])
def test_all_graders_pass_known_good(grader, validation_cases, candidates):
    case = validation_cases[0]
    assert grader.grade(case, candidates[case.case_id]).passed

@pytest.mark.parametrize("mutation,grader_id", [
    (lambda c: c.pop("status"), "GRD-001"),
    (lambda c: c.__setitem__("risk_tier", "low"), "GRD-002"),
    (lambda c: c.__setitem__("citations", ["EVID-UNAUTHORIZED"]), "GRD-003"),
    (lambda c: c["trace"].__setitem__("authorization_bypass", True), "GRD-004"),
    (lambda c: c.__setitem__("status", "approved"), "GRD-005"),
    (lambda c: c["trace"].__setitem__("tool_calls", [{"tool_id":"TOOL-999","gateway":"CMP-005"}]), "GRD-006"),
    (lambda c: c["trace"].__setitem__("turns", 99), "GRD-007"),
    (lambda c: c["trace"].__setitem__("authority_effect", "grant"), "GRD-011"),
    (lambda c: c["trace"].__setitem__("raw_payload_retained", True), "GRD-012"),
], ids=[f"TEST-{i}" for i in range(536,545)])
def test_faults_are_detected(mutation, grader_id, validation_cases, candidates):
    case = validation_cases[0]
    candidate = deepcopy(candidates[case.case_id])
    mutation(candidate)
    grader = next(g for g in DEFAULT_GRADERS if g.grader_id == grader_id)
    assert not grader.grade(case, candidate).passed
