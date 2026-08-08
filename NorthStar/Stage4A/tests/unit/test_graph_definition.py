from copy import deepcopy
from pathlib import Path
import json, pytest
from northstar_compliance.graph.definition import GraphDefinitionError, load_graph, validate_graph
from northstar_compliance.graph.models import EdgeDefinition, ExecutionGraphDefinition, NodeDefinition

ROOT = Path(__file__).resolve().parents[2]

def graph(): return load_graph(ROOT / "config/graph/stage4a-regulatory-impact-graph.json")

def test_110_valid_graph_definition(): assert len(graph().nodes) == 9

def test_111_duplicate_node_rejected():
    g=graph(); bad=ExecutionGraphDefinition(g.graph_id,g.graph_version,g.entry_node,g.terminal_nodes,g.nodes+(g.nodes[0],),g.edges)
    with pytest.raises(GraphDefinitionError, match="duplicate_node_id"): validate_graph(bad)

def test_112_unknown_edge_target_rejected():
    g=graph(); bad=ExecutionGraphDefinition(g.graph_id,g.graph_version,g.entry_node,g.terminal_nodes,g.nodes,g.edges+(EdgeDefinition("N00_VALIDATE_CONTEXT","x","NOPE"),))
    with pytest.raises(GraphDefinitionError, match="unknown_edge_target"): validate_graph(bad)

def test_113_unreachable_node_rejected():
    g=graph(); n=NodeDefinition("N99_ORPHAN","deterministic",(),"orphan")
    bad=ExecutionGraphDefinition(g.graph_id,g.graph_version,g.entry_node,g.terminal_nodes,g.nodes+(n,),g.edges)
    with pytest.raises(GraphDefinitionError, match="unreachable_nodes"): validate_graph(bad)

def test_114_duplicate_route_rejected():
    g=graph(); bad=ExecutionGraphDefinition(g.graph_id,g.graph_version,g.entry_node,g.terminal_nodes,g.nodes,g.edges+(g.edges[0],))
    with pytest.raises(GraphDefinitionError, match="duplicate_route"): validate_graph(bad)
