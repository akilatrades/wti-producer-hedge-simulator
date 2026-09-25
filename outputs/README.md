# Historical Results

Sample: **February 2015 – July 2026**

Assumed physical production: **100,000 barrels per month**

The producer realizes month-end WTI Cushing spot. A short futures hedge is initiated using the prior month-end continuous front-month WTI futures proxy and closed at the current month-end proxy.

## Risk metric

Rather than comparing the level of revenue over an 11-year period, the project measures **revenue surprise** versus the prior-month futures benchmark:

```text
Benchmark locked revenue = futures entry price × production

Revenue surprise =
physical revenue + futures P&L - benchmark locked revenue
```

Hedge effectiveness is the percentage reduction in the variance of that monthly revenue surprise relative to the unhedged case.

See `hedge_ratio_summary.csv` for the full output.


## Midland/Cushing basis stress test

The basis extension uses an **illustrative** set of realized Midland-minus-Cushing differentials:

`+$1, $0, -$1, -$3, -$5, -$10 per barrel`

Assumptions:

- 100,000 barrels/month of Midland production
- Cushing futures entry: $75/bbl
- Cushing futures exit: $60/bbl
- Cushing spot exit: $60/bbl
- 100% flat-price hedge with WTI futures
- basis initially locked at -$1/bbl
- basis-hedge ratios of 0%, 50%, and 100%

The key result is that a flat-price hedge does **not** eliminate location basis risk. With no basis swap, a move from -$1 to -$5/bbl produces a $400,000 revenue shortfall versus the locked benchmark. A full basis swap offsets that modeled change.

See `basis_risk_scenarios.csv` and `basis_risk_stress.svg`.
