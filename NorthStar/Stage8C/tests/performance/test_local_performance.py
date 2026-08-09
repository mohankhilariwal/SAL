from pathlib import Path
from time import perf_counter
from northstar_compliance.evaluation.judge_bias.lab import BiasLab

ROOT=Path(__file__).resolve().parents[2]

# TEST-683..684

def test_local_lab_under_two_seconds():
    t=perf_counter(); BiasLab(ROOT/"datasets/evaluation/judge-bias/v1.0.0/probe_families.jsonl",ROOT/"datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl").run(); assert perf_counter()-t<2.0

def test_dataset_under_five_mb(): assert (ROOT/"datasets/evaluation/judge-bias/v1.0.0/replay_observations.jsonl").stat().st_size<5_000_000
