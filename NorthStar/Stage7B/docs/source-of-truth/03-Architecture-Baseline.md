# 03 — Architecture Baseline — Version 1.7.0 overlay

## Preserved baseline

- NorthStar Financial Services and all eight accepted personas.
- `CMP-001`–`011`.
- Exactly one active `AGT-001`, specification `1.1.0`.
- `DATA-009/1.1.0`, `DATA-091`–`113`, `INT-063`–`086`, `TOOL-001`–`006`.
- `CMP-003` remains sole task, route, state, cancellation, aggregation and system-termination owner.
- `CMP-007` remains sole authority issuer.
- Human approval remains external and typed.
- Concurrent work remains immutable read-only or pure compute; no concurrent protected-state writes.
- Sequential fallback remains valid.

## Stage 7B architecture change

`GRAPH-001` advances from `1.2.0` to `1.3.0` by adding an assurance-side workload evidence loop:

1. `CMP-011` governs workload profile versions.
2. `CMP-008` owns profile validation, benchmark scenarios, evaluation and capacity analysis.
3. `CMP-010` executes local benchmark/simulation work under bounded resources.
4. `CMP-009` normalizes and records workload metrics.
5. `CMP-003` may receive an advisory capacity recommendation but retains admission authority.

No new top-level component or active agent is added.

## Architectural invariant

Capacity evidence is descriptive and advisory. It is never an authorization grant, approval, route decision or protected-state mutation.
