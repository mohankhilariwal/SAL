# 05 — Data and Schema Register

**Inherited:** `DATA-001`–`DATA-044` and `INT-001`–`INT-025` retain their accepted meanings. `DATA-009 AgentRunState` advances compatibly from schema `1.0.0` to `1.1.0` by adding budget/recovery/checkpoint fields while preserving goal, decisions, observations, milestones, artifacts and terminal semantics.

## New data objects

| ID | Name | Schema | Owner | Purpose |
|---|---|---|---|---|
| `DATA-045` | RuntimeBudget | `1.0.0` | `CMP-003` | Independent immutable run limits. |
| `DATA-046` | BudgetLedger | `1.0.0` | `CMP-003` | Monotonic resource use and recovery counters. |
| `DATA-047` | FailureEnvelope | `1.0.0` | `CMP-005`/`CMP-003` | Typed failure kind, stage, retryability and commit knowledge. |
| `DATA-048` | RecoveryRecord | `1.0.0` | `CMP-003` | Concise retry/fallback/replan/reconciliation evidence. |
| `DATA-049` | CancellationSignal | `1.0.0` | `CMP-001`/`CMP-003` | Cooperative cancellation request. |
| `DATA-050` | RunCheckpoint | `1.0.0` | `CMP-003`/`CMP-009` | Checksummed local state snapshot. |
| `DATA-051` | ReconciliationRecord | `1.0.0` | `CMP-005` | Commit-status lookup by tool and idempotency key. |
| `DATA-052` | RecoveryOutcome | `1.0.0` | `CMP-003`/`CMP-009` | Terminal or partial status, milestones, ledger and recovery evidence. |

## New interfaces

| ID | Contract | Inputs/outputs | Enforcement |
|---|---|---|---|
| `INT-026` | Budget Enforcement Contract | `DATA-045` + usage events → `DATA-046` or exact budget stop | Application-owned; monotonic time; provider cannot modify. |
| `INT-027` | Failure Classification and Recovery Contract | `DATA-047` + tool impact + ledger → bounded retry/fallback/replan/escalation | Deterministic matrix and attempt caps. |
| `INT-028` | Cancellation Contract | `DATA-049` → cooperative stop | Checked before new model/tool/retry work. |
| `INT-029` | Checkpoint and Resume Contract | `DATA-009` ↔ `DATA-050` | Atomic replace, checksum and schema validation. |
| `INT-030` | Ambiguous Write Reconciliation Contract | tool ID + idempotency key → `DATA-051` | Only gateway-owned store/adapter status; unresolved never blindly retried. |

## State invariants

- Ledger counters never decrease within a run.
- Milestones remain monotonic.
- Resume retains the same `run_id`, `AGT-001`, goal and authority envelope.
- Final disposition and human-review requirement are fixed application fields.
- Checkpoint checksum is integrity detection, not non-repudiation.
