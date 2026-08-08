from __future__ import annotations

import json
import shutil
from pathlib import Path

from northstar_compliance.tools.factory import build_local_gateway
from northstar_compliance.tools.models import ToolInvocationRequest, ToolPrincipalContext


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "examples" / "stage3a-output"
STORE = OUTPUT / "runtime-store"
EVENTS = OUTPUT / "tool-events.jsonl"


def invoke(gateway, principal, number, tool_id, arguments, key=None, dry_run=False):
    request = ToolInvocationRequest(
        invocation_id=f"TINV-DEMO-{number:03d}",
        tool_id=tool_id,
        tool_version="1.0.0",
        principal=principal,
        arguments=arguments,
        idempotency_key=key,
        dry_run=dry_run,
    )
    result = gateway.invoke(request)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return result


def main() -> None:
    if STORE.exists():
        shutil.rmtree(STORE)
    if EVENTS.exists():
        EVENTS.unlink()
    OUTPUT.mkdir(parents=True, exist_ok=True)

    gateway, store = build_local_gateway(ROOT / "config" / "tools", STORE, EVENTS)
    maya = ToolPrincipalContext(
        principal_id="maya.chen",
        groups=("regulatory_analysts",),
        clearance="confidential",
        purpose="regulatory_change_assessment",
        residency="CA",
        correlation_id="CORR-STAGE3A-DEMO",
        authenticated=False,
    )

    reg = invoke(
        gateway,
        maya,
        1,
        "TOOL-001",
        {"query": "ability repay", "jurisdiction": "CA", "as_of_date": "2026-07-31", "limit": 5},
    )
    evidence = invoke(
        gateway,
        maya,
        2,
        "TOOL-003",
        {"query": "ability repay", "top_k": 4, "jurisdiction": "CA"},
    )
    citations = [item["citation_id"] for item in evidence.data["evidence"]]
    case = invoke(
        gateway,
        maya,
        3,
        "TOOL-004",
        {
            "publication_id": reg.data["matches"][0]["publication_id"],
            "title": reg.data["matches"][0]["title"],
            "jurisdictions": ["CA"],
            "candidate_domains": ["lending"],
            "source_citation_ids": citations,
        },
        key="DEMO-CASE-001",
    )
    mapping = invoke(
        gateway,
        maya,
        4,
        "TOOL-005",
        {
            "case_id": case.data["case_id"],
            "policy_id": "POL-LEND-004",
            "control_ids": ["CTL-LEND-017"],
            "source_citation_ids": citations,
            "rationale": "The cited evidence indicates that ability-to-repay records may require analyst review.",
        },
        key="DEMO-MAPPING-001",
    )
    invoke(
        gateway,
        maya,
        5,
        "TOOL-006",
        {
            "case_id": case.data["case_id"],
            "mapping_ids": [mapping.data["mapping_id"]],
            "reviewer_group": "compliance_reviewers",
        },
        key="DEMO-REVIEW-001",
    )
    replay = invoke(
        gateway,
        maya,
        6,
        "TOOL-004",
        {
            "publication_id": reg.data["matches"][0]["publication_id"],
            "title": reg.data["matches"][0]["title"],
            "jurisdictions": ["CA"],
            "candidate_domains": ["lending"],
            "source_citation_ids": citations,
        },
        key="DEMO-CASE-001",
    )

    summary = {
        "tool_descriptors": len(gateway.registry.all()),
        "case_writes": store.write_counts["cases"],
        "mapping_writes": store.write_counts["mappings"],
        "review_writes": store.write_counts["reviews"],
        "duplicate_case_status": replay.status.value,
        "approval_granted": False,
        "external_notification_sent": False,
        "agent_identifier_allocated": False,
    }
    (OUTPUT / "demo-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("STAGE3A_DEMO_SUMMARY", json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
