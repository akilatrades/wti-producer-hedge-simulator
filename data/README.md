# Data

The project uses two main price series: WTI Cushing spot prices for the physical side and WTI futures prices for the hedge.

The saved analysis covers February 2015 through July 2026.

Public copies used for the saved results:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

The futures history is a continuous front-month series. That gives the project one long futures price history, but it is not the same as tracking the exact monthly contract a real producer would trade.

A live hedge program would need contract-specific prices, roll dates, transaction costs, margin, production changes, and location/quality differences.
