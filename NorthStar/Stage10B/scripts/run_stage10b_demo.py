from __future__ import annotations

import json
from pathlib import Path

from northstar_compliance.agentops.release import GateResult, ReleaseManager
from northstar_compliance.audit.port import InMemoryAuditPort
from northstar_compliance.deployment.plan import DeploymentPlanner
from northstar_compliance.integration.gateway import EnterpriseIntegrationGateway
from northstar_compliance.reliability.checkpoint import CheckpointStore
from northstar_compliance.reliability.dlq import DeadLetterQueue
from northstar_compliance.reliability.models import EffectClass, FailureClass, FailureEnvelope
from northstar_compliance.reliability.recovery import RecoveryPlanner


def main() -> None:
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    audit = InMemoryAuditPort()
    gateway = EnterpriseIntegrationGateway(audit)
    applied = gateway.protected_write(
        operation="create_review_request",
        payload={"case_id": "CASE-1001"},
        idempotency_key="CASE-1001-review-v1",
        grant={"issuer": "CMP-007", "operation": "create_review_request", "valid": True, "grant_id": "GRANT-1001"},
    )
    duplicate = gateway.protected_write(
        operation="create_review_request",
        payload={"case_id": "CASE-1001"},
        idempotency_key="CASE-1001-review-v1",
        grant={"issuer": "CMP-007", "operation": "create_review_request", "valid": True, "grant_id": "GRANT-1001"},
    )

    checkpoint = CheckpointStore(report_dir / "checkpoints")
    checkpoint_path = checkpoint.save(
        run_id="RUN-1001", graph_version="GRAPH-001/1.12.0", sequence=1, state={"node": "human_review", "case_id": "CASE-1001"}
    )
    dlq = DeadLetterQueue(report_dir / "dead-letter.jsonl")
    dlq_record = dlq.append(
        message_id="MSG-1001", reason="permanent schema mismatch", payload={"document_ref": "DOC-1001"}, idempotency_key=None, retry_count=3
    )
    planner = RecoveryPlanner()
    failure = FailureEnvelope(
        failure_id="FAIL-1001",
        component_id="CMP-005",
        operation="create_review_request",
        failure_class=FailureClass.AMBIGUOUS_OUTCOME,
        effect_class=EffectClass.PROTECTED_WRITE,
        retryable=False,
        ambiguous=True,
        safe_summary="gateway timed out after submission",
    )
    recovery = planner.decide(failure)

    releases = ReleaseManager()
    manifest = releases.build_manifest(
        release_id="REL-1.16.0-local",
        environment="production",
        source_files={"demo": "1"},
        config={"route": False},
        test_report={"passed": True},
    )
    promotion = releases.evaluate_promotion(
        manifest,
        [GateResult("unit", True, "digest")],
        human_release_approval=True,
    )
    deployment = DeploymentPlanner().prepare("pre-production")
    output = {
        "protected_effect": applied,
        "duplicate_effect": duplicate,
        "audit_events": len(audit.events),
        "checkpoint": str(checkpoint_path),
        "dead_letter": dlq_record,
        "recovery_action": recovery.action.value,
        "production_promotion_allowed": promotion.allowed,
        "production_promotion_reasons": promotion.reasons,
        "deployment_plan": deployment.__dict__,
    }
    print(json.dumps(output, indent=2, default=list))


if __name__ == "__main__":
    main()
