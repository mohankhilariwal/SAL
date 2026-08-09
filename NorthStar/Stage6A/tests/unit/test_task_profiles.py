from dataclasses import replace
from pathlib import Path
import pytest
from northstar_compliance.architecture_decision import AgentBoundaryPolicy,bind_task_profile,load_task_profiles,validate_task_profiles
ROOT=Path(__file__).resolve().parents[2];P=AgentBoundaryPolicy.from_path(ROOT/'config/architecture/agent-boundary-policy.json');PS=load_task_profiles(ROOT/'config/agents/AGT-001-task-profiles.json',P)
def test_256_six_profiles_exist():assert len(PS)==6
def test_257_all_profiles_bind_only_agt001():assert {x.agent_id for x in PS}=={'AGT-001'}
def test_258_node_keys_unique():assert len({x.node_key for x in PS})==6
def test_259_tools_subset_existing():assert set().union(*(set(x.exposed_tools) for x in PS))<=set(P.allowed_tool_ids)
def test_260_no_future_capability():assert all(not any((x.can_delegate,x.can_handoff,x.can_approve,x.can_finalize,x.can_write_memory,x.concurrent_execution)) for x in PS)
def test_261_no_direct_memory_write():assert all(not x.can_write_memory for x in PS)
def test_262_profile_digest_deterministic():assert [x.profile_sha256 for x in PS]==[x.profile_sha256 for x in load_task_profiles(ROOT/'config/agents/AGT-001-task-profiles.json',P)]
def test_263_changed_profile_not_same_digest():
 from northstar_compliance.architecture_decision.canonical import sha256_hex
 changed=replace(PS[0],purpose='Changed',profile_sha256='')
 assert sha256_hex(changed)!=PS[0].profile_sha256
def test_264_unknown_agent_rejected():
 with pytest.raises(ValueError):validate_task_profiles((replace(PS[0],agent_id='AGT-002'),)+PS[1:],P)
def test_265_unknown_tool_rejected():
 with pytest.raises(ValueError):validate_task_profiles((replace(PS[0],exposed_tools=('TOOL-999',)),)+PS[1:],P)
def test_266_delegation_rejected():
 with pytest.raises(ValueError):validate_task_profiles((replace(PS[0],can_delegate=True),)+PS[1:],P)
def test_267_binding_preserves_owners():
 b=bind_task_profile(run_id='RUN-1',profile=PS[0]);assert (b.agent_id,b.graph_id,b.graph_version)==('AGT-001','GRAPH-001','1.1.0') and b.authority_owner=='CMP-005/CMP-007/CMP-006'
def test_268_binding_rejects_spec_drift():
 with pytest.raises(ValueError):bind_task_profile(run_id='RUN-1',profile=PS[0],agent_spec_version='2.0.0')
def test_269_binding_rejects_path_run_id():
 with pytest.raises(ValueError):bind_task_profile(run_id='../escape',profile=PS[0])
