FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config
COPY scripts ./scripts
RUN pip install --no-cache-dir .
ENV PYTHONPATH=/app/src
CMD ["python", "scripts/run_stage10b_demo.py"]
