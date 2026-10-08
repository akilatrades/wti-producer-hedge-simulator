"""Multi-month producer hedge-book and hedge-ladder utilities."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from src.hedge_engine import CL_CONTRACT_SIZE_BBL


def build_hedge_ladder(
    schedule: pd.DataFrame,
    contract_size_bbl: int = CL_CONTRACT_SIZE_BBL,
) -> pd.DataFrame:
    """Convert a production schedule into whole-contract hedge positions."""
    required = {
        "production_month",
        "expected_production_bbl",
        "hedge_ratio",
    }
    missing = required.difference(schedule.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if contract_size_bbl <= 0:
        raise ValueError("contract_size_bbl must be positive.")

    out = schedule.copy()
    out["production_month"] = pd.to_datetime(out["production_month"])
    out["expected_production_bbl"] = pd.to_numeric(
        out["expected_production_bbl"], errors="raise"
    )
    out["hedge_ratio"] = pd.to_numeric(out["hedge_ratio"], errors="raise")

    if (out["expected_production_bbl"] < 0).any():
        raise ValueError("expected_production_bbl cannot be negative.")
    if ((out["hedge_ratio"] < 0) | (out["hedge_ratio"] > 1)).any():
        raise ValueError("hedge_ratio must be between 0 and 1.")

    raw_contracts = (
        out["expected_production_bbl"] * out["hedge_ratio"] / contract_size_bbl
    )
    out["contracts_short"] = np.rint(raw_contracts).astype(int)
    out["hedged_bbl"] = out["contracts_short"] * contract_size_bbl
    out["unhedged_bbl"] = (out["expected_production_bbl"] - out["hedged_bbl"]).clip(
        lower=0
    )
    out["overhedged_bbl"] = (out["hedged_bbl"] - out["expected_production_bbl"]).clip(
        lower=0
    )

    if "futures_price" in out.columns:
        out["futures_price"] = pd.to_numeric(out["futures_price"], errors="raise")
        out["hedge_notional"] = out["hedged_bbl"] * out["futures_price"]

    return out.sort_values("production_month").reset_index(drop=True)


def policy_schedule(
    production_months: Sequence,
    expected_production_bbl: Sequence[float] | float,
    hedge_ratios: Sequence[float],
    futures_contracts: Sequence[str] | None = None,
    futures_prices: Sequence[float] | None = None,
) -> pd.DataFrame:
    """Build a schedule DataFrame from simple policy inputs."""
    months = list(production_months)
    ratios = list(hedge_ratios)
    if len(months) != len(ratios):
        raise ValueError("production_months and hedge_ratios must align.")

    if np.isscalar(expected_production_bbl):
        production = [float(expected_production_bbl)] * len(months)
    else:
        production = list(expected_production_bbl)
        if len(production) != len(months):
            raise ValueError(
                "expected_production_bbl must align with production_months."
            )

    data = {
        "production_month": months,
        "expected_production_bbl": production,
        "hedge_ratio": ratios,
    }

    if futures_contracts is not None:
        contracts = list(futures_contracts)
        if len(contracts) != len(months):
            raise ValueError("futures_contracts must align with months.")
        data["futures_contract"] = contracts

    if futures_prices is not None:
        prices = list(futures_prices)
        if len(prices) != len(months):
            raise ValueError("futures_prices must align with months.")
        data["futures_price"] = prices

    return pd.DataFrame(data)
