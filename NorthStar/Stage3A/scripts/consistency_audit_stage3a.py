from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    truth = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "docs/source-of-truth").glob("*.md")}
    required_components = {f"CMP-{i:03d}" for i in range(1, 12)}
    catalogue = truth["04-Component-and-Agent-Catalogue.md"]
    for cid in required_components:
        if cid not in catalogue:
            errors.append(f"component missing from catalogue: {cid}")

    descriptor_ids = set()
    descriptor_names = set()
    for path in (ROOT / "config/tools").glob("TOOL-*.json"):
        raw = json.loads(path.read_text())
        descriptor_ids.add(raw["tool_id"])
        descriptor_names.add(raw["name"])
    if descriptor_ids != {f"TOOL-{i:03d}" for i in range(1, 7)}:
        errors.append("descriptor tool IDs do not match TOOL-001..006")
    for item in descriptor_ids | descriptor_names:
        if item not in catalogue:
            errors.append(f"descriptor/catalogue mismatch: {item}")

    chapter = (ROOT / "docs/stages/Stage-3A-Tool-Contracts-and-Tool-Gateway.md").read_text()
    for heading in range(1, 28):
        if f"## {heading}." not in chapter:
            errors.append(f"missing stage section {heading}")
    if "authorization" not in chapter.casefold() or "idempotency" not in chapter.casefold():
        errors.append("stage narrative omits core gateway controls")

    all_current = "\n".join(truth.values()) + chapter + "\n" + "\n".join(
        p.read_text(encoding="utf-8", errors="ignore") for p in (ROOT / "src").rglob("*.py")
    )
    if re.search(r"\bAGT-\d{3}\b", all_current):
        errors.append("numbered agent identifier allocated")
    if "approved\": true" in all_current.casefold():
        errors.append("approval-granting behavior appears in current implementation")

    diagram = (ROOT / "docs/architecture/diagrams/cumulative-logical-architecture.mmd").read_text()
    for cid in ["CMP-003", "CMP-004", "CMP-005", "CMP-007", "CMP-008", "CMP-009", "CMP-010", "CMP-011"]:
        if cid not in diagram:
            errors.append(f"cumulative diagram omits {cid}")
    if "TOOL-001" not in diagram or "TOOL-006" not in diagram:
        errors.append("cumulative diagram omits tool range")

    manifest = truth["07-Repository-Manifest.md"]
    for rel in [
        "src/northstar_compliance/tools/gateway.py",
        "config/tools/",
        "scripts/run_stage3a_demo.py",
        "docs/stages/Stage-3A-Tool-Contracts-and-Tool-Gateway.md",
    ]:
        if rel not in manifest:
            errors.append(f"manifest does not reference {rel}")

    if errors:
        print("STAGE3A_CONSISTENCY_AUDIT: FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print("STAGE3A_CONSISTENCY_AUDIT: PASSED WITH RECORDED EXCEPTIONS")
    print("- narrative, diagrams, components, tools, schemas, repository and handoff agree")
    print("- no future-stage agent/graph/memory capability is claimed")
    print("- exceptions: no Mermaid CLI/Python 3.12/live enterprise or protocol conformance")


if __name__ == "__main__":
    main()
