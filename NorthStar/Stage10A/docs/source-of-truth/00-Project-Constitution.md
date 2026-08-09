# 00 — Project Constitution — Version 1.15.0 Overlay

This overlay preserves the complete accepted NorthStar constitution through S09C and adds S10A invariants.

## S10A constitutional invariants

1. Observability and audit have `authority_effect: none`.
2. Correlation identifiers cannot authenticate a human/workload, establish tenant/case/resource scope, issue authority, approve/finalize or activate a route.
3. `CMP-009` owns observability/audit mechanics but not business decisions, authorization, tool invocation, protected state or deployment promotion.
4. Operational telemetry may be sampled, aggregated or dropped under a bounded policy with explicit accounting.
5. Mandatory accountability events cannot be sampled or silently dropped.
6. Protected effects require durable audit intent before execution and outcome/reconciliation afterward.
7. Mandatory audit failure blocks a protected effect.
8. Raw prompts, responses, documents, tool arguments, credentials and secrets are excluded by default; metadata, references, versions and digests are preferred.
9. Hidden model chain-of-thought is not an audit requirement and must not be collected as the accountability record.
10. `DATA-106` remains the business source of truth; audit replay is read-only.
11. A local hash/HMAC chain is not WORM, asymmetric non-repudiation, trusted timestamping or legal admissibility.
12. Exactly one active `AGT-001`, current authority owners, gateway-only tools and one concurrent protected write remain.
13. Stage 8D and Stage 9D remain unresolved and production promotion remains denied.

## Version state

- Architecture/repository/handoff: `1.15.0`
- Graph: `GRAPH-001/1.11.0`
- Threat model: `TM-001/1.3.0`
- New models: `OBS-001/1.0.0`, `AUD-001/1.0.0`, `EVID-001/1.0.0`
