from __future__ import annotations

import json
from collections import defaultdict

from _common import DATA, load_jsonl, write_report
from northstar_compliance.evaluation.judge.bias import measure_biases


def main() -> None:
    grouped = defaultdict(list)
    for row in load_jsonl(DATA / "bias_observations.jsonl"):
        grouped[row["judge_id"]].append(row)
    report = {judge_id: measure_biases(rows).__dict__ for judge_id, rows in sorted(grouped.items())}
    report["authority_effect"] = "none"
    path = write_report("stage8b-bias.json", report)
    print(path)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
