# 03 — Architecture Baseline — Version 1.15.0 Overlay

## Preserved architecture

Preserve `CMP-001–011`, exactly one active `AGT-001`, `TOOL-001–006`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, `GR-001/1.0.0`, `GOV-001/1.0.0` and bounded `CP-001/0.1.0`.

## Added architecture

- `OBS-001/1.0.0`: provider-neutral correlation, structured telemetry, redaction, sampling, metrics and export status.
- `AUD-001/1.0.0`: mandatory material-event matrix, canonical append-only records, SHA-256 chain, HMAC authenticity, idempotency and verification.
- `EVID-001/1.0.0`: verified, digest-bound, purpose-scoped evidence packages without hidden chain-of-thought.
- `GRAPH-001/1.11.0`: adds telemetry/audit side paths only; no business route or authority owner changes.
- `TM-001/1.3.0`: adds observability/audit threats and controls.

## Plane separation

- Data plane: regulatory intake, orchestration, retrieval, agent, tool and human-review workflow.
- Operational observability plane: sampled/buffered logs, metrics, traces and events.
- Accountability audit plane: unsampled material events and evidence packages.
- Management/control plane: remains bounded at CP-001/0.1.0; S09D unresolved.

See `docs/architecture/diagrams/cumulative-logical-architecture.mmd` and Stage 10A focused diagrams.
