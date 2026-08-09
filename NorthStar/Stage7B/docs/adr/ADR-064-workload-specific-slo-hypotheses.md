# ADR-064 — Workload-specific SLO hypotheses, not universal limits

- **Status:** Accepted
- **Context:** Interactive queries, long-document analysis and batch processing have different latency and throughput expectations.
- **Decision:** Define profile-specific TTFT, ITL/TPOT, queue, end-to-end and success-rate hypotheses. They remain hypotheses until business owners and measured evidence establish production SLOs.
- **Alternatives:** One global SLO; no SLO until production; vendor benchmark thresholds.
- **Rationale:** Prevents misleading global targets while creating testable objectives.
- **Consequences:** Admission and capacity decisions require profile classification.
- **Risks:** Too many profiles can fragment operations.
- **Mitigations:** Limit profiles to materially different workload regimes and review quarterly.
- **Review trigger:** User research, production telemetry or contractual requirements change.
