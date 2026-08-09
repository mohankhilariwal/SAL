import pytest
from northstar_compliance.evaluation.judge_bias.metrics import *

# TEST-626..641

def test_wilson_contains_rate():
    lo,hi=wilson_interval(5,10); assert lo<.5<hi

def test_wilson_rejects_zero_total():
    with pytest.raises(ValueError): wilson_interval(0,0)

def test_bootstrap_reproducible(): assert bootstrap_mean_ci([0,1,1],seed=1)==bootstrap_mean_ci([0,1,1],seed=1)
def test_bootstrap_rejects_empty():
    with pytest.raises(ValueError): bootstrap_mean_ci([])
def test_mcnemar_no_discordance(): assert exact_mcnemar_p(0,0)==1.0
def test_mcnemar_symmetric(): assert exact_mcnemar_p(1,5)==exact_mcnemar_p(5,1)
def test_binary_pairs_no_change():
    rows=[]
    for i in range(4):
        for v in ["control","treatment"]: rows.append({"pair_id":str(i),"variant":v,"observed_label":"pass","score":5})
    m=binary_pair_metrics(rows); assert m["flip_rate"]==0 and m["paired_delta"]==0

def test_binary_pairs_detect_change():
    rows=[]
    for i in range(6):
        rows += [{"pair_id":str(i),"variant":"control","observed_label":"fail","score":1},{"pair_id":str(i),"variant":"treatment","observed_label":"pass","score":5}]
    m=binary_pair_metrics(rows); assert m["paired_delta"]==1 and m["flip_rate"]==1

def test_binary_pairs_incomplete_rejected():
    with pytest.raises(ValueError): binary_pair_metrics([{"pair_id":"1","variant":"control","observed_label":"pass","score":5}])

def test_central_middle():
    m=central_tendency_metrics([3,3,3,3],[1,5,1,5]); assert m["middle_score_rate"]==1 and m["tail_recall"]==0

def test_central_perfect():
    m=central_tendency_metrics([1,5],[1,5]); assert m["tail_recall"]==1 and m["scale_compression"]==0

def test_position_consistent():
    rows=[]
    for i in range(5):
        rows += [{"pair_id":str(i),"order":0,"observed_label":"pass"},{"pair_id":str(i),"order":1,"observed_label":"pass"}]
    assert position_metrics(rows)["position_consistency"]==1

def test_position_flip():
    rows=[]
    for i in range(5): rows += [{"pair_id":str(i),"order":0,"observed_label":"pass"},{"pair_id":str(i),"order":1,"observed_label":"fail"}]
    assert position_metrics(rows)["order_flip_rate"]==1

def test_holm_empty(): assert holm_bonferroni({})=={}
def test_holm_adjusts():
    h=holm_bonferroni({"a":.001,"b":.04}); assert h["a"]["adjusted_p"]>=.001

def test_holm_rejects_bad_p():
    with pytest.raises(ValueError): holm_bonferroni({"a":1.2})
