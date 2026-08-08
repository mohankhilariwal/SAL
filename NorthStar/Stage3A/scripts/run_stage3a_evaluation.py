from __future__ import annotations

import json
import shutil
from pathlib import Path

from northstar_compliance.tools.factory import build_local_gateway
from northstar_compliance.tools.models import ToolInvocationRequest, ToolPrincipalContext

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "stage3a-tool-evaluation.json"
STORE = ROOT / "examples" / "stage3a-output" / "evaluation-store"


def principal(name: str, groups: tuple[str, ...], clearance: str, purpose: str) -> ToolPrincipalContext:
    return ToolPrincipalContext(
        principal_id=name,
        groups=groups,
        clearance=clearance,
        purpose=purpose,
        residency="CA",
        correlation_id=f"CORR-EVAL-{name.upper().replace('.', '-')}",
        authenticated=False,
    )


def invoke(gateway, who, number, tool_id, arguments, key=None):
    return gateway.invoke(ToolInvocationRequest(
        invocation_id=f"TINV-EVAL-{number:03d}",
        tool_id=tool_id,
        tool_version="1.0.0",
        principal=who,
        arguments=arguments,
        idempotency_key=key,
    ))


def main() -> None:
    if STORE.exists():
        shutil.rmtree(STORE)
    gateway, store = build_local_gateway(ROOT / "config" / "tools", STORE)
    maya = principal("maya.chen", ("regulatory_analysts",), "confidential", "regulatory_change_assessment")
    sofia = principal("sofia.alvarez", ("ai_governance",), "restricted", "model_risk_review")

    contract_results = []
    for descriptor in gateway.registry.all():
        contract_results.append({
            "tool_id": descriptor.tool_id,
            "descriptor_hash_present": len(descriptor.descriptor_hash) == 64,
            "allowed_impact": descriptor.impact_class.value in {"read_only", "reversible_write"},
        })

    maya_restricted = invoke(gateway, maya, 1, "TOOL-003", {"query":"Project Borealis sanctions","top_k":4,"jurisdiction":"CA"})
    sofia_restricted = invoke(gateway, sofia, 2, "TOOL-003", {"query":"Project Borealis sanctions","top_k":4,"jurisdiction":"CA"})

    case_args = {
        "publication_id":"REG-EVAL-001", "title":"Evaluation publication",
        "jurisdictions":["CA"], "candidate_domains":["lending"],
        "source_citation_ids":["CIT-EVAL-001"],
    }
    first = invoke(gateway, maya, 3, "TOOL-004", case_args, "EVAL-IDEM-001")
    replay = invoke(gateway, maya, 4, "TOOL-004", case_args, "EVAL-IDEM-001")

    report = {
        "schema_version":"1.0.0",
        "evaluation_ids":["EVAL-014","EVAL-015","EVAL-016","EVAL-017"],
        "contract_validity_rate": sum(all((r["descriptor_hash_present"], r["allowed_impact"])) for r in contract_results) / len(contract_results),
        "registered_tool_count": len(contract_results),
        "maya_restricted_hits": maya_restricted.data["result_count"],
        "sofia_restricted_hits": sofia_restricted.data["result_count"],
        "write_replay_status": replay.status.value,
        "case_write_count": store.write_counts["cases"],
        "unapproved_status_preserved": first.data["status"] == "DRAFT_UNAPPROVED" and first.data["disposition"] == "preliminary_unapproved",
        "agent_identifier_allocated": False,
        "boundary":"local synthetic adapters and locally asserted principal claims; not production assurance",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
