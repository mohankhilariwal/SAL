from decimal import Decimal
from time import perf_counter
from northstar_compliance.capacity.models import WorkloadDemandProfile
from northstar_compliance.capacity.planner import CapacityPlanner

def test_1053_capacity_calculation_is_bounded():
    p=WorkloadDemandProfile('WP',Decimal('10'),Decimal('5'),Decimal('20'),8,Decimal('0.7'),10000,1000)
    start=perf_counter()
    for _ in range(10000): CapacityPlanner().estimate(p)
    assert perf_counter()-start < 2.0
