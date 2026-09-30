"""WTI futures term-structure utilities.

This module studies the shape of the WTI futures curve in beginner-friendly
steps. Contract 1 is the nearest delivery contract in the EIA history,
followed by Contracts 2, 3, and 4.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

EIA_MONTHLY_URLS = {
    "contract_1": "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=m&n=pet&s=rclc1",
    "contract_2": "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=m&n=pet&s=rclc2",
    "contract_3": "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=m&n=pet&s=rclc3",
    "contract_4": "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=m&n=pet&s=rclc4",
}

MONTH_TO_NUMBER = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def _flatten_columns(columns: Iterable[object]) -> list[str]:
    """Turn HTML-table column labels into simple strings."""
    cleaned = []
    for col in columns:
        if isinstance(col, tuple):
            pieces = [
                str(piece).strip()
                for piece in col
                if str(piece) != "nan"
            ]
            cleaned.append(pieces[-1] if pieces else "")
        else:
            cleaned.append(str(col).strip())
    return cleaned


def _wide_eia_table_to_monthly(
    table: pd.DataFrame,
    value_name: str,
) -> pd.DataFrame:
    """Convert EIA's Year x Month table into one row per month."""
    out = table.copy()
    out.columns = _flatten_columns(out.columns)

    if "Year" not in out.columns:
        raise ValueError("Could not find the Year column in the EIA table.")

    available_months = [
        month for month in MONTH_TO_NUMBER if month in out.columns
    ]
    if not available_months:
        raise ValueError("Could not find month columns in the EIA table.")

    out = out[["Year", *available_months]].copy()
    out["Year"] = pd.to_numeric(out["Year"], errors="coerce")
    out = out.dropna(subset=["Year"])
    out["Year"] = out["Year"].astype(int)

    long = out.melt(
        id_vars="Year",
        value_vars=available_months,
        var_name="month_name",
        value_name=value_name,
    )

    long[value_name] = pd.to_numeric(
        long[value_name],
        errors="coerce",
    )
    long = long.dropna(subset=[value_name])
    long["month_number"] = long["month_name"].map(MONTH_TO_NUMBER)

    long["date"] = pd.to_datetime(
        {
            "year": long["Year"],
            "month": long["month_number"],
            "day": 1,
        }
    ) + pd.offsets.MonthEnd(0)

    return (
        long[["date", value_name]]
        .sort_values("date")
        .drop_duplicates("date", keep="last")
        .set_index("date")
    )


def load_eia_monthly_curve(
    start: str | None = "2015-01-01",
    end: str | None = None,
) -> pd.DataFrame:
    """Download monthly WTI Contract 1-4 prices from EIA history.

    EIA's NYMEX futures history ends in April 2024, so this function is for
    historical curve research rather than a live market-data feed.
    """
    pieces: list[pd.DataFrame] = []

    for value_name, url in EIA_MONTHLY_URLS.items():
        tables = pd.read_html(url)

        history_table = None
        for candidate in tables:
            candidate_columns = _flatten_columns(candidate.columns)
            if "Year" in candidate_columns and "Jan" in candidate_columns:
                history_table = candidate
                break

        if history_table is None:
            raise ValueError(
                f"Could not find EIA history table for {value_name}."
            )

        pieces.append(
            _wide_eia_table_to_monthly(history_table, value_name)
        )

    curve = pd.concat(pieces, axis=1).dropna().sort_index()

    if start is not None:
        curve = curve.loc[pd.Timestamp(start):]
    if end is not None:
        curve = curve.loc[:pd.Timestamp(end)]

    return curve


def add_curve_metrics(
    curve: pd.DataFrame,
    flat_threshold: float = 0.25,
) -> pd.DataFrame:
    """Add calendar spreads, curve slope, and a simple regime label.

    Main beginner rule:
        C1 - C4 > threshold  -> backwardation
        C1 - C4 < -threshold -> contango
        otherwise            -> flat
    """
    required = {
        "contract_1",
        "contract_2",
        "contract_3",
        "contract_4",
    }
    missing = required.difference(curve.columns)
    if missing:
        raise ValueError(
            f"Missing required curve columns: {sorted(missing)}"
        )
    if flat_threshold < 0:
        raise ValueError("flat_threshold must be zero or positive.")

    out = curve.copy().astype(float)

    out["c1_c2_spread"] = (
        out["contract_1"] - out["contract_2"]
    )
    out["c1_c3_spread"] = (
        out["contract_1"] - out["contract_3"]
    )
    out["c1_c4_spread"] = (
        out["contract_1"] - out["contract_4"]
    )

    # There are three contract steps from C1 to C4:
    # C1 -> C2 -> C3 -> C4.
    out["curve_slope_per_contract"] = (
        out["contract_4"] - out["contract_1"]
    ) / 3.0

    spread = out["c1_c4_spread"]
    out["curve_regime"] = np.select(
        [
            spread > flat_threshold,
            spread < -flat_threshold,
        ],
        [
            "backwardation",
            "contango",
        ],
        default="flat",
    )

    return out


def summarize_curve_regimes(
    curve_with_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize how often each curve regime appears in the sample."""
    if "curve_regime" not in curve_with_metrics.columns:
        raise ValueError(
            "Run add_curve_metrics() before summarizing regimes."
        )

    grouped = (
        curve_with_metrics.groupby(
            "curve_regime",
            observed=True,
        )
        .agg(
            months=("curve_regime", "size"),
            average_c1_c4_spread=("c1_c4_spread", "mean"),
            average_front_month_price=("contract_1", "mean"),
        )
        .reset_index()
    )

    grouped["share_of_sample"] = (
        grouped["months"] / grouped["months"].sum()
    )

    order = pd.Categorical(
        grouped["curve_regime"],
        categories=[
            "backwardation",
            "flat",
            "contango",
        ],
        ordered=True,
    )

    return (
        grouped.assign(_order=order)
        .sort_values("_order")
        .drop(columns="_order")
    )


def select_example_curves(
    curve_with_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Return the strongest backwardation and contango months."""
    if "c1_c4_spread" not in curve_with_metrics.columns:
        raise ValueError(
            "Run add_curve_metrics() before selecting examples."
        )

    strongest_backwardation = (
        curve_with_metrics["c1_c4_spread"].idxmax()
    )
    strongest_contango = (
        curve_with_metrics["c1_c4_spread"].idxmin()
    )

    examples = curve_with_metrics.loc[
        [
            strongest_backwardation,
            strongest_contango,
        ],
        [
            "contract_1",
            "contract_2",
            "contract_3",
            "contract_4",
            "c1_c4_spread",
            "curve_regime",
        ],
    ].copy()

    examples.index.name = "date"
    return examples
