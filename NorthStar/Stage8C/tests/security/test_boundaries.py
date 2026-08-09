import json
from pathlib import Path
from northstar_compliance.evaluation.judge_bias.lab import BiasLab

ROOT=Path(__file__).resolve().parents[2]
REPORT=BiasLab(ROOT/"datasets/evaluation/judge-bias/v1.0.0/probe_families.jsonl",ROOT/"datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl").run()

# TEST-662..670

def test_all_estimates_advisory(): assert all(e["authority_effect"]=="none" for e in REPORT["estimates"])
def test_all_recommendations_advisory(): assert all(r["authority_effect"]=="none" for r in REPORT["recommendations"])
def test_no_production_eligible(): assert not any(r["production_eligible"] for r in REPORT["recommendations"])
def test_route_inactive(): assert REPORT["model_route_activated"] is False
def test_critical_override_quarantines(): assert any(e["classification"]=="quarantine" for e in REPORT["estimates"])
def test_stage8a_sealed_absent_from_dataset():
    text=(ROOT/"datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl").read_text(); assert '"sealed_stage8a_case": true' not in text

def test_no_secret_env_names_in_policy():
    text=(ROOT/"config/evaluation/judge_bias/BIAS-LAB-POLICY-001.json").read_text().lower(); assert "api_key" not in text and "secret" not in text

def test_no_tool_ids_in_runtime_code():
    text=''.join(p.read_text() for p in (ROOT/"src/northstar_compliance/evaluation/judge_bias").glob("*.py")); assert "TOOL-001" not in text

def test_no_data106_mutation():
    text=''.join(p.read_text() for p in ROOT.rglob("*.py")); assert ("DATA-" + "106") not in text
