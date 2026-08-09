import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def test_1049_all_new_schemas_have_no_authority_effect():
    for p in (ROOT/'schemas').glob('DATA-*.schema.json'):
        assert json.loads(p.read_text())['properties']['authority_effect']['const']=='none'

def test_1050_no_tool007_introduced():
    text='\n'.join(p.read_text() for p in (ROOT/'docs').rglob('*.md'))
    assert 'TOOL-007 is not introduced' in text

def test_1051_production_route_is_false():
    assert json.loads((ROOT/'config/readiness/production-readiness-gates.json').read_text())['production_route_enabled'] is False

def test_1052_stage8d_and_stage9d_stay_unresolved():
    c=json.loads((ROOT/'config/readiness/production-readiness-gates.json').read_text()); assert not c['stage8d_resolved'] and not c['stage9d_resolved']
