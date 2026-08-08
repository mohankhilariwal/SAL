# 06 — ADR Register

**Version:** `0.6.0`

`ADR-001`–`ADR-021` remain accepted. S03B adds:

## `ADR-022` — One Application-Owned Bounded Single-Agent Loop

- **Status:** Accepted.
- **Context:** S03A's fixed caller cannot choose the next capability from observed progress; the gateway must not absorb goal pursuit.
- **Decision:** Introduce one `AGT-001` inside `CMP-003`, using a provider-neutral structured decision provider and an application-owned observation-action loop. Use plain Python now; do not adopt a graph/framework in S03B.
- **Alternatives:** fixed deterministic sequence; open-ended ReAct; plan-and-execute; graph/workflow engine; multiple agents.
- **Rationale:** one bounded loop provides the minimum agency required while preserving the existing gateway and keeping control visible.
- **Consequences:** action selection can be probabilistic later, but run semantics and authority remain deterministic; provider quality becomes a new evaluation concern.
- **Risks:** hijacking, poor action choice, repeated calls, premature completion.
- **Mitigations:** strict decision schema, allowlist, trusted context injection, gateway-only calls, progress/termination evaluator and negative tests.
- **Review triggers:** need for durable waiting/restart, complex branching, parallel work, multiple independent roles or production provider adoption.

## `ADR-023` — Explicit Run State and Layered Safe Termination

- **Status:** Accepted.
- **Context:** a model-generated final answer or `complete` token cannot prove that NorthStar's business and control invariants are satisfied.
- **Decision:** instantiate `DATA-009`, derive milestones only from validated results and separate semantic completion proposal from deterministic completion validation. Support explicit success, escalation and guard termination.
- **Alternatives:** stop on model text; only maximum-turn termination; tool-sequence completion; framework-native termination only.
- **Rationale:** layered termination distinguishes goal success from resource/safety stop and makes partial results auditable.
- **Consequences:** additional state and tests; completion logic is domain-specific and must evolve with requirements.
- **Risks:** incorrect milestone mapping, stale state, overly strict or permissive completion.
- **Mitigations:** typed projection, invariant tests, status/linkage checks, versioned state schema and human-review requirement.
- **Review triggers:** new tools/artifacts, changed business definition of completion, asynchronous approval, durable recovery or schema migration.

Detailed ADR files are under `docs/adr/`.
