from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = [
    "src/northstar_compliance/agent/budgets.py",
    "src/northstar_compliance/agent/cancellation.py",
    "src/northstar_compliance/agent/recovery.py",
    "src/northstar_compliance/state/checkpoint.py",
    "docs/source-of-truth/00-Project-Constitution.md",
    "docs/source-of-truth/09-Stage-Handoff-Pack.md",
    "docs/stages/Stage-3C-Loop-Failures-Recovery-and-Budgets.md",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    raise SystemExit(f"Missing required files: {missing}")
text = (root / "src/northstar_compliance/agent/runtime.py").read_text()
assert 'AGENT_ID = "AGT-001"' in text
assert 'ALLOWED_TOOLS' in text
assert "preliminary_grounded_unapproved" in (root / "src/northstar_compliance/agent/models.py").read_text()
for forbidden in ["AGT-002", "src/northstar_compliance/graph", "src/northstar_compliance/memory"]:
    assert forbidden not in "\n".join(str(p) for p in root.rglob("*"))
print("Stage 3C structural validation PASSED.")
