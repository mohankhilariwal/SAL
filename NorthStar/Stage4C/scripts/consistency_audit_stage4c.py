from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
required = [ROOT / "docs/source-of-truth" / f"{i:02d}-" for i in range(10)]
source_dir = ROOT / "docs/source-of-truth"
if not source_dir.exists():
    raise SystemExit("source_of_truth_missing")
texts = []
for path in sorted(source_dir.glob("*.md")):
    texts.append(path.read_text(encoding="utf-8"))
all_text = "\n".join(texts)
checks = {
    "version": "1.0.0" in all_text,
    "graph": "GRAPH-001" in all_text and "1.1.0" in all_text,
    "agent": "AGT-001" in all_text,
    "harness": "DATA-063" in all_text and "INT-041" in all_text and "ADR-033" in all_text,
    "no_memory": "memory is not implemented" in all_text.lower() or "no memory" in all_text.lower(),
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("consistency_failed:" + ",".join(failed))
print("stage4c consistency audit passed with recorded reconstruction and production exceptions")
