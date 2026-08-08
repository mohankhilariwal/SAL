from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
texts = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "docs").rglob("*.md"))
for cid, name in {
    "CMP-001":"Analyst Experience Portal", "CMP-002":"Regulatory Intake Boundary",
    "CMP-003":"Case and Workflow Orchestration Boundary", "CMP-004":"Knowledge and Evidence Access Boundary",
    "CMP-005":"Enterprise Integration Boundary", "CMP-006":"Human Review and Approval Boundary",
    "CMP-007":"Identity, Authorization and Policy Boundary", "CMP-008":"Evaluation and Assurance Boundary",
    "CMP-009":"Observability and Audit Boundary", "CMP-010":"Runtime and Deployment Boundary",
    "CMP-011":"Source-of-Truth Governance Pack",
}.items():
    assert cid in texts and name in texts
for item in ["AGT-001", *[f"TOOL-{i:03d}" for i in range(1,7)], *[f"DATA-{i:03d}" for i in range(45,58)], *[f"INT-{i:03d}" for i in range(26,36)], "ADR-027", "ADR-028", "ADR-029"]:
    assert item in texts, item
assert not (ROOT / "src/northstar_compliance/memory").exists()
assert not (ROOT / "src/northstar_compliance/harness").exists()
assert not (ROOT / "src/northstar_compliance/agents").exists()
assert texts.count("Regulatory Impact Assessment Agent") >= 2
print("PASSED WITH RECORDED EXCEPTIONS: ISS-014, ISS-015, ISS-021–ISS-035 and inherited production gaps")
