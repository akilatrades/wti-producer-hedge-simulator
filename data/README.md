# Data

The project intentionally does not commit downloaded market data.

`run_analysis.py` downloads:

- **WTI spot:** FRED series `DCOILWTICO`
- **WTI futures proxy:** Yahoo Finance ticker `CL=F`

This keeps the analysis reproducible without storing a stale market-data snapshot.

For institutional-quality work, replace the continuous front-month proxy with contract-specific WTI settlement data and an explicit roll schedule.
