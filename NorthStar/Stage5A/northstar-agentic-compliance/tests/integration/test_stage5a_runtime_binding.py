from __future__ import annotations

import copy

from northstar_compliance.specification.assertions import RuntimeAssertionEngine
from northstar_compliance.specification.canonical import sha256_digest
from northstar_compliance.specification.gates import DeploymentGateEvaluator
from northstar_compliance.specification.models import AgentSpecification
from northstar_compliance.specification.validator import AgentSpecificationValidator


def as_spec(raw: dict) -> AgentSpecification:
    return AgentSpecification(raw=raw, digest=sha256_digest(raw))


def full_evidence(specification) -> dict:
    tests = {f"TEST-{i:03d}": True for i in range(183, 213)}
    evaluations = {f"EVAL-{i:03d}": True for i in range(42, 48)}
    return {
        "specification_digest": specification.digest,
        "tests": tests,
        "evaluations": evaluations,
        "blocking_security_findings": 0,
        "future_stage_flags": {
            "memory_enabled": False,
            "concurrent_graph_branches": False,
            "multiple_agents_enabled": False,
        },
        "human_approval_semantics": True,
        "final_legal_or_compliance_closure": False,
    }


def test_192_manifest_specification_binding_passes(specification, manifest):
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    assert report.valid


def test_193_manifest_digest_mismatch_fails(specification, manifest):
    changed = copy.deepcopy(manifest)
    changed["agent_specification"]["sha256"] = "0" * 64
    report = AgentSpecificationValidator().validate(specification, manifest=changed)
    assert not report.valid
    assert any(f.code == "MANIFEST_SPEC_HASH" for f in report.findings)


def test_194_pre_start_assertions_pass(specification, manifest, valid_context):
    result = RuntimeAssertionEngine().pre_start(specification, manifest=manifest, context_envelope=valid_context)
    assert result.passed


def test_195_post_result_assertions_pass(specification, completed_result):
    result = RuntimeAssertionEngine().post_result(
        specification,
        result=completed_result,
        persisted_result={"status": "completed", "final_disposition": completed_result["final_disposition"]},
    )
    assert result.passed


def test_196_timeout_approval_fails(specification, completed_result):
    changed = dict(completed_result)
    changed["review_outcome"] = "expired_escalated"
    result = RuntimeAssertionEngine().post_result(specification, result=changed)
    assert not result.passed and "timeout_never_approves" in result.failures


def test_197_tool006_duplicate_effect_fails(specification, completed_result):
    changed = dict(completed_result)
    changed["tool006_effects"] = 2
    result = RuntimeAssertionEngine().post_result(specification, result=changed)
    assert not result.passed and "tool006_single_effect" in result.failures


def test_198_deployment_gate_passes(specification, manifest):
    validation = AgentSpecificationValidator().validate(specification, manifest=manifest)
    result = DeploymentGateEvaluator().evaluate(specification, validation, full_evidence(specification))
    assert result.allowed


def test_199_deployment_gate_fails_missing_evaluation(specification, manifest):
    validation = AgentSpecificationValidator().validate(specification, manifest=manifest)
    evidence = full_evidence(specification)
    evidence["evaluations"]["EVAL-045"] = False
    result = DeploymentGateEvaluator().evaluate(specification, validation, evidence)
    assert not result.allowed and "required_evaluations_passed" in result.blocking_reasons


def test_200_retired_specification_denies_new_start(raw_spec, manifest, valid_context):
    changed = copy.deepcopy(raw_spec)
    changed["lifecycle"]["status"] = "retired"
    specification = as_spec(changed)
    changed_manifest = copy.deepcopy(manifest)
    changed_manifest["agent_specification"]["sha256"] = specification.digest
    pre = RuntimeAssertionEngine().pre_start(specification, manifest=changed_manifest, context_envelope=valid_context)
    assert not pre.passed and "specification_active" in pre.failures
