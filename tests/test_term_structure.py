import pandas as pd

from src.term_structure import (
    add_curve_features,
    add_curve_metrics,
    select_example_curves,
    summarize_curve_regimes,
    summarize_regime_behavior,
)


def _curve():
    return pd.DataFrame(
        {
            "contract_1": [80.0, 70.0, 75.0, 78.0],
            "contract_2": [79.0, 71.0, 75.1, 77.5],
            "contract_3": [78.0, 72.0, 75.1, 77.0],
            "contract_4": [77.0, 73.0, 75.2, 76.5],
        },
        index=pd.to_datetime(
            ["2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30"]
        ),
    )


def test_curve_regimes_and_features():
    result = add_curve_metrics(_curve(), flat_threshold=0.25)

    assert result.loc["2024-01-31", "c1_c4_spread"] == 3.0
    assert result.loc["2024-01-31", "curve_regime"] == "backwardation"
    assert result.loc["2024-02-29", "c1_c4_spread"] == -3.0
    assert result.loc["2024-02-29", "curve_regime"] == "contango"
    assert round(result.loc["2024-03-31", "c1_c4_spread"], 2) == -0.20
    assert result.loc["2024-03-31", "curve_regime"] == "flat"

    summary = summarize_curve_regimes(result)
    assert summary["months"].sum() == 4

    examples = select_example_curves(result)
    assert len(examples) == 2

    features = add_curve_features(result, zscore_window=3)
    assert "curve_curvature" in features
    assert "c1_c4_zscore" in features
    assert "c1_c4_percentile" in features

    behavior = summarize_regime_behavior(features)
    assert "front_month_return_volatility" in behavior
