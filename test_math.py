import pandas as pd

from src.hedge_engine import (
    HedgeAssumptions,
    simulate_hedge,
    stress_test,
)

idx = pd.to_datetime(["2026-01-31", "2026-02-28"])

market = pd.DataFrame(
    {
        "spot_avg": [70.0, 60.0],
        "futures_entry": [72.0, 71.0],
        "futures_exit": [71.0, 61.0],
    },
    index=idx,
)

sim = simulate_hedge(
    market,
    0.50,
    HedgeAssumptions(monthly_production_bbl=100_000),
)

assert sim["contracts_short"].iloc[0] == 50
assert sim["futures_pnl"].iloc[0] == 50_000
assert sim["futures_pnl"].iloc[1] == 500_000

stress = stress_test(75, 76, -0.25, 0.75)
assert stress["contracts_short"] == 75

print("Hedge math checks passed.")


from src.basis_risk import (
    BasisHedgeAssumptions,
    simulate_basis_scenario,
)

# Full flat-price hedge, no basis swap:
# locked basis = -1, realized basis = -5 -> $4/bbl shortfall.
basis_unhedged = simulate_basis_scenario(
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
assert basis_unhedged["residual_revenue_risk"] == -400_000

# A full basis swap should offset the modeled location-basis change.
basis_hedged = simulate_basis_scenario(
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
assert basis_hedged["residual_revenue_risk"] == 0

print("Basis-risk math checks passed.")
