# NorthStar Agentic Compliance — Stage 4A

Version `0.8.0` converts the Stage 3C imperative single-agent loop into an explicit,
framework-neutral typed execution graph. It preserves `AGT-001`, `TOOL-001`–`006`,
application-owned budgets and recovery, gateway-only execution, unapproved output
semantics and the prohibition on blind retries of ambiguous writes.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python scripts/run_stage4a_demo.py
python scripts/run_stage4a_evaluation.py
python scripts/validate_stage4a.py
python scripts/consistency_audit_stage4a.py
```

This is a local/offline synthetic teaching implementation. It is not a durable
workflow service, audit ledger, enterprise identity system or human approval service.
