from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .canonical import sha256_digest
from .models import GuardrailDecision, GuardrailRequest


SENSITIVE_KEYS = {"token", "authorization", "password", "secret", "private_key", "raw_document", "prompt"}


def minimized_evidence(request: GuardrailRequest, decision: GuardrailDecision) -> dict[str, Any]:
    metadata = {k: v for k, v in request.metadata.items() if k.lower() not in SENSITIVE_KEYS}
    evidence = {
        "evidence_type": "DATA-197",
        "request_id": request.request_id,
        "decision_id": decision.decision_id,
        "stage": request.stage.value,
        "tenant_id": request.tenant_id,
        "case_id": request.case_id,
        "run_id": request.run_id,
        "task_id": request.task_id,
        "agent_id": request.agent_id,
        "agent_spec_version": request.agent_spec_version,
        "payload_digest": sha256_digest(request.payload),
        "metadata_digest": sha256_digest(metadata),
        "outcome": decision.outcome.value,
        "reason_codes": list(decision.reason_codes),
        "obligations": list(decision.obligations),
        "control_results": [
            {"control_id": f.control_id, "passed": f.passed, "reason_code": f.reason_code}
            for f in decision.findings
        ],
        "policy_bundle_id": decision.policy_bundle_id,
        "policy_bundle_version": decision.policy_bundle_version,
        "policy_bundle_digest": decision.policy_bundle_digest,
        "exception_id": decision.exception_id,
        "evaluated_at": decision.evaluated_at,
        "authority_effect": "none",
    }
    evidence["evidence_digest"] = sha256_digest(evidence)
    return evidence
