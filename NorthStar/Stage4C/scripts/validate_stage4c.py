from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        "config/harness/harness-manifest.json",
        "config/harness/instructions/AGT-001-system-1.0.0.txt",
        "src/northstar_compliance/harness/runtime.py",
        "src/northstar_compliance/harness/context.py",
        "src/northstar_compliance/harness/workspace.py",
        "src/northstar_compliance/harness/tracing.py",
        "docs/source-of-truth/09-Stage-Handoff-Pack.md",
    ]
    missing = [p for p in required if not (root / p).exists()]
    if missing:
        raise SystemExit(f"missing required paths: {missing}")
    manifest = json.loads((root / "config/harness/harness-manifest.json").read_text())
    assert manifest["agent_id"] == "AGT-001"
    assert manifest["graph_id"] == "GRAPH-001" and manifest["graph_version"] == "1.1.0"
    assert manifest["memory_enabled"] is False
    assert manifest["multiple_agents_enabled"] is False
    assert manifest["concurrent_graph_branches"] is False
    assert not (root / "src/northstar_compliance/memory").exists()
    assert not (root / "src/northstar_compliance/agents").exists()
    schema_files = list((root / "schemas").glob("DATA-06*.schema.json")) + list((root / "schemas").glob("DATA-070*.schema.json"))
    assert len(schema_files) == 8
    for path in schema_files:
        json.loads(path.read_text())
    print("stage4c structural validation passed")


if __name__ == "__main__":
    main()
