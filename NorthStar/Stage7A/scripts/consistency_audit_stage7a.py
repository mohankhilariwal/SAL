#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    files = {
        "handoff": ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md",
        "architecture": ROOT / "docs/source-of-truth/03-Architecture-Baseline.md",
        "catalogue": ROOT / "docs/source-of-truth/04-Component-and-Agent-Catalogue.md",
        "data": ROOT / "docs/source-of-truth/05-Data-and-Schema-Register.md",
        "adr": ROOT / "docs/source-of-truth/06-ADR-Register.md",
        "manifest": ROOT / "docs/source-of-truth/07-Repository-Manifest.md",
        "risk": ROOT / "docs/source-of-truth/08-Risk-Assumption-and-Issue-Register.md",
        "policy": ROOT / "config/concurrency/policy.json",
    }
    text = "\n".join(path.read_text(encoding="utf-8") for path in files.values())
    assertions = {
        "architecture_version_1_6_0": "1.6.0" in text,
        "exactly_one_active_agent": "exactly one active `AGT-001`" in text or "Only active agent" in text,
        "cmp003_orchestration_owner": "CMP-003" in text,
        "cmp007_authority_owner": "CMP-007" in text,
        "no_concurrent_protected_writes": "no concurrent protected-state writes" in text,
        "graph_001_1_2_0": "GRAPH-001/1.2.0" in text,
        "data_106_to_113": all(f"DATA-{number}" in text for number in range(106, 114)),
        "interfaces_079_to_086": all(f"INT-{number:03d}" in text for number in range(79, 87)),
        "adrs_056_to_061": all(f"ADR-{number:03d}" in text for number in range(56, 62)),
        "no_agt002_activation": not bool(re.search(r"AGT-002.*active", text, flags=re.IGNORECASE)),
        "reconstruction_exception_recorded": "ISS-088" in text,
    }
    payload = {
        "stage": "S07A",
        "result": "Passed with recorded reconstruction and production exceptions" if all(assertions.values()) else "Failed",
        "assertions": assertions,
    }
    output = ROOT / "reports" / "consistency-audit-report.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not all(assertions.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
