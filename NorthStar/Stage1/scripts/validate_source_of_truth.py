from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOT = ROOT / "docs/source-of-truth"
FILES = [
    "00-Project-Constitution.md",
    "01-Business-and-User-Story-Baseline.md",
    "02-Requirements-Register.md",
    "03-Architecture-Baseline.md",
    "04-Component-and-Agent-Catalogue.md",
    "05-Data-and-Schema-Register.md",
    "06-ADR-Register.md",
    "07-Repository-Manifest.md",
    "08-Risk-Assumption-and-Issue-Register.md",
    "09-Stage-Handoff-Pack.md",
]


def main() -> int:
    missing = [name for name in FILES if not (SOT / name).is_file()]
    if missing:
        raise SystemExit(f"Missing source-of-truth files: {missing}")
    combined = "\n".join((SOT / name).read_text() for name in FILES)
    for component in range(1, 12):
        token = f"CMP-{component:03d}"
        if token not in combined:
            raise SystemExit(f"Missing accepted component: {token}")
    if re.search(r"\b(?:AGT|TOOL)-\d{3}\b", combined):
        raise SystemExit("S01 must not allocate agent or tool identifiers")
    for adr in range(1, 11):
        token = f"ADR-{adr:03d}"
        if token not in combined:
            raise SystemExit(f"Missing ADR: {token}")
    handoff = (SOT / FILES[-1]).read_text()
    if "Stage 2" not in handoff or "Retrieval" not in handoff:
        raise SystemExit("Handoff must authorize only the retrieval stage")
    print("source-of-truth validation: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
