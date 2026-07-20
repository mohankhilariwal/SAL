import sys; sys.path.insert(0, "src")
from spincheck.config import ControlPlane
from spincheck.validators import parse_json, validate

cp = ControlPlane.load()
TEXT = "Crime is up 40% since the new DA took office."

def _doc(span=TEXT, start=0, end=len(TEXT)):
    return {"claims":[{"span":span,"start":start,"end":end,"claim_type":"statistical",
            "explicit":True,"attribution":"author","certainty":"neutral",
            "evidence_type":"numerical_support","confidence":"high",
            "normalized":span,"verification_questions":[]}],
            "rhetoric":[],"overall":{"satire_possible":False,
            "injection_suspected":False,"extraction_confidence":"high"}}

def test_parse_json_fenced():
    assert parse_json('```json\n{"a":1}\n```') == {"a": 1}

def test_span_offset_autocorrect():
    d = _doc(start=3, end=3+len(TEXT))          # drifted offsets
    rep = validate(d, cp.schema, TEXT)
    assert rep.ok and d["claims"][0]["start"] == 0

def test_hallucinated_span_dropped():
    d = _doc(span="The moon is made of cheese.", start=0, end=27)
    rep = validate(d, cp.schema, TEXT)
    assert not rep.ok and d["claims"] == [] and rep.dropped_items
