# NorthStar Stage 9C — Guardrails, Governance and Control Plane

This package is the executable `1.14.0` Stage 9C overlay for the NorthStar Agentic AI Architecture Playbook.

## What it implements

- `GR-001/1.0.0`: 59 controls across ten guardrail stages.
- `GOV-001/1.0.0`: policy lifecycle, ownership and soft-only exceptions.
- `CP-001/0.1.0`: bounded local release/distribution/pinning/status reference.
- `TM-001/1.2.0` delta.
- `DATA-193`–`216`, `INT-155`–`176`, `ADR-104`–`113`.
- 88 executable pytest cases plus validation, evaluation and audit scripts.

## What it does not implement

No full production control plane, production IAM/policy service, signed/KMS-backed bundles, WORM audit, live classifier, live human-review service, new agent/tool/protocol/route or Stage 8D deployment eligibility.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_stage9c_demo.py
PYTHONPATH=src python scripts/validate_stage9c.py
PYTHONPATH=src python scripts/run_stage9c_evaluation_gates.py
PYTHONPATH=src python scripts/consistency_audit_stage9c.py
```

Main stage chapter: `NorthStar-Stage-9C-Guardrails-Governance-and-Control-Plane.md`  
Reusable handoff: `NorthStar-Stage-9C-Handoff-Pack.md`
