"""Downside-risk statistics for producer hedge results.

The functions in this module operate on revenue-surprise or P&L series.
Negative values are unfavorable to the producer. Historical VaR and
Expected Shortfall are reported as positive loss magnitudes.
"""

from __future__ import annotations

from math import sqrt
from typing import Mapping

import numpy as np
import pandas as pd


def _clean_series(values: pd.Series) -> pd.Series:
    out = pd.Series(values, copy=True).dropna().astype(float)
    if out.empty:
        raise ValueError("Risk series must contain at least one observation.")
    return out


def historical_var(values: pd.Series, confidence: float = 0.95) -> float:
    """Return historical Value at Risk as a positive loss magnitude."""
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1.")
    series = _clean_series(values)
    losses = -series
    return float(max(np.quantile(losses, confidence), 0.0))


def expected_shortfall(values: pd.Series, confidence: float = 0.95) -> float:
    """Return average historical loss at or beyond the VaR threshold."""
    series = _clean_series(values)
    losses = -series
    var = historical_var(series, confidence)
    tail = losses[losses >= var]
    if tail.empty:
        return 0.0
    return float(max(tail.mean(), 0.0))


def downside_deviation(values: pd.Series) -> float:
    """Return the standard deviation of unfavorable observations only."""
    series = _clean_series(values)
    downside = series[series < 0]
    if len(downside) < 2:
        return 0.0
    return float(downside.std(ddof=1))


def summarize_revenue_risk(
    values: pd.Series,
    periods_per_year: int = 12,
) -> dict:
    """Summarize distribution and tail risk for a revenue-surprise series."""
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive.")

    series = _clean_series(values)
    monthly_vol = float(series.std(ddof=1)) if len(series) > 1 else 0.0
    worst_surprise = float(series.min())
    worst_loss = float(max(-worst_surprise, 0.0))

    return {
        "observations": int(len(series)),
        "mean_revenue_surprise": float(series.mean()),
        "monthly_volatility": monthly_vol,
        "annualized_volatility": monthly_vol * sqrt(periods_per_year),
        "downside_deviation": downside_deviation(series),
        "historical_var_95": historical_var(series, 0.95),
        "historical_es_95": expected_shortfall(series, 0.95),
        "historical_var_99": historical_var(series, 0.99),
        "historical_es_99": expected_shortfall(series, 0.99),
        "worst_revenue_surprise": worst_surprise,
        "worst_loss": worst_loss,
    }


def compare_hedge_risk(
    simulations: Mapping[float, pd.DataFrame],
    revenue_column: str = "revenue_surprise",
) -> pd.DataFrame:
    """Compare risk statistics across hedge-ratio simulations."""
    rows = []
    for hedge_ratio, simulation in simulations.items():
        if revenue_column not in simulation.columns:
            raise ValueError(
                f"Simulation for hedge ratio {hedge_ratio} is missing "
                f"{revenue_column!r}."
            )
        row = summarize_revenue_risk(simulation[revenue_column])
        row["hedge_ratio"] = float(hedge_ratio)
        rows.append(row)

    columns = [
        "hedge_ratio",
        "observations",
        "mean_revenue_surprise",
        "monthly_volatility",
        "annualized_volatility",
        "downside_deviation",
        "historical_var_95",
        "historical_es_95",
        "historical_var_99",
        "historical_es_99",
        "worst_revenue_surprise",
        "worst_loss",
    ]
    return pd.DataFrame(rows)[columns].sort_values("hedge_ratio")
