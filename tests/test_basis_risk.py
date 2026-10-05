from src.basis_risk import BasisHedgeAssumptions, simulate_basis_scenario
from src.hedge_engine import HedgeAssumptions


def test_basis_hedge_offsets_location_deterioration():
    unhedged = simulate_basis_scenario(
        cushing_futures_entry=75,
        cushing_futures_exit=60,
        cushing_spot_exit=60,
        realized_midland_basis=-5,
        assumptions=HedgeAssumptions(monthly_production_bbl=100_000),
        basis_assumptions=BasisHedgeAssumptions(
            locked_basis_per_bbl=-1,
            flat_price_hedge_ratio=1.0,
            basis_hedge_ratio=0.0,
        ),
    )
    fully_hedged = simulate_basis_scenario(
        cushing_futures_entry=75,
        cushing_futures_exit=60,
        cushing_spot_exit=60,
        realized_midland_basis=-5,
        assumptions=HedgeAssumptions(monthly_production_bbl=100_000),
        basis_assumptions=BasisHedgeAssumptions(
            locked_basis_per_bbl=-1,
            flat_price_hedge_ratio=1.0,
            basis_hedge_ratio=1.0,
        ),
    )

    assert unhedged["residual_revenue_risk"] == -400_000
    assert fully_hedged["residual_revenue_risk"] == 0
