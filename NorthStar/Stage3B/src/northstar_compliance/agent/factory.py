from __future__ import annotations

from pathlib import Path

from northstar_compliance.tools.factory import build_tool_gateway
from northstar_compliance.tools.models import ToolPrincipalContext

from .decision import DecisionProvider, RuleBasedDecisionProvider
from .models import AgentGoal
from .runtime import BoundedSingleAgentRuntime


def default_goal() -> AgentGoal:
    return AgentGoal(
        goal_id="GOAL-REG-2026-071",
        publication_id="REG-CA-2026-071",
        title="Supervisory expectations for automated credit and customer-data controls",
        objective="Prepare an evidence-backed unapproved impact-assessment package and queue human review.",
        jurisdictions=("CA",),
        business_domains=("Lending", "Customer Data", "Payments"),
        evidence_query="automated credit decision evidence retention customer-data sharing payment screening",
    )


def default_principal() -> ToolPrincipalContext:
    return ToolPrincipalContext(
        principal_id="PER-001-MAYA-CHEN",
        groups=("RegulatoryCompliance",),
        purpose="regulatory-impact-assessment",
        residency="CA",
        clearance="internal",
        write_scopes=("TOOL-004", "TOOL-005", "TOOL-006"),
        correlation_id="CORR-STAGE3B-DEMO",
    )


def build_agent_runtime(project_root: Path, artifact_root: Path, decision_provider: DecisionProvider | None = None) -> BoundedSingleAgentRuntime:
    gateway = build_tool_gateway(project_root, artifact_root)
    return BoundedSingleAgentRuntime(gateway, decision_provider or RuleBasedDecisionProvider(), artifact_root)
