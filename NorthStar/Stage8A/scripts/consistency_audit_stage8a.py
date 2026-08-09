from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
required = [
    "docs/source-of-truth/00-Project-Constitution.md",
    "docs/source-of-truth/01-Business-and-User-Story-Baseline.md",
    "docs/source-of-truth/02-Requirements-Register.md",
    "docs/source-of-truth/03-Architecture-Baseline.md",
    "docs/source-of-truth/04-Component-and-Agent-Catalogue.md",
    "docs/source-of-truth/05-Data-and-Schema-Register.md",
    "docs/source-of-truth/06-ADR-Register.md",
    "docs/source-of-truth/07-Repository-Manifest.md",
    "docs/source-of-truth/08-Risk-Assumption-and-Issue-Register.md",
    "docs/source-of-truth/09-Stage-Handoff-Pack.md",
    "docs/stages/NorthStar-Stage-8A-Evaluation-Architecture-and-Datasets.md",
]
missing = [p for p in required if not (ROOT / p).exists()]
assert not missing, missing
combined = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in required)
for token in ["AGT-001", "GRAPH-001/1.5.0", "DATA-131", "DATA-142", "INT-103", "INT-111", "ADR-072", "ADR-076", "WP-008", "ISS-114"]:
    assert token in combined, token
assert combined.count("Only active agent") >= 1
assert ("no automatic `DATA-106` mutation" in combined or "cannot mutate `DATA-106` automatically" in combined)
assert "semantic regulatory-answer caching remains prohibited" in combined
print("Stage 8A consistency audit passed with recorded exceptions ISS-096 and ISS-114–122")
