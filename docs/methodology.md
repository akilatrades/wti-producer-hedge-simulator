# Methodology

## Business interpretation

The project asks a commercial risk question:

> How can a crude-oil producer use WTI futures to reduce uncertainty in future revenue, and what risks remain after the hedge is applied?

The analysis separates the problem into distinct risk components instead of treating a hedge as one P&L number.

```text
Expected physical production
        |
        v
Flat-price exposure -----> NYMEX WTI futures hedge
        |
        +-----> Midland/Cushing basis exposure
        |
        +-----> delivery-month / curve exposure
        |
        +-----> production-volume uncertainty
        |
        v
Residual revenue risk
```

This structure is intentionally similar to how market-risk problems are decomposed on a trading or commercial desk: identify the exposure, select an instrument, measure residual risk, stress the assumptions, and validate the model.

## Analytical workflow

The project currently follows this sequence:

1. Load WTI spot and futures data.
2. Convert the daily data to aligned monthly observations.
3. Simulate fixed hedge ratios.
4. Measure hedge effectiveness and downside risk.
5. Decompose physical and futures P&L.
6. Estimate a minimum-variance hedge ratio.
7. Test hedge-ratio stability with rolling and walk-forward analysis.
8. Quantify sampling uncertainty with bootstrap confidence intervals.
9. Stress Midland/Cushing basis.
10. Build illustrative multi-month hedge ladders.
11. Stress production-volume uncertainty and over-hedging risk.
12. Analyze WTI term structure and curve regimes.
13. Optionally join EIA physical-market fundamentals to the curve dataset.

## Core hedge equation

For a producer that is long physical crude and short futures:

```text
Physical revenue
+ Futures hedge P&L
= Hedged revenue
```

For a short futures hedge:

```text
Futures P&L
= (entry futures price - exit futures price)
  × hedged barrels
```

A falling futures price produces positive hedge P&L; a rising futures price produces negative hedge P&L.

## Hedge effectiveness

The primary effectiveness statistic is variance reduction:

```text
Hedge effectiveness
= 1 - Var(hedged revenue surprise) / Var(unhedged revenue surprise)
```

A result of 0.90 means the hedge reduced modeled revenue-surprise variance by 90% relative to the unhedged exposure.

This is a risk statistic, not a statement that the hedge is economically optimal under every commercial objective.

## Minimum-variance hedge ratio

The classical minimum-variance hedge ratio is:

```text
h* = Cov(ΔSpot, ΔFutures) / Var(ΔFutures)
```

The estimate minimizes the historical variance of:

```text
ΔSpot - h × ΔFutures
```

The project treats this as a statistical benchmark, not an automatic commercial hedge recommendation.

## Risk metrics

The model also evaluates the lower tail of the revenue distribution using:

- volatility,
- historical Value at Risk (VaR),
- Expected Shortfall (ES),
- worst observed period,
- downside deviation,
- and stress scenarios.

See [risk_metrics.md](risk_metrics.md).

## Validation

A model can look excellent in the same sample used to estimate it. The project therefore includes:

- rolling hedge ratios,
- walk-forward / out-of-sample testing,
- bootstrap confidence intervals.

See [validation.md](validation.md).

## Reproducibility

The repository keeps calculation logic in `src/`, worked analysis in `notebooks/`, saved data in `data/`, and generated tables/charts in `outputs/`.

Tests validate the core hedge math and new risk modules. GitHub Actions runs the test suite automatically on pushes and pull requests.

## Interpretation rule

The project follows one consistent rule:

> A model result is evidence about historical risk behavior, not a guarantee about future prices or a substitute for commercial policy.

That distinction is especially important for minimum-variance estimates, curve regimes, and historical stress statistics.
