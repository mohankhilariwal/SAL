# ADR-055 — Require Exact Protocol Version and Approved Binding; Defer gRPC, Brokers and Framework Handoffs

- **Status:** Accepted
- **Context:** Silent downgrade or binding substitution can drop security and lifecycle semantics. NorthStar has no concurrency or durability requirement in S06C.
- **Decision:** Negotiate an exact supported version and approved binding, otherwise reject. Record DATA-103. Defer gRPC, queues/event buses and framework-native handoffs until topology/SLO/concurrency evidence exists.
- **Alternatives:** Best-effort downgrade; latest-version wins; select every adapter.
- **Rationale:** Makes compatibility explicit and prevents accidental future-stage capability.
- **Consequences:** Some otherwise reachable endpoints fail closed; profile management is required.
- **Risks:** Operational friction and version fragmentation.
- **Mitigations:** Compatibility matrix, staged conformance tests and controlled profile updates.
- **Review trigger:** Production endpoint onboarding or S06D asynchronous/concurrent execution design.
