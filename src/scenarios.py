"""Scenario analysis for production uncertainty and over-hedging risk."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from src.hedge_engine import CL_CONTRACT_SIZE_BBL


def production_volume_scenarios(
    expected_production_bbl: float,
    hedge_ratio: float,
    spot_exit: float,
    futures_entry: float,
    futures_exit: float,
    volume_shocks: Iterable[float] = (-0.20, -0.10, 0.0, 0.10, 0.20),
    contract_size_bbl: int = CL_CONTRACT_SIZE_BBL,
) -> pd.DataFrame:
    """Stress actual production around the forecast while keeping hedge fixed."""
    if expected_production_bbl < 0:
        raise ValueError("expected_production_bbl cannot be negative.")
    if not 0 <= hedge_ratio <= 1:
        raise ValueError("hedge_ratio must be between 0 and 1.")
    if contract_size_bbl <= 0:
        raise ValueError("contract_size_bbl must be positive.")

    contracts = int(
        round(expected_production_bbl * hedge_ratio / contract_size_bbl)
    )
    hedged_bbl = contracts * contract_size_bbl
    futures_pnl = (futures_entry - futures_exit) * hedged_bbl

    rows = []
    for shock in volume_shocks:
        actual = max(expected_production_bbl * (1 + float(shock)), 0.0)
        physical_revenue = spot_exit * actual
        total_revenue = physical_revenue + futures_pnl
        benchmark = futures_entry * actual

        rows.append(
            {
                "volume_shock_pct": float(shock),
                "expected_production_bbl": float(expected_production_bbl),
                "actual_production_bbl": float(actual),
                "hedge_ratio": float(hedge_ratio),
                "contracts_short": contracts,
                "hedged_bbl": hedged_bbl,
                "overhedged_bbl": float(max(hedged_bbl - actual, 0.0)),
                "underhedged_bbl": float(max(actual - hedged_bbl, 0.0)),
                "physical_revenue": float(physical_revenue),
                "futures_pnl": float(futures_pnl),
                "total_revenue": float(total_revenue),
                "benchmark_revenue": float(benchmark),
                "revenue_surprise": float(total_revenue - benchmark),
            }
        )

    return pd.DataFrame(rows)


def simulate_production_uncertainty(
    expected_production_bbl: float,
    hedge_ratio: float,
    spot_exit: float,
    futures_entry: float,
    futures_exit: float,
    production_std_pct: float = 0.10,
    n_sims: int = 10_000,
    seed: int = 42,
    contract_size_bbl: int = CL_CONTRACT_SIZE_BBL,
) -> pd.DataFrame:
    """Monte Carlo production-volume uncertainty around expected production."""
    if production_std_pct < 0:
        raise ValueError("production_std_pct cannot be negative.")
    if n_sims <= 0:
        raise ValueError("n_sims must be positive.")

    rng = np.random.default_rng(seed)
    shocks = rng.normal(0.0, production_std_pct, n_sims)
    actual = np.maximum(expected_production_bbl * (1 + shocks), 0.0)

    contracts = int(
        round(expected_production_bbl * hedge_ratio / contract_size_bbl)
    )
    hedged_bbl = contracts * contract_size_bbl
    futures_pnl = (futures_entry - futures_exit) * hedged_bbl

    physical_revenue = spot_exit * actual
    total_revenue = physical_revenue + futures_pnl
    benchmark = futures_entry * actual

    return pd.DataFrame(
        {
            "production_shock_pct": shocks,
            "actual_production_bbl": actual,
            "hedged_bbl": hedged_bbl,
            "overhedged_bbl": np.maximum(hedged_bbl - actual, 0.0),
            "underhedged_bbl": np.maximum(actual - hedged_bbl, 0.0),
            "physical_revenue": physical_revenue,
            "futures_pnl": futures_pnl,
            "total_revenue": total_revenue,
            "benchmark_revenue": benchmark,
            "revenue_surprise": total_revenue - benchmark,
        }
    )
