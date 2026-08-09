import json
from copy import deepcopy
from pathlib import Path

from northstar_compliance.evaluation.judge.io import envelope_from_case, load_policy
from northstar_compliance.evaluation.judge.models import JudgeCalibrationReport
from northstar_compliance.evaluation.judge.panel import aggregate_panel
from northstar_compliance.evaluation.judge.validation import parse_and_validate_output

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets/evaluation/judge-calibration/v1.0.0"

def load(name): return [json.loads(x) for x in (DATA/name).read_text().splitlines() if x]

def verdict(judge_id, case_id):
    case = envelope_from_case(next(r for r in load("calibration_cases.jsonl") if r["case_id"]==case_id))
    row = next(r for r in load("judge_replays.jsonl") if r["judge_id"]==judge_id and r["case_id"]==case_id)
    out = deepcopy(row["output"]); out["envelope_digest"] = case.digest
    return parse_and_validate_output(json.dumps(out), case)

def cal(judge_id, eligible=True):
    return JudgeCalibrationReport(judge_id,"JDS",1,1,1,1,1,1,1,0,0,0,0,0,1,eligible,(),24,"none")


def test_605_panel_recommends_pass_only_on_unanimous_eligible():
    p = load_policy(ROOT/"config/evaluation/judges/JUDGE-POLICY-001.json")
    vs=[verdict("JUDGE-B","JCAL-001"),verdict("JUDGE-C","JCAL-001")]
    result=aggregate_panel(panel_id="PANEL-1",case_id="JCAL-001",verdicts=vs,calibration={"JUDGE-B":cal("JUDGE-B"),"JUDGE-C":cal("JUDGE-C")},policy=p)
    assert result.outcome=="recommend_pass" and result.authority_effect=="none"


def test_606_panel_requires_human_on_disagreement():
    p = load_policy(ROOT/"config/evaluation/judges/JUDGE-POLICY-001.json")
    pass_v=verdict("JUDGE-B","JCAL-001")
    fail_v=verdict("JUDGE-C","JCAL-002")
    # Align case id for a synthetic aggregation conflict.
    object.__setattr__(fail_v,"case_id","JCAL-001")
    result=aggregate_panel(panel_id="PANEL-2",case_id="JCAL-001",verdicts=[pass_v,fail_v],calibration={"JUDGE-B":cal("JUDGE-B"),"JUDGE-C":cal("JUDGE-C")},policy=p)
    assert result.outcome=="human_review"


def test_607_panel_blocks_mandatory_failure():
    p = load_policy(ROOT/"config/evaluation/judges/JUDGE-POLICY-001.json")
    result=aggregate_panel(panel_id="PANEL-3",case_id="JCAL-001",verdicts=[],calibration={},policy=p,mandatory_failure=True)
    assert result.outcome=="blocked"


def test_608_panel_rejects_insufficient_eligible_judges():
    p = load_policy(ROOT/"config/evaluation/judges/JUDGE-POLICY-001.json")
    v=verdict("JUDGE-B","JCAL-001")
    result=aggregate_panel(panel_id="PANEL-4",case_id="JCAL-001",verdicts=[v],calibration={"JUDGE-B":cal("JUDGE-B")},policy=p)
    assert result.requires_human_review
