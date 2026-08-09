# NorthStar Stage 10B Reliability, Deployment and AgentOps

This repository is a runnable compatibility overlay for NorthStar architecture version `1.16.0`.

It demonstrates deterministic failure classification, bounded retries, circuit breakers, bulkheads, digest-verified workflow checkpoints, dead-letter quarantine, protected-effect idempotency/reconciliation, local chaos invariants, release manifests and explicit production-promotion denial.

## Safety boundary

- Exactly one active agent remains `AGT-001`.
- `CMP-005` is the only protected-effect gateway.
- `CMP-007` is the only authority issuer.
- Audit failure blocks protected effects.
- Checkpoint and audit replay cannot mutate `DATA-106`.
- Production route and promotion are disabled.

## Run

```bash
export PYTHONPATH=src
python scripts/validate_stage10b.py
pytest
python scripts/run_stage10b_demo.py
python scripts/run_stage10b_chaos.py
python scripts/run_stage10b_evaluation_gates.py
python scripts/consistency_audit_stage10b.py
```

Target Python: `>=3.12,<3.14`. Validated in the supplied environment with Python `3.13.5`.

The Docker and Kubernetes files are local/pre-production references only. They are not production manifests.
