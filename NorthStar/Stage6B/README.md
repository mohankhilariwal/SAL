# NorthStar Agentic Compliance — Stage 6B

This package is the `1.4.0` compatible reconstruction overlay for **Stage 6B — Bounded Agent Handoff, Communication and Authority Contracts**.

It preserves one active `AGT-001` and implements:

- canonical signed handoff envelopes;
- strictly attenuated authority grants;
- authorization-before-artefact-load;
- immutable hashed artefact manifests;
- signed receipts;
- deterministic status, timeout and cancellation semantics;
- a sequential two-party contract sandbox;
- tests/evaluations proving no second active agent, concurrency or protocol selection.

It does **not** implement a production multi-agent runtime, OAuth/DPoP, MCP/A2A, a network transport, queues, concurrent workers, audit/WORM or production IAM/KMS.

## Run

```bash
python -m compileall -q src scripts
pytest
PYTHONPATH=src python scripts/run_stage6b_demo.py
PYTHONPATH=src python scripts/run_stage6b_evaluation.py
PYTHONPATH=src python scripts/benchmark_stage6b.py
PYTHONPATH=src python scripts/validate_stage6b.py
PYTHONPATH=src python scripts/consistency_audit_stage6b.py
```

The full tutorial stage is in `docs/stages/Stage-6B-Bounded-Agent-Handoff-Communication-and-Authority-Contracts.md`.
