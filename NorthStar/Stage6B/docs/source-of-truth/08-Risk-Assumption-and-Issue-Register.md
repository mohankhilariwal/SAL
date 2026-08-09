# 08 — Risk, Assumption and Issue Register

**Version:** `1.4.0`

## New risks

| ID | Risk | Current response/status |
|---|---|---|
| RSK-144 | Endpoint impersonation. | Signed endpoint-bound envelope/grant; production workload identity open. |
| RSK-145 | Authority scope escalation. | Deterministic subset checks; tests pass. |
| RSK-146 | Bearer-token theft/replay. | Nonce/use/revocation reference; production sender-constrained token open. |
| RSK-147 | Message tampering/forgery. | Canonical digest/HMAC locally; KMS/non-repudiation open. |
| RSK-148 | Artefact tampering/substitution. | Content hash, case/access/provenance, receipt binding. |
| RSK-149 | Confused deputy at recipient/tool. | Audience/resource/data scope; authorization before load. |
| RSK-150 | Late result accepted after timeout. | Expiry and terminal-state rules. |
| RSK-151 | Cancellation not stopping remote work. | Cooperative semantics documented; transport/process control open. |
| RSK-152 | Duplicate task/message processing. | Duplicate envelope/use checks; distributed dedup open. |
| RSK-153 | Shared-state or memory bypass. | Disabled flags, immutable artefacts, tests. |
| RSK-154 | Candidate endpoint activated without governance. | One-active-agent release gate. |
| RSK-155 | Receipt/signature key compromise. | Production key lifecycle open. |
| RSK-156 | Clock skew affects expiry. | Fixed UTC local tests; trusted clock/skew policy open. |
| RSK-157 | Protocol adapter drops semantics. | Deferred conformance suite required. |
| RSK-158 | Added latency/cost exceeds value. | No activation; future representative benchmark. |
| RSK-159 | Verification result mistaken for approval. | Schema/non-goal/UI governance; human boundary preserved. |
| RSK-160 | Candidate/agent configuration poisoning. | Config scan/digests local; signed registry open. |

## New assumptions

| ID | Assumption | Status |
|---|---|---|
| ASM-048 | `CMP-003` remains the sole route/state/termination owner. | Accepted invariant. |
| ASM-049 | A one-hop sequential sandbox is sufficient to validate contracts. | Tutorial-only; revisit for distributed runtime. |
| ASM-050 | SHA-256/HMAC are available in supported Python versions. | Verified locally. |
| ASM-051 | Production identity can later map canonical grant fields to enterprise mechanisms. | Unverified; future design. |
| ASM-052 | Immutable artefact references are acceptable for future transport adapters. | To be validated in S06C. |

## New issues

| ID | Issue | Status |
|---|---|---|
| ISS-072 | Byte-exact S06A repository/registers not mounted; compatible overlay used. | Open/documented. |
| ISS-073 | No production IAM/token exchange/proof-of-possession/KMS. | Open. |
| ISS-074 | No durable distributed replay/revocation ledger or trusted clock. | Open. |
| ISS-075 | No transport/protocol adapter or conformance tests. | Open; next stage. |
| ISS-076 | No live second-agent/model quality benchmark. | Open; promotion still denied. |
| ISS-077 | No concurrency, queue, worker or distributed cancellation. | Open; later stage. |
| ISS-078 | Mermaid not CLI-rendered. | Open; static inspection only. |
| ISS-079 | No production audit/WORM, control plane, deployment or DR. | Open. |

All inherited active risks/issues remain.
