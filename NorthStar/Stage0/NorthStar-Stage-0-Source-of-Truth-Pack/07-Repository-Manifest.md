# 07 - Repository Manifest

| Field | Value |
|---|---|
| Repository | `northstar-agentic-compliance` |
| Repository version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Stage 0 scaffold implemented |
| Python baseline | 3.12 |
| Stage 0 tests executed with | Python 3.13.5 |
| External runtime dependencies | None |

## 1. Repository tree

```text
northstar-agentic-compliance/
├── .env.example
├── README.md
├── pyproject.toml
├── stage0-build-manifest.json
├── stage0-validation-report.txt
├── config/
│   └── README.md
├── datasets/
│   └── README.md
├── deployment/
│   └── README.md
├── docs/
│   ├── adr/
│   │   └── README.md
│   ├── architecture/
│   │   └── README.md
│   ├── runbooks/
│   │   └── README.md
│   ├── source-of-truth/
│   │   ├── 00-Project-Constitution.md
│   │   ├── 01-Business-and-User-Story-Baseline.md
│   │   ├── 02-Requirements-Register.md
│   │   ├── 03-Architecture-Baseline.md
│   │   ├── 04-Component-and-Agent-Catalogue.md
│   │   ├── 05-Data-and-Schema-Register.md
│   │   ├── 06-ADR-Register.md
│   │   ├── 07-Repository-Manifest.md
│   │   ├── 08-Risk-Assumption-and-Issue-Register.md
│   │   └── 09-Stage-Handoff-Pack.md
│   └── stages/
│       └── Stage-0-Playbook-Foundation-and-Architecture-Constitution.md
├── notebooks/
│   └── README.md
├── scripts/
│   └── validate_source_of_truth.py
├── src/
│   └── northstar_agentic_compliance/
│       ├── __init__.py
│       └── constitution.py
└── tests/
    ├── __init__.py
    └── unit/
        ├── __init__.py
        └── test_source_of_truth.py
```

## 2. Important entry points

| Path | Purpose |
|---|---|
| `docs/stages/Stage-0-Playbook-Foundation-and-Architecture-Constitution.md` | Complete Stage 0 tutorial section. |
| `docs/source-of-truth/00-Project-Constitution.md` | Rules, identifiers, conventions, roadmap and definitions of done. |
| `docs/source-of-truth/09-Stage-Handoff-Pack.md` | Exact reconstruction and continuation input. |
| `scripts/validate_source_of_truth.py` | Dependency-free structural validation. |
| `tests/unit/test_source_of_truth.py` | Executable Stage 0 tests. |
| `src/northstar_agentic_compliance/constitution.py` | Machine-readable Stage 0 constants and required artefact names. |

## 3. Files added in Stage 0

All files shown in the tree were added.

## 4. Files modified in Stage 0

None; this is the initial repository baseline.

## 5. Files retired in Stage 0

None.

## 6. Environment and configuration

`.env.example` contains no secret values. Stage 0 requires no model key or external service.

## 7. Commands

```bash
cd northstar-agentic-compliance
python3.12 scripts/validate_source_of_truth.py
python3.12 -m unittest discover -s tests -p 'test_*.py' -v
```

The Stage 0 validation was executed with Python 3.13.5 because Python 3.12 was not installed in the execution environment. Python 3.12 remains the selected project baseline; direct 3.12 execution must be confirmed before Stage 1 implementation is accepted.

## 8. Compatibility notes

- No external package or API compatibility exists yet.
- Markdown artefact names and canonical paths are compatibility constraints.
- Component, requirement, data, interface and ADR identifiers are stable after acceptance.
- Mermaid diagrams are source-controlled text; full renderer validation is pending a stage with an approved Mermaid toolchain.

## 9. Repository evolution rules

1. Extend existing modules rather than creating disconnected chapter projects.
2. Record complete code for foundational or materially changed files.
3. Add external dependencies only with version verification, rationale and lockfile update.
4. Keep local mocks for optional paid services.
5. Do not commit secrets, generated credentials or production data.
6. Update this manifest and the handoff pack in every stage.
