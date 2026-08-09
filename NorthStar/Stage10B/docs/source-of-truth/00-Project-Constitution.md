# 00 — Project Constitution: Stage 10B Overlay

Version: `1.16.0`

This overlay preserves the accepted NorthStar constitution and adds the following reliability principles:

1. Recovery is not authority. No retry, fallback, checkpoint, compensation, dead-letter redrive, rollback, feature flag or deployment mechanism may issue, enlarge or substitute for authority owned by `CMP-007`, approval owned by `CMP-006` and authenticated humans, routing/state ownership held by `CMP-003`, or tool execution held by `CMP-005`.
2. Fail closed for authorization, policy, audit, security and integrity failures. Degraded operation is permitted only for explicitly classified, non-protected read paths with visible limitations.
3. A protected effect is never blindly retried after an ambiguous timeout. Reconciliation by idempotency reference precedes any repeat.
4. Workflow checkpoint recovery is not business-state replay. `DATA-106` remains authoritative and can be changed only through accepted business interfaces.
5. Mandatory audit intent and outcome events remain unsampled. Audit unavailability blocks protected effects.
6. Production promotion remains denied while Stages 8D and 9D, production retention, WORM/KMS guarantees, enterprise RTO/RPO and production routing remain unresolved.
7. Chaos experiments in this stage are local or isolated non-production tests only.
8. Exactly one active agent remains `AGT-001`; no recovery controller, deployment controller, release manager or chaos harness is an agent.

Historical note: the full pre-Stage-10A source-of-truth files were not supplied. This is a compatible overlay, not a byte-exact historical merge.
