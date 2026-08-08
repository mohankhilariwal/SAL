from pathlib import Path
import copy, pytest
from northstar_compliance.graph.definition import load_graph
from northstar_compliance.graph.factory import build_state
from northstar_compliance.graph.models import GraphStatePatch
from northstar_compliance.graph.state import PatchOwnershipError, apply_patch

ROOT=Path(__file__).resolve().parents[2]

def test_115_unauthorized_patch_rejected():
    graph=load_graph(ROOT/'config/graph/stage4a-regulatory-impact-graph.json')
    node={n.node_id:n for n in graph.nodes}['N20_MODEL_DECIDE']
    with pytest.raises(PatchOwnershipError): apply_patch(build_state(),node,GraphStatePatch({'run_state.principal':{'principal_id':'ATTACKER'}}))

def test_116_patch_is_copy_on_write():
    graph=load_graph(ROOT/'config/graph/stage4a-regulatory-impact-graph.json')
    node={n.node_id:n for n in graph.nodes}['N20_MODEL_DECIDE']
    original=build_state(); changed=apply_patch(original,node,GraphStatePatch({'pending_decision':{'kind':'complete'}}))
    assert original.pending_decision is None and changed.pending_decision['kind']=='complete'

def test_117_model_cannot_change_final_disposition():
    graph=load_graph(ROOT/'config/graph/stage4a-regulatory-impact-graph.json')
    node={n.node_id:n for n in graph.nodes}['N20_MODEL_DECIDE']
    with pytest.raises(PatchOwnershipError): apply_patch(build_state(),node,GraphStatePatch({'run_state.final_disposition':'approved'}))
