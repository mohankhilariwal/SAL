# ADR-076 — Implement a local isolated evaluation harness with advisory outputs

- **Status:** Accepted
- **Context:** No production endpoint, model portfolio, telemetry store or approved dataset exists. The architecture still needs executable contracts.
- **Decision:** Implement a Python standard-library harness that loads immutable JSONL cases, runs isolated independent trials with bounded concurrency, applies deterministic graders, emits payload-minimized digests, blocks the test split by default and never mutates production authority/state.
- **Alternatives:** Adopt a vendor evaluation platform now; wait for production infrastructure; embed evaluation inside `CMP-003`.
- **Rationale:** A small local harness proves interfaces and failure semantics without vendor lock-in or unsupported production claims.
- **Consequences:** It is not a production evaluation service and does not execute a live LLM.
- **Risks:** Harness behaviour may diverge from production; synthetic candidate outputs can overstate readiness.
- **Mitigations:** Isolated environment IDs, explicit evidence kind, negative tests, production-equivalence issue and future adapter layer.
- **Review trigger:** Live endpoint integration, production trace replay, online evaluation or enterprise registry adoption.
