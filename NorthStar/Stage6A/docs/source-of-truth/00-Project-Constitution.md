# 00 — Project Constitution
**Version:** `1.3.0`  
**Stage:** `S06A`

All accepted `1.2.0` principles remain. Stage 6A adds:

1. An agent is an independently governed goal-directed runtime identity—not a prompt, model call, graph node, role label or output schema.
2. Agent count is a risk-bearing decision. A new agent requires an independent identity/authority/lifecycle/fault/termination boundary or representative measured value that cannot be achieved by the existing agent, graph nodes and task profiles.
3. `AGT-001` remains the only agent; `AGT-001-spec 1.1.0`, `GRAPH-001 1.1.0`, and `DATA-009 1.1.0` remain unchanged.
4. `DATA-089` profiles may narrow instructions, context, tool exposure and outputs. They cannot grant authority, create identity, choose routes, mutate protected state, approve/finalize, write memory, delegate, hand off, create concurrency or allocate agents.
5. `INT-062` may deny or require architecture review; it cannot allocate an agent or grant runtime authority.
6. `CMP-003` owns state/routes/termination; `CMP-005/CMP-007` own tool authorization; `CMP-006` owns human decisions; the harness owns the memory lifecycle.
7. Multi-agent, delegation, handoff, shared-agent memory, MCP/A2A and concurrent branches remain disabled until separately required, reviewed, implemented and evaluated.
8. Value must be compared with coordination overhead, duplicate work, error propagation, security surface, latency, cost and operability.

**Definition of done:** all artefacts agree; exactly one agent remains; no future-stage runtime capability is claimed.
