# 07 — Repository Manifest — Version 1.7.0 overlay

```text
northstar-agentic-compliance-stage7b/
├── config/workloads/
│   ├── WP-001.json ... WP-008.json
│   └── service-model-local.json
├── docs/
│   ├── adr/ADR-062...ADR-066-*.md
│   ├── architecture/diagrams/
│   ├── references/stage7b-primary-sources.md
│   ├── source-of-truth/00...09-*.md
│   └── stages/Stage-7B-ISL-OSL-and-Workload-Modelling.md
├── reports/
├── schemas/DATA-114...DATA-121-*.schema.json
├── scripts/
│   ├── run_stage7b_demo.py
│   ├── run_stage7b_benchmark.py
│   ├── run_stage7b_capacity_plan.py
│   ├── run_stage7b_evaluation.py
│   ├── validate_stage7b.py
│   └── consistency_audit_stage7b.py
├── src/northstar_compliance/workload/
│   ├── adapters.py
│   ├── evaluation.py
│   ├── io.py
│   ├── metrics.py
│   ├── models.py
│   ├── sampling.py
│   └── simulation.py
├── tests/{unit,integration,security,evaluation,performance}/
├── README.md
└── pyproject.toml
```

- Python: `>=3.11,<3.15`
- Runtime dependencies: standard library only
- Test dependency: `pytest==9.0.2`
- Tested interpreter: recorded in `reports/environment.txt`
