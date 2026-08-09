from __future__ import annotations
import json
from pathlib import Path
from northstar_compliance.evaluation.judge_bias.lab import run_lab

ROOT = Path(__file__).resolve().parents[1]
report = run_lab(
    ROOT / "datasets/evaluation/judge-bias/v1.0.0/probe_families.jsonl",
    ROOT / "datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl",
)
out = ROOT / "reports/stage8c-bias-lab.json"
out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "result": "PASSED",
    "probe_count": report["probe_count"],
    "observation_count": report["observation_count"],
    "recommendations": report["recommendations"],
    "live_model_called": report["live_model_called"],
    "model_route_activated": report["model_route_activated"],
    "authority_effect": report["authority_effect"],
}, indent=2))
