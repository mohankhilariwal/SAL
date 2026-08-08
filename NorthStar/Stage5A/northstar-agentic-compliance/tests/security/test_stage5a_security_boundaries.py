from __future__ import annotations

import copy

import pytest

from northstar_compliance.specification.assertions import RuntimeAssertionEngine
from northstar_compliance.specification.canonical import sha256_digest
from northstar_compliance.specification.context_policy import ContextPolicyViolation, enforce_context_profile
from northstar_compliance.specification.models import AgentSpecification
from northstar_compliance.specification.validator import AgentSpecificationValidator


def as_spec(raw: dict) -> AgentSpecification:
    return AgentSpecification(raw=raw, digest=sha256_digest(raw))


def finding_codes(report) -> set[str]:
    return {f.code for f in report.findings}


def test_201_authority_expansion_fails(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["authority"]["can_approve_or_finalize"] = True
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "AUTHORITY_APPROVE" in finding_codes(report)


def test_202_dynamic_tool_injection_fails(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["authority"]["allowed_tools"].append({
        "id": "TOOL-999", "version": "1.0.0", "purpose": "admin", "impact": "read_only", "via": "INT-017/CMP-005"
    })
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "TOOL_ALLOWLIST" in finding_codes(report)


def test_203_direct_adapter_path_fails(raw_spec):
    changed = copy.deepcopy(raw_spec)
    changed["authority"]["allowed_tools"][0]["via"] = "direct_adapter"
    report = AgentSpecificationValidator().validate(as_spec(changed))
    assert not report.valid and "TOOL_GATEWAY" in finding_codes(report)


def test_204_memory_context_is_rejected(specification, valid_context):
    changed = copy.deepcopy(valid_context)
    changed["items"].append({
        "source_id": "MEM-001", "kind": "memory", "authorized": True, "content": "remember", "content_sha256": "c" * 64
    })
    with pytest.raises(ContextPolicyViolation, match="context_kind_not_allowed:memory"):
        enforce_context_profile(specification.raw["context_policy"], changed)


def test_205_unauthorized_context_is_rejected(specification, valid_context):
    changed = copy.deepcopy(valid_context)
    changed["items"][0]["authorized"] = False
    with pytest.raises(ContextPolicyViolation, match="unauthorized_context_item"):
        enforce_context_profile(specification.raw["context_policy"], changed)


def test_206_context_budget_is_enforced(specification):
    envelope = {
        "items": [
            {"source_id": f"E-{i}", "kind": "evidence", "authorized": True, "content": "x", "content_sha256": "d" * 64}
            for i in range(9)
        ]
    }
    with pytest.raises(ContextPolicyViolation, match="context_item_budget_exceeded"):
        enforce_context_profile(specification.raw["context_policy"], envelope)


def test_207_persisted_callback_token_fails(specification, completed_result):
    persisted = {"status": "completed", "callback_token": "secret"}
    result = RuntimeAssertionEngine().post_result(specification, result=completed_result, persisted_result=persisted)
    assert not result.passed and "no_persisted_approval_token" in result.failures


def test_208_final_legal_closure_fails(specification, completed_result):
    changed = dict(completed_result)
    changed["final_legal_or_compliance_closure"] = True
    result = RuntimeAssertionEngine().post_result(specification, result=changed)
    assert not result.passed and "no_final_closure" in result.failures
