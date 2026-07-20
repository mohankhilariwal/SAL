.PHONY: install dev test lint run analyze regression calibrate eval docker
install:
	pip install -r requirements.txt && python -m spacy download en_core_web_sm || true
dev:
	pip install -r requirements-dev.txt
test:
	python -m pytest tests -q
lint:
	ruff check src tests control_plane eval
run:
	uvicorn spincheck.api:app --app-dir src --host 0.0.0.0 --port 8000 --reload
analyze:
	PYTHONPATH=src python -m spincheck.cli analyze --text "$(TEXT)"
regression:
	PYTHONPATH=src python control_plane/regression.py --dataset eval/data/eval_sample.jsonl
calibrate:
	PYTHONPATH=src python control_plane/calibration.py --log-dir logs
eval:
	PYTHONPATH=src python eval/run_poc.py --dataset eval/data/eval_sample.jsonl
docker:
	docker build -f docker/Dockerfile -t spincheck-poc:latest .
