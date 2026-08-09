# 08 Risk, Assumption and Issue Register - S09A Overlay

## Threat risks

| ID | Threat | Scope | Score | Status |
|---|---|---|---|---|
| `RSK-310` | Direct prompt injection changes the task goal | current | inherent 20 / residual 8 | open_controlled |
| `RSK-311` | Indirect prompt injection embedded in regulatory publication | current | inherent 25 / residual 12 | open_controlled |
| `RSK-312` | Jailbreak defeats model behavioural constraints | current | inherent 16 / residual 9 | open_controlled |
| `RSK-313` | Retrieval poisoning supplies false or malicious evidence | current | inherent 20 / residual 12 | open_controlled |
| `RSK-314` | Tool description or schema poisoning redirects capability use | current | inherent 15 / residual 8 | open_controlled |
| `RSK-315` | Compromised tool returns hostile instructions or forged success | current | inherent 20 / residual 12 | open_controlled |
| `RSK-316` | Excessive agency causes unauthorized action | current | inherent 15 / residual 4 | open_controlled |
| `RSK-317` | Confused-deputy abuse of integration proxy | current | inherent 20 / residual 12 | open_controlled |
| `RSK-318` | Authorization token replay or audience confusion | current | inherent 20 / residual 8 | open_controlled |
| `RSK-319` | Agent, worker or service impersonation | current | inherent 15 / residual 8 | open_controlled |
| `RSK-320` | Cross-tenant or cross-case evidence leakage | current | inherent 15 / residual 10 | open_controlled |
| `RSK-321` | Secrets or credentials exposed to model/context/logs | current | inherent 15 / residual 8 | open_controlled |
| `RSK-322` | Dependency, model, prompt or configuration supply-chain compromise | current | inherent 20 / residual 12 | open_controlled |
| `RSK-323` | Malicious MCP server or dynamic capability poisoning | future | inherent 15 / residual 5 | future_not_active |
| `RSK-324` | Unexpected code execution from natural-language or tool arguments | current | inherent 15 / residual 5 | open_controlled |
| `RSK-325` | Sandbox escape or browser/computer-use compromise | future | inherent 10 / residual 5 | future_not_active |
| `RSK-326` | Case-working memory poisoning changes later behaviour | current | inherent 20 / residual 8 | open_controlled |
| `RSK-327` | Cross-case memory leakage or unauthorized recall | current | inherent 15 / residual 5 | open_controlled |
| `RSK-328` | Checkpoint or protected state tampering | current | inherent 15 / residual 8 | open_controlled |
| `RSK-329` | Duplicate or replayed work causes repeated side effects | current | inherent 20 / residual 8 | open_controlled |
| `RSK-330` | Audit or trace tampering enables repudiation | current | inherent 15 / residual 8 | open_controlled |
| `RSK-331` | Judge manipulation or instruction contamination hides unsafe output | current | inherent 20 / residual 8 | open_controlled |
| `RSK-332` | Evaluation dataset poisoning or sealed-test contamination | current | inherent 15 / residual 8 | open_controlled |
| `RSK-333` | Resource exhaustion through oversized context or repeated calls | current | inherent 20 / residual 9 | open_controlled |
| `RSK-334` | Infinite loop, retry amplification or cost attack | current | inherent 16 / residual 6 | open_controlled |
| `RSK-335` | Queue flooding, starvation or cancellation abuse | current | inherent 16 / residual 9 | open_controlled |
| `RSK-336` | False evidence or tool failure cascades into incorrect assessment | current | inherent 20 / residual 12 | open_controlled |
| `RSK-337` | Polished explanation exploits reviewer trust or automation bias | current | inherent 20 / residual 12 | open_controlled |
| `RSK-338` | Reviewer account compromise or approval forgery | current | inherent 15 / residual 10 | open_controlled |
| `RSK-339` | Future Agent Card or capability advertisement spoofing | future | inherent 20 / residual 5 | future_not_active |
| `RSK-340` | Future inter-agent message spoofing, tampering or replay | future | inherent 20 / residual 5 | future_not_active |
| `RSK-341` | Future shared-memory poisoning across agents | future | inherent 20 / residual 5 | future_not_active |
| `RSK-342` | Future multi-agent cascading hallucination or error amplification | future | inherent 20 / residual 5 | future_not_active |
| `RSK-343` | Future agent collusion, consensus capture or voting manipulation | future | inherent 15 / residual 5 | future_not_active |
| `RSK-344` | Future rogue agent conceals or self-directs actions | future | inherent 15 / residual 5 | future_not_active |
| `RSK-345` | Threat-model report is mistaken for proof of security or release approval | current | inherent 16 / residual 8 | open_controlled |

## Assumptions

- `ASM-105`: The supplied S08C handoff accurately describes accepted `1.11.0` boundaries.
- `ASM-106`: Current executable paths have exactly one active `AGT-001`.
- `ASM-107`: MCP/A2A/multiple-agent paths remain inactive and are modelled only for future design review.
- `ASM-108`: A 1-5 ordinal scale is sufficient for tutorial prioritization when raw factors and limitations are preserved.
- `ASM-109`: Local synthetic misuse cases can validate control plumbing but not estimate production attack prevalence.
- `ASM-110`: Security acceptance remains a qualified human governance decision.

## Issues

| ID | Issue | Status |
|---|---|---|

| `ISS-140` | User-requested S09A precedes unresolved S08D. | Open; recorded by ADR-089. |
| `ISS-141` | Exact merged 1.11.0 repository/register set was not mounted. | Open; compatible overlay only. |
| `ISS-142` | No production identity, workload credential, mTLS/PoP or signed-message implementation. | Open for Stage 9B. |
| `ISS-143` | No adaptive red-team exercise or live external integration test. | Open. |
| `ISS-144` | Local trace/checkpoint evidence is not WORM or cryptographically signed. | Open for later audit stage. |
| `ISS-145` | Ordinal risk values are tutorial prioritization, not measured probability. | Accepted limitation. |
| `ISS-146` | Mermaid sources require renderer validation in target publication toolchain. | Open/recorded. |

