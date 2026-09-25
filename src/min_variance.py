"""Minimum-variance hedge-ratio utilities.

The classic minimum-variance hedge ratio is:

    h* = Cov(ΔS, ΔF) / Var(ΔF)

where ΔS is the physical spot-price change and ΔF is the futures-price change.

For a producer that is long physical crude, h* is the fraction of physical
volume to hedge by shorting futures, before whole-contract rounding.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def price_changes(market: pd.DataFrame) -> pd.DataFrame:
    """Return aligned monthly spot and futures price changes."""
    out = pd.DataFrame(index=market.index)
    out["spot_change"] = market["spot_exit"].diff()
    out["futures_change"] = (
        market["futures_exit"] - market["futures_entry"]
    )
    return out.dropna()


def minimum_variance_hedge_ratio(market: pd.DataFrame) -> float:
    """Estimate the static minimum-variance hedge ratio."""
    changes = price_changes(market)
    covariance = changes["spot_change"].cov(changes["futures_change"])
    futures_variance = changes["futures_change"].var(ddof=1)

    if futures_variance <= 0:
        raise ValueError("Futures variance must be positive.")

    return float(covariance / futures_variance)


def hedge_ratio_diagnostics(
    market: pd.DataFrame,
    hedge_ratio: float,
) -> dict:
    """Measure residual monthly price risk after applying a hedge ratio."""
    changes = price_changes(market)
    residual = (
        changes["spot_change"]
        - hedge_ratio * changes["futures_change"]
    )

    unhedged_variance = changes["spot_change"].var(ddof=1)
    residual_variance = residual.var(ddof=1)

    return {
        "hedge_ratio": float(hedge_ratio),
        "observations": int(len(changes)),
        "spot_futures_change_correlation": float(
            changes["spot_change"].corr(changes["futures_change"])
        ),
        "unhedged_price_change_std": float(
            changes["spot_change"].std(ddof=1)
        ),
        "residual_price_change_std": float(residual.std(ddof=1)),
        "variance_reduction": float(
            1 - residual_variance / unhedged_variance
        ),
    }


def rolling_minimum_variance_hedge_ratio(
    market: pd.DataFrame,
    window: int = 24,
) -> pd.Series:
    """Estimate a rolling minimum-variance hedge ratio."""
    if window < 3:
        raise ValueError("window must be at least 3 observations.")

    changes = price_changes(market)
    cov = changes["spot_change"].rolling(window).cov(
        changes["futures_change"]
    )
    var = changes["futures_change"].rolling(window).var(ddof=1)

    ratio = (cov / var).dropna()
    ratio.name = "min_variance_hedge_ratio"
    return ratio


def contracts_for_hedge_ratio(
    monthly_production_bbl: int,
    hedge_ratio: float,
    contract_size_bbl: int = 1_000,
) -> int:
    """Convert a continuous hedge ratio into whole futures contracts."""
    return int(
        round(monthly_production_bbl * hedge_ratio / contract_size_bbl)
    )
