"""Location-basis risk utilities for a WTI producer hedge.

Basis is defined as:

    Midland price - Cushing price

A negative number means Midland trades below Cushing.

The functions below separate:
1. flat-price exposure hedged with NYMEX WTI futures; and
2. location-basis exposure hedged with a basis swap.

This is an educational model. The default examples use illustrative basis
scenarios rather than claiming a historical Midland cash-price series.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from src.hedge_engine import HedgeAssumptions


@dataclass(frozen=True)
class BasisHedgeAssumptions:
    """Assumptions for a Midland-vs-Cushing basis hedge."""

    locked_basis_per_bbl: float = -1.00
    flat_price_hedge_ratio: float = 1.00
    basis_hedge_ratio: float = 0.00


def simulate_basis_scenario(
    cushing_futures_entry: float,
    cushing_futures_exit: float,
    cushing_spot_exit: float,
    realized_midland_basis: float,
    assumptions: HedgeAssumptions = HedgeAssumptions(),
    basis_assumptions: BasisHedgeAssumptions = BasisHedgeAssumptions(),
) -> dict:
    """Simulate physical Midland revenue plus WTI futures and a basis swap.

    The producer sells physical crude at:

        Midland price = Cushing spot + Midland/Cushing basis

    The flat-price hedge is a short WTI futures position.

    The basis swap is modeled from the producer's perspective:

        basis swap P&L =
        (locked basis - realized basis) * basis-hedged barrels

    If the Midland discount widens from -$1/bbl to -$5/bbl, a fully hedged
    basis swap pays +$4/bbl and offsets the physical basis deterioration.
    """
    if not 0 <= basis_assumptions.flat_price_hedge_ratio <= 1:
        raise ValueError("flat_price_hedge_ratio must be between 0 and 1.")
    if not 0 <= basis_assumptions.basis_hedge_ratio <= 1:
        raise ValueError("basis_hedge_ratio must be between 0 and 1.")

    production = assumptions.monthly_production_bbl
    contract_size = assumptions.contract_size_bbl

    flat_contracts = int(
        round(
            production
            * basis_assumptions.flat_price_hedge_ratio
            / contract_size
        )
    )
    flat_hedged_bbl = flat_contracts * contract_size

    basis_hedged_bbl = (
        production * basis_assumptions.basis_hedge_ratio
    )

    midland_spot_exit = cushing_spot_exit + realized_midland_basis

    physical_revenue = midland_spot_exit * production

    flat_futures_pnl = (
        cushing_futures_entry - cushing_futures_exit
    ) * flat_hedged_bbl

    basis_swap_pnl = (
        basis_assumptions.locked_basis_per_bbl
        - realized_midland_basis
    ) * basis_hedged_bbl

    total_revenue = (
        physical_revenue + flat_futures_pnl + basis_swap_pnl
    )

    benchmark_locked_revenue = (
        cushing_futures_entry
        + basis_assumptions.locked_basis_per_bbl
    ) * production

    residual_revenue_risk = (
        total_revenue - benchmark_locked_revenue
    )

    return {
        "production_bbl": production,
        "flat_price_hedge_ratio": (
            basis_assumptions.flat_price_hedge_ratio
        ),
        "basis_hedge_ratio": basis_assumptions.basis_hedge_ratio,
        "locked_basis_per_bbl": basis_assumptions.locked_basis_per_bbl,
        "realized_midland_basis": realized_midland_basis,
        "cushing_futures_entry": cushing_futures_entry,
        "cushing_futures_exit": cushing_futures_exit,
        "cushing_spot_exit": cushing_spot_exit,
        "midland_spot_exit": midland_spot_exit,
        "physical_revenue": physical_revenue,
        "flat_futures_pnl": flat_futures_pnl,
        "basis_swap_pnl": basis_swap_pnl,
        "total_revenue": total_revenue,
        "benchmark_locked_revenue": benchmark_locked_revenue,
        "residual_revenue_risk": residual_revenue_risk,
    }


def compare_basis_scenarios(
    realized_basis_values: Iterable[float] = (
        1.0, 0.0, -1.0, -3.0, -5.0, -10.0
    ),
    basis_hedge_ratios: Iterable[float] = (0.0, 0.50, 1.00),
    cushing_futures_entry: float = 75.0,
    cushing_futures_exit: float = 60.0,
    cushing_spot_exit: float = 60.0,
    locked_basis_per_bbl: float = -1.0,
    flat_price_hedge_ratio: float = 1.0,
    assumptions: HedgeAssumptions = HedgeAssumptions(),
) -> pd.DataFrame:
    """Create a scenario table showing residual location-basis risk."""
    rows = []

    for basis_hedge_ratio in basis_hedge_ratios:
        for realized_basis in realized_basis_values:
            result = simulate_basis_scenario(
                cushing_futures_entry=cushing_futures_entry,
                cushing_futures_exit=cushing_futures_exit,
                cushing_spot_exit=cushing_spot_exit,
                realized_midland_basis=realized_basis,
                assumptions=assumptions,
                basis_assumptions=BasisHedgeAssumptions(
                    locked_basis_per_bbl=locked_basis_per_bbl,
                    flat_price_hedge_ratio=flat_price_hedge_ratio,
                    basis_hedge_ratio=basis_hedge_ratio,
                ),
            )
            rows.append(result)

    return pd.DataFrame(rows)
