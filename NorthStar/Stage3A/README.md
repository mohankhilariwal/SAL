# NorthStar Agentic Compliance — Stage 3A

This repository is the `0.5.0` local tutorial implementation for **Tool Contracts and Tool Gateway**. It extends the accepted S02B retrieval boundary with six controlled capabilities and one deterministic application-owned gateway. It does not implement an agent.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
python scripts/run_stage3a_demo.py
python scripts/run_stage3a_evaluation.py
python scripts/benchmark_stage3a_gateway.py
python scripts/validate_stage3a.py
python scripts/consistency_audit_stage3a.py
```

## Safety boundary

All sources and writes are synthetic/local. Outputs remain preliminary and unapproved. The principal context is not authenticated. Do not connect the package to production systems without enterprise identity/PDP, secrets, records, audit, adapter security, threat modelling and deployment controls.
