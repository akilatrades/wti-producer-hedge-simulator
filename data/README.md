# Data

I used two main price series for this project: WTI Cushing spot prices and WTI futures prices.

The spot data comes from public FRED/EIA sources. The futures side uses Yahoo Finance ticker `CL=F`.

The saved results cover **February 2015 through July 2026**.

Public copies used for the saved analysis:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## One important limitation

The futures data is a continuous front-month series. It is useful for this type of project, but it is not the same as following the exact futures contract a real producer would trade each month.

A live trading or risk system would need to handle individual contracts, expiration and roll dates, trading costs, margin, production changes, and local price differences.
