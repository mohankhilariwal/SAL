from __future__ import annotations

from pathlib import Path

import pytest

from northstar_compliance.tools.factory import build_local_gateway
from northstar_compliance.tools.models import ToolPrincipalContext


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def gateway_store(tmp_path, repo_root):
    gateway, store = build_local_gateway(repo_root / "config" / "tools", tmp_path / "store")
    return gateway, store


@pytest.fixture
def maya() -> ToolPrincipalContext:
    return ToolPrincipalContext(
        principal_id="maya.chen",
        groups=("regulatory_analysts",),
        clearance="confidential",
        purpose="regulatory_change_assessment",
        residency="CA",
        correlation_id="CORR-TEST-MAYA",
        authenticated=False,
    )


@pytest.fixture
def sofia() -> ToolPrincipalContext:
    return ToolPrincipalContext(
        principal_id="sofia.alvarez",
        groups=("ai_governance",),
        clearance="restricted",
        purpose="model_risk_review",
        residency="CA",
        correlation_id="CORR-TEST-SOFIA",
        authenticated=False,
    )
