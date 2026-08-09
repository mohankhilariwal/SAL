# 02 — Requirements Register: Stage 10B Overlay

Version: `1.16.0`

The full historical requirements register was not supplied. To avoid collisions, this overlay uses stage-qualified IDs pending an authoritative merge.

| ID | Requirement | Owner | Verification |
|---|---|---|---|
| `S10B-FR-001` | Classify failures by source, permanence, ambiguity, effect class and retry safety. | `CMP-003`/`CMP-010` | `TEST-961`–`968` |
| `S10B-FR-002` | Enforce operation-specific timeout, retry, backoff, jitter and total-budget policies. | `CMP-010` | `TEST-969`–`982` |
| `S10B-FR-003` | Prohibit automatic retry for authorization, policy, audit, security, integrity and permanent failures. | `CMP-003` | `TEST-983`–`990` |
| `S10B-FR-004` | Require idempotency for write retries and reconciliation for ambiguous protected outcomes. | `CMP-005` | `TEST-991`–`998` |
| `S10B-FR-005` | Isolate dependency failure with circuit breakers and bulkheads. | `CMP-010` | `TEST-999`–`1005` |
| `S10B-FR-006` | Persist digest-verified workflow checkpoints atomically. | `CMP-003` | `TEST-1006`–`1008` |
| `S10B-FR-007` | Quarantine poison/permanent messages without raw sensitive payloads. | `CMP-003`/`CMP-009` | `TEST-1009`–`1012` |
| `S10B-FR-008` | Require authenticated approval and corrected cause before dead-letter redrive. | `CMP-006`/`CMP-003` | `TEST-1013`–`1014` |
| `S10B-FR-009` | Execute compensation only through `CMP-005` with current grant and approval requirements. | `CMP-005` | security invariant |
| `S10B-FR-010` | Define fail-closed and read-only degraded modes. | `CMP-003`/`CMP-007` | `EVAL-253`–`260` |
| `S10B-FR-011` | Record incident, failure, recovery and release evidence through `CMP-009`. | `CMP-009` | integration tests |
| `S10B-FR-012` | Bind code, graph, agent, configuration and test evidence in a release manifest. | `CMP-011` | release tests |
| `S10B-FR-013` | Gate promotion by tests, security, compatibility, evaluation and human release approval. | `CMP-011` | promotion tests |
| `S10B-FR-014` | Deny production route activation and promotion on the current baseline. | `CMP-010`/`CMP-011` | `TEST-1015`–`1016` |
| `S10B-FR-015` | Provide local-container and pre-production Kubernetes reference artefacts. | `CMP-010` | manifest validation |
| `S10B-FR-016` | Run isolated chaos tests against authority, audit and duplicate-effect invariants. | `CMP-008`/`CMP-010` | chaos tests |
| `S10B-NFR-001` | Reliability controls shall have `authority_effect: none`. | All | security tests |
| `S10B-NFR-002` | Retry, fallback and degradation shall be bounded by latency, token, cost and concurrency budgets. | `CMP-010` | policy validation |
| `S10B-NFR-003` | One concurrent protected write remains the maximum. | `CMP-003`/`CMP-005` | compatibility audit |
| `S10B-NFR-004` | Recovery data shall minimize sensitive content and prefer references/digests. | `CMP-009` | DLQ tests |
| `S10B-NFR-005` | Local recovery decisions should complete in less than 1 second for 10,000 deterministic evaluations on the tested machine. This is a local guard, not a production SLO. | `CMP-010` | performance test |
| `S10B-NFR-006` | Deployment artefacts shall run as non-root with read-only filesystems and no default service-account token where supported. | `CMP-010` | manifest review |
| `S10B-NFR-007` | Production RTO/RPO, capacity, residency and multi-region topology remain unclaimed until enterprise owners approve them. | `CMP-011` | issue register |
| `S10B-NFR-008` | Rollback shall not reverse completed external effects; it changes software/config and invokes explicit compensation where permitted. | `CMP-005`/`CMP-010` | ADR review |
