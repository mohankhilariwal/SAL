from .helpers import make_engine

def test_706_all_stride_categories_covered():
    counts=make_engine().report()['stride_counts']; assert set(counts)=={'Spoofing','Tampering','Repudiation','Information Disclosure','Denial of Service','Elevation of Privilege'}
def test_707_all_owasp_categories_covered(): assert set(make_engine().report()['owasp_counts'])=={f'ASI{i:02d}' for i in range(1,11)}
def test_708_boundary_exposure_nonempty(): assert make_engine().report()['boundary_exposure']
def test_709_evaluations_16():
    e=make_engine().evaluate(); assert len(e['passed'])==16 and e['failed']==[]
def test_710_report_digest_present(): assert len(make_engine().evaluate()['report_digest'])==64

def test_711_invariants_preserved():
    inv=set(make_engine().report()['invariants']); assert {'CMP-005_only_tool_gateway','CMP-007_only_authority_issuer','humans_own_approval_and_finalization'}<=inv
