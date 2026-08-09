# 08 — Risk, Assumption and Issue Register

**Version:** 1.5.0

All inherited active items remain.

## New risks

| ID | Risk | Status |
|---|---|---|
| `RSK-161` | Capability/Agent Card spoofing | Open; local digest only |
| `RSK-162` | Protocol downgrade or version confusion | Mitigated locally by exact match |
| `RSK-163` | Binding substitution | Mitigated locally |
| `RSK-164` | Extension stripping | Mitigated by conformance failure |
| `RSK-165` | MCP remote server/tool poisoning | Open; no server activated |
| `RSK-166` | Tool annotations mistaken for authorization | Controlled by CMP-005/CMP-007 ownership |
| `RSK-167` | Endpoint impersonation | Open for production identity |
| `RSK-168` | Discovery SSRF/unsafe URL | Open; static loopback only |
| `RSK-169` | Header/body digest mismatch | Mitigated locally |
| `RSK-170` | Replay and stale capability records | Open for durable infrastructure |
| `RSK-171` | Cancellation/status forgery | Partially mitigated locally |
| `RSK-172` | Cross-tenant routing confusion | Open; synthetic tenant fixture |
| `RSK-173` | Oversized payload/resource exhaustion | Partially mitigated by bounded server |
| `RSK-174` | Error leakage | Mitigated by minimized errors |
| `RSK-175` | Adapter semantic loss | Mitigated by DATA-104/tests |
| `RSK-176` | Adapter/SDK supply-chain compromise | Open |
| `RSK-177` | Reference transport mistaken for production | Mitigated by status/warnings |
| `RSK-178` | Protocol evolution breaks mappings | Open; version-pinned profiles |
| `RSK-179` | False inference that protocol conformance justifies AGT-002 | Mitigated by inventory/gate tests |

## New assumptions

- `ASM-053`: exact version negotiation is acceptable for the regulated reference boundary.
- `ASM-054`: one serialized request is sufficient to prove S06C receiver enforcement.
- `ASM-055`: MCP's primary NorthStar fit remains tool/resource interoperability.
- `ASM-056`: A2A 1.0 plus an explicit extension can represent the candidate task mapping.
- `ASM-057`: concurrency remains unnecessary in S06C.

## New issues

- `ISS-080`: byte-exact prior repository/registers not all mounted; compatible overlay.
- `ISS-081`: no live MCP SDK/server/client conformance run.
- `ISS-082`: no live A2A SDK/server/client conformance run.
- `ISS-083`: no production identity/TLS/KMS/replay/revocation.
- `ISS-084`: no signed discovery/Agent Card registry.
- `ISS-085`: no gRPC/broker/framework adapter.
- `ISS-086`: no production workload/SLO/cost benchmark.
- `ISS-087`: Mermaid sources not CLI-rendered in repository validation.
