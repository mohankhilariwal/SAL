from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    stage = (ROOT / "docs/stages/NorthStar-Stage-11-Final-Capstone.md").read_text()
    handoff = (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text()
    architecture = (ROOT / "docs/architecture/diagrams/cumulative-logical-architecture.mmd").read_text()
    assertions = {
        "version": "1.18.0" in stage and "1.18.0" in handoff,
        "one_agent": "exactly one active `AGT-001`" in stage,
        "route_denied": "production route remains disabled" in stage.lower(),
        "component_range": all(f"CMP-{i:03d}" in architecture for i in range(1, 12)),
        "no_tool_007": "TOOL-007" in stage and "not introduced" in stage,
        "data_range": "DATA-279" in stage and "DATA-290" in stage,
        "interface_range": "INT-239" in stage and "INT-250" in stage,
        "adr_range": "ADR-149" in stage and "ADR-156" in stage,
        "stage8d9d": "Stage 8D" in stage and "Stage 9D" in stage,
        "authority_none": stage.count("authority_effect: none") >= 2,
        "mermaid": architecture.startswith("flowchart"),
    }
    failed = [name for name, ok in assertions.items() if not ok]
    if failed:
        raise SystemExit(f"consistency audit failed: {failed}")
    report = (
        "PASSED WITH RECORDED EXCEPTIONS: historical byte-exact merge, "
        "production evidence, Stage 8D and Stage 9D remain unresolved.\n"
    )
    (ROOT / "reports/stage11-consistency-audit.txt").write_text(report)
    print(report.strip())


if __name__ == "__main__":
    main()
