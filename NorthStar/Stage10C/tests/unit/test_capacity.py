from decimal import Decimal
import pytest
from northstar_compliance.capacity.models import WorkloadDemandProfile
from northstar_compliance.capacity.planner import CapacityPlanner


def profile(**kw):
    return WorkloadDemandProfile("WP", Decimal(str(kw.get("rps", 0.2))), Decimal(str(kw.get("peak", 3))), Decimal(str(kw.get("service",45))), kw.get("concurrency",4), Decimal(str(kw.get("util",0.65))), 16000, 2200, Decimal(str(kw.get("protected",0.05))), Decimal("60"))

def test_1031_capacity_uses_littles_law_concurrency():
    e = CapacityPlanner().estimate(profile(), headroom_fraction=Decimal("0"))
    assert e.offered_concurrency == Decimal("27.0")

def test_1032_capacity_adds_headroom():
    a = CapacityPlanner().estimate(profile(), headroom_fraction=Decimal("0"))
    b = CapacityPlanner().estimate(profile(), headroom_fraction=Decimal("0.25"))
    assert b.required_workers >= a.required_workers

def test_1033_capacity_preserves_one_protected_write_limit(): assert CapacityPlanner().estimate(profile()).protected_write_concurrency_limit == 1

def test_1034_capacity_computes_token_rates(): assert CapacityPlanner().estimate(profile()).input_tokens_per_second == Decimal("9600.0")

def test_1035_zero_arrival_requires_zero_workers(): assert CapacityPlanner().estimate(profile(rps=0)).required_workers == 0

def test_1036_invalid_utilization_rejected():
    with pytest.raises(ValueError): profile(util=0)
