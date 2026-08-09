from __future__ import annotations
import json
from pathlib import Path
from northstar_compliance.evaluation.judge_bias.lab import BiasLab

ROOT = Path(__file__).resolve().parents[1]
lab = BiasLab(
    ROOT / "datasets/evaluation/judge-bias/v1.0.0/probe_families.jsonl",
    ROOT / "datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl",
)
errors = lab.validate()
policy = json.loads((ROOT / "config/evaluation/judge_bias/BIAS-LAB-POLICY-001.json").read_text())
assert policy["authority_effect"] == "none"
assert policy["live_model_allowed"] is False
assert policy["production_eligibility_allowed"] is False
schemas = list((ROOT / "schemas").glob("DATA-*.schema.json"))
assert len(schemas) == 10
for path in schemas:
    obj = json.loads(path.read_text())
    assert obj["$schema"].endswith("2020-12/schema")
if errors:
    raise SystemExit("FAILED\n" + "\n".join(errors))
print("PASSED: Stage 8C contracts, dataset, policy and schemas validate")
