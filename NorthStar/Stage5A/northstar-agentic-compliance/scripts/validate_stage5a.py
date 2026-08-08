from __future__ import annotations

import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.specification.loader import AgentSpecificationStore
from northstar_compliance.specification.validator import AgentSpecificationValidator

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"stage5a validation failed: {message}")


def main() -> None:
    required = [
        ROOT / "config/agents/AGT-001.spec.json",
        ROOT / "config/harness/harness-manifest.json",
        ROOT / "config/evaluation/stage5a-gates.json",
        *[ROOT / f"schemas/DATA-{i:03d}-{name}.schema.json" for i, name in [
            (71, "AgentSpecification"), (72, "SpecificationBinding"), (73, "RuntimeAssertionResult"),
            (74, "SpecificationValidationReport"), (75, "EvaluationObligation"),
            (76, "DeploymentGateResult"), (77, "ContextPolicyProfile"), (78, "RetirementDecision")]],
        *[ROOT / f"docs/source-of-truth/{name}" for name in [
            "00-Project-Constitution.md", "01-Business-and-User-Story-Baseline.md",
            "02-Requirements-Register.md", "03-Architecture-Baseline.md",
            "04-Component-and-Agent-Catalogue.md", "05-Data-and-Schema-Register.md",
            "06-ADR-Register.md", "07-Repository-Manifest.md",
            "08-Risk-Assumption-and-Issue-Register.md", "09-Stage-Handoff-Pack.md"]],
    ]
    for path in required:
        require(path.is_file() and path.stat().st_size > 0, f"missing or empty {path.relative_to(ROOT)}")

    manifest = json.loads((ROOT / "config/harness/harness-manifest.json").read_text(encoding="utf-8"))
    specification = AgentSpecificationStore(ROOT / "config/agents/AGT-001.spec.json").load()
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    require(report.valid, f"specification invalid: {[finding.code for finding in report.findings]}")

    require(manifest["agent_count"] == 1 and manifest["agent_id"] == "AGT-001", "one-agent invariant")
    require(manifest["graph"] == {"id": "GRAPH-001", "version": "1.1.0"}, "graph version changed")
    require(manifest["future_stage_flags"] == {"memory_enabled": False, "concurrent_graph_branches": False, "multiple_agents_enabled": False}, "future flags enabled")

    stage_text = (ROOT / "docs/stages/Stage-5A-Agent-Specification-and-Context-Engineering.md").read_text(encoding="utf-8")
    for heading in range(1, 28):
        require(re.search(rf"^## {heading}\. ", stage_text, re.MULTILINE) is not None, f"missing stage heading {heading}")
    require("Stage Consistency Audit" in stage_text, "consistency audit not documented")
    require("Stage 5B" in stage_text and "memory" in stage_text.lower(), "next-stage bridge missing")

    mermaid_files = list((ROOT / "docs/architecture/diagrams").glob("stage-5a-*.mmd"))
    require(len(mermaid_files) >= 5, "expected five Mermaid sources")
    for path in mermaid_files:
        text = path.read_text(encoding="utf-8")
        require(text.startswith(("flowchart", "sequenceDiagram", "stateDiagram")), f"unsupported Mermaid declaration in {path.name}")
        require("AGT-002" not in text, f"future agent leaked into {path.name}")

    print("stage5a structural validation passed")


if __name__ == "__main__":
    main()
