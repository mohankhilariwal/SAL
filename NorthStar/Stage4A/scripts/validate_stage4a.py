from pathlib import Path
import json
from northstar_compliance.graph.definition import load_graph

ROOT = Path(__file__).resolve().parents[1]
required = [
    "docs/source-of-truth/00-Project-Constitution.md",
    "docs/source-of-truth/01-Business-and-User-Story-Baseline.md",
    "docs/source-of-truth/02-Requirements-Register.md",
    "docs/source-of-truth/03-Architecture-Baseline.md",
    "docs/source-of-truth/04-Component-and-Agent-Catalogue.md",
    "docs/source-of-truth/05-Data-and-Schema-Register.md",
    "docs/source-of-truth/06-ADR-Register.md",
    "docs/source-of-truth/07-Repository-Manifest.md",
    "docs/source-of-truth/08-Risk-Assumption-and-Issue-Register.md",
    "docs/source-of-truth/09-Stage-Handoff-Pack.md",
    "docs/stages/Stage-4A-Graph-Foundations-and-Typed-State.md",
]
missing = [p for p in required if not (ROOT/p).exists()]
if missing: raise SystemExit("missing:" + ",".join(missing))
graph = load_graph(ROOT / "config/graph/stage4a-regulatory-impact-graph.json")
assert graph.graph_id == "GRAPH-001" and len(graph.nodes) == 9
for schema in (ROOT / "schemas").glob("DATA-05*.schema.json"):
    json.loads(schema.read_text())
chapter = (ROOT / required[-1]).read_text()
for heading in range(1, 28):
    assert f"## {heading}." in chapter, heading
assert "Stage 4B" in chapter and "multi-agent" in chapter
print("Stage 4A structural validation PASSED")
