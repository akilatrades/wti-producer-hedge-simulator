import pandas as pd

from src.hedge_engine import simulate_hedge
from src.pnl_attribution import attribute_flat_price, basis_attribution


def test_flat_price_attribution_reconciles():
    market = pd.DataFrame(
        {
            "spot_exit": [60.0],
            "futures_entry": [75.0],
            "futures_exit": [60.0],
        },
        index=pd.to_datetime(["2026-01-31"]),
    )
    sim = simulate_hedge(market, 0.75)
    attribution = attribute_flat_price(sim)

    assert abs(attribution["attribution_check"].iloc[0]) < 1e-9


def test_basis_attribution_reconciles_effects():
    result = {
        "production_bbl": 100_000,
        "locked_basis_per_bbl": -1.0,
        "realized_midland_basis": -5.0,
        "basis_swap_pnl": 200_000.0,
    }
    out = basis_attribution(result)
    assert out["physical_basis_effect"] == -400_000
    assert out["residual_basis_effect"] == -200_000
