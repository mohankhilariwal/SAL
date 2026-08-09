# 02 — Requirements Register

**Version:** `1.4.0`  
All requirements through S06A remain accepted. S06B adds the following.

## Functional requirements

| ID | Requirement | Owner | Implementation | Verification |
|---|---|---|---|---|
| FR-170 | Versioned endpoint descriptor. | CMP-003/CMP-011 | `models.py`, candidate config | TEST-299–303 |
| FR-171 | Canonical signed task/message envelope. | CMP-003 | `HandoffEnvelope`, `EnvelopeService` | TEST-281–285 |
| FR-172 | Bind sender/recipient/case/run/task/purpose. | CMP-003/CMP-007 | envelope + grant checks | TEST-284, 305 |
| FR-173 | Goal/non-goals/schema/deadline/attempt/hop limits. | CMP-003 | `HandoffPolicy`, envelope validation | TEST-281, 285 |
| FR-174 | `CMP-007` attenuated authority grant. | CMP-007 | `AuthorityService` | TEST-271–280 |
| FR-175 | Child scope must be a subset. | CMP-007 | `attenuate()` | TEST-273–276 |
| FR-176 | Audience/time/nonce/proof-key/task binding. | CMP-007 | grant model/verify | TEST-278–280, 305 |
| FR-177 | Use count, depth and revocation. | CMP-007 | `GrantUseLedger` | TEST-279–280 |
| FR-178 | Authorization before artefact load. | Recipient/CMP-007 | sandbox execution order | TEST-298 |
| FR-179 | Immutable hashed provenance artefacts. | CMP-003/store | `ArtifactDescriptor`, store | TEST-286–289 |
| FR-180 | Signed receipt binds envelope/grant/artefacts. | Recipient/CMP-003 | `HandoffReceipt` | TEST-290, 298 |
| FR-181 | Explicit deterministic lifecycle. | CMP-003 | `HandoffCoordinator` | TEST-291–297 |
| FR-182 | Cancellation/timeout/failure are non-success. | CMP-003 | lifecycle/schema | TEST-294–295 |
| FR-183 | Reject replay/duplicate/tamper/late/scope mismatch. | CMP-003/CMP-007 | validators/ledger | TEST-279, 282–289, 296 |
| FR-184 | Orchestrator remains sole task/route/termination owner. | CMP-003 | coordinator/policy | TEST-300, 302 |
| FR-185 | `DATA-009` ownership unchanged. | CMP-003 | architecture/config | consistency audit |
| FR-186 | Ephemeral private scratch; no automatic memory transfer. | CMP-003/CMP-010 | endpoint/config/payload checks | TEST-300, 303–304 |
| FR-187 | Sequential two-party contract sandbox. | CMP-010 | `SequentialHandoffSandbox` | TEST-298 |
| FR-188 | Exactly one active agent; candidate only. | CMP-011 | agent config/policy | TEST-299, 301 |
| FR-189 | Defer protocol and concurrency. | CMP-011 | disabled flags | TEST-302–303 |

## Non-functional requirements

| ID | Requirement | Verification |
|---|---|---|
| NFR-134 | Deterministic canonical serialization and digest. | TEST-306 |
| NFR-135 | Versioned schemas and strict unknown-power rejection. | validation/config tests |
| NFR-136 | Fail closed on signature/digest mismatch. | TEST-277, 282–283, 290 |
| NFR-137 | Least-privilege attenuation. | TEST-272–276 |
| NFR-138 | Bounded TTL/deadline/hops/attempts/use/depth. | TEST-275, 285, 294 |
| NFR-139 | Replay resistance in local reference ledger. | TEST-279 |
| NFR-140 | Stable trace/correlation/causation identity. | envelope schema/tests |
| NFR-141 | Privacy-minimized messages and safe failure fields. | TEST-304 |
| NFR-142 | Transport-neutral contracts. | ADR-047/config |
| NFR-143 | Deterministic state transitions. | TEST-291–297 |
| NFR-144 | Local/offline reproducibility. | demo/evaluation/tests |
| NFR-145 | Standard-library runtime. | manifest/compile |
| NFR-146 | Honest benchmark scope. | benchmark report |
| NFR-147 | Backward compatibility with `1.3.0` invariants. | consistency audit |
| NFR-148 | Explicit non-production cryptography limitations. | docs/references |
| NFR-149 | No false multi-agent/protocol/concurrency claim. | config/tests/audit |

## Controls

| ID | Control |
|---|---|
| CTL-113 | Exact active/candidate endpoint allowlist. |
| CTL-114 | Only `CMP-007` can issue a grant. |
| CTL-115 | Subset attenuation for tools/operations/resources/data. |
| CTL-116 | Audience/case/run/task/purpose binding. |
| CTL-117 | Expiry/not-before/use/depth constraints. |
| CTL-118 | Nonce replay and revocation ledger. |
| CTL-119 | Authorization before artefact load. |
| CTL-120 | Immutable content hash and case/access checks. |
| CTL-121 | Signed receipt binding. |
| CTL-122 | Lifecycle transition allowlist. |
| CTL-123 | Terminal-state immutability and late-result denial. |
| CTL-124 | Cancellation acknowledgement or expiry. |
| CTL-125 | No raw credentials, callback tokens, memory or hidden reasoning in envelope. |
| CTL-126 | Recipient has no tools/routing/memory/delegation/approval/finalization/concurrency. |
| CTL-127 | Exactly one active agent release gate. |
| CTL-128 | No shared mutable state/shared-agent memory. |
| CTL-129 | No protocol or concurrency activation. |
| CTL-130 | Stage validation and consistency audit gate. |
