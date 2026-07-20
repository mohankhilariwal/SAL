"""HTTP data plane (FastAPI). Run: make run"""
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .config import ControlPlane
from .orchestrator import Orchestrator
from .telemetry import log_request

cp = ControlPlane.load()
orch = Orchestrator(cp)
app = FastAPI(title="SpinCheck POC", version="0.1.0")


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


@app.get("/healthz")
def healthz():
    return {"ok": True, "version_vector": cp.version_vector()}


@app.post("/v1/analyze")
def analyze(req: AnalyzeRequest):
    resp = orch.analyze(req.text)
    d = resp.to_dict()
    log_request(dict(d), len(req.text))
    return d
