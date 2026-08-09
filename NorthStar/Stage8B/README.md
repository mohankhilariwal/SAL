# NorthStar Stage 8B - LLM-as-a-Judge

This repository is a compatible `1.10.0` reconstruction overlay on the Stage 8A `1.9.0` handoff. It implements a provider-neutral, advisory LLM-judge workflow, a synthetic replay-based calibration dataset, bias probes, structured output validation, panel aggregation and payload-minimized evidence export.

It does **not** select or route a production model, call a paid model, mutate protected workflow state, approve/finalize a regulatory assessment, expose sealed Stage 8A tests, or implement CI/CD deployment promotion.

## Run

```bash
export PYTHONPATH=src
python scripts/validate_stage8b.py
python scripts/run_stage8b_demo.py
python scripts/run_stage8b_calibration.py
python scripts/run_stage8b_bias_lab.py
python scripts/run_stage8b_evaluation_gates.py
pytest
python scripts/consistency_audit_stage8b.py
```

The local lab uses immutable synthetic calibration fixtures and replayed judge outputs. Replace `ReplayJudgeAdapter` only through an approved provider adapter after a separate model-selection/routing decision.
