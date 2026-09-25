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
