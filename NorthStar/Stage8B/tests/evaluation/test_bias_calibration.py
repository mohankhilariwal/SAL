import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

from northstar_compliance.evaluation.judge.bias import measure_biases
from northstar_compliance.evaluation.judge.calibration import calibrate_judge
from northstar_compliance.evaluation.judge.io import envelope_from_case, human_label_from_row, load_policy
from northstar_compliance.evaluation.judge.validation import parse_and_validate_output

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets/evaluation/judge-calibration/v1.0.0"

def load(name):
    return [json.loads(x) for x in (DATA/name).read_text(encoding="utf-8").splitlines() if x]


def report(judge_id):
    cases = {r["case_id"]: envelope_from_case(r) for r in load("calibration_cases.jsonl")}
    labels = {r["case_id"]: human_label_from_row(r) for r in load("human_labels.jsonl")}
    verdicts = {}
    for row in load("judge_replays.jsonl"):
        if row["judge_id"] != judge_id: continue
        output = deepcopy(row["output"])
        output["envelope_digest"] = cases[row["case_id"]].digest
        try:
            verdicts[row["case_id"]] = parse_and_validate_output(json.dumps(output), cases[row["case_id"]])
        except ValueError:
            verdicts[row["case_id"]] = None
    bias = measure_biases([r for r in load("bias_observations.jsonl") if r["judge_id"] == judge_id])
    policy = load_policy(ROOT / "config/evaluation/judges/JUDGE-POLICY-001.json")
    return calibrate_judge(judge_id=judge_id, dataset_id="JDS-001/1.0.0", human_labels=labels, verdicts=verdicts, bias=bias, policy=policy), bias


def test_595_biased_judge_ineligible():
    r,_ = report("JUDGE-A")
    assert not r.eligible


def test_596_calibrated_judge_b_eligible():
    r,_ = report("JUDGE-B")
    assert r.eligible


def test_597_calibrated_judge_c_eligible():
    r,_ = report("JUDGE-C")
    assert r.eligible


def test_598_biased_position_flip_detected():
    _,b = report("JUDGE-A")
    assert b.position_flip_rate > 0


def test_599_calibrated_position_stable():
    _,b = report("JUDGE-B")
    assert b.position_flip_rate == 0


def test_600_injection_asr_detected():
    _,b = report("JUDGE-A")
    assert b.injection_asr == 1


def test_601_calibrated_injection_asr_zero():
    _,b = report("JUDGE-B")
    assert b.injection_asr == 0


def test_602_language_gap_detected():
    _,b = report("JUDGE-A")
    assert b.language_gap == 1


def test_603_tail_recall_detected():
    _,b = report("JUDGE-A")
    assert b.tail_recall < 1


def test_604_report_authority_none():
    r,_ = report("JUDGE-B")
    assert r.authority_effect == "none"
