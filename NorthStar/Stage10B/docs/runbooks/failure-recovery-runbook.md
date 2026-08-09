# NorthStar Failure Recovery Runbook — Stage 10B

1. Confirm incident correlation, affected component, operation, effect class and current graph node.
2. Freeze automatic retries when outcome is ambiguous, authority is invalid, audit is unavailable or integrity is uncertain.
3. For protected writes, query `CMP-005` by idempotency reference before any repeat.
4. For authorization or authentication failure, obtain a fresh scoped grant from `CMP-007`; do not reuse checkpoint or trace identity.
5. For policy or audit failure, fail closed and preserve the blocked-action evidence.
6. For corrupt checkpoints, quarantine the record and reconstruct from `DATA-106` plus external status; do not replay into business state.
7. For dead letters, correct the root cause, validate current schema and obtain authenticated redrive approval.
8. For human timeout, keep the item pending and escalate; timeout never approves.
9. For overload, shed lower-priority work and protect policy, audit and human-review capacity.
10. Close only after final disposition, audit verification and preventive-action owner are recorded.
