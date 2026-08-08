# 08 — Risk, Assumption and Issue Register

**Version:** `1.2.0`  
All inherited active items remain open unless previously closed. S05B adds the following.

## 1. Risks

| ID | Risk | Current mitigation / residual status |
|---|---|---|
| `RSK-112` | Memory overrides newer authoritative state. | Architectural precedence and regeneration-from-state; residual adapter/integration risk. |
| `RSK-113` | Model-generated or hallucinated facts become durable memory. | Origin allowlist and no direct model writes; residual future adapter risk. |
| `RSK-114` | Cross-tenant/cross-case/cross-user leakage. | Exact scope grants, partitioning, path validation and tests; production IAM/PDP unresolved. |
| `RSK-115` | Stale memory influences an assessment. | Source-version comparison and default exclusion; source-version feed not production-integrated. |
| `RSK-116` | Compaction drops a critical qualification. | Required item pinning, complete typed items and omission ledger; schema coverage remains important. |
| `RSK-117` | Memory poisoning through instruction-like content. | Authoritative origins and content rejection; sophisticated semantic poisoning remains possible upstream. |
| `RSK-118` | Consent is absent, expired, revoked or wrong-purpose. | Operation-specific grant checks; local grants are synthetic/unsigned. |
| `RSK-119` | Retention is too long or inappropriate for legal/records obligations. | Provisional 14/30-day limits; qualified privacy/records review required. |
| `RSK-120` | Deletion leaves recoverable replicas/backups. | Local content deletion and tombstone; distributed backup deletion not implemented. |
| `RSK-121` | Tombstone leaks sensitive facts. | Content-free tombstone; production logs/telemetry still require review. |
| `RSK-122` | Hashing is mistaken for authenticated integrity. | Explicitly documented as local tamper detection only; KMS/signatures pending. |
| `RSK-123` | Idempotency or concurrent writers create duplicate/conflicting records. | Idempotency key and one active record locally; distributed concurrency unresolved. |
| `RSK-124` | Context regeneration causes excess latency/cost. | Deterministic local projection and target budget; enterprise-scale benchmark pending. |
| `RSK-125` | Memory storage grows or creates unbounded profiles. | One active record/case, limits, expiry, no cross-case consolidation. |
| `RSK-126` | Approval tokens or final decisions leak into memory. | Field stripping/rejection and tests; upstream logging remains separate risk. |
| `RSK-127` | User requests stale inclusion and relies on it. | `include_stale` is off by default; production policy should restrict override to controlled diagnostics. |
| `RSK-128` | Future teams enable broader memory categories through configuration drift. | Policy boundary validator, specification flags and deployment evaluation; signed config pending. |

## 2. Assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-039` | `DATA-009` and source versions are available at resume time. | Required; no production availability proof. |
| `ASM-040` | One case-local continuity record is sufficient for S05B's use case. | Accepted for tutorial; review with real analyst workflows. |
| `ASM-041` | Fourteen-day default and 30-day maximum are safe tutorial values, not legal policy. | Explicitly provisional. |
| `ASM-042` | Source version identifiers accurately represent material changes. | Synthetic/local evidence only. |
| `ASM-043` | Current context item schemas expose all critical qualifiers that must be pinned. | Requires domain evaluation before production. |

## 3. Issues

| ID | Issue | Status |
|---|---|---|
| `ISS-057` | S05B is a compatible reconstruction overlay, not a byte-exact extension of the unavailable full S05A repository/register set. | Open/documented. |
| `ISS-058` | Consent and principal claims are synthetic local objects, not enterprise IAM/PDP decisions. | Open. |
| `ISS-059` | Local JSON is unencrypted and unsigned; SHA-256 is not attacker-resistant authentication. | Open. |
| `ISS-060` | No production retention schedule, legal basis, records classification or deletion propagation. | Open. |
| `ISS-061` | No distributed concurrency, transaction, replica, backup or DR validation for memory lifecycle. | Open. |
| `ISS-062` | No large-case semantic quality study of compacted context or human analyst benchmark. | Open. |
| `ISS-063` | Mermaid sources were structurally checked but not CLI-rendered. | Open. |
| `ISS-064` | Python 3.11/3.12/3.14 and external JSON Schema validators were not separately executed. | Open. |

## 4. Risk acceptance boundary

The local controls demonstrate architecture semantics only. They do not establish legal compliance, enterprise security certification, production reliability or evidence admissibility.
