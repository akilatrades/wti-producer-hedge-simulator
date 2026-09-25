"""WTI producer hedging utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

CL_CONTRACT_SIZE_BBL = 1_000


@dataclass(frozen=True)
class HedgeAssumptions:
    monthly_production_bbl: int = 100_000
    contract_size_bbl: int = CL_CONTRACT_SIZE_BBL


def prepare_monthly_market_data(
    spot_daily: pd.Series,
    futures_daily: pd.Series,
) -> pd.DataFrame:
    """Convert daily spot/futures observations into monthly hedge periods."""
    spot = spot_daily.dropna().sort_index().astype(float)
    fut = futures_daily.dropna().sort_index().astype(float)

    spot_monthly = spot.resample("ME").mean().rename("spot_avg")
    fut_monthly = fut.resample("ME").last().rename("futures_exit")

    df = pd.concat([spot_monthly, fut_monthly], axis=1).dropna()
    df["futures_entry"] = df["futures_exit"].shift(1)
    df = df.dropna()

    return df[["spot_avg", "futures_entry", "futures_exit"]]


def simulate_hedge(
    market: pd.DataFrame,
    hedge_ratio: float,
    assumptions: HedgeAssumptions = HedgeAssumptions(),
) -> pd.DataFrame:
    """Simulate a short WTI futures hedge against monthly production."""
    if not 0 <= hedge_ratio <= 1:
        raise ValueError("hedge_ratio must be between 0 and 1.")

    out = market.copy()
    production = assumptions.monthly_production_bbl
    contract_size = assumptions.contract_size_bbl

    contracts = int(round((production * hedge_ratio) / contract_size))
    hedged_bbl = contracts * contract_size

    out["hedge_ratio"] = hedge_ratio
    out["production_bbl"] = production
    out["contracts_short"] = contracts
    out["hedged_bbl"] = hedged_bbl

    out["physical_revenue"] = out["spot_avg"] * production
    out["futures_pnl"] = (
        out["futures_entry"] - out["futures_exit"]
    ) * hedged_bbl
    out["hedged_revenue"] = out["physical_revenue"] + out["futures_pnl"]

    return out


def summarize_strategy(sim: pd.DataFrame) -> dict:
    """Summarize revenue risk for one hedge ratio."""
    revenue = sim["hedged_revenue"]
    physical = sim["physical_revenue"]

    physical_var = physical.var(ddof=1)
    hedged_var = revenue.var(ddof=1)

    hedge_effectiveness = (
        1 - hedged_var / physical_var if physical_var > 0 else np.nan
    )

    return {
        "hedge_ratio": float(sim["hedge_ratio"].iloc[0]),
        "contracts_short": int(sim["contracts_short"].iloc[0]),
        "avg_monthly_revenue": float(revenue.mean()),
        "monthly_revenue_std": float(revenue.std(ddof=1)),
        "annualized_revenue_std": float(revenue.std(ddof=1) * np.sqrt(12)),
        "p05_monthly_revenue": float(revenue.quantile(0.05)),
        "minimum_monthly_revenue": float(revenue.min()),
        "average_futures_pnl": float(sim["futures_pnl"].mean()),
        "hedge_effectiveness": float(hedge_effectiveness),
    }


def compare_hedge_ratios(
    market: pd.DataFrame,
    hedge_ratios: Iterable[float] = (0, 0.25, 0.50, 0.75, 1.00),
    assumptions: HedgeAssumptions = HedgeAssumptions(),
) -> tuple[pd.DataFrame, dict[float, pd.DataFrame]]:
    summaries = []
    simulations = {}

    for ratio in hedge_ratios:
        sim = simulate_hedge(market, ratio, assumptions)
        simulations[ratio] = sim
        summaries.append(summarize_strategy(sim))

    return pd.DataFrame(summaries).sort_values("hedge_ratio"), simulations


def stress_test(
    spot_price: float,
    futures_entry: float,
    spot_shock_pct: float,
    hedge_ratio: float,
    assumptions: HedgeAssumptions = HedgeAssumptions(),
    basis_change_per_bbl: float = 0.0,
) -> dict:
    """Apply a one-period crude-price shock to physical + futures exposure."""
    if not 0 <= hedge_ratio <= 1:
        raise ValueError("hedge_ratio must be between 0 and 1.")

    production = assumptions.monthly_production_bbl
    contracts = int(
        round(production * hedge_ratio / assumptions.contract_size_bbl)
    )
    hedged_bbl = contracts * assumptions.contract_size_bbl

    futures_exit = futures_entry * (1 + spot_shock_pct)
    realized_spot = spot_price * (1 + spot_shock_pct) + basis_change_per_bbl

    physical_revenue = realized_spot * production
    futures_pnl = (futures_entry - futures_exit) * hedged_bbl
    hedged_revenue = physical_revenue + futures_pnl

    return {
        "spot_shock_pct": spot_shock_pct,
        "basis_change_per_bbl": basis_change_per_bbl,
        "hedge_ratio": hedge_ratio,
        "contracts_short": contracts,
        "realized_spot": realized_spot,
        "futures_exit": futures_exit,
        "physical_revenue": physical_revenue,
        "futures_pnl": futures_pnl,
        "hedged_revenue": hedged_revenue,
    }
