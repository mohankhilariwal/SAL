# 07 — Repository Manifest

**Version:** 1.14.0

```text
northstar-agentic-compliance-stage9c-guardrails-control-plane/
├── config/guardrails/
├── docs/
│   ├── adr/ADR-104..113-*.md
│   ├── architecture/diagrams/*.mmd
│   ├── references/stage9c-primary-sources.md
│   ├── source-of-truth/00..09-*.md
│   ├── stages/NorthStar-Stage-9C-Guardrails-Governance-and-Control-Plane.md
│   └── threat-model/TM-001-v1.2.0.md
├── reports/
├── schemas/DATA-193..216.schema.json
├── scripts/
├── src/northstar_compliance/guardrails/
├── tests/{unit,integration,security,performance}/
├── README.md
└── pyproject.toml
```

## Entry points

- `scripts/run_stage9c_demo.py`
- `scripts/validate_stage9c.py`
- `scripts/run_stage9c_evaluation_gates.py`
- `scripts/consistency_audit_stage9c.py`

## Environment

Python `>=3.11,<3.15`; executed with Python 3.13.5, pytest 9.0.2, jsonschema 4.26.0. No network/paid service required.

## Commands

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_stage9c_demo.py
PYTHONPATH=src python scripts/validate_stage9c.py
PYTHONPATH=src python scripts/run_stage9c_evaluation_gates.py
PYTHONPATH=src python scripts/consistency_audit_stage9c.py
```

This is a compatible overlay, not a byte-exact historical merge.
