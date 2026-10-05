import numpy as np
import pandas as pd

from src.validation import (
    bootstrap_minimum_variance_ratio,
    summarize_walk_forward,
    walk_forward_min_variance,
)


def _market(n=40):
    rng = np.random.default_rng(7)
    futures_change = rng.normal(0, 2, n)
    spot_change = futures_change + rng.normal(0, 0.25, n)

    futures_exit = 70 + np.cumsum(futures_change)
    spot_exit = 69 + np.cumsum(spot_change)
    futures_entry = np.r_[futures_exit[0] - 1, futures_exit[:-1]]

    return pd.DataFrame(
        {
            "spot_exit": spot_exit,
            "futures_entry": futures_entry,
            "futures_exit": futures_exit,
        },
        index=pd.date_range("2020-01-31", periods=n, freq="ME"),
    )


def test_walk_forward_and_bootstrap_outputs():
    market = _market()

    walk = walk_forward_min_variance(market, window=12)
    summary = summarize_walk_forward(walk)
    bootstrap, samples = bootstrap_minimum_variance_ratio(
        market,
        n_bootstrap=250,
        seed=1,
    )

    assert len(walk) > 0
    assert summary["model_residual_std"] >= 0
    assert bootstrap["lower_bound"].iloc[0] < bootstrap["upper_bound"].iloc[0]
    assert len(samples) > 0
