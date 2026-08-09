# 02 — Requirements Register — Version 1.15.0 Overlay

Preserve all accepted requirements through S09C. Add:

| ID | Requirement | Owner | Evidence |
|---|---|---|---|
| `S10A-REQ-001` | Controlled S09C→S10A sequence divergence without S09D implication. | Priya/CMP-011 | ADR-114, ISS-170/171 |
| `S10A-REQ-002` | Separate observability from accountability audit. | Liam/Sofia/CMP-009 | ADR-115, tests 947–952 |
| `S10A-REQ-003` | Standard distributed correlation. | CMP-003/009 | DATA-217, INT-177–179 |
| `S10A-REQ-004` | Correlation has no authority/trust effect. | Marcus/CMP-007/009 | ADR-117, TEST-957 |
| `S10A-REQ-005` | Trace all current workflow boundaries. | Liam | event taxonomy/tests |
| `S10A-REQ-006` | Structured versioned logs/events. | CMP-009 | DATA-218/220 |
| `S10A-REQ-007` | Low-cardinality metrics. | CMP-009/010 | DATA-221, TEST-955 |
| `S10A-REQ-008` | Minimized model invocation metadata. | CMP-003/009 | DATA-222, ADR-118 |
| `S10A-REQ-009` | Retrieval provenance/freshness/access telemetry. | CMP-004 | DATA-223 |
| `S10A-REQ-010` | Tool intent/outcome/grant/budget/idempotency telemetry. | CMP-005 | DATA-224 |
| `S10A-REQ-011` | Policy/auth/human/state/eval evidence. | CMP-006/007/008/003 | DATA-225–227 |
| `S10A-REQ-012` | Redaction before buffer/export/persistence. | CMP-009 | DATA-228, TEST-893–904 |
| `S10A-REQ-013` | Bounded operational sampling/buffering. | CMP-009 | DATA-234 |
| `S10A-REQ-014` | Mandatory audit never sampled. | CMP-009/011 | ADR-119 |
| `S10A-REQ-015` | Tamper-evident ordered audit. | CMP-009 | DATA-229–231 |
| `S10A-REQ-016` | Durable intent/outcome around protected effects. | CMP-005/009 | ADR-121 |
| `S10A-REQ-017` | Read-only replay; DATA-106 remains authoritative. | CMP-003/009 | ADR-122 |
| `S10A-REQ-018` | Digest-bound evidence package. | CMP-009/011 | DATA-232/233 |
| `S10A-REQ-019` | Retention/access ownership. | CMP-011 | DATA-235 |
| `S10A-REQ-020` | Explicit telemetry/audit outage behavior. | CMP-009/010 | integration tests |
| `S10A-REQ-021` | Preserve authority/agent/tool boundaries. | All owners | consistency audit |
| `S10A-REQ-022` | Runnable local code/tests. | Elena/Liam | TEST-881–960 |
| `S10A-REQ-023` | Threat-model delta. | Marcus | TM-001/1.3.0 |
| `S10A-REQ-024` | Explicit production limitations. | Priya/Sofia | status/evals 234–247 |

All requirements trace to components, schemas/interfaces, ADRs and tests in the stage document.
