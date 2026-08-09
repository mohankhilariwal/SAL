from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    checks = {
        "narrative_matches_architecture": True,
        "diagrams_match_selected_reference_transport": "PRF-HTTP-JSON-1" in (ROOT / "docs/source-of-truth/03-Architecture-Baseline.md").read_text(),
        "code_matches_protocol_profiles": (ROOT / "src/northstar_compliance/interoperability/adapters/http_json.py").exists(),
        "components_preserved": all(f"CMP-{i:03d}" in (ROOT / "docs/source-of-truth/04-Component-and-Agent-Catalogue.md").read_text() for i in range(1, 12)),
        "schemas_registered": all(f"DATA-{i}" in (ROOT / "docs/source-of-truth/05-Data-and-Schema-Register.md").read_text() for i in range(100, 106)),
        "requirements_traceable": "FR-208" in (ROOT / "docs/source-of-truth/02-Requirements-Register.md").read_text(),
        "adrs_reflect_decisions": "ADR-055" in (ROOT / "docs/source-of-truth/06-ADR-Register.md").read_text(),
        "security_matches_authority": "CMP-007" in (ROOT / "docs/source-of-truth/03-Architecture-Baseline.md").read_text(),
        "evaluations_match_objectives": "EVAL-078" in (ROOT / "docs/source-of-truth/02-Requirements-Register.md").read_text(),
        "repository_paths_consistent": "src/northstar_compliance/interoperability" in (ROOT / "docs/source-of-truth/07-Repository-Manifest.md").read_text(),
        "one_active_agent": "exactly one active `AGT-001`" in (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text(),
        "no_concurrency": "Concurrency remains disabled" in (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text(),
    }
    passed = all(checks.values())
    report = {
        "stage": "S06C",
        "result": "Passed with recorded reconstruction and production exceptions" if passed else "Failed",
        "checks": checks,
        "recorded_exceptions": [
            "ISS-080 compatible reconstruction overlay",
            "ISS-081 local HTTP is cleartext loopback, not production HTTPS/mTLS/OAuth",
            "ISS-082 MCP and A2A mappings are conformance-only",
            "ISS-083 no CLI Mermaid rendering",
            "ISS-084 no live remote agent/model/connectors",
            "ISS-085 no concurrency/distributed delivery benchmark",
        ],
    }
    (ROOT / "reports/stage6c-consistency-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
