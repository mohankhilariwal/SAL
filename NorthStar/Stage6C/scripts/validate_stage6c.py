from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SOURCE = [
    "00-Project-Constitution.md",
    "01-Business-and-User-Story-Baseline.md",
    "02-Requirements-Register.md",
    "03-Architecture-Baseline.md",
    "04-Component-and-Agent-Catalogue.md",
    "05-Data-and-Schema-Register.md",
    "06-ADR-Register.md",
    "07-Repository-Manifest.md",
    "08-Risk-Assumption-and-Issue-Register.md",
    "09-Stage-Handoff-Pack.md",
]


def main() -> None:
    errors: list[str] = []
    source_dir = ROOT / "docs/source-of-truth"
    for name in REQUIRED_SOURCE:
        if not (source_dir / name).exists():
            errors.append(f"missing:{name}")
    policy = json.loads((ROOT / "config/architecture/interoperability-policy-v1.json").read_text())
    if policy["activeAgentCount"] != 1:
        errors.append("active_agent_count_not_one")
    if policy["concurrencyEnabled"]:
        errors.append("concurrency_enabled")
    if policy["selectedReferenceTransport"] != "PRF-HTTP-JSON-1":
        errors.append("reference_transport_mismatch")
    profiles = json.loads((ROOT / "config/protocols/protocol-profiles-v1.json").read_text())
    statuses = {item["profile_id"]: item["implementation_status"] for item in profiles}
    if statuses.get("PRF-MCP-2026-07-28") != "current_conformance_profile":
        errors.append("mcp_status_invalid")
    if statuses.get("PRF-A2A-1.0") != "conformance_only_candidate_profile":
        errors.append("a2a_status_invalid")
    stage = (ROOT / "docs/stages/Stage-6C-Agent-Communication-MCP-A2A-and-Interoperability.md").read_text()
    for token in ("ADR-051", "ADR-052", "ADR-053", "ADR-054", "ADR-055", "DATA-100", "INT-078", "EVAL-078"):
        if token not in stage:
            errors.append(f"stage_missing:{token}")
    if re.search(r"AGT-002\s+active", stage, re.IGNORECASE):
        errors.append("false_second_agent_claim")
    result = {"stage": "S06C", "passed": not errors, "errors": errors}
    (ROOT / "reports/stage6c-validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
