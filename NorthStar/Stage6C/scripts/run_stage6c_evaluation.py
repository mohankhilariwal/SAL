from __future__ import annotations

import json
from pathlib import Path

from northstar_compliance.interoperability.evaluation import run_evaluations


def main() -> None:
    records = run_evaluations()
    report = {
        "stage": "S06C",
        "architectureVersion": "1.5.0",
        "passed": all(item["passed"] for item in records),
        "evaluations": records,
    }
    path = Path("reports/stage6c-evaluation.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
