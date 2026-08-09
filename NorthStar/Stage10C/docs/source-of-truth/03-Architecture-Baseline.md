# 03 — Architecture Baseline, Stage 10C Overlay

Architecture `1.17.0`; `GRAPH-001/1.12.0` unchanged.

Preserve `CMP-001`–`011`, exactly one active `AGT-001`, `TOOL-001`–`006`, `DATA-001`–`256`, `INT-001`–`216`, and all accepted security and reliability models.

Add:

- `FIN-001/1.0.0` — cost event, allocation, budget, forecast and unit economics.
- `CAP-001/1.0.0` — workload profile and capacity envelope.
- `SLO-001/0.1.0` — proposed SLI/SLO and error-budget/control-gate model.
- `PRR-001/0.1.0` — machine-readable readiness evidence and denial.
- `DR-001/0.2.0` — proposed business-impact tiers and recovery-objective ownership.

No new runtime route, agent, top-level component, protocol or tool is introduced. Production remains denied.
