# Data

This project uses two main price series:

- **WTI Cushing spot price** from FRED/EIA
- **WTI futures price** using Yahoo Finance ticker `CL=F`

The saved project results use public copies of those datasets so the analysis can be reproduced.

Historical sample used in the saved results:

**February 2015 through July 2026**

Sources:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Important limitation

The futures data is a **continuous front-month series**.

That is useful for a portfolio project, but it is not the same as tracking the exact futures contract a real producer would trade each month.

A real trading or risk system would also need:

- individual futures contracts
- contract expiration and roll dates
- trading costs
- margin requirements
- production uncertainty
- location and quality price differences
