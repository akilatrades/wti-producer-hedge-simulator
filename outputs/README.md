# Historical Results

These are the saved results from the model.

The sample runs from **February 2015 through July 2026**, and I assume the producer sells **100,000 barrels per month**.

## Hedge results

I wanted to see how much the futures hedge could keep monthly revenue closer to what the producer expected at the start of the month.

I call that difference **revenue surprise**. The smaller it is, the more stable the revenue is.

The main files are `hedge_ratio_summary.csv`, `monthly_analysis.csv`, `hedge_effectiveness.svg`, and `revenue_surprise_history.svg`.

## Midland vs. Cushing basis test

I also tested what happens if Midland crude gets cheaper relative to Cushing.

In the example, the producer expects a Midland basis of **-$1/bbl**, but it ends up at **-$5/bbl**. That is a $4/bbl move against the producer.

On 100,000 barrels, that creates a **$400,000 shortfall** with no basis hedge. A 50% basis hedge cuts it to about **$200,000**. In the simplified model, a full basis hedge offsets the move.

The related files are `basis_risk_scenarios.csv` and `basis_risk_stress.svg`.

## Hedge-size estimate

The project also estimates the hedge size that reduced price risk the most in the historical sample.

Those results are in `min_variance_summary.csv`, `min_variance_comparison.csv`, `min_variance_comparison.svg`, `rolling_min_variance_ratio.csv`, and `rolling_min_variance_ratio.svg`.
