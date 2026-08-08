# 08 — Risk, Assumption and Issue Register

**Version:** `0.6.0`

Inherited risks and issues remain active unless explicitly closed. S03A additions `RSK-040`–`RSK-048`, `ASM-016`–`ASM-019` and `ISS-021`–`ISS-024` are preserved.

## New risks

| ID | Risk | Severity | S03B treatment | Residual status |
|---|---|---:|---|---|
| `RSK-049` | Agent declares completion before required artifacts exist. | High | Deterministic completion invariants and negative test. | Open, partially mitigated. |
| `RSK-050` | Repeated actions or no-progress loop consume resources. | High | Action signatures, no-progress counter and finite iterations. | Open; full budgets/recovery deferred. |
| `RSK-051` | Untrusted publication/evidence redirects tool selection. | Critical | Evidence remains untrusted data; provider cannot authorize; gateway allowlist; red-team case required later. | Open. |
| `RSK-052` | Run-state mutation/corruption causes wrong completion. | High | Application-owned typed projection and linkage checks. | Open; no durable integrity mechanism. |
| `RSK-053` | Decision arguments attempt to widen authority or select privileged tools. | Critical | Trusted principal injection, strict schemas, agent allowlist and pre-adapter policy. | Open, materially mitigated locally. |
| `RSK-054` | Local draft/mapping/review artifacts are mistaken for approved enterprise records. | Critical | Fixed status/disposition and repeated limitation labels. | Open. |
| `RSK-055` | Iteration-only guard does not bound tokens, time or monetary cost. | High | Finite iteration cap; S03C explicitly required. | Open. |
| `RSK-056` | Managed decision provider change degrades action or termination accuracy. | High | Provider-neutral contract and deterministic oracle; no live quality claim. | Open. |

## New assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-020` | The six S03A tools are sufficient to demonstrate one local unapproved impact-package goal. | Accepted for S03B only. |
| `ASM-021` | The deterministic decision provider is an executable test oracle, not evidence of managed-model planning quality. | Accepted. |

## New issues

| ID | Issue | Status | Resolution/plan |
|---|---|---|---|
| `ISS-025` | Exact S03A ZIP and individual `0.5.0` registers were not mounted in this execution. | Open/recorded | Reconstructed from the complete S03A chapter and handoff; package is a compatible overlay, not byte-exact continuation. |
| `ISS-026` | No managed decision model was live-called or evaluated. | Open | Add provider-specific adapter/evaluation only after current SDK and data-governance review. |
| `ISS-027` | Time, token, cost, tool-call/failure budgets, fallback, cancellation and recovery are not implemented. | Open; next-stage trigger | Execute S03C. |
| `ISS-028` | Final local state persistence is not durable checkpoint/resume or tamper-evident audit. | Open | Graph/harness and later audit stages. |

## Immediate next-stage priorities

`RSK-050`, `RSK-055`, `ISS-027` and `ISS-028` drive S03C. Enterprise identity, live connectors and production records remain later-stage gaps.
