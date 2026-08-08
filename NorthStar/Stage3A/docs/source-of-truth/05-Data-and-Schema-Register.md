# 05 — Data and Schema Register

**Version:** `0.5.0`

`DATA-001`–`DATA-033` and `INT-001`–`INT-015` retain their accepted meanings from S02B. `DATA-015` remains `stage1-summary-v1`; `DATA-032 RetrievalContext` remains bounded evidence and cannot be widened by a tool.

## New data objects

| ID | Object | Schema/owner | Main fields and invariants |
|---|---|---|---|
| `DATA-034` | ToolPrincipalContext | `1.0.0`; caller/CMP-007 future | principal, groups, clearance, purpose, residency, correlation, authenticated flag. Local claims are not authentication. |
| `DATA-035` | ToolDescriptor | `1.0.0`; CMP-005/CMP-011 | tool ID/name/version, impact, strict input/output schemas, authorization metadata, runtime limits, descriptor hash. |
| `DATA-036` | ToolInvocationRequest | `1.0.0`; CMP-003 | invocation, exact tool/version, principal, arguments, idempotency key, dry-run, approval reference. No model-specific field. |
| `DATA-037` | ToolAuthorizationDecision | `1.0.0`; CMP-007 logical boundary | allow/deny, reason codes and obligations. Local implementation is unsigned and unauthenticated. |
| `DATA-038` | ToolResultEnvelope | `1.0.0`; CMP-005 | status, timing, attempts, authorization decision, typed data/error, replay flag, descriptor hash. |
| `DATA-039` | ToolIdempotencyRecord | local/transient; CMP-005 | principal + tool + version + key, arguments hash and prior successful result. Not durable. |
| `DATA-040` | ToolExecutionEvent | `1.0.0`; CMP-009 logical boundary | event/invocation/tool/principal/correlation, status, argument hash, redacted fields, timing, descriptor hash. Not tamper-evident. |

Tool-specific arguments/results are defined inside versioned `DATA-035` schemas. Local case/mapping/review JSON files are demonstrations of reversible write output; they do not instantiate the accepted enterprise `DATA-002 RegulatoryCase` or `DATA-007 ReviewDecision` contracts.

## New interfaces

| ID | Contract | Inputs/outputs | Authorization/control |
|---|---|---|---|
| `INT-016` | Tool Registry and Discovery Contract | exact tool ID/version → `DATA-035` | allowlisted files, meta-schema validation, descriptor hash, prohibited impact rejection. |
| `INT-017` | Tool Invocation Contract | `DATA-036` → `DATA-038` | gateway-only; input validation, idempotency, runtime controls. |
| `INT-018` | Tool Policy Decision Contract | principal + descriptor + invocation context → `DATA-037` | deterministic local PDP; enterprise authenticated PDP pending. |
| `INT-019` | Tool Adapter Contract | validated arguments + bounded principal → typed result/error | adapter receives no unrestricted credentials; output validation follows. |
| `INT-020` | Tool Execution Evidence Contract | invocation/result → `DATA-040` | hash/redact; local JSONL only, not append-only enterprise audit. |

## Error taxonomy

`not_found`, `version_mismatch`, `validation_error`, `denied`, `approval_required`, `idempotency_conflict`, `rate_limited`, `circuit_open`, `timeout`, `execution_error`, `output_validation_error`, and `result_too_large` are application-owned statuses. Transport protocols may map them later but may not erase their meaning.
