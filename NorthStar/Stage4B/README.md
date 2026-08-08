# NorthStar Agentic Compliance — Stage 4B

Version `0.9.0` adds durable human-review waits, signed single-use decision callbacks,
timeout/escalation, lease-protected resume, and approved/rejected routes to `GRAPH-001`.

The runtime remains one sequential process with one low-authority agent. It does not add
memory, a harness, concurrent graph branches, multiple agents, event sourcing, an audit
ledger, or production IAM.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python scripts/run_stage4b_demo.py
python scripts/run_stage4b_evaluation.py
python scripts/validate_stage4b.py
python scripts/consistency_audit_stage4b.py
```
