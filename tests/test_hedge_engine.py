import pandas as pd

from src.hedge_engine import HedgeAssumptions, simulate_hedge, stress_test


def test_simulate_hedge_contracts_and_pnl():
    idx = pd.to_datetime(["2026-01-31", "2026-02-28"])
    market = pd.DataFrame(
        {
            "spot_exit": [70.0, 60.0],
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


def test_stress_test_contract_count():
    result = stress_test(75, 76, -0.25, 0.75)
    assert result["contracts_short"] == 75
