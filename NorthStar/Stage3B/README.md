# NorthStar Agentic Compliance — Stage 3B

This package is the `0.6.0` local/offline tutorial overlay for **Stage 3B — Single-Agent Loop and Termination**.

It adds exactly one low-authority agent over the six Stage 3A tool contracts. All actions traverse the deterministic gateway. Completion, authority and final disposition remain application-owned.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
python scripts/run_stage3b_demo.py
python scripts/run_stage3b_evaluation.py
python scripts/validate_stage3b.py
python scripts/consistency_audit_stage3b.py
```

For an environment that already provides compatible dependencies:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_stage3b_demo.py
```

## Scope boundary

Implemented: one bounded loop, typed run state, structured decisions, gateway-only tools, deterministic progress/completion, escalation and iteration/repetition/no-progress termination.

Not implemented: live model provider, advanced budgets/recovery, cancellation, checkpoints, graph, memory, multi-agent, enterprise IAM/PDP, live connectors, approval decisions, production audit or deployment.
