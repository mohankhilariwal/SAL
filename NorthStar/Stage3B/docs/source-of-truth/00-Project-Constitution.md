# 00 — Project Constitution

**Architecture/repository version:** `0.6.0`  
**Current completed stage:** `S03B — Single-Agent Loop and Termination`  
**Updated:** 2026-07-31

## Source hierarchy

1. Execution Controller.
2. Narrative-Driven Agentic AI Architecture Playbook.
3. Accepted cumulative source-of-truth artefacts.
4. Latest accepted stage handoff.
5. Continuation instruction.
6. Supplementary legacy master prompt.

## Stable narrative

- Organization: **NorthStar Financial Services**.
- Primary user: **Maya Chen**, Regulatory Compliance Analyst.
- Accountable executive: **Daniel Brooks**, Chief Compliance Officer.
- Architecture owner: **Priya Raman**, Enterprise Agentic AI Architect.
- Platform, security, governance, reliability and business-control personas remain Elena Petrov, Marcus Green, Sofia Alvarez, Liam O’Connor and Aisha Rahman.
- AI output remains advisory. Legal applicability, approval and final compliance disposition remain accountable human decisions.

## S03B constitutional invariants

1. `AGT-001` is the only accepted agent.
2. `AGT-001` may propose only `TOOL-001`–`TOOL-006`; every call traverses `CMP-005` and `INT-017`.
3. The decision provider cannot create or widen identity, group membership, purpose, residency, clearance, write scope, approval or final disposition.
4. `DATA-009 AgentRunState` is explicit application state; it is not hidden model reasoning and is not long-term memory.
5. A `complete` proposal is advisory. `INT-024` deterministically validates completion invariants.
6. Successful completion means only that an evidence-backed, reversible, **unapproved** draft package exists and a human review request is queued.
7. Reversible writes remain idempotent and receive no automatic write retry under `ADR-020`.
8. Retrieval authorization remains before scoring/text exposure; `KSV-*`, `CHK-*`, `CIT-*` and `DATA-032` semantics remain unchanged.
9. Local events, final run files, draft cases, candidate mappings and review queue entries are not enterprise records or a tamper-evident audit ledger.
10. S03B does not implement graph execution, durable checkpoints, memory, multi-agent behavior, MCP/A2A, enterprise IAM/PDP or production deployment.

## Technology and execution baseline

- Python: `>=3.11,<3.15`; executed on the container's installed Python.
- `jsonschema==4.26.0` target; local installed compatible release used for tests.
- `pytest==9.0.2` target; local installed compatible release used for tests.
- Canonical contracts remain application-owned JSON Schema Draft 2020-12.
- The accepted validation path is local/offline and uses synthetic/public-safe data.

## Change history

| Version | Stage | Summary |
|---|---|---|
| `0.1.0`–`0.4.0` | S00–S02B | Constitution, assistant, knowledge preparation and authorized retrieval. |
| `0.5.0` | S03A | Six tool contracts and one deterministic gateway; no agent. |
| `0.6.0` | S03B | One bounded agent, explicit run state, progress projection and safe termination. |

## Definition of done for S03B

S03B is complete only when one runnable agent loop:

- receives a typed goal and trusted principal context;
- produces schema-valid `call_tool`, `complete` or `escalate` decisions;
- invokes only registered tools through the gateway;
- stores validated observations and monotonic milestones in `DATA-009`;
- rejects premature completion;
- terminates on success, escalation, iteration, repetition, no progress, invalid decision or tool failure;
- preserves unapproved/human-review semantics;
- passes the recorded tests, validation and consistency audit;
- updates all ten artefacts and stops before S03C.
