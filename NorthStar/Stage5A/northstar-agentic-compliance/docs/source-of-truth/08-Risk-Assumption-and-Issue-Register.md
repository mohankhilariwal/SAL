# 08 — Risk, Assumption and Issue Register

**Version:** `1.1.0`

All inherited active production risks/issues remain. S05A adds:

## Risks

| ID | Risk | Control/response | Status |
|---|---|---|---|
| `RSK-099` | Specification drifts from code/graph/tools. | Semantic validation, manifest binding, assertions, audit. | Partially mitigated |
| `RSK-100` | Specification is mistaken for runtime authority. | Non-authority invariant; independent gateway/PDP/approval/graph ownership. | Mitigated by design; human misuse remains |
| `RSK-101` | Structurally valid spec omits unsafe semantic contradiction. | Application semantic validator and negative tests. | Partial; validator completeness risk remains |
| `RSK-102` | Spec/manifest file substitution or tampering. | Canonical digest mismatch fails. | Partial; no signing/KMS/attestation |
| `RSK-103` | Stale active spec permits obsolete operation. | lifecycle/effective date/change policy/gate. | Partial; no production registry |
| `RSK-104` | Teams game tests/gates rather than business risk. | required human/security review; evaluation not authority. | Open |
| `RSK-105` | Provisional local SLOs create false production confidence. | explicit scope labels and no production claim. | Mitigated/documented |
| `RSK-106` | Retired agent remains callable. | active-status pre-start assertion. | Locally mitigated |
| `RSK-107` | Context profile is too broad/narrow, causing leakage or poor quality. | exact allowlists, access-first, budgets, future review. | Partial |
| `RSK-108` | JSON Schema/tooling portability differs across validators. | application validator remains canonical local check; conformance deferred. | Open |
| `RSK-109` | Strict mismatch blocks legitimate continuation. | fail closed; controlled correction/new run/migration ADR. | Accepted trade-off |
| `RSK-110` | Constraints duplicated across spec, manifest and code diverge. | generated/derived checks and consistency audit. | Partial |
| `RSK-111` | Specification governance slows safe changes. | owners, semantic versioning, bounded review triggers. | Open |

## Assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-035` | JSON is acceptable as the canonical local machine-readable form. | Accepted for S05A |
| `ASM-036` | Named business, technical, risk and operations owners review relevant changes. | Accepted, not operationally proven |
| `ASM-037` | Supplied S04C handoff/chapter accurately represent accepted runtime semantics. | Accepted with reconstruction caveat |
| `ASM-038` | Local benchmark evidence is only control-path evidence, not production workload evidence. | Accepted |

## Issues

| ID | Issue | Status |
|---|---|---|
| `ISS-050` | Byte-exact complete S04C repository and all ten individual `1.0.0` registers were not mounted; S05A is a compatible reconstruction overlay. | Open/recorded |
| `ISS-051` | No external JSON Schema implementation/conformance matrix executed; application validator enforces the local subset. | Open |
| `ISS-052` | Mermaid CLI rendering not available; sources receive structural checks only. | Open |
| `ISS-053` | Python 3.11, 3.12 and 3.14 were not separately executed; 3.13.5 passed. | Open |
| `ISS-054` | No signed remote registry, KMS, build provenance or deployment attestation. | Open |
| `ISS-055` | No production performance, availability, cost, semantic quality, legal or human-review benchmark. | Open |
| `ISS-056` | Context compaction, regeneration, memory write/read/delete/expiry and cross-case isolation are deliberately deferred to S05B. | Deferred |
