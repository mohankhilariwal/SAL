# NorthStar Agentic Compliance — Stage 2B

This repository overlay advances the accepted NorthStar architecture from prepared knowledge to **authorized retrieval, ranking, exact citations and retrieval/RAG evaluation**.

It remains deliberately non-agentic:

- no `AGT-*` identifier;
- no `TOOL-*` identifier;
- no model-selected actions;
- no workflow/case state;
- no approval or legal conclusion;
- no grounded model generation.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
# Standard installation (requires access to the configured package index)
pip install -e '.[dev]'
python scripts/run_stage2b_demo.py
python -m pytest
python scripts/validate_stage2b.py
python scripts/consistency_audit_stage2b.py
```

The acceptance environment used Python 3.13.5, NumPy 2.3.5 and pytest 9.0.2.

## Offline acceptance path

The supplied scripts add `src/` to `sys.path`, and the test configuration points pytest at `src/`. In an environment where NumPy and pytest are already installed, run the scripts and tests directly without downloading packages. The editable package install was also verified in the acceptance environment with `python -m pip install --no-build-isolation --no-deps -e .`.
