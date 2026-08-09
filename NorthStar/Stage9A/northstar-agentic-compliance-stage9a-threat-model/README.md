# NorthStar Stage 9A Threat-Modelling Overlay

A standard-library local reference that versions the NorthStar architecture snapshot, enumerates data flows and trust boundaries, validates 36 current/future agentic threat scenarios, produces STRIDE and OWASP Agentic Top 10 summaries, validates attack trees/misuse cases, and emits advisory treatment evidence.

It does **not** implement production identity, authorization, signed messages, WORM audit, red-team automation, deployment gates, model routing or additional agents.

```bash
export PYTHONPATH=src
python scripts/validate_stage9a.py
python scripts/run_stage9a_threat_model.py
python scripts/run_stage9a_evaluation_gates.py
pytest -q
python scripts/consistency_audit_stage9a.py
```
