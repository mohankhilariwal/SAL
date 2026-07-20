FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && python -m spacy download en_core_web_sm
COPY config ./config
COPY prompts ./prompts
COPY schemas ./schemas
COPY src ./src
ENV PYTHONPATH=/app/src SPINCHECK_ENV=prod
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/healthz')"
CMD ["uvicorn","spincheck.api:app","--host","0.0.0.0","--port","8000","--workers","2"]
