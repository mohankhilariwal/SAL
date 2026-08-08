# NorthStar Agentic Compliance — Stage 5A

This package is the runnable local reconstruction for **Stage 5A — Specification and Context Engineering: Agent Specification Boundary**.

It adds a formal machine-readable specification for `AGT-001`, strict semantic validation, manifest binding, runtime assertions, a bounded no-memory context policy and deny-by-default local evaluation/deployment gates. It preserves `GRAPH-001` `1.1.0`, `DATA-009` `1.1.0`, one-agent execution, gateway-only `TOOL-001`–`006` and external human approval.

## Run

```bash
python -m pip install -e . --no-deps --no-build-isolation
python -m pytest -q
python -m compileall -q src scripts tests
python scripts/run_stage5a_demo.py
python scripts/run_stage5a_evaluation.py
python scripts/benchmark_stage5a.py
python scripts/validate_stage5a.py
python scripts/consistency_audit_stage5a.py
```

The package uses standard-library runtime dependencies. Tests use pytest 9.0.2. The executed environment was Python 3.13.5.

## Boundary

The package does not implement memory, context compaction, concurrent graph branches, multiple agents, live models/connectors, production IAM/PDP/KMS, signing/attestation, audit/WORM, deployment or disaster recovery.
