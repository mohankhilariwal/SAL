# 00 — Project Constitution — Stage 7B overlay

- **Architecture version:** 1.7.0
- **Overlay basis:** Stage 7A handoff 1.6.0
- **Historical merge status:** Required; see `ISS-096`.

## Constitution updates

1. Capacity, SLO and cost claims must identify workload profile, tokenizer, profile version, evidence kind, model/server identity and benchmark configuration.
2. Fixed ISL/OSL smoke tests may not be represented as complete workload evidence.
3. Synthetic and simulated results are planning evidence only.
4. Workload telemetry must avoid raw prompt and response capture by default.
5. Capacity recommendations cannot grant authority, approve work, change routes, mutate protected state or alter `DATA-106` automatically.
6. Exactly one active `AGT-001` remains. `WP-008` is an inactive profile placeholder only.
