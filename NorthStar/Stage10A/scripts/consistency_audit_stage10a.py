from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_HEADINGS = [
    "# Stage 10A — Observability and Audit",
    "## 1. Context Carried Forward",
    "## 10. Selected Architecture and Rationale",
    "## 12. Architecture After the Change",
    "## 15. Implementation",
    "## 27. Stage Handoff Pack",
]


def main() -> None:
    errors: list[str] = []
    for name in [
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
    ]:
        if not (ROOT / "docs/source-of-truth" / name).exists():
            errors.append(f"missing source-of-truth file: {name}")
    stage = ROOT / "docs/stages/NorthStar-Stage-10A-Observability-and-Audit.md"
    text = stage.read_text(encoding="utf-8") if stage.exists() else ""
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing stage heading: {heading}")
    for invariant in [
        "AGT-001",
        "TOOL-001–006",
        "CMP-003",
        "CMP-005",
        "CMP-006",
        "CMP-007",
        "Stage 8D remains unresolved",
        "Stage 9D remains unresolved",
        "authority_effect: none",
    ]:
        if invariant not in text:
            errors.append(f"stage narrative missing invariant: {invariant}")
    if "production_ready: true" in text.lower() or "full production control plane is implemented" in text.lower():
        errors.append("future-stage capability falsely claimed")
    diagrams = list((ROOT / "docs/architecture/diagrams").glob("*.mmd"))
    for diagram in diagrams:
        value = diagram.read_text(encoding="utf-8")
        if not any(value.lstrip().startswith(prefix) for prefix in ("flowchart", "sequenceDiagram", "stateDiagram", "graph")):
            errors.append(f"unknown Mermaid declaration in {diagram.name}")
    report = {
        "result": "passed with recorded exceptions" if not errors else "failed",
        "errors": errors,
        "diagrams_checked": len(diagrams),
        "schemas_checked": len(list((ROOT / "schemas").glob("DATA-*.schema.json"))),
        "recorded_exceptions": ["ISS-096", "ISS-131", "ISS-141", "ISS-158", "ISS-170", "ISS-171", "ISS-179"],
    }
    output = json.dumps(report, indent=2, sort_keys=True)
    (ROOT / "reports/stage10a-consistency-audit.json").write_text(output, encoding="utf-8")
    (ROOT / "reports/stage10a-consistency-audit.txt").write_text(
        f"Stage 10A consistency audit: {report['result']}\n" + "\n".join(errors), encoding="utf-8"
    )
    print(output)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
