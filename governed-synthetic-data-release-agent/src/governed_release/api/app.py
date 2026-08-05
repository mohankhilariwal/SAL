from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from governed_release.application.workflow import build_service
from governed_release.domain.enums import ApprovalOutcome, ApprovalRole, Scenario

app = FastAPI(
    title="Governed Autonomous Synthetic Data Release Agent",
    version="0.1.0",
    description="Local control-plane governed synthetic-data release reference implementation.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8501", "http://localhost:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["content-type"],
)
service = build_service()
MAX_REQUEST_BYTES = 128 * 1024


class ApprovalBody(BaseModel):
    role: ApprovalRole
    approver_id: str = Field(min_length=3, max_length=80)
    comment: str = Field(min_length=3, max_length=1000)
    outcome: ApprovalOutcome = ApprovalOutcome.APPROVE


class KillSwitchBody(BaseModel):
    enabled: bool
    reason: str = Field(min_length=3, max_length=500)
    updated_by: str = Field(default="local_operator", min_length=3, max_length=80)


@app.middleware("http")
async def request_size_limit(request: Request, call_next: Any) -> Any:
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_BYTES:
        raise HTTPException(status_code=413, detail="Request body too large")
    return await call_next(request)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, Any]:
    return {
        "status": "ready",
        "generator": service.settings.generator,
        "policy_engine": service.settings.policy_engine,
        "model_gateway": service.settings.model_gateway,
        "database": "sqlite" if service.settings.database_url.startswith("sqlite") else "external",
    }


@app.get("/scenarios")
def scenarios() -> list[dict[str, str]]:
    return [
        {"id": Scenario.INTERNAL_ALLOW.value, "name": "Internal sandbox release allowed"},
        {"id": Scenario.EXTERNAL_APPROVAL.value, "name": "External release requires approval"},
        {"id": Scenario.PRIVACY_LEAKAGE.value, "name": "Privacy leakage detected"},
        {
            "id": Scenario.PROMPT_INJECTION.value,
            "name": "Prompt injection and exfiltration attempt",
        },
    ]


@app.post("/workflows/run/{scenario}")
def run_workflow(scenario: Scenario) -> dict[str, Any]:
    try:
        return service.run_scenario(scenario).model_dump(mode="json")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/workflows")
def list_workflows() -> list[dict[str, Any]]:
    return [state.model_dump(mode="json") for state in service.store.list()]


@app.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: str) -> dict[str, Any]:
    try:
        return service.store.get(workflow_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/workflows/{workflow_id}/approve")
def approve(workflow_id: str, body: ApprovalBody) -> dict[str, Any]:
    try:
        return service.approve(
            workflow_id,
            body.role,
            body.approver_id,
            body.comment,
            body.outcome,
        ).model_dump(mode="json")
    except (KeyError, ValueError, PermissionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/workflows/{workflow_id}/resume")
def resume(workflow_id: str) -> dict[str, Any]:
    try:
        return service.resume(workflow_id).model_dump(mode="json")
    except (KeyError, ValueError, PermissionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/operator/kill-switch/{name}")
def set_kill_switch(name: str, body: KillSwitchBody) -> dict[str, Any]:
    try:
        service.set_kill_switch(name, body.enabled, body.reason, body.updated_by)
        return {"name": name, "enabled": body.enabled, "status": "recorded"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
