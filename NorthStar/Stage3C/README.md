# NorthStar Agentic Compliance — Stage 3C

This repository is the executable Stage 3C overlay for the NorthStar Agentic AI Architecture Playbook.
It preserves one low-authority agent (`AGT-001`), six gateway-only tools (`TOOL-001`–`TOOL-006`),
application-owned completion, and the fixed `preliminary_grounded_unapproved` disposition.

Stage 3C adds independent iteration, time, token, cost, tool-call and failure budgets; typed failure
classification; bounded retry/replan; provider and read-tool fallback; cooperative cancellation;
ambiguous-write reconciliation; partial completion; and atomic local checkpoint/resume.

It deliberately does **not** add a graph, memory, a second agent, enterprise identity/PDP, live systems,
or an audit ledger.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python scripts/run_stage3c_demo.py
python scripts/run_stage3c_evaluation.py
python scripts/validate_stage3c.py
python scripts/consistency_audit_stage3c.py
```
