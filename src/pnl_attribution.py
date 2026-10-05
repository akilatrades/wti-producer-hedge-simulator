"""P&L attribution helpers for the producer hedge model."""

from __future__ import annotations

import pandas as pd


def attribute_flat_price(simulation: pd.DataFrame) -> pd.DataFrame:
    """Decompose revenue surprise into physical and futures contributions."""
    required = {
        "physical_revenue",
        "benchmark_locked_revenue",
        "futures_pnl",
        "revenue_surprise",
    }
    missing = required.difference(simulation.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = pd.DataFrame(index=simulation.index)
    out["physical_flat_price_effect"] = (
        simulation["physical_revenue"]
        - simulation["benchmark_locked_revenue"]
    )
    out["futures_hedge_effect"] = simulation["futures_pnl"]
    out["residual_flat_price_effect"] = (
        out["physical_flat_price_effect"]
        + out["futures_hedge_effect"]
    )
    out["reported_revenue_surprise"] = simulation["revenue_surprise"]
    out["attribution_check"] = (
        out["residual_flat_price_effect"]
        - out["reported_revenue_surprise"]
    )
    return out


def summarize_attribution(attribution: pd.DataFrame) -> dict:
    """Summarize average and volatility of the main attribution components."""
    required = {
        "physical_flat_price_effect",
        "futures_hedge_effect",
        "residual_flat_price_effect",
    }
    missing = required.difference(attribution.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return {
        "avg_physical_flat_price_effect": float(
            attribution["physical_flat_price_effect"].mean()
        ),
        "avg_futures_hedge_effect": float(
            attribution["futures_hedge_effect"].mean()
        ),
        "avg_residual_flat_price_effect": float(
            attribution["residual_flat_price_effect"].mean()
        ),
        "residual_std": float(
            attribution["residual_flat_price_effect"].std(ddof=1)
        ),
        "max_abs_attribution_check": float(
            attribution.get(
                "attribution_check",
                pd.Series(0.0, index=attribution.index),
            ).abs().max()
        ),
    }


def basis_attribution(result: dict) -> dict:
    """Decompose one basis scenario into physical basis and hedge effects."""
    required = {
        "production_bbl",
        "locked_basis_per_bbl",
        "realized_midland_basis",
        "basis_swap_pnl",
    }
    missing = required.difference(result)
    if missing:
        raise ValueError(f"Missing required keys: {sorted(missing)}")

    physical_basis_effect = (
        result["realized_midland_basis"]
        - result["locked_basis_per_bbl"]
    ) * result["production_bbl"]

    basis_hedge_effect = float(result["basis_swap_pnl"])
    residual_basis_effect = physical_basis_effect + basis_hedge_effect

    return {
        "physical_basis_effect": float(physical_basis_effect),
        "basis_hedge_effect": basis_hedge_effect,
        "residual_basis_effect": float(residual_basis_effect),
    }
