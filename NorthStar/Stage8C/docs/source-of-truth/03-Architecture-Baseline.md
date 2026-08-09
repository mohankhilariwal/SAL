# 03 Architecture Baseline - S08C Overlay 1.11.0

- Architecture version: `1.11.0`
- Graph: `GRAPH-001/1.7.0`
- Components: `CMP-001`-`011` unchanged.
- Exactly one active agent: `AGT-001` specification `1.1.0`.

Change: `CMP-008` gains an internal judge-bias laboratory comprising immutable probe catalogue, counterbalanced trial planner, replay adapter, strict observation validator, paired estimator, slice reporter and quarantine recommender. `CMP-006` owns expert validation/adjudication; `CMP-007` authorizes dataset/rubric access; `CMP-009` receives minimized evidence; `CMP-011` governs versions.

No new top-level component, agent, tool, state writer, approval writer, route writer or production endpoint is introduced.
