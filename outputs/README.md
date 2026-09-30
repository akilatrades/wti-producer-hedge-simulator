# Historical Results

This folder contains the saved outputs from the hedge model.

The example assumes 100,000 barrels of monthly production, and the historical sample runs from February 2015 through July 2026.

## Main hedge comparison

The model combines physical revenue with futures P&L and compares the result with the starting monthly futures benchmark.

The difference is called revenue surprise.

A smaller revenue surprise means modeled revenue stays closer to the starting benchmark.

The main files for this section are `hedge_ratio_summary.csv`, `monthly_analysis.csv`, `hedge_effectiveness.svg`, and `revenue_surprise_history.svg`.

## Midland/Cushing basis test

This stress test assumes Midland is expected to trade $1 below Cushing but later trades $5 below Cushing.

That $4/bbl move creates a $400,000 modeled shortfall on 100,000 barrels when basis is left unhedged.

A 50% basis hedge cuts the modeled shortfall to about $200,000. In the simplified model, a full basis hedge offsets the move.

The related files are `basis_risk_scenarios.csv` and `basis_risk_stress.svg`.

## Data-driven hedge size

The project also estimates the hedge ratio that minimizes residual price-change variance in the historical sample.

The static estimate is 1.016, or about 102 CL contracts after rounding for 100,000 barrels.

The rolling output shows how that estimate changes through time.

See `min_variance_summary.csv`, `min_variance_comparison.csv`, `min_variance_comparison.svg`, `rolling_min_variance_ratio.csv`, and `rolling_min_variance_ratio.svg`.

## WTI term structure

Module 2 studies the first four WTI futures delivery contracts and calculates C1-C2, C1-C3, and C1-C4 calendar spreads.

The C1-C4 spread is used to label each month as backwardation, contango, or relatively flat under a simple +/- $0.25/bbl threshold.

The saved historical snapshot covers January 2015 through April 2024. Under that rule, the sample contains 48 backwardation months, 54 contango months, and 10 flat months.

The main files are `term_structure_monthly.csv`, `term_structure_regime_summary.csv`, and `term_structure_example_curves.csv`.

Running `python run_term_structure.py` also creates:

- `term_structure_c1_c4_spread.svg`
- `term_structure_curve_examples.svg`

For a step-by-step beginner explanation, see `TERM_STRUCTURE_README.md`.

