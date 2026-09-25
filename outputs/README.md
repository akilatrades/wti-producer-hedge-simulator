# Historical Results

This folder holds the saved outputs from the hedge model.

The example producer sells 100,000 barrels per month, and the historical sample runs from February 2015 through July 2026.

## Main hedge comparison

I compare the producer's physical revenue plus futures P&L against the starting monthly futures benchmark. The difference is called revenue surprise.

The smaller that surprise is over time, the more stable the modeled revenue is.

The main result files are `hedge_ratio_summary.csv`, `monthly_analysis.csv`, `hedge_effectiveness.svg`, and `revenue_surprise_history.svg`.

## Midland/Cushing basis test

This stress test assumes the producer expected Midland to trade $1 below Cushing, but the difference widened to $5 below Cushing.

That $4/bbl move creates a $400,000 modeled shortfall on 100,000 barrels when the basis is left unhedged. A 50% basis hedge cuts the shortfall to about $200,000. In the simplified model, a full basis hedge offsets the move.

The related files are `basis_risk_scenarios.csv` and `basis_risk_stress.svg`.

## Data-driven hedge size

I also estimate the hedge ratio that minimized residual price-change variance in the historical sample.

The static estimate was 1.016, or about 102 CL contracts after rounding for 100,000 barrels. The rolling file shows how that estimate changed through time.

See `min_variance_summary.csv`, `min_variance_comparison.csv`, `min_variance_comparison.svg`, `rolling_min_variance_ratio.csv`, and `rolling_min_variance_ratio.svg`.
