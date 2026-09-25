# Historical Results

Sample: **February 2015 – July 2026**

Assumed production: **100,000 barrels per month**

This folder contains the main results and charts from the project.

## Hedge results

The model compares expected monthly revenue with the revenue produced after combining:

- physical oil sales
- WTI futures P&L

The main question is simple:

> How much does hedging reduce the producer's revenue risk?

The model measures this using **revenue surprise**, which is the difference between the revenue expected at the start of the month and the revenue produced by the model.

A smaller revenue surprise means the hedge kept revenue closer to expectations.

See:

- `hedge_ratio_summary.csv`
- `monthly_analysis.csv`
- `hedge_effectiveness.svg`
- `revenue_surprise_history.svg`

## Midland vs. Cushing basis stress test

This section tests what happens when Midland crude becomes cheaper or more expensive compared with Cushing WTI.

The example assumes:

- 100,000 barrels per month
- WTI futures entered at $75/bbl
- WTI futures exited at $60/bbl
- Cushing spot price of $60/bbl
- 100% of the main WTI price risk is hedged
- expected Midland basis of -$1/bbl
- basis hedges of 0%, 50%, and 100%

If Midland basis moves from **-$1/bbl to -$5/bbl**, the producer loses **$4/bbl** compared with the expected basis.

For 100,000 barrels, that equals a **$400,000 revenue shortfall** without a basis hedge.

A 50% basis hedge cuts that shortfall to about **$200,000**.

A full basis hedge offsets the modeled basis move.

See:

- `basis_risk_scenarios.csv`
- `basis_risk_stress.svg`

## Minimum-variance hedge results

The project also estimates the hedge size that historically reduced price risk the most.

See:

- `min_variance_summary.csv`
- `min_variance_comparison.csv`
- `min_variance_comparison.svg`
- `rolling_min_variance_ratio.csv`
- `rolling_min_variance_ratio.svg`
