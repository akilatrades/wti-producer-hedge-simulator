import pandas as pd

from src.risk_metrics import (
    expected_shortfall,
    historical_var,
    summarize_revenue_risk,
)


def test_tail_risk_metrics_use_positive_loss_magnitudes():
    values = pd.Series([100.0, 50.0, 0.0, -50.0, -100.0, -200.0])

    var95 = historical_var(values, 0.95)
    es95 = expected_shortfall(values, 0.95)
    summary = summarize_revenue_risk(values)

    assert var95 > 0
    assert es95 >= var95
    assert summary["worst_loss"] == 200.0
