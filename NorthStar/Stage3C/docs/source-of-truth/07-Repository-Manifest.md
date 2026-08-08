# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `0.7.0`  
**Python:** tested on `3.13.5`; target `>=3.11,<3.15`  
**Test runner:** pytest `9.0.2`  
**Runtime dependencies:** Python standard library only.

## Important tree

```text
northstar-agentic-compliance/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── config/runtime/stage3c-budget.json
├── schemas/DATA-045...DATA-052*.schema.json
├── docs/
│   ├── adr/ADR-024...ADR-026*.md
│   ├── architecture/diagrams/stage-3c-*.mmd
│   ├── references/Stage-3C-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-3C-Loop-Failures-Recovery-and-Budgets.md
├── src/northstar_compliance/
│   ├── agent/models.py
│   ├── agent/budgets.py
│   ├── agent/cancellation.py
│   ├── agent/decision.py
│   ├── agent/recovery.py
│   ├── agent/termination.py
│   ├── agent/runtime.py
│   ├── agent/factory.py
│   ├── tools/gateway.py
│   ├── tools/local_tools.py
│   └── state/checkpoint.py
├── scripts/run_stage3c_demo.py
├── scripts/run_stage3c_evaluation.py
├── scripts/validate_stage3c.py
├── scripts/consistency_audit_stage3c.py
└── tests/{unit,integration,security,evaluation}/
```

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python -m compileall -q src scripts tests
python scripts/run_stage3c_demo.py
python scripts/run_stage3c_evaluation.py
python scripts/validate_stage3c.py
python scripts/consistency_audit_stage3c.py
```

## Compatibility and migration

- `DATA-009` schema `1.1.0` is a backward-compatible Stage 3C extension in this overlay.
- Existing tool IDs/versions remain unchanged.
- Existing S03B final outcome fields remain present.
- A `0.6.0` terminal artifact is not automatically a resumable checkpoint; only `DATA-050` schema `1.0.0` is resumable.
- No files are retired.
- The exact prior repository archive was unavailable; `ISS-029` applies.
