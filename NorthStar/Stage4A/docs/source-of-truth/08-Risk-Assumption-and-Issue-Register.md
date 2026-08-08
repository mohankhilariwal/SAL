# 08 — Risk, Assumption and Issue Register

**Version:** `0.8.0`

Inherited active risks, assumptions and issues remain. S04A adds:

## Risks

| ID | Risk | Mitigation/status |
|---|---|---|
| `RSK-067` | Invalid or unreachable graph path causes unsafe/stranded execution. | Definition validator and tests; open production validation. |
| `RSK-068` | Node mutates authority or unrelated state. | Exact patch ownership/protected paths; mitigated locally. |
| `RSK-069` | Model indirectly selects arbitrary route/node. | Application route table; mitigated. |
| `RSK-070` | Graph cycles cause runaway work. | Independent transition budget plus S03C budgets; mitigated locally. |
| `RSK-071` | Checkpoint resumes under incompatible graph version. | ID/version binding; running migration deferred. |
| `RSK-072` | Policy preflight is mistaken for authoritative authorization. | Gateway rechecks every invocation; documentation/tests. |
| `RSK-073` | Custom graph kernel accumulates framework-level complexity. | Small feature boundary and ADR review trigger. |
| `RSK-074` | Copy-on-write state becomes expensive at scale. | Small local state; benchmark deferred. |
| `RSK-075` | Transition evidence is mistaken for audit/event sourcing. | Explicit non-claim; audit stage deferred. |
| `RSK-076` | Static sequential graph cannot represent real human waits/durable timers. | Deferred to S04B. |

## Assumptions

- `ASM-025`: One sequential graph and one agent remain sufficient for the current local use case.
- `ASM-026`: The six milestone sequence is stable enough to prove graph semantics before human waiting/parallelism.
- `ASM-027`: Graph definitions are trusted deployment artifacts in this local stage.

## Issues

- `ISS-032`: Byte-exact `0.7.0` repository and nine individual registers were not mounted; this is a compatible overlay reconstructed from the authoritative S03C handoff and prior exported records.
- `ISS-033`: Mermaid CLI rendering was not executed; structural/static review only.
- `ISS-034`: Migration of an in-flight `GRAPH-001` checkpoint across graph versions is not implemented.
- `ISS-035`: No framework conformance, managed workflow, durable timer, multi-process lease or production benchmark is verified.
