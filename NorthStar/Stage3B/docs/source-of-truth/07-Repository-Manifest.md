# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `0.6.0`  
**Python:** `>=3.11,<3.15`  
**Dependencies:** `jsonschema==4.26.0`; development `pytest==9.0.2`.

## Repository boundary

This is a compatible S03B overlay reconstructed from the complete S03A chapter and handoff. It includes the six S03A tool contracts/gateway surface required by the new agent. It is not a byte-exact copy of the unavailable S03A archive (`ISS-025`).

## Important entry points

- `src/northstar_compliance/agent/runtime.py` — `INT-021` bounded loop.
- `src/northstar_compliance/agent/decision.py` — `INT-022` provider-neutral decision contract.
- `src/northstar_compliance/agent/termination.py` — `INT-024` completion and guard rules.
- `src/northstar_compliance/tools/gateway.py` — retained gateway-only execution.
- `scripts/run_stage3b_demo.py` — accepted local happy path.
- `scripts/run_stage3b_evaluation.py` — terminal/authority scenarios.
- `scripts/validate_stage3b.py` — structural/schema validator.
- `scripts/consistency_audit_stage3b.py` — cross-artifact audit.

## Complete file inventory

```text
.env.example
CHANGELOG.md
README.md
config/tools/TOOL-001.json
config/tools/TOOL-002.json
config/tools/TOOL-003.json
config/tools/TOOL-004.json
config/tools/TOOL-005.json
config/tools/TOOL-006.json
config/tools/tool-descriptor.schema.json
datasets/stage3b/decision-scenarios.json
docs/adr/ADR-022-bounded-single-agent-loop.md
docs/adr/ADR-023-explicit-run-state-and-layered-termination.md
docs/architecture/diagrams/cumulative-logical-architecture.mmd
docs/architecture/diagrams/stage-3b-agent-loop.mmd
docs/architecture/diagrams/stage-3b-architecture-before.mmd
docs/architecture/diagrams/stage-3b-sequence.mmd
docs/architecture/diagrams/stage-3b-state-transition.mmd
docs/architecture/diagrams/stage-3b-trust-boundary.mmd
docs/references/Stage-3B-Technical-Sources.md
docs/source-of-truth/00-Project-Constitution.md
docs/source-of-truth/01-Business-and-User-Story-Baseline.md
docs/source-of-truth/02-Requirements-Register.md
docs/source-of-truth/03-Architecture-Baseline.md
docs/source-of-truth/04-Component-and-Agent-Catalogue.md
docs/source-of-truth/05-Data-and-Schema-Register.md
docs/source-of-truth/06-ADR-Register.md
docs/source-of-truth/07-Repository-Manifest.md
docs/source-of-truth/08-Risk-Assumption-and-Issue-Register.md
docs/source-of-truth/09-Stage-Handoff-Pack.md
docs/stages/Stage-3B-Single-Agent-Loop-and-Termination.md
docs/validation/Stage-3B-Validation-Report.txt
examples/stage3b-output/cases/CASE-09C3D1058846E9F0.json
examples/stage3b-output/demo-console.txt
examples/stage3b-output/evaluation-report.json
examples/stage3b-output/events/tool-events.jsonl
examples/stage3b-output/mappings/MAP-95CC56C68DEDA513.json
examples/stage3b-output/review-queue/REV-3ABDFE076F1AB28D.json
examples/stage3b-output/runs/RUN-D4C4A1A5A3DD49A0.json
pyproject.toml
scripts/consistency_audit_stage3b.py
scripts/run_stage3b_demo.py
scripts/run_stage3b_demo.sh
scripts/run_stage3b_evaluation.py
scripts/validate_stage3b.py
src/northstar_compliance/__init__.py
src/northstar_compliance/agent/__init__.py
src/northstar_compliance/agent/decision.py
src/northstar_compliance/agent/factory.py
src/northstar_compliance/agent/models.py
src/northstar_compliance/agent/runtime.py
src/northstar_compliance/agent/termination.py
src/northstar_compliance/tools/__init__.py
src/northstar_compliance/tools/adapters.py
src/northstar_compliance/tools/factory.py
src/northstar_compliance/tools/gateway.py
src/northstar_compliance/tools/models.py
src/northstar_compliance/tools/policy.py
src/northstar_compliance/tools/registry.py
src/northstar_compliance/tools/storage.py
tests/evaluation/test_stage3b_evaluation.py
tests/integration/test_agent_loop.py
tests/security/test_agent_authority.py
tests/unit/test_agent_models.py
tests/unit/test_termination.py
```

## Files added in S03B

- `src/northstar_compliance/agent/` and related tests/scripts/dataset.
- `ADR-022`, `ADR-023` and S03B diagrams/references/chapter.
- Updated source-of-truth artefacts at `0.6.0`.
- Executed demo/evaluation and validation evidence.

## Files modified/reconstructed

- package metadata, README and changelog;
- cumulative architecture;
- compatible S03A tool descriptor/gateway surface included in this overlay.

## Files retired

None.

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
python scripts/run_stage3b_demo.py
python scripts/run_stage3b_evaluation.py
python scripts/validate_stage3b.py
python scripts/consistency_audit_stage3b.py
python -m compileall -q src scripts
```

## Compatibility constraints

- preserve schema version `1.0.0` for current executable contracts;
- preserve `AGT-001` as the only agent;
- preserve `TOOL-001`–`TOOL-006` exact versions and gateway-only invocation;
- preserve fixed unapproved/human-review semantics;
- preserve application-owned identity, progress, completion and disposition;
- do not add graph, memory or additional agents during S03C.
