# Requirements Register — 0.9.0

## Functional requirements

| ID | Requirement | Implementation | Verification |
|---|---|---|---|
| FR-096 | Enter an explicit approval wait only after the six-milestone unapproved package is complete. | N70/N75 | TEST-146 |
| FR-097 | Persist run, wait, correlation and expiry and release execution resources. | DATA-058/059, INT-036/037 | TEST-146/147 |
| FR-098 | Accept only approve or reject review decisions. | DATA-007, INT-038 | TEST-144/148/149 |
| FR-099 | Validate signature, active token, expiry, role, SoD and single use. | CTL-051–054 | TEST-139–145 |
| FR-100 | Route approved and rejected decisions deterministically. | N80/N82/N84 | TEST-148/149 |
| FR-101 | Route expiry to escalation; never auto-approve. | N80/N86 | TEST-150 |
| FR-102 | Resume from durable state without repeating completed `TOOL-006`. | INT-040 | TEST-151/155 |
| FR-103 | Prevent simultaneous duplicate resume with a bounded lease. | DATA-062 | TEST-152/153 |
| FR-104 | Bind durable state and callback claims to `GRAPH-001` version `1.1.0`. | DATA-058/060 | TEST-154 |
| FR-105 | Expose waiting, decision and timeout transition evidence. | DATA-057/061 | TEST-156 |

## Non-functional requirements

`NFR-075` durable across process restart; `NFR-076` atomic transaction boundaries; `NFR-077` fail-closed deterministic validation; `NFR-078` bounded lease; `NFR-079` no busy polling; `NFR-080` standard-library local runtime; `NFR-081` privacy-minimal callback claims; `NFR-082` checksummed state/decision payloads; `NFR-083` no model/tool replay after wait.

## Controls

`CTL-051` HMAC signature; `CTL-052` expiry and active-token digest; `CTL-053` reviewer role and initiator/reviewer SoD; `CTL-054` unique wait/decision/nonce; `CTL-055` reject reason; `CTL-056` timeout escalates; `CTL-057` graph-version binding; `CTL-058` idempotent `TOOL-006`; `CTL-059` bounded resume lease.
