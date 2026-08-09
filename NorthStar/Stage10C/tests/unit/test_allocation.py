from decimal import Decimal
import pytest
from northstar_compliance.finops.allocation import allocate
from northstar_compliance.finops.costing import CostCalculator, RateCard
from northstar_compliance.finops.models import CostCategory, CostEvent, CostRate


def test_1041_allocation_by_business_unit():
    c=CostCalculator(RateCard([CostRate(CostCategory.TOOL,Decimal("1"),"call")]))
    e=[CostEvent("R1","Q1",CostCategory.TOOL,Decimal("2"),"call","WP","Payments","CA","test"),CostEvent("R2","Q2",CostCategory.TOOL,Decimal("1"),"call","WP","Lending","CA","test")]
    rows=allocate(e,c,"business_unit"); assert {r.value:r.amount for r in rows}=={"Lending":Decimal("1.000000"),"Payments":Decimal("2.000000")}

def test_1042_invalid_allocation_dimension_rejected():
    c=CostCalculator(RateCard([CostRate(CostCategory.TOOL,Decimal("1"),"call")]))
    with pytest.raises(ValueError): allocate([],c,"secret")
