import pytest
from northstar_compliance.evaluation.judge.metrics import (
    attack_success_rate, binary_agreement, coverage, exact_score_agreement,
    flip_rate, group_accuracy_gap, mean_absolute_error, middle_score_rate, tail_recall,
)


def test_579_binary_perfect():
    m = binary_agreement([True, False], [True, False])
    assert m.accuracy == 1 and m.kappa == 1


def test_580_binary_false_positive():
    m = binary_agreement([False, False], [True, False])
    assert m.fp == 1


def test_581_binary_false_negative():
    m = binary_agreement([True, True], [False, True])
    assert m.fn == 1


def test_582_coverage():
    assert coverage([1, None, 2, 3]) == 0.75


def test_583_exact_score_agreement():
    assert exact_score_agreement([0,4], [0,4]) == 1


def test_584_mae():
    assert mean_absolute_error([0,4], [1,3]) == 1


def test_585_flip_rate():
    assert flip_rate({"x":"pass"},{"x":"fail"}) == 1


def test_586_middle_score_rate():
    assert middle_score_rate([0,2,4]) == pytest.approx(1/3)


def test_587_tail_recall():
    assert tail_recall([0,4,2],[0,3,2]) == 0.5


def test_588_attack_success_rate():
    assert attack_success_rate([True, True], [False, True]) == 0.5


def test_589_group_gap_zero():
    assert group_accuracy_gap([True,True],[True,True],["en","fr"]) == 0


def test_590_group_gap_one():
    assert group_accuracy_gap([True,True],[True,False],["en","fr"]) == 1

@pytest.mark.parametrize("bad", [([], []), ([True],[True,False])])
def test_591_592_invalid_binary_inputs(bad):
    with pytest.raises(ValueError):
        binary_agreement(*bad)

@pytest.mark.parametrize("scores,expected", [([0,4],0.0),([2,2],1.0)])
def test_593_594_middle_rate_cases(scores, expected):
    assert middle_score_rate(scores) == expected
