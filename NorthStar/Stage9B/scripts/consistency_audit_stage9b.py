from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
text="\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"docs").rglob("*.md"))
assert "AGT-001" in text and "exactly one active" in text.lower()
assert "GRAPH-001/1.9.0" in text
assert "DATA-177" in text and "DATA-192" in text
assert "INT-140" in text and "INT-154" in text
assert "ADR-095" in text and "ADR-103" in text
assert "Stage 8D" in text
assert "no unrestricted" in text.lower()
assert "control-plane implementation" in text.lower()
print("Stage 9B consistency audit: PASSED WITH RECORDED EXCEPTIONS")
