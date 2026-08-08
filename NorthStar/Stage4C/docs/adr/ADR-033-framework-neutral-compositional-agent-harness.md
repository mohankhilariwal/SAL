# ADR-033 — Framework-Neutral Compositional Agent Harness

- **Status:** Accepted
- **Context:** Cross-cutting runtime behavior is scattered while `GRAPH-001` 1.1.0 and gateway/approval contracts are already accepted.
- **Decision:** Add an application-owned harness within `CMP-003`/`CMP-010` that composes, rather than replaces, the graph runtime, tool gateway, durable store and approval service.
- **Alternatives:** Keep ad hoc wiring; adopt an SDK-native agent runtime; replace the graph with a framework runtime; adopt a managed control plane now.
- **Rationale:** Composition preserves accepted routes, local/offline execution, testability and migration boundaries without adding memory, concurrent branches or another agent.
- **Consequences:** NorthStar owns harness contracts and adapters; framework conveniences are not inherited automatically.
- **Risks:** Duplicate responsibilities, adapter drift and a harness becoming a monolith.
- **Mitigations:** Thin lifecycle boundary, immutable registries, explicit interfaces, tests and no business reasoning in the harness.
- **Review trigger:** Production framework selection, distributed workers, multi-agent introduction or material runtime throughput requirements.
