# ADR-049 — Orchestrator-Mediated Sequential Ownership Transfer

- **Status:** Accepted
- **Context:** Peer-to-peer delegation could bypass graph routing, complicate termination and create cycles before concurrency engineering.
- **Decision:** `CMP-003` alone creates, routes, cancels and terminates handoffs. S06B permits one hop and one attempt in a sequential sandbox. Recipients return status/artefacts but cannot delegate again or route `GRAPH-001`.
- **Alternatives:** Peer handoffs; supervisor agent; event choreography; concurrent workers.
- **Rationale:** Preserves accepted graph/state/termination ownership and isolates handoff semantics from concurrency.
- **Consequences:** Coordinator remains in the path; later scale may require durable queues/workers without changing ownership semantics.
- **Risks:** Coordinator bottleneck in future production; not material to current local sandbox.
- **Review trigger:** Stage dedicated to concurrency/distributed execution with workload evidence.
