from __future__ import annotations
from pathlib import Path
import pytest
from northstar_compliance.guardrails.engine import GuardrailEngine
from northstar_compliance.guardrails.models import GuardrailRequest, GuardrailStage
from northstar_compliance.guardrails.policy import PolicyBundle

ROOT=Path(__file__).resolve().parents[1]

@pytest.fixture(scope='session')
def bundle():
    return PolicyBundle.load(ROOT/'config/guardrails/guardrail_policy_bundle.json')

@pytest.fixture
def engine(bundle):
    return GuardrailEngine(bundle)


def make_request(stage: GuardrailStage, payload=None, metadata=None, suffix='TEST'):
    return GuardrailRequest(
        request_id=f'REQ-{suffix}', stage=stage, tenant_id='TENANT-CA-001', case_id='CASE-2026-0001',
        run_id='RUN-001', task_id=f'TASK-{suffix}', payload=payload or {}, metadata=metadata or {},
    )
