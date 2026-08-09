from pathlib import Path
from northstar_compliance.evaluation.judge_bias.lab import BiasLab

ROOT=Path(__file__).resolve().parents[2]
LAB=BiasLab(ROOT/"datasets/evaluation/judge-bias/v1.0.0/probe_families.jsonl",ROOT/"datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl")

# TEST-652..661

def test_lab_valid(): assert LAB.validate()==[]
def test_lab_probe_count(): assert len(LAB.probes)==23
def test_lab_observation_count(): assert len(LAB.observations)==3312
def test_report_advisory(): assert LAB.run()["authority_effect"]=="none"
def test_no_live_model(): assert LAB.run()["live_model_called"] is False
def test_no_route(): assert LAB.run()["model_route_activated"] is False
def test_biased_quarantined(): assert [r for r in LAB.run()["recommendations"] if r["judge_id"]=="JUDGE-BIASED"][0]["status"]=="quarantine"
def test_control_not_production_eligible(): assert [r for r in LAB.run()["recommendations"] if r["judge_id"]=="JUDGE-CONTROL"][0]["production_eligible"] is False
def test_special_metrics_exist(): assert LAB.run()["special_metrics"]
def test_report_digest_stable(): assert LAB.run()["report_digest"]==LAB.run()["report_digest"]
