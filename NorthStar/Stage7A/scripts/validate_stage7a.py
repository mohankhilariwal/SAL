#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = [
        ROOT / "config/concurrency/policy.json",
        ROOT / "schemas/DATA-106.schema.json",
        ROOT / "schemas/DATA-113.schema.json",
        ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md",
        ROOT / "docs/architecture/diagrams/stage7a-cumulative-architecture.mmd",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")
    policy = json.loads((ROOT / "config/concurrency/policy.json").read_text())
    assert policy["owners"]["orchestration"] == "CMP-003"
    assert policy["owners"]["authority"] == "CMP-007"
    assert set(policy["allowed_work_kinds"]) == {"read_only", "pure_compute"}
    for path in (ROOT / "src").rglob("*.py"):
        py_compile.compile(str(path), doraise=True)
    print(json.dumps({"validated": True, "python": sys.version.split()[0], "files": len(required)}, indent=2))


if __name__ == "__main__":
    main()
