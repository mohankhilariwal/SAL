# NorthStar Agentic Compliance — Stage 7B

This repository is the Stage 7B reconstruction overlay for **ISL, OSL and Workload Modelling**.

## What it does

- Defines seven executable NorthStar workload profiles and one inactive future multi-agent placeholder.
- Generates reproducible joint ISL/OSL and arrival samples.
- Runs a local, deterministic capacity-planning simulation.
- Calculates queue, TTFT, ITL/TPOT, end-to-end latency and throughput metrics.
- Produces advisory capacity envelopes and external benchmark command plans.
- Preserves Stage 7A authority, state, human approval, memory and concurrency boundaries.

## Important limitation

The simulator is planning evidence only. It does not model a real inference server, GPU, batching scheduler or KV cache. Do not use its output as a production limit.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
python scripts/validate_stage7b.py
python scripts/run_stage7b_demo.py
python scripts/run_stage7b_capacity_plan.py
python scripts/run_stage7b_evaluation.py --request-rate 0.2
pytest -q
python scripts/consistency_audit_stage7b.py
```

See `docs/stages/Stage-7B-ISL-OSL-and-Workload-Modelling.md` for the complete stage.
