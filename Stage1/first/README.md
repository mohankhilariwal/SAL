# Agentic AI Architect Tutorial — Stage 1

This package contains the complete Stage 1 tutorial and its runnable supporting code.

## Contents

- `STAGE_1_PLAYBOOK.md` — executive overview, tutorial map, reference architecture, Chapters 1–5, 13 Mermaid diagrams, five labs, glossary and Stage 2 continuation heading.
- `src/stage1_agent/core.py` — fully offline bounded agent loop and harness.
- `examples/plain_python_agent.py` — offline runnable demonstration.
- `examples/langgraph_agent.py` — LangGraph 1.2.10 mapping using deterministic local tools.
- `examples/openai_agents_sdk_agent.py` — OpenAI Agents SDK 0.19.0 mapping with structured output.
- `scripts/check_compatibility.py` — exact dependency/interpreter compatibility report.
- `scripts/validate_artifacts.py` — required-heading, Mermaid-structure and audit-JSONL validation.
- `tests/` — behavioural tests and optional-framework import checks.

## Supported environment

- Python `>=3.11,<3.14`.
- Core code executed in the authoring environment with Python 3.13.5, Pydantic 2.13.4 and pytest 9.0.2.
- Optional framework versions are pinned to versions verified from official package metadata on 28 July 2026.

## Setup: source-tree method

This method avoids editable-package build isolation and is the method used for validation in the supplied environment.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-core-pinned.txt
export PYTHONPATH=src      # Windows PowerShell: $env:PYTHONPATH = "src"
```

## Setup: editable package method

Use this when your environment can access PyPI or an approved internal mirror for the build backend and dependencies.

```bash
python -m pip install -e '.[dev]'
python -m pip install -e '.[graph,dev]'
python -m pip install -e '.[sdk,dev]'
# or all optional dependencies:
python -m pip install -e '.[all]'
```

## Run the offline loop

```bash
PYTHONPATH=src python examples/plain_python_agent.py
PYTHONPATH=src python examples/plain_python_agent.py --approve-write
```

The first command safely pauses before the reversible write. The second completes and writes append-only JSONL teaching audit events to `artifacts/`.

## Validate

```bash
PYTHONPATH=src python -m compileall -q src examples tests scripts
PYTHONPATH=src python scripts/validate_artifacts.py
PYTHONPATH=src pytest -q
PYTHONPATH=src python scripts/check_compatibility.py
```

The compatibility checker intentionally exits non-zero when an exact target is missing or mismatched. Optional framework tests are skipped unless their dependencies are installed.

## Run LangGraph example

```bash
python -m pip install 'langgraph==1.2.10'
PYTHONPATH=src python examples/langgraph_agent.py
```

`InMemorySaver` is used only for the lab and does not survive a process restart.

## Run OpenAI Agents SDK example

```bash
python -m pip install 'openai-agents==0.19.0'
export OPENAI_API_KEY='...'
export OPENAI_MODEL='gpt-5.4-mini'  # replace only with a model you have verified and can access
PYTHONPATH=src python examples/openai_agents_sdk_agent.py
```

The SDK example produces a recommendation only. It deliberately does not let the model authorize or execute a critical write. External execution was not performed in the isolated authoring environment because the optional SDK and provider credentials were unavailable.
