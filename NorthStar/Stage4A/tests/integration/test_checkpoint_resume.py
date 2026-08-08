from pathlib import Path
import json, tempfile, pytest
from northstar_compliance.graph.factory import build_runtime, build_state
from northstar_compliance.state.checkpoint import CheckpointError, LocalCheckpointStore

ROOT=Path(__file__).resolve().parents[2]

def test_125_graph_checkpoint_round_trip():
    with tempfile.TemporaryDirectory() as td:
        runtime,_=build_runtime(ROOT,checkpoint_dir=Path(td)); p=runtime.run(build_state(run_id='RUN-T125'),stop_after_transitions=8)
        loaded=LocalCheckpointStore(Path(td)).load('RUN-T125',graph_id='GRAPH-001',graph_version='1.0.0')
        assert loaded.current_node==p.current_node and loaded.run_state.resumed_from_checkpoint

def test_126_resume_does_not_repeat_completed_tool_work():
    with tempfile.TemporaryDirectory() as td:
        runtime,gw=build_runtime(ROOT,checkpoint_dir=Path(td)); p=runtime.run(build_state(run_id='RUN-T126'),stop_after_transitions=12)
        completed=len(gw.calls); loaded=LocalCheckpointStore(Path(td)).load('RUN-T126',graph_id='GRAPH-001',graph_version='1.0.0')
        s=runtime.run(loaded)
        assert s.run_state.status=='completed'; assert len(gw.calls)>completed
        assert sum(1 for tool,_ in gw.calls if tool=='TOOL-001')==1

def test_127_graph_version_mismatch_rejected():
    with tempfile.TemporaryDirectory() as td:
        runtime,_=build_runtime(ROOT,checkpoint_dir=Path(td)); runtime.run(build_state(run_id='RUN-T127'),stop_after_transitions=2)
        with pytest.raises(CheckpointError,match='graph_version_mismatch'):
            LocalCheckpointStore(Path(td)).load('RUN-T127',graph_id='GRAPH-001',graph_version='2.0.0')

def test_128_checkpoint_tamper_detected():
    with tempfile.TemporaryDirectory() as td:
        runtime,_=build_runtime(ROOT,checkpoint_dir=Path(td)); runtime.run(build_state(run_id='RUN-T128'),stop_after_transitions=2)
        p=LocalCheckpointStore(Path(td)).path_for('RUN-T128'); raw=json.loads(p.read_text()); raw['state']['current_node']='N90_TERMINATE'; p.write_text(json.dumps(raw))
        with pytest.raises(CheckpointError,match='checksum'):
            LocalCheckpointStore(Path(td)).load('RUN-T128',graph_id='GRAPH-001',graph_version='1.0.0')
