# 05 — Data and Schema Register

**Version:** `0.8.0`

`DATA-001`–`DATA-052` and `INT-001`–`INT-030` remain accepted. `DATA-009` remains schema `1.1.0`. `DATA-050` remains the checksummed atomic local current-state checkpoint; it now carries `DATA-054` as its payload without becoming event sourcing or durable distributed execution.


## Retained S03C runtime objects

| ID | Name | Status |
|---|---|---|
| `DATA-045` | RuntimeBudget | Retained |
| `DATA-046` | BudgetLedger | Retained |
| `DATA-047` | FailureEnvelope | Retained |
| `DATA-048` | RecoveryRecord | Retained |
| `DATA-049` | CancellationSignal | Retained |
| `DATA-050` | RunCheckpoint | Retained; payload extended to `DATA-054` |
| `DATA-051` | ReconciliationRecord | Retained |
| `DATA-052` | RecoveryOutcome | Retained |

| ID | Contract | Status |
|---|---|---|
| `INT-026` | Budget Enforcement Contract | Retained |
| `INT-027` | Failure Classification and Recovery Contract | Retained |
| `INT-028` | Cancellation Contract | Retained |
| `INT-029` | Checkpoint and Resume Contract | Retained |
| `INT-030` | Ambiguous Write Reconciliation Contract | Retained |

## New data objects

| ID | Name | Schema/version | Owner |
|---|---|---|---|
| `DATA-053` | ExecutionGraphDefinition | JSON `1.0.0` | `CMP-003` |
| `DATA-054` | TypedGraphExecutionState | JSON `1.0.0`; wraps `DATA-009` | `CMP-003` |
| `DATA-055` | GraphNodeResult | JSON `1.0.0` | Executing node/runtime |
| `DATA-056` | GraphStatePatch | JSON `1.0.0` | Node proposes; runtime applies |
| `DATA-057` | GraphTransitionRecord | JSON `1.0.0` | `CMP-003`/`CMP-009` local evidence |

## New interfaces

| ID | Contract | Semantics/control |
|---|---|---|
| `INT-031` | Graph Definition Validation Contract | Fail closed on duplicate/unreachable nodes, invalid targets/routes or missing terminal end route. |
| `INT-032` | Node Execution Contract | Snapshot in; typed `DATA-055` out; no direct shared-state mutation. |
| `INT-033` | State Patch Application Contract | Exact owned-path allowlist; protected authority/disposition fields rejected; copy-on-write. |
| `INT-034` | Transition Routing Contract | Application-owned `(source, route) → target`; model cannot choose arbitrary target. |
| `INT-035` | Graph Run and Resume Contract | Bind state/checkpoint to graph ID/version and continue from `current_node`. |

## Tool inventory retained

`TOOL-001` search regulatory sources; `TOOL-002` query control library; `TOOL-003` retrieve authorized evidence; `TOOL-004` create local draft case; `TOOL-005` save candidate mapping; `TOOL-006` queue human review. The first three are read-only; the latter three are reversible, unapproved writes.
