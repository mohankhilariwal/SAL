# 07 - Repository Manifest (S09B overlay)

Repository/version: `northstar-agentic-compliance-stage9b-identity-blast-radius` / `1.13.0`.

Important paths and entry points are listed in the Stage 9B chapter and README. Tested environment: Python 3.13.5, cryptography 46.0.4, pytest 9.0.2, jsonschema 4.26.0. Local install: `pip install -e '.[test]'`. Commands: `pytest`; `python scripts/run_stage9b_demo.py`; `python scripts/run_stage9b_evaluation_gates.py`; `python scripts/validate_stage9b.py`; `python scripts/consistency_audit_stage9b.py`.

This is a compatible overlay because the byte-exact `1.12.0` tree was not mounted.
