from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import json

from _common import CONFIG, DATA, load_jsonl, write_report
from northstar_compliance.evaluation.judge.bias import measure_biases
from northstar_compliance.evaluation.judge.calibration import calibrate_judge
from northstar_compliance.evaluation.judge.io import envelope_from_case, human_label_from_row, load_policy
from northstar_compliance.evaluation.judge.validation import parse_and_validate_output


def main() -> None:
    policy = load_policy(CONFIG)
    cases = {row["case_id"]: envelope_from_case(row) for row in load_jsonl(DATA / "calibration_cases.jsonl")}
    labels = {row["case_id"]: human_label_from_row(row) for row in load_jsonl(DATA / "human_labels.jsonl")}
    replay_rows = load_jsonl(DATA / "judge_replays.jsonl")
    bias_rows = defaultdict(list)
    for row in load_jsonl(DATA / "bias_observations.jsonl"):
        bias_rows[row["judge_id"]].append(row)

    verdicts = defaultdict(dict)
    invalid = defaultdict(list)
    for row in replay_rows:
        case = cases[row["case_id"]]
        output = deepcopy(row["output"])
        output["envelope_digest"] = case.digest
        raw = json.dumps(output, separators=(",", ":"), ensure_ascii=False)
        try:
            verdicts[row["judge_id"]][row["case_id"]] = parse_and_validate_output(raw, case)
        except ValueError as exc:
            invalid[row["judge_id"]].append({"case_id": row["case_id"], "error": str(exc)})
            verdicts[row["judge_id"]][row["case_id"]] = None

    reports = {}
    for judge_id in sorted(bias_rows):
        bias = measure_biases(bias_rows[judge_id])
        reports[judge_id] = calibrate_judge(
            judge_id=judge_id,
            dataset_id="JDS-001/1.0.0",
            human_labels=labels,
            verdicts=verdicts[judge_id],
            bias=bias,
            policy=policy,
        ).__dict__
        reports[judge_id]["invalid_outputs"] = invalid[judge_id]
    reports["authority_effect"] = "none"
    reports["production_claim"] = False
    reports["live_model_called"] = False
    path = write_report("stage8b-calibration.json", reports)
    print(path)
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
