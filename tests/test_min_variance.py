import pandas as pd

from src.min_variance import (
    contracts_for_hedge_ratio,
    hedge_ratio_diagnostics,
    minimum_variance_hedge_ratio,
)


def test_one_for_one_changes_produce_ratio_one():
    market = pd.DataFrame(
        {
            "spot_exit": [70.0, 72.0, 69.0, 74.0],
            "futures_entry": [69.0, 70.0, 72.0, 69.0],
            "futures_exit": [70.0, 72.0, 69.0, 74.0],
        },
        index=pd.to_datetime(["2026-01-31", "2026-02-28", "2026-03-31", "2026-04-30"]),
    )

    ratio = minimum_variance_hedge_ratio(market)
    assert round(ratio, 6) == 1.0
    assert contracts_for_hedge_ratio(100_000, ratio) == 100

    diagnostics = hedge_ratio_diagnostics(market, ratio)
    assert round(diagnostics["variance_reduction"], 6) == 1.0
