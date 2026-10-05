import numpy as np
import pandas as pd

from src.fundamentals import prepare_fundamentals, to_monthly_fundamentals


def test_fundamental_features_and_monthly_conversion():
    dates = pd.date_range("2024-01-05", periods=20, freq="W-FRI")
    raw = pd.DataFrame(
        {
            "date": dates,
            "commercial_crude_stocks_kb": 400_000 + np.arange(20),
            "cushing_stocks_kb": 30_000 + np.arange(20),
            "imports_kbd": 7_000,
            "exports_kbd": 4_000,
        }
    )

    prepared = prepare_fundamentals(raw, zscore_window=3)
    monthly = to_monthly_fundamentals(prepared)

    assert "net_imports_kbd" in prepared
    assert "commercial_crude_stocks_kb_change" in prepared
    assert len(monthly) > 0
