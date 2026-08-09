from __future__ import annotations

import json
from pathlib import Path

from _common import CONFIG, DATA, load_jsonl, write_report
from northstar_compliance.evaluation.judge.io import envelope_from_case, load_policy
from northstar_compliance.evaluation.judge.prompt import build_judge_prompt


def main() -> None:
    policy = load_policy(CONFIG)
    case = envelope_from_case(load_jsonl(DATA / "calibration_cases.jsonl")[0])
    prompt = build_judge_prompt(case)
    result = {
        "stage": "S08B",
        "architecture_version": "1.10.0",
        "policy_id": policy.policy_id,
        "case_id": case.case_id,
        "envelope_digest": case.digest,
        "prompt_length_chars": len(prompt),
        "candidate_is_json_encoded": json.dumps(case.candidate_text) in prompt,
        "authority_effect": "none",
        "live_model_called": False,
        "model_route_activated": False,
    }
    path = write_report("stage8b-demo.json", result)
    print(path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
