# ADR-035 — Observer Hooks and Privacy-Preserving Tracing

- **Status:** Accepted
- **Context:** Evaluation and tracing hooks are inconsistent, but Stage 4C must not create an audit ledger or leak prompts, secrets or hidden reasoning.
- **Decision:** Use immutable observer payloads, required deterministic invariant hooks and redacted JSONL trace events behind an adapter boundary compatible with later OpenTelemetry export.
- **Alternatives:** No hooks; arbitrary mutable callbacks; provider-specific tracing; full prompt/tool content capture.
- **Rationale:** Lifecycle evidence becomes testable and portable while keeping authority and state mutation in existing components.
- **Consequences:** Local traces are useful for debugging/evaluation but are not tamper-evident audit records.
- **Risks:** Hook latency/failure, trace leakage and semantic-convention drift.
- **Mitigations:** Bounded synchronous hooks, fail-closed required validators, redaction, hashes/counts instead of raw content and future exporter conformance tests.
- **Review trigger:** Production telemetry backend, regulated records requirements, asynchronous hooks or OpenTelemetry semantic-convention stabilization.
