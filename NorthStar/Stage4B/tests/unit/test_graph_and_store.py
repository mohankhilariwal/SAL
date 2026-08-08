import json, sqlite3
from pathlib import Path
import pytest
from northstar_compliance.graph.definition import GraphDefinitionError, load_graph
from northstar_compliance.durable.store import StateIntegrityError

def test_134_graph_definition_is_valid(runtime):
    assert runtime.graph.graph_id=='GRAPH-001' and runtime.graph.graph_version=='1.1.0'

def test_135_duplicate_route_fails(tmp_path):
    p=Path(__file__).resolve().parents[2]/'config/graph/stage4b-regulatory-impact-graph.json'
    raw=json.loads(p.read_text()); raw['edges'].append(raw['edges'][0]); q=tmp_path/'bad.json';q.write_text(json.dumps(raw))
    with pytest.raises(GraphDefinitionError): load_graph(q)

def test_136_tables_exist(runtime):
    with sqlite3.connect(runtime.store.db_path) as c:
        tables={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert {'workflow_runs','approval_waits','approval_decisions','tool_effects'} <= tables

def test_137_state_checksum_tamper_detected(runtime,t0):
    w=runtime.start(now=t0)
    with sqlite3.connect(runtime.store.db_path) as c:
        c.execute("update workflow_runs set state_json='{}' where run_id=?",(w.run_id,));c.commit()
    with pytest.raises(StateIntegrityError): runtime.store.load_run(w.run_id)

def test_138_raw_token_not_persisted(runtime,t0):
    w=runtime.start(now=t0)
    data=Path(runtime.store.db_path).read_bytes()
    assert w.approval_token.encode() not in data
