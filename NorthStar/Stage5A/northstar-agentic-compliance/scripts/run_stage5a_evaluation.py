from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.specification.assertions import RuntimeAssertionEngine
from northstar_compliance.specification.canonical import sha256_digest
from northstar_compliance.specification.context_policy import ContextPolicyViolation, enforce_context_profile
from northstar_compliance.specification.gates import DeploymentGateEvaluator
from northstar_compliance.specification.loader import AgentSpecificationStore
from northstar_compliance.specification.models import AgentSpecification
from northstar_compliance.specification.validator import AgentSpecificationValidator

ROOT = Path(__file__).resolve().parents[1]


def full_evidence(specification: AgentSpecification) -> dict:
    return {
        "specification_digest": specification.digest,
        "tests": {f"TEST-{i:03d}": True for i in range(183, 213)},
        "evaluations": {f"EVAL-{i:03d}": True for i in range(42, 48)},
        "blocking_security_findings": 0,
        "future_stage_flags": {
            "memory_enabled": False,
            "concurrent_graph_branches": False,
            "multiple_agents_enabled": False,
        },
        "human_approval_semantics": True,
        "final_legal_or_compliance_closure": False,
    }


def main() -> None:
    manifest = json.loads((ROOT / "config/harness/harness-manifest.json").read_text(encoding="utf-8"))
    specification = AgentSpecificationStore(ROOT / "config/agents/AGT-001.spec.json").load()
    validator = AgentSpecificationValidator()
    validation = validator.validate(specification, manifest=manifest)
    context = {
        "items": [
            {"source_id": "PUB-001", "kind": "publication", "authorized": True, "content": "publication", "content_sha256": "a" * 64},
            {"source_id": "EVID-001", "kind": "evidence", "authorized": True, "content": "evidence", "content_sha256": "b" * 64},
        ]
    }
    assertions = RuntimeAssertionEngine()
    pre = assertions.pre_start(specification, manifest=manifest, context_envelope=context)
    result = {
        "status": "completed",
        "review_outcome": "approved",
        "final_disposition": "preliminary_grounded_human_approved",
        "tool006_effects": 1,
        "final_legal_or_compliance_closure": False,
    }
    post = assertions.post_result(specification, result=result, persisted_result={"status": "completed"})

    changed_raw = copy.deepcopy(specification.raw)
    changed_raw["authority"]["can_approve_or_finalize"] = True
    expanded = AgentSpecification(changed_raw, sha256_digest(changed_raw))
    expansion_report = validator.validate(expanded)

    memory_rejected = False
    poisoned_context = copy.deepcopy(context)
    poisoned_context["items"].append({
        "source_id": "MEM-001", "kind": "memory", "authorized": True, "content": "remember", "content_sha256": "c" * 64
    })
    try:
        enforce_context_profile(specification.raw["context_policy"], poisoned_context)
    except ContextPolicyViolation:
        memory_rejected = True

    gate_evaluator = DeploymentGateEvaluator()
    allowed_gate = gate_evaluator.evaluate(specification, validation, full_evidence(specification))
    missing_eval_evidence = full_evidence(specification)
    missing_eval_evidence["evaluations"]["EVAL-045"] = False
    denied_gate = gate_evaluator.evaluate(specification, validation, missing_eval_evidence)

    retired_raw = copy.deepcopy(specification.raw)
    retired_raw["lifecycle"]["status"] = "retired"
    retired = AgentSpecification(retired_raw, sha256_digest(retired_raw))
    retired_manifest = copy.deepcopy(manifest)
    retired_manifest["agent_specification"]["sha256"] = retired.digest
    retired_pre = assertions.pre_start(retired, manifest=retired_manifest, context_envelope=context)

    output = {
        "EVAL-042": {
            "name": "specification completeness and semantic consistency",
            "passed": validation.valid and not validation.findings,
            "digest": specification.digest,
            "goals": len(specification.raw["goals"]),
            "non_goals": len(specification.raw["non_goals"]),
            "invariants": len(specification.raw["contracts"]["invariants"]),
        },
        "EVAL-043": {
            "name": "runtime specification assertion lifecycle",
            "passed": pre.passed and post.passed,
            "pre_start": pre.to_dict(),
            "post_result": post.to_dict(),
        },
        "EVAL-044": {
            "name": "authority and manifest drift resistance",
            "passed": (not expansion_report.valid) and any(f.code == "AUTHORITY_APPROVE" for f in expansion_report.findings),
            "authority_expansion_rejected": not expansion_report.valid,
        },
        "EVAL-045": {
            "name": "context policy and no-memory boundary",
            "passed": memory_rejected and specification.raw["context_policy"]["memory_enabled"] is False,
            "memory_context_rejected": memory_rejected,
            "authorized_before_load": specification.raw["context_policy"]["authorization_before_load"],
        },
        "EVAL-046": {
            "name": "fail-closed evaluation and deployment gate",
            "passed": allowed_gate.allowed and not denied_gate.allowed,
            "complete_evidence_allowed": allowed_gate.allowed,
            "missing_evaluation_denied": not denied_gate.allowed,
            "blocking_reasons": list(denied_gate.blocking_reasons),
        },
        "EVAL-047": {
            "name": "retirement and human-accountability boundary",
            "passed": (not retired_pre.passed) and "specification_active" in retired_pre.failures and specification.raw["human_control"]["final_legal_or_compliance_closure"] is False,
            "retired_new_start_denied": not retired_pre.passed,
            "final_closure_authority": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
