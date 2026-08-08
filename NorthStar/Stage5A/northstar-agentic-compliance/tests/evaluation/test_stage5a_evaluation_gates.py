from __future__ import annotations

from northstar_compliance.specification.gates import DeploymentGateEvaluator
from northstar_compliance.specification.validator import AgentSpecificationValidator


def evidence(specification) -> dict:
    return {
        "specification_digest": specification.digest,
        "tests": {f"TEST-{i:03d}": True for i in range(183, 213)},
        "evaluations": {f"EVAL-{i:03d}": True for i in range(42, 48)},
        "blocking_security_findings": 0,
        "future_stage_flags": {"memory_enabled": False, "concurrent_graph_branches": False, "multiple_agents_enabled": False},
        "human_approval_semantics": True,
        "final_legal_or_compliance_closure": False,
    }


def test_209_eval_042_spec_completeness(specification, manifest):
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    assert report.valid and not report.findings


def test_210_eval_043_authority_and_context_gate(specification, manifest, valid_context):
    assert specification.allowed_tool_ids == tuple(f"TOOL-{i:03d}" for i in range(1, 7))
    assert specification.raw["context_policy"]["memory_enabled"] is False
    assert manifest["agent_count"] == 1


def test_211_eval_046_security_finding_blocks(specification, manifest):
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    candidate = evidence(specification)
    candidate["blocking_security_findings"] = 1
    result = DeploymentGateEvaluator().evaluate(specification, report, candidate)
    assert not result.allowed and "security_findings_zero" in result.blocking_reasons


def test_212_eval_047_human_semantics_block(specification, manifest):
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    candidate = evidence(specification)
    candidate["human_approval_semantics"] = False
    result = DeploymentGateEvaluator().evaluate(specification, report, candidate)
    assert not result.allowed and "human_approval_semantics_passed" in result.blocking_reasons
