SHELL := /bin/bash
PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup setup-core verify seed test test-fast test-integration lint format typecheck api ui demo scenarios reset evidence-check clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip setuptools
	$(BIN)/pip install -e ".[dev,full]"
	$(BIN)/python scripts/bootstrap.py
	$(BIN)/python scripts/seed_demo.py
	$(BIN)/pip freeze > requirements.lock

setup-core:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip setuptools
	$(BIN)/pip install -e ".[dev]"
	$(BIN)/python scripts/bootstrap.py
	$(BIN)/python scripts/seed_demo.py
	$(BIN)/pip freeze > requirements.lock

verify:
	$(BIN)/python scripts/verify_environment.py

seed:
	$(BIN)/python scripts/seed_demo.py

test:
	$(BIN)/pytest

test-fast:
	GOVERNED_RELEASE_GENERATOR=fallback $(BIN)/pytest -m "not integration"

test-integration:
	$(BIN)/pytest -m integration

lint:
	$(BIN)/ruff check src tests scripts

format:
	$(BIN)/ruff format src tests scripts

typecheck:
	$(BIN)/mypy src/governed_release

api:
	$(BIN)/uvicorn governed_release.api.app:app --host 127.0.0.1 --port 8000

ui:
	$(BIN)/streamlit run src/governed_release/ui/app.py --server.address 127.0.0.1 --server.port 8501

demo:
	$(BIN)/python scripts/run_demo.py

scenarios:
	$(BIN)/python scripts/run_scenarios.py

reset:
	$(BIN)/python scripts/reset_demo.py

evidence-check:
	$(BIN)/python scripts/verify_evidence.py

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
