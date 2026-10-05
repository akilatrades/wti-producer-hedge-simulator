# Model Validation

## Business interpretation

A hedge model should not be judged only on the same data used to estimate it.

The project therefore adds two validation tools:

1. **walk-forward testing** — estimate the hedge ratio using historical data available at the time, then test it on the next observation;
2. **bootstrap uncertainty** — repeatedly resample the historical price changes to estimate how uncertain the hedge-ratio estimate is.

These analyses help distinguish a robust relationship from an in-sample result that may be overly precise.

## Walk-forward minimum-variance hedge ratio

For a 24-month training window:

```text
Months 1-24 -> estimate h*
Month 25    -> test residual

Months 2-25 -> estimate h*
Month 26    -> test residual

...
```

For each test month, the project stores:

- estimated hedge ratio,
- spot change,
- futures change,
- hedged residual,
- residual using a 1.0 hedge benchmark.

The summary compares out-of-sample residual volatility.

## Why this is useful

Suppose a static in-sample estimate reduces variance by 96%.

That does not mean a hedge ratio estimated in real time would have delivered the same result.

Walk-forward testing asks the more realistic question:

> If only prior information had been available, how well would the estimate have hedged the next period?

## Bootstrap confidence interval

The minimum-variance estimate is:

```text
h* = Cov(ΔS, ΔF) / Var(ΔF)
```

The point estimate can look more precise than the data justify.

The bootstrap procedure:

1. creates many resampled datasets from the historical monthly changes;
2. recalculates h* for each sample;
3. reports the empirical confidence interval.

Example interpretation:

```text
Point estimate: 1.02
95% interval: [lower, upper]
```

The interval is more informative than reporting 1.016 as if it were a known constant.

## Validation philosophy

The project treats a hedge ratio as a time-varying risk estimate.

A statistically optimal historical ratio can still be commercially inappropriate because of production uncertainty, hedge limits, basis risk, liquidity, or accounting constraints.
