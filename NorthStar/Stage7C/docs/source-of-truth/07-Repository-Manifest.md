# 07 — Repository Manifest: Stage 7C Overlay

- **Repository version:** `1.8.0`
- **Python:** `>=3.11,<3.15`
- **Executed:** Python `3.13.5`
- **Runtime dependencies:** standard library
- **Test dependency:** `pytest==9.0.2`

```text
northstar-agentic-compliance-stage7c/
├── config/
│   ├── inference/{INF-001,INF-002,INF-003,service-rates-local}.json
│   └── workloads/WP-001...WP-008.json
├── docs/
│   ├── adr/ADR-067...ADR-071.md
│   ├── architecture/diagrams/*.mmd
│   ├── references/stage7c-primary-sources.md
│   ├── source-of-truth/00...09-*.md
│   └── stages/NorthStar-Stage-7C-Inference-Optimization-and-Speculative-Decoding.md
├── reports/
├── schemas/DATA-122...DATA-130.schema.json
├── scripts/
│   ├── run_stage7c_demo.py
│   ├── run_stage7c_inference_plan.py
│   ├── run_stage7c_speculative_benchmark.py
│   ├── run_stage7c_evaluation.py
│   ├── validate_stage7c.py
│   └── consistency_audit_stage7c.py
├── src/northstar_compliance/inference/
│   ├── adapters.py
│   ├── evaluation.py
│   ├── io.py
│   ├── models.py
│   ├── planner.py
│   ├── simulation.py
│   └── speculative.py
├── tests/{unit,integration,security,evaluation,performance}/
├── README.md
└── pyproject.toml
```

## Commands

```bash
python -m compileall -q src tests scripts
pytest -q
python scripts/run_stage7c_inference_plan.py
python scripts/run_stage7c_demo.py
python scripts/run_stage7c_speculative_benchmark.py
python scripts/run_stage7c_evaluation.py
python scripts/validate_stage7c.py
python scripts/consistency_audit_stage7c.py
```

This is a compatible reconstruction overlay, not a byte-exact merge with the absent `1.7.0` repository (`ISS-096`).
