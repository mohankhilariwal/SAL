from __future__ import annotations
from dataclasses import asdict
from datetime import datetime, timezone
from .crypto import Ed25519KeyPair
from .issuer import GrantIssuer
from .proof import ProofService
from .gateway import ToolAuthorizationGateway
from .models import *
from .canonical import sha256_hex


def build_demo():
    now=datetime(2026,8,1,21,0,tzinfo=timezone.utc)
    issuer_key=Ed25519KeyPair("northstar-cmp007-issuer-1")
    workload_key=Ed25519KeyPair("northstar-workload-agt001-1")
    execution=AgentExecutionIdentity(
        execution_id="EXEC-001", agent_id="AGT-001", agent_spec_version="1.1.0",
        human_subject_id="USR-MAYA-CHEN", workload_principal_id="spiffe://northstar.ca/workload/agt-001",
        tenant_id="TENANT-NORTHSTAR", case_id="CASE-2026-0001", run_id="RUN-0001", task_id="TASK-DRAFT-0001", started_at=now,
    )
    approval=ApprovalBinding(None,ApprovalStatus.NOT_REQUIRED)
    issuer=GrantIssuer(issuer_key)
    grant,envelope=issuer.issue(execution,human_actor_id=execution.human_subject_id,workload_principal_id=execution.workload_principal_id,
        purpose="create_unapproved_draft",audience="CMP-005",intended_tool="TOOL-004",
        operations=("create_draft_impact_assessment",),resource_prefixes=("case://CASE-2026-0001/drafts/",),
        data_scopes=("case_internal",),region_allowlist=("CA",),max_authority_tier=2,max_uses=1,max_tool_calls=1,
        max_records=1,max_bytes=250000,max_external_messages=0,monetary_limit_cad=0.25,reversible_only=True,
        approval=approval,proof_key_thumbprint=workload_key.thumbprint,ttl_seconds=120,now=now)
    context=ToolInvocationContext(tenant_id=execution.tenant_id,case_id=execution.case_id,run_id=execution.run_id,task_id=execution.task_id,
        execution_id=execution.execution_id,human_actor_id=execution.human_subject_id,workload_principal_id=execution.workload_principal_id,
        tool_id="TOOL-004",audience="CMP-005",operation="create_draft_impact_assessment",resource="case://CASE-2026-0001/drafts/v1",
        data_scope="case_internal",region="CA",authority_tier=AuthorityTier.REVERSIBLE_INTERNAL,record_count=1,byte_count=12000,
        estimated_cost_cad=0.01,method="POST",body_digest=sha256_hex({"draft":"example"}))
    proof=ProofService.create(grant,context,workload_key,request_nonce="request-001",now=now)
    budget=BlastRadiusBudget("BRB-001",execution.tenant_id,execution.case_id,execution.run_id,AuthorityTier.CONTROLLED_EXTERNAL,
        ("TOOL-001","TOOL-002","TOOL-003","TOOL-004","TOOL-005","TOOL-006"),
        {"TOOL-001":5,"TOOL-002":5,"TOOL-003":5,"TOOL-004":1,"TOOL-005":1,"TOOL-006":1},
        18,200,2_000_000,1,2.00,1,("CA",),("public","internal","case_internal"),(),True,False)
    gateway=ToolAuthorizationGateway(issuer_key.public_key,{workload_key.thumbprint:workload_key.public_key})
    first=gateway.authorize(grant,envelope,proof,context,budget,now=now)
    replay=gateway.authorize(grant,envelope,proof,context,budget,now=now)
    return {"grant_id":grant.grant_id,"first_decision":asdict(first),"replay_decision":asdict(replay),"consumption":asdict(gateway.blast.consumption(budget.budget_id))}
