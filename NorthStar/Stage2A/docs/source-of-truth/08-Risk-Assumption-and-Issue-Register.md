# 08 — Risk, Assumption and Issue Register

**Version:** `0.3.0`

## 1. Preserved active items

The S01 handoff keeps active: `RSK-003`, `RSK-005`, `RSK-010`, `RSK-015`, `RSK-018`–`RSK-023`; `ASM-001`, `ASM-002`, `ASM-005`, `ASM-009`; and `ISS-002`, `ISS-003`, `ISS-004`, `ISS-006`, `ISS-007`, `ISS-008`. Their detailed text was not supplied separately and is not rewritten here.

## 2. New risks

| ID | Risk | Treatment / current status |
|---|---|---|
| `RSK-024` | Poisoned or instruction-bearing documents influence later model behavior. | Content is untrusted; limited risk flags; no model in S02A; adversarial tests; remains open for S02B. |
| `RSK-025` | Missing or incorrect access metadata leads to permission leakage. | Fail closed on missing groups; exact propagation tests; enterprise identity/PDP still open. |
| `RSK-026` | Chunk fragmentation separates conditions, exceptions or definitions. | Section boundaries, overlap, coordinate preservation; retrieval evaluation/tuning deferred. |
| `RSK-027` | Stale or superseded content is treated as current. | Active/historical versions and effective dates; authoritative connector reconciliation remains open. |
| `RSK-028` | Parser/chunker changes silently alter retrieval behavior. | Transformation versions in identity; immutable history; rebuild/evaluation required. |
| `RSK-029` | Local JSON corpus is corrupted or partially published. | staging, atomic replace and independent validator; no tamper-evident store. |
| `RSK-030` | Manual export is incomplete or delayed. | manifest/run evidence; source-owner review; live connectors deferred. |
| `RSK-031` | Regex risk flags create false negatives or false confidence. | Explicitly diagnostic only; no safety claim; future retrieval/output controls required. |
| `RSK-032` | Character/line chunk limits do not match tokenizer or semantic boundaries. | Configurable policy; tune during S02B evaluation. |

## 3. New assumptions

| ID | Assumption | Status |
|---|---|---|
| `ASM-010` | Synthetic Markdown fixtures are sufficient to validate the S02A contract. | Accepted for tutorial only. |
| `ASM-011` | Source owners can supply accurate authority, dates, groups, purpose and residency metadata. | Unverified production assumption. |
| `ASM-012` | S02B indexes can consume JSONL chunks without changing their evidence semantics. | To verify in S02B. |

## 4. New issues

| ID | Issue | Status |
|---|---|---|
| `ISS-009` | The nine detailed S01 registers/repository files were not attached; baseline reconstructed from S01 handoff. | Open documentation exception. |
| `ISS-010` | No PDF/Office/HTML/image/OCR parser selected. | Open by stage scope. |
| `ISS-011` | No enterprise source connector/change feed. | Open for later implementation. |
| `ISS-012` | No authenticated identity/PDP or source-system ACL reconciliation. | Open; must precede production retrieval. |
| `ISS-013` | No large-corpus performance/concurrency benchmark. | Open pending workload evidence. |
| `ISS-014` | Mermaid CLI rendering not executed. | Open tooling exception. |
| `ISS-015` | Python 3.12 direct execution not performed. | Open compatibility exception. |

## 5. Immediate S02B priorities

`RSK-024`, `RSK-025`, `RSK-026`, `RSK-027`, `RSK-032`, `ISS-011`, `ISS-012` and `ASM-012` must drive retrieval design and evaluation.
