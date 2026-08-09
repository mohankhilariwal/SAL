# 07 — Repository Manifest (Reconstructed 1.6.0 Overlay)

## Repository

`northstar-agentic-compliance-stage7a/` is a compatible reconstruction overlay of the evolving NorthStar repository.

## Important entry points

- `scripts/run_stage7a_demo.py`
- `scripts/run_stage7a_evaluation.py`
- `scripts/benchmark_stage7a.py`
- `scripts/validate_stage7a.py`
- `scripts/consistency_audit_stage7a.py`

## Stage tree

```text
config/concurrency/policy.json
docs/adr/ADR-056.md ... ADR-061.md
docs/architecture/diagrams/stage7a-*.mmd
docs/source-of-truth/00-Project-Constitution.md ... 09-Stage-Handoff-Pack.md
docs/stages/Stage-7A-Concurrency-and-Distributed-Execution.md
reports/{demo-output,evaluation-report,benchmark-report,test-report,consistency-audit-report}.*
schemas/DATA-106.schema.json ... DATA-113.schema.json
scripts/*.py
src/northstar_compliance/concurrency/*.py
tests/{unit,integration,security,evaluation,performance}/*.py
README.md
pyproject.toml
```

## Runtime compatibility

- Python target: `>=3.11,<3.15`
- Executed Python: `3.13.5`
- Runtime dependencies: Python standard library
- Development dependency: pytest `9.0.2`
- External services: none
- Paid services: none
