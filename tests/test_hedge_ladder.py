import pandas as pd

from src.hedge_ladder import build_hedge_ladder, policy_schedule


def test_policy_schedule_builds_whole_contract_ladder():
    schedule = policy_schedule(
        pd.date_range("2026-01-31", periods=3, freq="ME"),
        100_000,
        [0.80, 0.70, 0.60],
        futures_contracts=["CLG26", "CLH26", "CLJ26"],
        futures_prices=[70.0, 71.0, 72.0],
    )
    ladder = build_hedge_ladder(schedule)

    assert ladder["contracts_short"].tolist() == [80, 70, 60]
    assert ladder["hedged_bbl"].tolist() == [80_000, 70_000, 60_000]
    assert "hedge_notional" in ladder
