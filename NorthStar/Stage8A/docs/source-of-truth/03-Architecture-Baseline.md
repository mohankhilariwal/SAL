# 03 — Architecture Baseline (1.9.0 Overlay)

## Preserved baseline

`CMP-001`–`011`, exactly one active `AGT-001`, `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `TOOL-001`–`006`, S07A bounded concurrency, S07B workloads and S07C inference/cache/speculation boundaries remain.

## Stage 8A change

`CMP-008` owns canonical evaluation suites, datasets, graders, isolated runs and advisory aggregation. `CMP-011` governs versions. `CMP-007` authorizes case materialization. `CMP-009` records evidence. `CMP-006` receives human-review assignments. `CMP-003` production ownership is unchanged.

## Cumulative architecture

```mermaid
flowchart TB
  C11["CMP-011 Governance"] --> REG["DATA-131/132/140/141 Registry"]
  REG --> C8["CMP-008 Evaluation"]
  C7["CMP-007 Authorization"] --> CASE["DATA-133..136 Case/Rubric/Grader"]
  CASE --> RUN["DATA-137/138 Isolated Run/Trial"]
  RUN --> A1["AGT-001 contract - only active agent"]
  RUN --> RES["DATA-139 Result"]
  C9["CMP-009 Evidence"] --> RES
  RES --> C6["DATA-142 Human Review Sample"]
  RES --> X["INT-111 Advisory Export"]
  X -. "no DATA-106 mutation" .-> C3["CMP-003"]
  W8["WP-008 inactive_future"] -. "blocked" .-> RUN
```

Graph source: `docs/architecture/diagrams/GRAPH-001-v1.5.0.mmd`.
