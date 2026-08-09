# 07 — Repository Manifest: Stage 10B Overlay

Version: `1.16.0`
Python target: `>=3.12,<3.14`; locally validated with Python `3.13.5`.

```text
northstar-agentic-compliance-stage10b-reliability-agentops/
├── .github/workflows/stage10b.yml
├── config/{agentops,deployment,reliability}/
├── deployment/{docker,kubernetes}/
├── docs/{adr,architecture/diagrams,references,runbooks,source-of-truth,stages}/
├── reports/
├── schemas/DATA-237..256.schema.json
├── scripts/
├── src/northstar_compliance/
│   ├── agentops/
│   ├── audit/
│   ├── common/
│   ├── deployment/
│   ├── integration/
│   ├── orchestration/
│   └── reliability/
├── tests/{chaos,integration,performance,security,unit}/
├── .env.example
├── README.md
└── pyproject.toml
```

Important entry points:

- `scripts/run_stage10b_demo.py`
- `scripts/run_stage10b_chaos.py`
- `scripts/validate_stage10b.py`
- `scripts/run_stage10b_evaluation_gates.py`
- `scripts/consistency_audit_stage10b.py`

The repository is a compatible Stage 10B overlay because the complete Stage 10A repository was not supplied.
