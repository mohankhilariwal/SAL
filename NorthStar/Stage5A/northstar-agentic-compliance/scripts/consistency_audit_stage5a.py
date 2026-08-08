from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from northstar_compliance.specification.loader import AgentSpecificationStore
from northstar_compliance.specification.validator import AgentSpecificationValidator

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest = json.loads((ROOT / "config/harness/harness-manifest.json").read_text(encoding="utf-8"))
    specification = AgentSpecificationStore(ROOT / "config/agents/AGT-001.spec.json").load()
    report = AgentSpecificationValidator().validate(specification, manifest=manifest)
    assert report.valid, [finding.code for finding in report.findings]
    assert manifest["architecture_version"] == manifest["repository_version"] == "1.1.0"
    assert specification.agent_id == "AGT-001"
    assert specification.raw["agent"]["graph"] == {"id": "GRAPH-001", "version": "1.1.0"}
    assert set(specification.allowed_tool_ids) == {f"TOOL-{i:03d}" for i in range(1, 7)}
    assert specification.raw["context_policy"]["memory_enabled"] is False
    assert specification.raw["authority"]["can_approve_or_finalize"] is False
    assert specification.raw["human_control"]["final_legal_or_compliance_closure"] is False
    assert specification.raw["evaluation"]["deployment_gate"] == "deny_by_default"
    assert specification.raw["lifecycle"]["retirement"]["criteria"]
    print("stage5a consistency audit passed with recorded reconstruction and production exceptions")


if __name__ == "__main__":
    main()
