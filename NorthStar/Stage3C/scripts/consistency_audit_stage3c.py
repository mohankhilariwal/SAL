from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
all_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*.md"))
assert "AGT-001" in all_text
assert "TOOL-001" in all_text and "TOOL-006" in all_text
assert "DATA-052" in all_text and "INT-030" in all_text
assert "ADR-026" in all_text
assert "0.7.0" in all_text
assert "preliminary_grounded_unapproved" in all_text
assert not (root / "src/northstar_compliance/graph").exists()
assert not (root / "src/northstar_compliance/memory").exists()
assert len(list((root / "docs/source-of-truth").glob("*.md"))) == 10
print("PASSED WITH RECORDED EXCEPTIONS: ISS-014, ISS-015, ISS-021-ISS-031 and inherited production gaps.")
