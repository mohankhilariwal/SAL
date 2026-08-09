import json
from pathlib import Path
import pytest

from northstar_compliance.evaluation.judge.io import envelope_from_case
from northstar_compliance.evaluation.judge.prompt import build_judge_prompt
from northstar_compliance.evaluation.judge.validation import detect_injection

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets/evaluation/judge-calibration/v1.0.0/calibration_cases.jsonl"
CASES = [json.loads(x) for x in DATA.read_text().splitlines() if x]

@pytest.mark.parametrize("case_id", ["JCAL-019","JCAL-020"])
def test_609_610_injection_fixtures_detected(case_id):
    row=next(x for x in CASES if x["case_id"]==case_id)
    assert detect_injection(row["candidate_text"])


def test_611_prompt_does_not_request_chain_of_thought():
    env=envelope_from_case(CASES[0])
    prompt=build_judge_prompt(env)
    assert "not hidden chain-of-thought" in prompt


def test_612_no_sealed_stage8a_material():
    assert all(not x["metadata"]["sealed_test_material"] for x in CASES)


def test_613_all_cases_synthetic():
    assert all(x["metadata"]["synthetic"] for x in CASES)


def test_614_authorization_scope_present():
    assert all(x["authorization_scope"] for x in CASES)


def test_615_no_tool_or_route_fields():
    forbidden={"tool_call","route","approval","finalization"}
    assert all(not forbidden.intersection(x) for x in CASES)


def test_616_candidate_identity_hidden_except_probe():
    for x in CASES:
        if x["candidate_model_identity"] is not None:
            assert x["metadata"].get("self_preference_probe")
