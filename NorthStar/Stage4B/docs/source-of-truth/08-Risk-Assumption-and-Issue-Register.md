# Risk, Assumption and Issue Register — 0.9.0

Inherited active items remain.

## New risks

- `RSK-077` stolen callback token; mitigated locally by signature, expiry, active-token digest and role/SoD checks.
- `RSK-078` duplicate/conflicting decisions; unique wait/nonce/decision constraints.
- `RSK-079` stale worker or duplicate resume; bounded lease and optimistic revision.
- `RSK-080` timer delay or clock skew; UTC timestamps and explicit escalation, production clock service pending.
- `RSK-081` approval fatigue/bottleneck; measurable wait age and later queue policy required.
- `RSK-082` local database loss/corruption; checksums help detection but no backup/DR.
- `RSK-083` synthetic roles accepted as identity; enterprise IAM/PDP required.
- `RSK-084` human approval mistaken for final legal conclusion; preliminary disposition naming and governance warning.
- `RSK-085` callback endpoint abuse/rate exhaustion; production gateway/rate limits pending.
- `RSK-086` graph/token version drift; exact version binding and fail closed.

## Assumptions

`ASM-028` local host clock is sufficiently accurate for tests; `ASM-029` one SQLite database is available to the single-process tutorial runtime; `ASM-030` Daniel's identity/role claims are synthetic fixtures, not production credentials.

## Issues

`ISS-036` byte-exact 0.8.0 repository/registers were not mounted; this is a compatible 0.9.0 overlay. `ISS-037` no enterprise reviewer authentication/PDP. `ISS-038` no managed durable engine conformance or multi-region durability. `ISS-039` no production callback endpoint, rate limit or notification delivery. `ISS-040` no dual approval/delegation/override. `ISS-041` Mermaid statically checked but not rendered. `ISS-042` SQLite durability/throughput not benchmarked at enterprise scale.
