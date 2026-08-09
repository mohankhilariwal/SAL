# 04 — Component and Agent Catalogue

**Version:** `1.4.0`

## Components

| ID | Name | S06B responsibility/status |
|---|---|---|
| CMP-001 | Analyst Experience Portal | Starts/resumes cases; surfaces preliminary handoff evidence. |
| CMP-002 | Regulatory Intake Boundary | Unchanged provenance boundary. |
| CMP-003 | Case and Workflow Orchestration Boundary | Owns task creation, envelope, lifecycle, cancellation, aggregation, state and termination. |
| CMP-004 | Knowledge and Evidence Access Boundary | Unchanged authorized evidence source. |
| CMP-005 | Enterprise Integration Boundary | Unchanged gateway-only `TOOL-001`–`006`; recipient cannot bypass. |
| CMP-006 | Human Review and Approval Boundary | Unchanged external typed human authority. |
| CMP-007 | Identity, Authorization and Policy Boundary | Owns parent/child grant issue, attenuation, verification and revocation semantics. |
| CMP-008 | Evaluation and Assurance Boundary | Evaluates handoff, authority, integrity and one-agent invariants. |
| CMP-009 | Observability and Audit Boundary | Local receipts/status evidence only; not audit/WORM. |
| CMP-010 | Runtime and Deployment Boundary | Local sequential two-party contract sandbox. |
| CMP-011 | Source-of-Truth Governance Pack | Governance at `1.4.0`; active/candidate status and future flags. |

## Active agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| AGT-001 | Regulatory Impact Assessment Agent | Existing gateway-only tools and proposal/complete/escalate boundaries; cannot approve/finalize, route/mutate protected state, grant consent, write memory, create agents, run concurrent branches or bypass control owners. | **Only active agent**, spec `1.1.0`, six profiles. |

## Candidate endpoint inventory

| Endpoint ID | Name | Powers | Status |
|---|---|---|---|
| CAND-EVIDENCE-VERIFIER-001 | Candidate Evidence Verification Endpoint | `evidence_verification` purpose; no tools, memory write, route, delegation, approval, finalization or concurrency. | `candidate_sandbox_only`; not an `AGT-*` allocation. |

## Agent-count rule

The active agent count is one. A candidate endpoint is a test subject and schema target; it does not supersede `ADR-044`–`046` or qualify as an implemented multi-agent runtime.
