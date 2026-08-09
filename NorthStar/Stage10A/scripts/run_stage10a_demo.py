from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

from northstar_compliance.audit import AuditActor
from northstar_compliance.observability.service import ObservabilityAuditService

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> None:
    demo_dir = REPORTS / "stage10a-demo"
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    demo_dir.mkdir(parents=True)

    key = os.getenv("NORTHSTAR_AUDIT_HMAC_KEY", "stage10a-local-demo-key").encode()
    service = ObservabilityAuditService(
        report_dir=demo_dir,
        audit_key=key,
        sampling_ratio=1.0,
    )
    context = service.start_context(
        session_id="SES-2026-0001",
        run_id="RUN-2026-10A-0001",
        task_id="TASK-IMPACT-0001",
        case_id="CASE-2026-0001",
        tenant_id="NORTHSTAR",
    )
    maya = AuditActor(actor_type="human", actor_id="MAYA-CHEN", role="Regulatory Compliance Analyst")
    runtime = AuditActor(actor_type="workload", actor_id="AGT-001", workload_id="northstar-runtime")
    reviewer = AuditActor(actor_type="human", actor_id="AISHA-RAHMAN", role="Business Process and Controls Owner")

    results = []
    results.append(service.record(
        event_name="task.started",
        context=context,
        component_id="CMP-003",
        actor=maya,
        payload={"publication_id": "PUB-2026-081", "goal": "evidence-backed impact assessment"},
        idempotency_key="RUN-2026-10A-0001:start",
    ))
    results.append(service.record(
        event_name="guardrail.decided",
        context=context,
        component_id="CMP-002",
        actor=runtime,
        payload={
            "decision_id": "GRD-10A-001",
            "bundle_id": "GR-BUNDLE-001",
            "bundle_version": "1.0.0",
            "outcome": "allow",
            "reason_codes": ["INPUT_TYPE_ALLOWED", "MALWARE_CLEAR"],
            "raw_prompt": "quoted source contained hostile text but must not be stored",
        },
        idempotency_key="RUN-2026-10A-0001:guardrail:input",
    ))
    results.append(service.record(
        event_name="retrieval.completed",
        context=context,
        component_id="CMP-004",
        actor=runtime,
        payload={
            "query_digest": digest("payments data retention obligations"),
            "result_count": 4,
            "source_refs": ["POL-RET-2026#12", "CTL-DATA-019#3"],
            "freshness_status": "current",
            "raw_documents_captured": False,
        },
        idempotency_key="RUN-2026-10A-0001:retrieval:1",
        audit_required=False,
    ))
    results.append(service.record(
        event_name="authorization.decided",
        context=context,
        component_id="CMP-007",
        actor=runtime,
        payload={
            "grant_id": "AUTH-GRANT-0007",
            "grant_digest": digest("AUTH-GRANT-0007"),
            "tool_id": "TOOL-006",
            "operation": "create_review_request",
            "outcome": "allow",
            "authority_effect": "none"
        },
        idempotency_key="RUN-2026-10A-0001:auth:tool6",
    ))
    intent, outcome = service.record_protected_action(
        context=context,
        actor=runtime,
        component_id="CMP-005",
        action="TOOL-006.create_review_request",
        payload={
            "approval_id": "APR-2026-0001",
            "artefact_digest": digest("draft impact assessment v1"),
            "access_token": "Bearer local-demo-secret"
        },
        outcome_payload={"status": "queued", "external_reference": "REVIEW-QUEUE-044"},
    )
    results.extend([intent, outcome])
    results.append(service.record(
        event_name="human.approval.requested",
        context=context,
        component_id="CMP-006",
        actor=runtime,
        payload={"approval_id": "APR-2026-0001", "artefact_digest": digest("draft impact assessment v1")},
        idempotency_key="RUN-2026-10A-0001:approval:requested",
    ))
    results.append(service.record(
        event_name="human.approval.decided",
        context=context,
        component_id="CMP-006",
        actor=reviewer,
        payload={
            "approval_id": "APR-2026-0001",
            "decision": "request_changes",
            "artefact_digest": digest("draft impact assessment v1"),
            "reason_codes": ["CONTROL_MAPPING_INCOMPLETE"],
        },
        idempotency_key="RUN-2026-10A-0001:approval:decision:1",
    ))
    results.append(service.record(
        event_name="state.transitioned",
        context=context,
        component_id="CMP-003",
        actor=runtime,
        payload={
            "state_object_id": "DATA-106:CASE-2026-0001",
            "from_state": "awaiting_review",
            "to_state": "changes_requested",
            "from_version": 7,
            "to_version": 8,
            "owner_component": "CMP-003",
        },
        idempotency_key="RUN-2026-10A-0001:state:8",
    ))
    results.append(service.record(
        event_name="task.disposed",
        context=context,
        component_id="CMP-003",
        actor=runtime,
        payload={
            "final_disposition": "changes_requested_by_human",
            "approved": False,
            "production_route": False,
        },
        idempotency_key="RUN-2026-10A-0001:disposed",
    ))

    exported = service.flush_telemetry()
    package = service.build_evidence_package(
        "RUN-2026-10A-0001",
        artefact_digests={
            "draft_impact_assessment": digest("draft impact assessment v1"),
            "source_publication": digest("PUB-2026-081"),
        },
        release_refs={
            "GR-BUNDLE-001": "1.0.0",
            "AUTH-001": "1.0.0",
            "BR-001": "1.0.0",
            "OBS-001": "1.0.0",
            "AUD-001": "1.0.0",
        },
    )
    (demo_dir / "evidence-package.json").write_text(json.dumps(package, indent=2, sort_keys=True), encoding="utf-8")
    summary = {
        "stage": "S10A",
        "architecture_version": "1.15.0",
        "graph_version": "GRAPH-001/1.11.0",
        "observability_model": "OBS-001/1.0.0",
        "audit_model": "AUD-001/1.0.0",
        "results": results,
        "telemetry_exported": exported,
        "status": service.status(),
        "evidence_package_digest": package["package_digest"],
        "authority_effect": "none",
    }
    (REPORTS / "stage10a-demo.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
