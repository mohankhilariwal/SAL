# NorthStar Stage 8C - Judge-Bias Laboratory

Compatible reconstruction overlay extending the S08B `1.10.0` handoff to architecture/repository `1.11.0` and `GRAPH-001/1.7.0`.

This package implements a local, provider-neutral, replay-only judge-bias laboratory. It does **not** call a live model, activate a route, establish production thresholds, approve a regulatory decision or implement CI/CD deployment gates.

```bash
export PYTHONPATH=src
python scripts/validate_stage8c.py
python scripts/run_stage8c_bias_lab.py
python scripts/run_stage8c_evaluation_gates.py
pytest -q
python scripts/consistency_audit_stage8c.py
```
