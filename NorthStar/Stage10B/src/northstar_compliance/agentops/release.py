from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from northstar_compliance.common.canonical import sha256_digest
from northstar_compliance.reliability.models import ReleaseManifest


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    passed: bool
    evidence_digest: str


@dataclass(frozen=True)
class PromotionDecision:
    environment: str
    allowed: bool
    reasons: tuple[str, ...]
    authority_effect: str = "none"


class ReleaseManager:
    def build_manifest(
        self,
        *,
        release_id: str,
        environment: str,
        source_files: dict[str, str],
        config: dict[str, object],
        test_report: dict[str, object],
    ) -> ReleaseManifest:
        return ReleaseManifest(
            release_id=release_id,
            environment=environment,
            architecture_version="1.16.0",
            repository_version="1.16.0",
            graph_version="GRAPH-001/1.12.0",
            agent_spec_version="AGT-001/1.1.0",
            config_digest=sha256_digest(config),
            source_digest=sha256_digest(source_files),
            test_report_digest=sha256_digest(test_report),
        )

    def evaluate_promotion(
        self,
        manifest: ReleaseManifest,
        gates: Iterable[GateResult],
        *,
        human_release_approval: bool,
    ) -> PromotionDecision:
        reasons: list[str] = []
        failed = [gate.gate_id for gate in gates if not gate.passed]
        if failed:
            reasons.append("failed gates: " + ", ".join(failed))
        if not human_release_approval:
            reasons.append("authenticated human release approval is absent")
        if manifest.environment == "production":
            if manifest.unresolved_stage_8d:
                reasons.append("Stage 8D promotion eligibility remains unresolved")
            if manifest.unresolved_stage_9d:
                reasons.append("Stage 9D enterprise control plane remains unresolved")
            if not manifest.production_route_enabled:
                reasons.append("production route is disabled")
        return PromotionDecision(manifest.environment, not reasons, tuple(reasons))

    @staticmethod
    def manifest_dict(manifest: ReleaseManifest) -> dict[str, object]:
        return asdict(manifest)
