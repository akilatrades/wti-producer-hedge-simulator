# Data and historical snapshot

The runtime analysis downloads:

- **WTI Cushing spot:** FRED series `DCOILWTICO`, sourced from the U.S. Energy Information Administration.
- **WTI continuous futures proxy:** Yahoo Finance ticker `CL=F`.

The committed historical results in `outputs/` use:

- WTI spot observations from the public `datasets/oil-prices` GitHub dataset, which mirrors the FRED/EIA WTI series.
- A continuous WTI futures history from the public `JavierLuqueGarcia/Crude-oil-Backtest` dataset, sourced from Yahoo Finance.

The overlapping committed sample runs from **February 2015 through July 2026**.

## Modeling limitation

A continuous front-month series is useful for portfolio analysis but is not the same as a contract-specific institutional hedge book. A production implementation should use individual futures contracts, explicit roll/expiry logic, transaction costs, margin requirements, and location/quality basis.
