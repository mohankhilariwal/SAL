from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]

def test_exactly_one_active_agent():
    data=json.loads((ROOT/"config/identity/authorization_policy.json").read_text()); assert data["active_agent_ids"]==["AGT-001"]

def test_tool_tiers_complete():
    data=json.loads((ROOT/"config/identity/tool_authority_tiers.json").read_text()); assert set(data)=={f"TOOL-{i:03d}" for i in range(1,7)}

def test_stage8d_stays_open():
    text=(ROOT/"docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text(); assert "Stage 8D remains unresolved" in text

def test_no_production_route_claim():
    text=(ROOT/"README.md").read_text().lower(); assert "does not activate a production" in text

def test_no_data106_writer():
    source="\n".join(p.read_text() for p in (ROOT/"src").rglob("*.py"))
    forbidden=("mutate_data_106", "write_data_106", "set_data_106", "update_data_106")
    assert not any(token in source.lower() for token in forbidden)

def test_all_schemas_load():
    for p in (ROOT/"schemas").glob("*.schema.json"): json.loads(p.read_text())

def test_mermaid_files_present(): assert len(list((ROOT/"docs/architecture/diagrams").glob("*.mmd")))>=5

def test_adr_range_present():
    text=(ROOT/"docs/source-of-truth/06-ADR-Register.md").read_text()
    for n in range(95,104): assert f"ADR-{n:03d}" in text
