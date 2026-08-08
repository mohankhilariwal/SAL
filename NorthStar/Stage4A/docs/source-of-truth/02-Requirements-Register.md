# 02 — Requirements Register

**Version:** `0.8.0`

`FR-001`–`FR-083`, `NFR-001`–`NFR-064` and `CTL-001`–`CTL-042` remain accepted and unchanged from the reconstructed `0.7.0` baseline.

## New functional requirements

| ID | Requirement | Status |
|---|---|---|
| `FR-084` | Represent orchestration as a versioned graph of typed nodes and named routes. | Implemented locally |
| `FR-085` | Validate unique/reachable nodes, valid edge targets, unique source-route pairs and terminal end routes before execution. | Implemented |
| `FR-086` | Support deterministic, model, policy, tool, recovery and termination node types without allocating another agent. | Implemented |
| `FR-087` | Wrap unchanged `DATA-009` in typed graph execution state. | Implemented |
| `FR-088` | Require each node to return a typed result and node-owned state patch. | Implemented |
| `FR-089` | Reject direct/protected state mutations, including authority, budgets and final disposition. | Implemented |
| `FR-090` | Route tool actions only through `CMP-005`, preserving gateway authorization and idempotency. | Implemented |
| `FR-091` | Reuse `INT-026`–`INT-030` within graph nodes and error routes. | Implemented |
| `FR-092` | Persist a checksummed checkpoint after every accepted transition and bind it to graph ID/version. | Implemented locally |
| `FR-093` | Resume from the exact next node without repeating completed tool milestones. | Implemented locally |
| `FR-094` | Record ordered graph transitions with route and concise evidence. | Implemented |
| `FR-095` | Produce the same deterministic unapproved completion outcome as S03C. | Implemented |

## New non-functional requirements

| ID | Requirement | Status |
|---|---|---|
| `NFR-065` | Framework-neutral graph contracts and runtime. | Implemented |
| `NFR-066` | Fail closed on invalid graph definitions, unknown routes or unauthorized patches. | Implemented |
| `NFR-067` | Maximum graph transitions independent of model/tool budgets. | Implemented |
| `NFR-068` | Deterministic path reproducibility for the local scripted provider. | Verified |
| `NFR-069` | Checkpoint checksum and graph-version compatibility validation. | Verified |
| `NFR-070` | No hidden state mutation by nodes or provider output. | Verified |
| `NFR-071` | Preserve S02 authorization-before-evidence and S03 gateway-only boundaries. | Verified |
| `NFR-072` | Preserve local/offline Python `>=3.11,<3.15`; executed on `3.13.5`. | Verified |
| `NFR-073` | Record path coverage and transition efficiency metrics. | Implemented locally |
| `NFR-074` | Do not claim distributed durability, replay, audit or exactly-once execution. | Enforced in docs/tests |

## New controls

| ID | Control |
|---|---|
| `CTL-043` | Graph-definition validation before runtime creation. |
| `CTL-044` | Exact node-owned path allowlists and protected paths. |
| `CTL-045` | Application-owned conditional route table; provider cannot select arbitrary node IDs. |
| `CTL-046` | Policy preflight before tool node and authoritative gateway recheck. |
| `CTL-047` | S03C recovery manager owns fallback/reconciliation routes. |
| `CTL-048` | Graph transition budget and cancellation check before new model work. |
| `CTL-049` | Checkpoint checksum plus graph ID/version binding. |
| `CTL-050` | Completion node validates all six unapproved milestones and linkage. |

## Traceability

| Requirement set | Components/data/interfaces | Code | Tests/evaluations |
|---|---|---|---|
| `FR-084`–`086`, `NFR-065`–`068` | `CMP-003`, `DATA-053`, `INT-031`, `INT-034` | `graph/definition.py`, graph JSON, `graph/runtime.py` | `TEST-110`–`114`, `118`–`119`, `EVAL-027` |
| `FR-087`–`089`, `NFR-070` | `DATA-054`–`056`, `INT-032`–`033`, `CTL-044` | `graph/models.py`, `graph/state.py` | `TEST-115`–`117` |
| `FR-090`–`091`, `NFR-071` | `CMP-005`, `INT-017`, `INT-026`–`030`, `CTL-046`–`047` | `graph/nodes.py`, `tools/gateway.py` | `TEST-120`–`123`, `130`–`131`, `EVAL-028`–`029`, `031` |
| `FR-092`–`094`, `NFR-067`, `069`, `073` | `DATA-050`, `DATA-057`, `INT-035`, `CTL-048`–`049` | `state/checkpoint.py`, `graph/runtime.py` | `TEST-124`–`128`, `132`, `EVAL-030`, `032` |
| `FR-095`, `NFR-074` | `DATA-052`, `CTL-050` | `agent/termination.py`, `N70`, `N90` | `TEST-118`, `123`, `129`, `EVAL-027`, `031` |
