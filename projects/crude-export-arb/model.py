"""Cushing-to-Europe crude export economics in USD per barrel, not a trading signal.

Buy WTI at Cushing, move it by pipeline to the Gulf Coast, load it on a ship and
sell it against Brent in Northwest Europe. The arb is open when Brent covers
WTI plus every cost of getting the barrel there.
"""

from dataclasses import dataclass
from math import exp, isfinite

import pandas as pd


@dataclass(frozen=True)
class ExportCosts:
    pipeline_cushing_to_gulf: float = 1.00  # USD/bbl, uncommitted tariff
    terminal_and_loading: float = 0.50  # USD/bbl
    freight_gulf_to_europe: float = 3.00  # USD/bbl, Aframax-sized cargo
    losses_and_insurance_rate: float = 0.002  # share of cargo value
    annual_financing_rate: float = 0.06
    days_in_transit: float = 45  # pipeline, tank time and voyage

    def __post_init__(self):
        if not all(isfinite(x) and x >= 0 for x in vars(self).values()):
            raise ValueError("Finite nonnegative costs required")


def export_economics(brent, wti, costs=None):
    costs = costs or ExportCosts()
    if not all(isfinite(x) for x in (brent, wti)) or wti <= 0:
        raise ValueError("Finite prices and positive WTI required")
    financing = wti * (
        exp(costs.annual_financing_rate * costs.days_in_transit / 365) - 1
    )
    losses = wti * costs.losses_and_insurance_rate
    before_freight = (
        costs.pipeline_cushing_to_gulf + costs.terminal_and_loading + losses + financing
    )
    spread = brent - wti
    return {
        "brent_wti_spread": spread,
        "pipeline": costs.pipeline_cushing_to_gulf,
        "terminal": costs.terminal_and_loading,
        "freight": costs.freight_gulf_to_europe,
        "losses_and_insurance": losses,
        "financing": financing,
        "total_delivered_cost": before_freight + costs.freight_gulf_to_europe,
        "arb_margin": spread - before_freight - costs.freight_gulf_to_europe,
        "breakeven_freight": spread - before_freight,
    }


def monthly_prices(brent, wti, min_days=15):
    """Monthly average of each series over the days it was published.

    Months with fewer than ``min_days`` observations in either series fail
    instead of being filled.
    """
    frames = []
    for frame, column in [(brent, "brent"), (wti, "wti_cushing")]:
        series = frame.assign(date=pd.to_datetime(frame.date)).set_index("date")[column]
        if series.index.duplicated().any() or series.isna().any():
            raise ValueError("Unique, complete daily observations required")
        grouped = series.resample("MS")
        frames.append(grouped.mean().rename(column))
        frames.append(grouped.count().rename(column + "_days"))
    monthly = pd.concat(frames, axis=1)
    thin = (monthly.brent_days < min_days) | (monthly.wti_cushing_days < min_days)
    if thin.iloc[:-1].any():
        raise ValueError("A full month has too few observations; do not interpolate")
    return monthly
