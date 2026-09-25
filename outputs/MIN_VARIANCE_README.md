# Minimum-Variance Hedge Results

Historical sample: **March 2015 – July 2026** for monthly price changes.

## Static estimate

```text
h* = Cov(ΔSpot, ΔFutures) / Var(ΔFutures)
```

Estimated hedge ratio: **1.016**

For a producer with 100,000 barrels/month, that corresponds to approximately **102 CL contracts** after whole-contract rounding, or a practical hedge ratio of **1.02**.

Spot/futures monthly-change correlation: **0.983**

Using the rounded 1.02 hedge ratio:

- unhedged monthly price-change volatility: **$7.29/bbl**
- residual hedged price-change volatility: **$1.35/bbl**
- variance reduction: **96.6%**

## Interpretation

The estimated minimum-variance ratio is slightly above 1.0 because the historical spot and continuous-futures changes did not move one-for-one in every month.

The result should not be interpreted as "always hedge more than 100%." Commercial hedge limits, production uncertainty, liquidity, basis exposure, accounting treatment, and risk policy can all make a lower operational hedge ratio appropriate.

The 24-month rolling estimate is also included to show that the statistically optimal ratio is not constant through time.
