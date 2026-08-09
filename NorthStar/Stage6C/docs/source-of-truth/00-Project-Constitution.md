# 00 — Project Constitution

**Version:** 1.5.0  
**Stage:** S06C

All prior accepted constitutional principles remain. S06C adds these invariants:

1. `DATA-091`–`099` remain the canonical handoff semantic layer above every protocol and framework adapter.
2. A protocol profile or capability advertisement cannot allocate an agent, grant authority, route the graph, mutate protected state, approve, finalize or determine system termination.
3. `CMP-003`, `CMP-005`, `CMP-006` and `CMP-007` ownership remains unchanged.
4. Protocol version and binding must be exact and approved; silent downgrade fails closed.
5. Receiver/resource authorization and integrity checks occur before data load/action.
6. MCP is used only for tool/resource interoperability unless a future ADR proves complete task semantics.
7. A2A agent-task mapping requires the approved NorthStar extension and does not activate a second agent.
8. Exactly one active `AGT-001`, sequential execution, no shared state/memory, no peer delegation and no concurrency remain.
9. Local HTTP/HMAC is a reference mechanism, not production identity, security, availability or non-repudiation.
10. Claims of implementation must distinguish direct test, reference boundary, conformance-only, deferred and production-approved status.
