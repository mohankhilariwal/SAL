# ADR-073 — Use layered, outcome-first evaluation with trace evidence

- **Status:** Accepted
- **Context:** A fluent final answer can hide unauthorized evidence, repeated tool calls, state corruption or premature finalization. A correct trace can still end in the wrong business outcome.
- **Decision:** Evaluate both end-state outcome and bounded execution evidence across component, retrieval, tool, loop, graph, security, performance and business layers. Deterministic checks own hard invariants. Transcript/trace evidence explains failures but does not substitute for outcome verification.
- **Alternatives:** Output-only scoring; trace-only scoring; one aggregate score.
- **Rationale:** NorthStar’s regulated workflow needs proof that the system did the right thing through permitted means.
- **Consequences:** More schemas and evidence are required; failures are more diagnosable.
- **Risks:** Grader overlap and contradictory findings.
- **Mitigations:** Criterion ownership, stable grader IDs, fail-closed mandatory gates and explicit advisory aggregation.
- **Review trigger:** New agent topology, new side-effecting tools or production business KPIs.
