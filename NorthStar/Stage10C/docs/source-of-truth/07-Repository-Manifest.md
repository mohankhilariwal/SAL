# 07 — Repository Manifest, Stage 10C Overlay

Repository version `1.17.0`; Python `>=3.12,<3.14`; executed with Python `3.13.5`, pytest `9.0.2`, jsonschema `4.26.0`.

Important entry points:

- `scripts/validate_stage10c.py`
- `scripts/run_stage10c_demo.py`
- `scripts/run_stage10c_evaluation_gates.py`
- `scripts/consistency_audit_stage10c.py`

Important modules: `src/northstar_compliance/{finops,capacity,readiness}`.

This is a compatible overlay because the byte-exact Stage 10B repository is not mounted. Merge must preserve prior code and stable identifiers.
