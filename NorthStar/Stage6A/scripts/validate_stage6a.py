import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    required = [
        "docs/stages/Stage-6A-Single-Agent-versus-Multi-Agent-Architecture-Decision-and-Agent-Boundary-Analysis.md",
        "docs/source-of-truth/00-Project-Constitution.md",
        "docs/source-of-truth/09-Stage-Handoff-Pack.md",
        "config/architecture/agent-boundary-policy.json",
        "config/agents/AGT-001-task-profiles.json",
        "schemas/DATA-087-AgentBoundaryQuestionnaire.schema.json",
        "schemas/DATA-090-TaskProfileBinding.schema.json",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append("missing " + rel)
    profiles = json.loads((ROOT / "config/agents/AGT-001-task-profiles.json").read_text())["profiles"]
    if len(profiles) != 6:
        errors.append("profile count")
    if {p["agent_id"] for p in profiles} != {"AGT-001"}:
        errors.append("agent identity")
    corpus = (ROOT / "config/agents/AGT-001-task-profiles.json").read_text(errors="ignore")
    if "AGT-002" in corpus:
        errors.append("AGT-002 marker in runtime profile configuration")
    stage = (ROOT / required[0]).read_text()
    for heading in ("## 1. Context Carried Forward", "## 27. Stage Handoff Pack", "# Stage Consistency Audit"):
        if heading not in stage:
            errors.append("missing " + heading)
    for path in ROOT.glob("docs/architecture/diagrams/*.mmd"):
        if not re.search(r"^(flowchart|sequenceDiagram|stateDiagram)", path.read_text(), re.M):
            errors.append("Mermaid " + str(path))
    if errors:
        print("FAILED")
        for item in errors:
            print("-", item)
        return 1
    print("PASSED WITH RECORDED EXCEPTIONS")
    print("- required artefacts and stable IDs present")
    print("- exactly one AGT-001 in profiles")
    print("- no AGT-002 in JSON configuration")
    print("- Mermaid structurally checked, not CLI-rendered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
