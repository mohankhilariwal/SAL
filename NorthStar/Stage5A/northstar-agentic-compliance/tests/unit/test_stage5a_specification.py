from __future__ import annotations

import copy

from northstar_compliance.specification.canonical import sha256_digest
from northstar_compliance.specification.models import AgentSpecification
from northstar_compliance.specification.validator import AgentSpecificationValidator


def as_spec(raw: dict) -> AgentSpecification:
    return AgentSpecification(raw=raw, digest=sha256_digest(raw))


def codes(report) -> set[str]:
    return {finding.code for finding in report.findings}


def test_183_valid_specification_passes(specification, manifest):
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    assert report.valid


def test_184_digest_is_canonical(raw_spec):
    shuffled = dict(reversed(list(raw_spec.items())))
    assert sha256_digest(raw_spec) == sha256_digest(shuffled)


def test_185_unknown_top_level_property_fails(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["secret_override"] = True
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "UNKNOWN_PROPERTY" in codes(report)


def test_186_missing_goal_fails(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["goals"] = []
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "LIST_REQUIRED" in codes(report)


def test_187_agent_name_and_id_are_stable(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["agent"]["id"] = "AGT-002"
    changed["agent"]["name"] = "Supervisor Agent"
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid
    assert {"AGENT_ID", "AGENT_NAME"} <= codes(report)


def test_188_graph_and_state_versions_are_preserved(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["agent"]["graph"]["version"] = "2.0.0"
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "GRAPH_BINDING" in codes(report)


def test_189_owners_are_required(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["ownership"]["risk_owner"] = ""
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "OWNER_REQUIRED" in codes(report)


def test_190_required_invariant_cannot_be_removed(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["contracts"]["invariants"].remove("timeout_never_approves")
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "INVARIANT_MISSING" in codes(report)


def test_191_retirement_criteria_are_required(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["lifecycle"]["retirement"]["criteria"] = []
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "RETIREMENT_CRITERIA" in codes(report)
