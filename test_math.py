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


from src.min_variance import (
    contracts_for_hedge_ratio,
    hedge_ratio_diagnostics,
    minimum_variance_hedge_ratio,
)

# Synthetic data where spot and futures changes move one-for-one.
mv_market = pd.DataFrame(
    {
        "spot_exit": [70.0, 72.0, 69.0, 74.0],
        "futures_entry": [69.0, 70.0, 72.0, 69.0],
        "futures_exit": [70.0, 72.0, 69.0, 74.0],
    },
    index=pd.to_datetime(
        ["2026-01-31", "2026-02-28", "2026-03-31", "2026-04-30"]
    ),
)

mv_ratio = minimum_variance_hedge_ratio(mv_market)
assert round(mv_ratio, 6) == 1.0
assert contracts_for_hedge_ratio(100_000, mv_ratio) == 100

mv_diag = hedge_ratio_diagnostics(mv_market, mv_ratio)
assert round(mv_diag["variance_reduction"], 6) == 1.0

print("Minimum-variance hedge math checks passed.")


# Futures-curve calculations
from src.term_structure import (
    add_curve_metrics,
    select_example_curves,
    summarize_curve_regimes,
)

# Small made-up dataset used only to test the math.
curve = pd.DataFrame(
    {
        "contract_1": [80.0, 70.0, 75.0],
        "contract_2": [79.0, 71.0, 75.1],
        "contract_3": [78.0, 72.0, 75.1],
        "contract_4": [77.0, 73.0, 75.2],
    },
    index=pd.to_datetime(
        [
            "2024-01-31",
            "2024-02-29",
            "2024-03-31",
        ]
    ),
)

result = add_curve_metrics(
    curve,
    flat_threshold=0.25,
)

# January: C1 ($80) > C4 ($77) -> +$3 -> backwardation.
assert (
    result.loc["2024-01-31", "c1_c4_spread"]
    == 3.0
)
assert (
    result.loc["2024-01-31", "curve_regime"]
    == "backwardation"
)

# February: C1 ($70) < C4 ($73) -> -$3 -> contango.
assert (
    result.loc["2024-02-29", "c1_c4_spread"]
    == -3.0
)
assert (
    result.loc["2024-02-29", "curve_regime"]
    == "contango"
)

# March is within the +/- $0.25 flat threshold.
assert round(
    result.loc["2024-03-31", "c1_c4_spread"],
    2,
) == -0.20
assert (
    result.loc["2024-03-31", "curve_regime"]
    == "flat"
)

summary = summarize_curve_regimes(result)
assert summary["months"].sum() == 3

examples = select_example_curves(result)
assert len(examples) == 2

print("Futures-curve math checks passed.")

