# Historical Results

This folder holds the saved charts and result files from the model.

The sample runs from February 2015 through July 2026. The example producer sells 100,000 barrels per month.

## Main hedge results

The basic question is whether the futures hedge keeps revenue closer to what the producer expected.

I measure that difference as revenue surprise.

If the revenue surprise is smaller, the hedge did a better job of reducing uncertainty.

The main files for this section are `hedge_ratio_summary.csv`, `monthly_analysis.csv`, `hedge_effectiveness.svg`, and `revenue_surprise_history.svg`.

## Midland and Cushing basis test

This test looks at what happens when Midland crude gets cheaper relative to Cushing.

The producer expects Midland to trade $1 below Cushing, but the difference later widens to $5 below Cushing. That is a $4 per barrel move against the producer.

On 100,000 barrels, the difference is $400,000.

With no basis hedge, the full $400,000 remains. With a 50% basis hedge, about $200,000 remains. In this simplified model, a full basis hedge offsets the move.

The files for this section are `basis_risk_scenarios.csv` and `basis_risk_stress.svg`.

## Hedge-size estimate

I also used the historical relationship between WTI spot and futures prices to estimate the hedge size that reduced price movement the most.

Those results are in `min_variance_summary.csv`, `min_variance_comparison.csv`, `min_variance_comparison.svg`, `rolling_min_variance_ratio.csv`, and `rolling_min_variance_ratio.svg`.
