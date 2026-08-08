# Data and Schema Register — 0.9.0

All `DATA-001`–`057` remain. `DATA-009` remains `1.1.0`; `DATA-050` remains a local current-state checkpoint contract for the earlier graph. Stage 4B makes `DATA-007 ReviewDecision` executable locally at `1.0.0` and adds:

| ID | Name | Owner |
|---|---|---|
| DATA-058 | DurableWorkflowRecord | CMP-003/CMP-010 |
| DATA-059 | HumanApprovalWait | CMP-006 |
| DATA-060 | ApprovalCallbackTokenClaims | CMP-006/CMP-007 |
| DATA-061 | ApprovalInboxEvent | CMP-006 |
| DATA-062 | WorkflowResumeLease | CMP-010 |

Interfaces: `INT-036 Durable Workflow Persistence`, `INT-037 Human Approval Wait`, `INT-038 Decision Submission and Validation`, `INT-039 Timeout and Escalation`, `INT-040 Safe Resume and Lease`.

Raw callback tokens are not persisted. `DATA-058` and `DATA-007` payloads are checksummed. These records are not an event-sourced audit ledger or enterprise records store.
