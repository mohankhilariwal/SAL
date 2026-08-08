# 06 — ADR Register

**Version:** `1.0.0`

## 1. Inherited decisions

`ADR-001`–`ADR-032` remain accepted and unchanged. Especially binding are human accountability/externalized critical controls, gateway-only tools, one bounded agent, independent budgets/recovery/reconciliation, framework-neutral graph, node-owned state patches, approval placement, external-event wait and the local durable adapter.

## 2. New decisions

### ADR-033 — Framework-neutral compositional agent harness

- **Status:** Accepted.
- **Context:** Correct graph/tool/approval modules are wired inconsistently across callers.
- **Decision:** Add one application-owned harness package inside `CMP-003`/`CMP-010` that composes existing contracts. Preserve `GRAPH-001` 1.1.0 and `AGT-001`; do not create another component/agent/workflow engine.
- **Alternatives:** keep ad hoc wiring; put everything in prompts; select a framework-specific harness; build a separate service/control plane.
- **Rationale:** establishes NorthStar semantics locally and keeps framework migration open without moving authority into prompts.
- **Consequences:** more lifecycle code and configuration, but a single testable composition boundary.
- **Risks/mitigations:** god-object risk mitigated by narrow modules/protocols and owner-preserving delegation.
- **Review triggers:** multi-runtime deployment, multiple agents, distributed workers, or a framework whose contract materially improves operations.

### ADR-034 — Versioned instructions, authorized context and deterministic validation

- **Status:** Accepted.
- **Decision:** Bind each run to immutable `DATA-063`/`064`/`065`, frozen registries and lifecycle validators. Authorize before context loader invocation; reject memory and unsupported context kinds.
- **Alternatives:** dynamic prompt assembly without provenance; mutable runtime registries; post-filtering; model-based validation only.
- **Rationale:** repeatability and security require deterministic data/control contracts outside model reasoning.
- **Consequences:** explicit version/hash/quotas and fail-closed upgrades; configuration changes require coordinated release.
- **Review triggers:** signed configuration service, formal agent specification, production context policy, or schema migration.

### ADR-035 — Observer-only evaluation hooks and privacy-preserving local tracing

- **Status:** Accepted.
- **Decision:** Hooks return findings from immutable summaries and cannot mutate/authorize/route. Emit redacted correlated JSONL for local diagnostics, explicitly not audit.
- **Alternatives:** hooks with runtime handles; logging raw prompts/context/tokens; no tracing; immediate OpenTelemetry/vendor dependency.
- **Rationale:** enables test/evaluation integration without hidden control paths or premature platform lock-in.
- **Consequences:** limited local diagnostics and no production exporter/integrity guarantees.
- **Review triggers:** OpenTelemetry deployment, audit/WORM stage, privacy classification changes, or plugin ecosystem.

## 3. Change history

- Architecture/repository/handoff advance `0.9.0` -> `1.0.0`.
- `GRAPH-001` stays `1.1.0`; no in-flight graph migration is required.
- No ADR is superseded and no stable ID is retired.
