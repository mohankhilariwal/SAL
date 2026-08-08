# 02 — Requirements Register

**Inherited requirements:** `FR-001`–`FR-070`, `NFR-001`–`NFR-054`, and `CTL-001`–`CTL-032` remain accepted. Their meanings are preserved from the S03B handoff.

## New functional requirements

| ID | Requirement | Component/interface | Verification |
|---|---|---|---|
| `FR-071` | Enforce independent iteration, wall-time, input-token, output-token, total-token, cost, tool-call, model-call, failure, retry and replan budgets. | `CMP-003`, `INT-026`, `DATA-045/046` | `TEST-088`–`090`, `108`, `109`, `EVAL-026` |
| `FR-072` | Settle provider-reported usage and record a provider-neutral budget ledger. | `INT-026` | `TEST-088/089/106` |
| `FR-073` | Classify every model/tool failure into a typed application-owned failure envelope. | `INT-027`, `DATA-047` | `TEST-094`–`098` |
| `FR-074` | Retry only when failure semantics and tool impact make retry safe; cap retries. | `INT-027` | `TEST-094/098/109` |
| `FR-075` | Permit a bounded provider fallback without changing agent authority. | `INT-027` | `TEST-096`, `EVAL-025` |
| `FR-076` | Permit registered fallback adapters only for read-only tools. | `CMP-005`, `INT-027` | `TEST-094`, `EVAL-023` |
| `FR-077` | Detect dead ends and request bounded replanning with blocked action signatures. | `CMP-003`, `DATA-048` | `TEST-101` |
| `FR-078` | Observe an application cancellation signal before new decision/tool work and return a non-success terminal outcome. | `INT-028`, `DATA-049` | `TEST-100` |
| `FR-079` | Return partial completion with completed/missing milestones and recovery/budget evidence. | `DATA-052`, `INT-025` | `TEST-097/098/109` |
| `FR-080` | Reconcile ambiguous writes by tool ID and idempotency key; never blindly retry unresolved writes. | `INT-030`, `DATA-051` | `TEST-095`, `EVAL-024` |
| `FR-081` | Persist an atomic checksummed local checkpoint after accepted transitions and resume the same run. | `INT-029`, `DATA-050` | `TEST-091/092/099` |
| `FR-082` | Persist concise recovery records without hidden chain-of-thought. | `DATA-048/052` | `TEST-094`–`106` |
| `FR-083` | Define compensation as explicit, authority-controlled and plan-only unless an authoritative inverse operation exists. | `INT-027` | Structural validation and ADR-025 |

## New non-functional requirements

| ID | Requirement |
|---|---|
| `NFR-055` | Budget and recovery decisions fail closed outside model reasoning. |
| `NFR-056` | Wall-time measurement uses a monotonic clock. |
| `NFR-057` | Recovery attempts are finite and visible in the ledger. |
| `NFR-058` | An ambiguous write produces zero blind retries and no duplicate local artifact. |
| `NFR-059` | Checkpoint corruption is detected before resume. |
| `NFR-060` | Checkpoint/resume does not broaden principal, write scope or tool allowlist. |
| `NFR-061` | Local happy-path overhead remains measurable; no production SLO is claimed. |
| `NFR-062` | Cost examples use CAD and explicitly state tariff assumptions. |
| `NFR-063` | Recovery evidence contains concise actions/results, not hidden reasoning. |
| `NFR-064` | Exactly one agent remains and no graph/memory module exists. |

## New controls

| ID | Control |
|---|---|
| `CTL-033` | Pre-iteration and pre-tool budget enforcement. |
| `CTL-034` | Post-model usage settlement and exact budget termination reason. |
| `CTL-035` | Failure classification by kind, stage and known commit state. |
| `CTL-036` | Retry matrix combining error class and tool impact. |
| `CTL-037` | Registered fallback allowlist; write-tool fallback prohibited. |
| `CTL-038` | Idempotency-key reconciliation before ambiguous-write continuation. |
| `CTL-039` | Cooperative cancellation checks before decisions, retries and tool calls. |
| `CTL-040` | Atomic checksummed checkpoint and schema validation. |
| `CTL-041` | Partial outcome preserves unapproved/human-review semantics. |
| `CTL-042` | Bounded replan with action-signature blocklist. |

## Traceability summary

`FR-071`–`083` map to `CMP-003`, `CMP-005`, `CMP-008`, `CMP-009`; `DATA-045`–`052`; `INT-026`–`030`; `ADR-024`–`026`; and `TEST-088`–`109`/`EVAL-022`–`026`. No requirement is claimed production-complete.
