# NorthStar Stage 10A — Observability and Audit

This repository is a compatible `1.15.0` overlay on the accepted S09C `1.14.0` baseline. It implements a local, provider-neutral reference for:

- correlation context and W3C-compatible `traceparent` handling;
- structured traces, events, logs and low-cardinality metrics;
- privacy-first redaction and metadata-only defaults;
- sampled operational telemetry;
- unsampled material audit events;
- append-only SHA-256 hash chaining with local HMAC authenticity;
- audit-chain verification and evidence-package generation.

It does **not** implement WORM storage, KMS/HSM signing, a production OpenTelemetry Collector/backend, the full enterprise control plane, Stage 8D promotion gates, Stage 9D, production routing or certification.

## Run

```bash
python -m pip install -e .[dev]
python scripts/run_stage10a_demo.py
pytest
python scripts/validate_stage10a.py
python scripts/run_stage10a_evaluation_gates.py
python scripts/consistency_audit_stage10a.py
```
