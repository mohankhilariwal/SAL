from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SOURCE_FILES = [
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
    errors = []
    source_dir = ROOT / "docs/source-of-truth"
    for name in REQUIRED_SOURCE_FILES:
        if not (source_dir / name).is_file():
            errors.append(f"missing_source_of_truth:{name}")
    for data_id in range(79, 87):
        if not any((ROOT / "schemas").glob(f"DATA-{data_id:03d}-*.schema.json")):
            errors.append(f"missing_schema:DATA-{data_id:03d}")
    policy = json.loads((ROOT / "config/memory/policy.json").read_text())
    if policy["allowed_memory_kinds"] != ["case_working"]:
        errors.append("memory_kind_boundary_changed")
    for flag in [
        "allow_cross_case_recall", "allow_user_profile_memory", "allow_semantic_memory",
        "allow_episodic_memory", "allow_organizational_memory", "allow_shared_agent_memory"
    ]:
        if policy[flag]:
            errors.append(f"future_memory_enabled:{flag}")
    manifest = json.loads((ROOT / "config/harness/manifest.json").read_text())
    if manifest["agent_count"] != 1:
        errors.append("agent_count_changed")
    if manifest["graph"] != {"id": "GRAPH-001", "version": "1.1.0"}:
        errors.append("graph_binding_changed")
    chapter = (ROOT / "docs/stages/Stage-5B-Context-Lifecycle-Compaction-and-Memory-Boundaries.md").read_text()
    for heading in ["## 1. Context Carried Forward", "## 27. Stage Handoff Pack", "# Stage Consistency Audit"]:
        if heading not in chapter:
            errors.append(f"missing_chapter_heading:{heading}")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        sys.exit(1)
    print(json.dumps({"valid": True, "checks": 10 + 8 + 8, "errors": []}, indent=2))


if __name__ == "__main__":
    main()
