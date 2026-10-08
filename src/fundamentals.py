"""Optional physical-market context for WTI curve research."""

from __future__ import annotations

import pandas as pd


FUNDAMENTAL_COLUMNS = (
    "commercial_crude_stocks_kb",
    "cushing_stocks_kb",
    "refinery_utilization_pct",
    "crude_production_kbd",
    "imports_kbd",
    "exports_kbd",
)


def prepare_fundamentals(
    fundamentals: pd.DataFrame,
    zscore_window: int = 13,
) -> pd.DataFrame:
    """Create changes, net imports, and rolling z-scores."""
    if zscore_window < 3:
        raise ValueError("zscore_window must be at least 3.")

    out = fundamentals.copy()
    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"])
        out = out.set_index("date")
    if not isinstance(out.index, pd.DatetimeIndex):
        raise ValueError("Fundamentals must use a DatetimeIndex or date column.")

    available = [c for c in FUNDAMENTAL_COLUMNS if c in out.columns]
    if not available:
        raise ValueError("No recognized fundamental columns were supplied.")

    for col in available:
        out[col] = pd.to_numeric(out[col], errors="coerce")
        out[f"{col}_change"] = out[col].diff()
        rolling_mean = out[col].rolling(zscore_window).mean()
        rolling_std = out[col].rolling(zscore_window).std(ddof=1)
        out[f"{col}_zscore"] = (out[col] - rolling_mean) / rolling_std

    if {"imports_kbd", "exports_kbd"}.issubset(out.columns):
        out["net_imports_kbd"] = out["imports_kbd"] - out["exports_kbd"]

    return out.sort_index()


def to_monthly_fundamentals(fundamentals: pd.DataFrame) -> pd.DataFrame:
    """Convert weekly/daily physical-market observations to month-end rows."""
    if not isinstance(fundamentals.index, pd.DatetimeIndex):
        raise ValueError("fundamentals must use a DatetimeIndex.")
    return fundamentals.sort_index().resample("ME").last()


def join_curve_and_fundamentals(
    curve: pd.DataFrame,
    fundamentals: pd.DataFrame,
) -> pd.DataFrame:
    """Join monthly curve metrics with prepared physical-market context."""
    if not isinstance(curve.index, pd.DatetimeIndex):
        raise ValueError("curve must use a DatetimeIndex.")
    monthly = to_monthly_fundamentals(fundamentals)
    return curve.join(monthly, how="inner")


def summarize_fundamentals_by_regime(
    combined: pd.DataFrame,
) -> pd.DataFrame:
    """Average selected physical variables by curve regime."""
    if "curve_regime" not in combined.columns:
        raise ValueError("combined data must include curve_regime.")

    numeric = [c for c in FUNDAMENTAL_COLUMNS if c in combined.columns]
    if "net_imports_kbd" in combined.columns:
        numeric.append("net_imports_kbd")
    if not numeric:
        raise ValueError("No fundamental columns available to summarize.")

    return combined.groupby("curve_regime", observed=True)[numeric].mean().reset_index()
