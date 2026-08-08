from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> None:
    root = Path(__file__).parents[1]
    required = [root / "docs" / "source-of-truth" / f"{n:02d}-{name}.md" for n, name in [
        (0,"Project-Constitution"),(1,"Business-and-User-Story-Baseline"),(2,"Requirements-Register"),(3,"Architecture-Baseline"),(4,"Component-and-Agent-Catalogue"),(5,"Data-and-Schema-Register"),(6,"ADR-Register"),(7,"Repository-Manifest"),(8,"Risk-Assumption-and-Issue-Register"),(9,"Stage-Handoff-Pack")]]
    missing = [str(p) for p in required if not p.exists() or not p.read_text().strip()]
    if missing:
        raise SystemExit("Missing source-of-truth files: " + ", ".join(missing))
    meta = json.loads((root / "config" / "tools" / "tool-descriptor.schema.json").read_text())
    validator = Draft202012Validator(meta)
    descriptors = sorted((root / "config" / "tools").glob("TOOL-*.json"))
    if len(descriptors) != 6:
        raise SystemExit("Expected six tool descriptors")
    for path in descriptors:
        validator.validate(json.loads(path.read_text()))
    combined = "\n".join(p.read_text() for p in required)
    for token in ["0.6.0", "AGT-001", "DATA-009", "DATA-041", "INT-021", "ADR-022", "TEST-074", "EVAL-018"]:
        if token not in combined:
            raise SystemExit(f"Missing token {token}")
    if re.search(r"AGT-(?!001)\d{3}", combined):
        raise SystemExit("Unexpected additional agent ID")
    print("Stage 3B structural validation: PASSED")


if __name__ == "__main__":
    main()
