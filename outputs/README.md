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

## WTI futures curve / term structure

Module 2 compares the first four historical WTI futures delivery positions.

The main beginner calculation is:

```text
C1-C4 spread = Contract 1 price - Contract 4 price
```

The sign tells us which side of the curve is higher:

```text
positive C1-C4 -> C1 is above C4
negative C1-C4 -> C1 is below C4
```

The project then applies a simple teaching threshold:

```text
above +$0.25/bbl -> backwardation
below -$0.25/bbl -> contango
otherwise        -> flat
```

The $0.25 threshold is a project setting, not a universal market rule.

The saved historical snapshot covers January 2015 through April 2024. Under this rule, the sample contains 48 backwardation months, 54 contango months, and 10 flat months.

Main files:

- `term_structure_monthly.csv` — every monthly C1-C4 observation plus the calculated spreads and label.
- `term_structure_regime_summary.csv` — counts and averages by curve label.
- `term_structure_example_curves.csv` — one strong backwardation example and one strong contango example.
- `term_structure_c1_c4_spread.svg` — the C1-C4 spread through time.
- `term_structure_curve_examples.svg` — visual examples of the two main curve shapes.

For the full beginner lesson, read `TERM_STRUCTURE_README.md`.

For a notebook that walks through the calculation one cell at a time, open:

`../notebooks/WTI_Term_Structure_Beginner_Walkthrough.ipynb`

