import pandas as pd

from src.hedge_engine import (
    HedgeAssumptions,
    prepare_monthly_market_data,
    simulate_hedge,
    stress_test,
)


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


def test_spot_and_futures_are_taken_on_the_same_day():
    # Futures stop on 10 July while spot runs to 31 July: July must pair both
    # prices from 10 July (the last common date), not 31 July spot with
    # 10 July futures.
    days = pd.bdate_range("2026-06-01", "2026-07-31")
    spot = pd.Series(range(len(days)), index=days, dtype=float) + 70.0
    fut = spot[spot.index <= "2026-07-10"] + 1.0
    out = prepare_monthly_market_data(spot, fut, max_stale_days=31)
    july = out.loc["2026-07-31"]
    assert pd.Timestamp(july.price_date) == pd.Timestamp("2026-07-10")
    assert abs((july.futures_exit - july.spot_exit) - 1.0) < 1e-9


def test_an_incomplete_final_month_is_dropped():
    days = pd.bdate_range("2026-05-01", "2026-07-31")
    spot = pd.Series(70.0, index=days)
    fut = spot[spot.index <= "2026-07-10"] + 1.0
    out = prepare_monthly_market_data(spot, fut)
    assert pd.Timestamp("2026-07-31") not in out.index
    assert pd.Timestamp("2026-06-30") in out.index
