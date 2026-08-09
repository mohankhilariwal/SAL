# 03 Architecture Baseline - S09A Overlay

- Current logical architecture: `GRAPH-001/1.8.0`.
- Runtime execution semantics are unchanged from `GRAPH-001/1.7.0`.
- New design-time assurance path: immutable architecture snapshot -> `TM-001` -> STRIDE/crosswalk/attack-tree/misuse/risk report -> advisory treatment.
- `CMP-008` owns threat analysis; `CMP-011` owns version/change governance; `CMP-009` receives minimized evidence only.
- Future MCP/A2A/multi-agent surfaces are modelled under `TB-07` and remain inactive.

Canonical diagram: `docs/architecture/diagrams/GRAPH-001-v1.8.0.mmd`.
