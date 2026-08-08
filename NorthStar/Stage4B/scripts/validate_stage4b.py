from pathlib import Path
from northstar_compliance.graph.definition import load_graph
root=Path(__file__).resolve().parents[1]
g=load_graph(root/'config/graph/stage4b-regulatory-impact-graph.json')
assert g.graph_id=='GRAPH-001' and g.graph_version=='1.1.0'
for name in ['00-Project-Constitution.md','01-Business-and-User-Story-Baseline.md','02-Requirements-Register.md','03-Architecture-Baseline.md','04-Component-and-Agent-Catalogue.md','05-Data-and-Schema-Register.md','06-ADR-Register.md','07-Repository-Manifest.md','08-Risk-Assumption-and-Issue-Register.md','09-Stage-Handoff-Pack.md']:
    assert (root/'docs/source-of-truth'/name).exists(), name
print('stage4b structural validation passed')
