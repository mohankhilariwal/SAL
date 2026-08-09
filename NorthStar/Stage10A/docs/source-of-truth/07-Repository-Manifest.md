# 07 — Repository Manifest — Version 1.15.0 Overlay

## Repository

`northstar-agentic-compliance-stage10a-observability-audit/`

## Runtime and dependencies

- Python 3.12–3.13; executed on 3.13.5.
- jsonschema 4.26.0.
- pytest 9.0.2.
- Standard-library JSON, hashing, HMAC, filesystem and threading for the local reference.
- No production OpenTelemetry SDK/Collector/backend dependency.

## Important entry points

- `scripts/run_stage10a_demo.py`
- `scripts/run_stage10a_performance.py`
- `scripts/validate_stage10a.py`
- `scripts/run_stage10a_evaluation_gates.py`
- `scripts/consistency_audit_stage10a.py`

## Environment

- `NORTHSTAR_AUDIT_HMAC_KEY` — local demo key; production must not use the default.

## Scope

Files under `src/northstar_compliance/observability` and `audit` implement the S10A slice. Existing S09C code is preserved by architectural overlay because the byte-exact prior repository was not mounted as one mergeable tree.
