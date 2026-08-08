from __future__ import annotations

from typing import Any, Protocol

from northstar_compliance.common.jsonutil import canonical_json, sha256_text
from northstar_compliance.harness.models import ContextEnvelope, HarnessManifest, HarnessRunResult


class ValidationError(RuntimeError):
    pass


class Validator(Protocol):
    name: str
    points: tuple[str, ...]
    def validate(self, point: str, payload: Any) -> None: ...


class ManifestValidator:
    name = "manifest_validator"
    points = ("pre_start", "pre_resume")

    def __init__(self, expected_digest: str):
        self.expected_digest = expected_digest

    def validate(self, point: str, payload: Any) -> None:
        manifest = payload if isinstance(payload, HarnessManifest) else payload["manifest"]
        if manifest.memory_enabled or manifest.concurrent_graph_branches or manifest.multiple_agents_enabled:
            raise ValidationError("future_stage_capability_enabled")
        if manifest.digest != self.expected_digest:
            raise ValidationError("harness_manifest_mismatch")
        if manifest.agent_id != "AGT-001" or manifest.graph_id != "GRAPH-001" or manifest.graph_version != "1.1.0":
            raise ValidationError("accepted_runtime_identity_mismatch")
        if not manifest.critical_controls_external:
            raise ValidationError("critical_controls_must_be_external")


class ContextEnvelopeValidator:
    name = "context_envelope_validator"
    points = ("post_context",)

    def validate(self, point: str, payload: ContextEnvelope) -> None:
        if payload.agent_id != "AGT-001":
            raise ValidationError("context_agent_mismatch")
        if any(item.kind == "memory" for item in payload.items):
            raise ValidationError("memory_not_enabled")
        basis = {
            "agent_id": payload.agent_id,
            "items": [i.to_dict(include_content=True) for i in payload.items],
            "omitted": list(payload.omitted_source_ids),
            "created_at": payload.created_at,
        }
        if sha256_text(canonical_json(basis)) != payload.content_sha256:
            raise ValidationError("context_checksum_mismatch")


class ResultValidator:
    name = "result_validator"
    points = ("post_start", "post_resume")
    ALLOWED = {
        "preliminary_grounded_unapproved",
        "preliminary_grounded_human_approved",
        "preliminary_grounded_human_rejected",
    }

    def validate(self, point: str, payload: HarnessRunResult) -> None:
        if payload.disposition not in self.ALLOWED:
            raise ValidationError("invalid_disposition")
        if payload.disposition.startswith("final_"):
            raise ValidationError("final_disposition_prohibited")
        if payload.status == "waiting_for_human_review" and not payload.wait_id:
            raise ValidationError("waiting_result_requires_wait")


class ValidationPipeline:
    def __init__(self, validators: list[Validator]):
        self.validators = tuple(validators)

    def run(self, point: str, payload: Any) -> None:
        for validator in self.validators:
            if point in validator.points:
                validator.validate(point, payload)
