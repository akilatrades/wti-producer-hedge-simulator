"""Validation utilities for minimum-variance hedge-ratio research."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.min_variance import minimum_variance_hedge_ratio, price_changes


def _ratio_from_changes(changes: pd.DataFrame) -> float:
    covariance = changes["spot_change"].cov(changes["futures_change"])
    futures_variance = changes["futures_change"].var(ddof=1)
    if futures_variance <= 0:
        raise ValueError("Futures variance must be positive.")
    return float(covariance / futures_variance)


def walk_forward_min_variance(
    market: pd.DataFrame,
    window: int = 24,
    benchmark_ratio: float = 1.0,
) -> pd.DataFrame:
    """Estimate h* on a trailing window and test it on the next month."""
    if window < 3:
        raise ValueError("window must be at least 3 observations.")

    changes = price_changes(market)
    if len(changes) <= window:
        raise ValueError("Not enough observations for walk-forward testing.")

    rows = []
    for test_idx in range(window, len(changes)):
        train = changes.iloc[test_idx - window:test_idx]
        test = changes.iloc[test_idx]
        ratio = _ratio_from_changes(train)

        rows.append(
            {
                "date": changes.index[test_idx],
                "training_observations": int(len(train)),
                "estimated_hedge_ratio": ratio,
                "spot_change": float(test["spot_change"]),
                "futures_change": float(test["futures_change"]),
                "model_residual": float(
                    test["spot_change"] - ratio * test["futures_change"]
                ),
                "one_to_one_residual": float(
                    test["spot_change"]
                    - benchmark_ratio * test["futures_change"]
                ),
            }
        )

    return pd.DataFrame(rows).set_index("date")


def summarize_walk_forward(results: pd.DataFrame) -> dict:
    """Summarize out-of-sample residual risk."""
    required = {
        "estimated_hedge_ratio",
        "model_residual",
        "one_to_one_residual",
    }
    missing = required.difference(results.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return {
        "test_observations": int(len(results)),
        "average_estimated_hedge_ratio": float(
            results["estimated_hedge_ratio"].mean()
        ),
        "model_residual_std": float(
            results["model_residual"].std(ddof=1)
        ),
        "one_to_one_residual_std": float(
            results["one_to_one_residual"].std(ddof=1)
        ),
    }


def bootstrap_minimum_variance_ratio(
    market: pd.DataFrame,
    n_bootstrap: int = 5_000,
    confidence: float = 0.95,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    """Bootstrap the minimum-variance hedge ratio and its confidence interval."""
    if n_bootstrap <= 0:
        raise ValueError("n_bootstrap must be positive.")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1.")

    changes = price_changes(market).reset_index(drop=True)
    if len(changes) < 3:
        raise ValueError("At least 3 price-change observations are required.")

    rng = np.random.default_rng(seed)
    ratios = []

    for _ in range(n_bootstrap):
        sample_idx = rng.integers(0, len(changes), len(changes))
        sample = changes.iloc[sample_idx]
        futures_variance = sample["futures_change"].var(ddof=1)
        if futures_variance <= 0 or np.isnan(futures_variance):
            continue
        ratios.append(_ratio_from_changes(sample))

    if not ratios:
        raise ValueError("Bootstrap produced no valid hedge-ratio samples.")

    ratio_series = pd.Series(ratios, name="bootstrap_hedge_ratio")
    alpha = (1 - confidence) / 2

    summary = pd.DataFrame(
        [
            {
                "point_estimate": minimum_variance_hedge_ratio(market),
                "bootstrap_mean": float(ratio_series.mean()),
                "bootstrap_std": float(ratio_series.std(ddof=1)),
                "confidence_level": float(confidence),
                "lower_bound": float(ratio_series.quantile(alpha)),
                "upper_bound": float(ratio_series.quantile(1 - alpha)),
                "bootstrap_samples": int(len(ratio_series)),
            }
        ]
    )
    return summary, ratio_series
