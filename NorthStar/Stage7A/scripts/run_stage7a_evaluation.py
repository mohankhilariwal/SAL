#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from northstar_compliance.concurrency.evaluation import run_evaluations_sync


def main() -> None:
    results = run_evaluations_sync()
    payload = {
        "stage": "S07A",
        "architecture_version": "1.6.0",
        "results": results,
        "passed": all(item["passed"] for item in results),
    }
    output = Path(__file__).resolve().parents[1] / "reports" / "evaluation-report.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
