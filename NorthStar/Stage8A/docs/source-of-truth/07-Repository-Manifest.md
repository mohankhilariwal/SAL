# 07 — Repository Manifest (1.9.0 Overlay)

```text
northstar-agentic-compliance-stage8a/
├── config/evaluation/{graders,suites}/
├── datasets/evaluation/v1.0.0/
├── docs/
│   ├── adr/ADR-072..076-*.md
│   ├── architecture/diagrams/{GRAPH-001-v1.5.0,stage-8a-*}.mmd
│   ├── references/stage8a-primary-sources.md
│   ├── source-of-truth/00..09-*.md
│   └── stages/NorthStar-Stage-8A-Evaluation-Architecture-and-Datasets.md
├── reports/{stage8a-demo,stage8a-evaluation,stage8a-contamination}.json
├── schemas/DATA-131..142.schema.json
├── scripts/{run_stage8a_demo,run_stage8a_evaluation,generate_dataset_manifest,validate_stage8a,consistency_audit_stage8a}.py
├── src/northstar_compliance/evaluation/{models,datasets,graders,registry,harness,sampling,gates,io}.py
├── tests/{unit,integration,security,evaluation,performance}/
├── README.md
└── pyproject.toml
```

- Python: `>=3.11,<3.15`; executed `3.13.5`.
- Runtime dependencies: standard library only.
- Test dependency: pytest `9.0.2`.
- Local command: `export PYTHONPATH=src` before scripts/tests in offline environments.
- No environment variables or external services required.
