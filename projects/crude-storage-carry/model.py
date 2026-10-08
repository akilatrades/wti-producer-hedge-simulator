"""Forward-starting storage economics in USD per barrel, not a trading signal."""
from dataclasses import dataclass
from math import exp,isfinite


@dataclass(frozen=True)
class CarryCosts:
    months: float = 3
    storage_per_month: float = .50
    annual_financing_rate: float = .06
    annual_insurance_rate: float = .003
    handling_round_trip: float = .20

    def __post_init__(self):
        if not all(isfinite(x) and x>=0 for x in vars(self).values()) or self.months<=0:
            raise ValueError("Finite nonnegative costs and positive duration required")


def storage_economics(near, deferred, costs=CarryCosts()):
    if not all(isfinite(x) for x in (near,deferred)) or near<=0:
        raise ValueError("Finite prices and positive acquisition cost required")
    years=costs.months/12
    financing=near*(exp(costs.annual_financing_rate*years)-1)
    insurance=near*costs.annual_insurance_rate*years
    storage=costs.months*costs.storage_per_month
    non_storage=financing+insurance+costs.handling_round_trip
    spread=deferred-near
    return dict(gross_spread=spread,storage_cost=storage,financing_cost=financing,
                insurance_cost=insurance,handling_cost=costs.handling_round_trip,
                total_carry_cost=storage+non_storage,net_carry=spread-storage-non_storage,
                breakeven_monthly_storage=(spread-non_storage)/costs.months)
