from __future__ import annotations

import json
from pathlib import Path

from _common import CONFIG, DATA, ROOT, load_jsonl
from northstar_compliance.evaluation.judge.io import envelope_from_case, load_policy
from northstar_compliance.evaluation.judge.prompt import build_judge_prompt


def main() -> None:
    policy = load_policy(CONFIG)
    assert policy.authority_effect == "none"
    cases = load_jsonl(DATA / "calibration_cases.jsonl")
    labels = load_jsonl(DATA / "human_labels.jsonl")
    assert len(cases) == 24 == len(labels)
    assert {x["case_id"] for x in cases} == {x["case_id"] for x in labels}
    assert all(x["metadata"]["synthetic"] for x in cases)
    assert all(not x["metadata"]["sealed_test_material"] for x in cases)
    for row in cases:
        env = envelope_from_case(row)
        prompt = build_judge_prompt(env)
        assert env.candidate_text in json.loads(prompt.split("BEGIN_UNTRUSTED_EVALUATION_ENVELOPE\n",1)[1].split("\nEND_UNTRUSTED_EVALUATION_ENVELOPE",1)[0])["candidate_text"]
        assert env.authority_effect == "none"
    for num in range(143, 155):
        assert (ROOT / f"schemas/DATA-{num}.schema.json").exists()
    print("STAGE8B VALIDATION PASSED")


if __name__ == "__main__":
    main()
