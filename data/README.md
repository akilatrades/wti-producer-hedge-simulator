# Data

This project uses two price series.

The first is the WTI Cushing spot price. That is a cash-market reference price for crude oil at Cushing.

The second is WTI futures, using Yahoo Finance ticker `CL=F`.

The saved analysis covers February 2015 through July 2026.

Public copies of the data used for the saved results:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## One thing to know about the futures data

The futures series is continuous. In simple terms, it links several futures contracts together so there is one long price history.

That is useful for this project, but it is not the same as following the exact contract a real producer would trade each month.

A real hedge program would need to track individual contracts, expiration and roll dates, trading costs, margin, production changes, and local price differences.
