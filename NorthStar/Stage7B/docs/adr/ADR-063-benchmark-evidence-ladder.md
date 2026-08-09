# ADR-063 — Benchmark evidence ladder

- **Status:** Accepted
- **Context:** NorthStar needs useful planning now but lacks production traces and a selected production inference stack.
- **Decision:** Use four explicit evidence classes: simulated, synthetic endpoint, trace replay and production. Higher classes may supersede lower classes; lower classes may not be presented as production proof.
- **Alternatives:** Wait for production; rely only on synthetic tests; use vendor benchmark claims.
- **Rationale:** Enables progressive evidence without overstating maturity.
- **Consequences:** Reports must carry evidence kind, configuration, tokenizer, software/hardware identity and limitations.
- **Risks:** Stakeholders may compare unlike evidence classes.
- **Mitigations:** Separate dashboards and gates; prohibit unlabeled aggregation.
- **Review trigger:** Representative endpoint or trace data becomes available.
