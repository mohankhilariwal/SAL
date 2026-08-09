# 02 — Requirements Register (1.9.0 Overlay)

All accepted requirements through S07C remain. New requirements:

| ID | Requirement | Status |
|---|---|---|
| `S08A-REQ-001` | Define layered evaluation hierarchy. | Implemented/local |
| `S08A-REQ-002` | Register immutable suites/datasets/cases/graders. | Implemented/local |
| `S08A-REQ-003` | Separate dev/validation/sealed test. | Implemented/local |
| `S08A-REQ-004` | Require provenance, scope, locale, risk and temporal metadata. | Implemented/local |
| `S08A-REQ-005` | Cover nine required scenario families, with multi-agent inactive. | Implemented/local |
| `S08A-REQ-006` | Keep WP-008 inactive. | Implemented/local |
| `S08A-REQ-007` | Separate outcome and trace grading. | Implemented/local |
| `S08A-REQ-008` | Use deterministic hard-control graders. | Implemented/local |
| `S08A-REQ-009` | Defer LLM-as-a-Judge. | Implemented/local |
| `S08A-REQ-010` | Isolate trial environments. | Implemented/local |
| `S08A-REQ-011` | Support bounded repeated trials. | Implemented/local |
| `S08A-REQ-012` | Generate digests and duplicate checks. | Implemented/local |
| `S08A-REQ-013` | Block test execution by default. | Implemented/local |
| `S08A-REQ-014` | Minimize evidence payloads. | Implemented/local |
| `S08A-REQ-015` | Define human-review sampling. | Implemented/local |
| `S08A-REQ-016` | Quarantine rather than mutate accepted cases. | Implemented/local |
| `S08A-REQ-017` | Preserve all S07C constraints. | Implemented/local |
| `S08A-REQ-018` | Keep results advisory and block DATA-106 mutation. | Implemented/local |
| `S08A-REQ-019` | Provide runnable local code and negative tests. | Implemented/local |
| `S08A-REQ-020` | Update all artefacts and audit. | Implemented/local |

## Traceability summary

- Registry/lineage: `DATA-131/132/140/141`, `INT-103/104/110`, `ADR-074`.
- Cases/rubrics/graders: `DATA-133`–`136`, `INT-105/107`, `ADR-073/075`.
- Runs/results: `DATA-137`–`139`, `INT-106/109/111`, `ADR-076`.
- Human sampling: `DATA-142`, `INT-108`, `CMP-006`.
- Sequencing: `ADR-072`, `ISS-114`.
- Executable evidence: `TEST-508`–`562`, `EVAL-116`–`130`.
