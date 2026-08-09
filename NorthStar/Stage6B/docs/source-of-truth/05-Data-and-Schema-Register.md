# 05 — Data and Schema Register

**Version:** `1.4.0`  
`DATA-001`–`090` and `INT-001`–`062` remain accepted. S06B adds:

## Data objects

| ID | Name | Owner | Executable status |
|---|---|---|---|
| DATA-091 | AgentEndpointDescriptor | CMP-003/CMP-011 | Dataclass + JSON Schema |
| DATA-092 | DelegatedTaskEnvelope | CMP-003 | Dataclass + JSON Schema |
| DATA-093 | AttenuatedAuthorityGrant | CMP-007 | Dataclass + JSON Schema |
| DATA-094 | HandoffReceipt | Recipient/CMP-003 | Dataclass + JSON Schema |
| DATA-095 | HandoffArtifactManifest | Artefact owner/store | Dataclass + JSON Schema |
| DATA-096 | VerificationResultArtifact | Candidate sandbox | JSON Schema + output manifest |
| DATA-097 | HandoffStatusEvent | CMP-003 | Dataclass + JSON Schema |
| DATA-098 | HandoffFailureEnvelope | Failure origin/CMP-003 | JSON Schema |
| DATA-099 | HandoffTerminationRecord | CMP-003 | JSON Schema |

## Interface contracts

| ID | Name | Authorization/control |
|---|---|---|
| INT-063 | Endpoint and Handoff Contract Validation | Exact endpoint/schema/policy versions; deny prohibited powers. |
| INT-064 | Authority Mint, Attenuate and Verify | Issuer `CMP-007`; subset scope, audience, expiry, nonce, use/depth. |
| INT-065 | Task Offer and Receipt | Signed envelope and signed accept/reject/result receipt. |
| INT-066 | Immutable Artefact Exchange | Authorization before load; hash/provenance/case/subject checks. |
| INT-067 | Status and Progress | Orchestrator-owned transition allowlist and correlation. |
| INT-068 | Timeout, Cancellation and Failure Propagation | Expiry/revocation, cancellation acknowledgement, typed safe failures. |
| INT-069 | Sequential Handoff Contract Sandbox | Local deterministic test-only execution. |
| INT-070 | System Termination Decision | All tracked tasks terminal, grants contained, artefacts verified; human owner preserved. |

## Schema and state constraints

- Canonical UTC timestamps and canonical JSON are used for local digests.
- Unknown/prohibited capabilities fail closed.
- `DATA-009` is not embedded or directly mutated.
- `DATA-081` is not automatically transferred.
- Artefacts are immutable and content-hashed.
- `DATA-096` is an evidence verdict with `approval_status=not_an_approval`.
- Handoff status cannot set graph routes or final disposition by itself.
