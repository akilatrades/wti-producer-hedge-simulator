# Risk Metrics

## Business interpretation

Hedge effectiveness is useful, but variance alone does not describe the entire downside distribution.

A commercial or market-risk review should also answer:

- How large are bad months?
- What loss threshold is exceeded only 5% or 1% of the time?
- When the threshold is exceeded, how severe are losses on average?
- What was the worst historical observation?
- How much downside volatility remains after hedging?

The project therefore calculates historical tail-risk statistics for each hedge ratio.

## Volatility

For monthly revenue surprise:

```text
Monthly volatility = standard deviation(revenue surprise)
```

Annualized volatility is reported as:

```text
Monthly standard deviation × sqrt(12)
```

This annualization is a scaling convention, not a forecast of a future annual loss.

## Historical Value at Risk

The project defines loss as:

```text
Loss = -Revenue surprise
```

Historical 95% VaR is the 95th percentile of that loss distribution.

Example interpretation:

> A 95% historical VaR of $500,000 means 95% of historical modeled monthly losses were at or below $500,000; 5% were worse.

It is not a maximum-loss estimate.

## Expected Shortfall

Expected Shortfall (ES), also called Conditional VaR, averages the losses at or beyond the VaR threshold.

```text
ES = average loss conditional on loss >= VaR
```

ES is useful because two strategies can have similar VaR while one has a much worse extreme tail.

## Downside deviation

Downside deviation measures dispersion of negative revenue surprises only.

It is useful when the objective is specifically to understand unfavorable deviations from the benchmark.

## Worst period

The model reports the most negative historical revenue surprise and the corresponding loss.

This is descriptive stress evidence rather than a guarantee that future losses cannot be larger.

## Comparing strategies

The generated risk table is designed to compare:

- 0% hedge,
- 25% hedge,
- 50% hedge,
- 75% hedge,
- 100% hedge.

A professional interpretation should consider both risk reduction and the economic/commercial constraints of the hedge.
