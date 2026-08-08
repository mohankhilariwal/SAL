# NorthStar Agentic Compliance — Stage 4C

This package is the local/offline Stage 4C reference implementation for **Agent Harness Engineering**.
It composes the accepted `GRAPH-001` `1.1.0`, gateway-only `TOOL-001`–`006`, durable wait/decision contracts and one `AGT-001` behind a framework-neutral harness.

## Verification boundary

- Python target: `>=3.11,<3.15`; executed on Python 3.13.5.
- Runtime dependencies: Python standard library only.
- Tests: pytest 9.0.2.
- Local SQLite and synthetic identities only.
- No memory, concurrent graph branches, second agent, live model, enterprise connector, IAM/PDP, audit ledger or production sandbox.
- The supplied Stage 4B handoff, rather than a byte-exact Stage 4B archive, was the reconstruction baseline (`ISS-043`).

## Run

```bash
python -m pip install -e . --no-deps --no-build-isolation
python -m pytest -q
python scripts/run_stage4c_demo.py
python scripts/run_stage4c_evaluation.py
python scripts/validate_stage4c.py
python scripts/consistency_audit_stage4c.py
```

The approval secret is supplied in process memory by tests/scripts and is never stored in the repository or workspace.
