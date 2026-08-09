# ADR-050 — Private State by Default and Immutable Artefact Exchange

- **Status:** Accepted
- **Context:** Shared mutable state or shared agent memory would create race, provenance, privacy, poisoning and deletion problems.
- **Decision:** `DATA-009` remains owned by `CMP-003`. A recipient receives only explicit immutable `DATA-095` artefacts and a bounded context policy. Private scratch is ephemeral. `DATA-081` is not automatically transferred and shared-agent memory remains disabled.
- **Alternatives:** Shared database row; blackboard; shared workspace; transcript replay; shared vector memory.
- **Rationale:** Artefact references can be hashed, authorized and attributed; shared mutable memory cannot be safely introduced without concurrency and privacy controls.
- **Consequences:** More explicit packaging and possible duplication; stronger lineage and isolation.
- **Risks:** Large artefacts and repeated serialization; mitigated later with content-addressed storage and references.
- **Review trigger:** Proven need for shared workspace/memory plus concurrency, privacy and consistency design.
