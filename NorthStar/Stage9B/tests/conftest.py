from __future__ import annotations
import pytest
from datetime import datetime, timezone
from northstar_compliance.security.identity import *
from northstar_compliance.security.identity.canonical import sha256_hex

@pytest.fixture
def env():
    now=datetime(2026,8,1,21,0,tzinfo=timezone.utc)
    issuer_key=Ed25519KeyPair("issuer")
    workload_key=Ed25519KeyPair("workload")
    execution=AgentExecutionIdentity("EXEC-1","AGT-001","1.1.0","USR-MAYA","spiffe://northstar.ca/workload/agt-001","TENANT-NORTHSTAR","CASE-1","RUN-1","TASK-1",now)
    approval=ApprovalBinding(None,ApprovalStatus.NOT_REQUIRED)
    grant,envelope=GrantIssuer(issuer_key).issue(execution,human_actor_id="USR-MAYA",workload_principal_id=execution.workload_principal_id,purpose="draft",
        audience="CMP-005",intended_tool="TOOL-004",operations=("create_draft_impact_assessment",),resource_prefixes=("case://CASE-1/drafts/",),data_scopes=("case_internal",),region_allowlist=("CA",),max_authority_tier=2,max_uses=2,max_tool_calls=2,max_records=2,max_bytes=10000,max_external_messages=0,monetary_limit_cad=1.0,reversible_only=True,approval=approval,proof_key_thumbprint=workload_key.thumbprint,ttl_seconds=120,now=now)
    context=ToolInvocationContext("TENANT-NORTHSTAR","CASE-1","RUN-1","TASK-1","EXEC-1","USR-MAYA",execution.workload_principal_id,"TOOL-004","CMP-005","create_draft_impact_assessment","case://CASE-1/drafts/v1","case_internal","CA",AuthorityTier.REVERSIBLE_INTERNAL,1,100,0,0.01,"POST",sha256_hex({"x":1}))
    budget=BlastRadiusBudget("BUDGET-1","TENANT-NORTHSTAR","CASE-1","RUN-1",AuthorityTier.CONTROLLED_EXTERNAL,("TOOL-001","TOOL-002","TOOL-003","TOOL-004","TOOL-005","TOOL-006"),{"TOOL-001":5,"TOOL-002":5,"TOOL-003":5,"TOOL-004":2,"TOOL-005":1,"TOOL-006":1},15,100,100000,1,2.0,1,("CA",),("case_internal","internal","public"),(),True,False)
    gateway=ToolAuthorizationGateway(issuer_key.public_key,{workload_key.thumbprint:workload_key.public_key})
    return locals()
