# Data

The project uses two main price series: WTI Cushing spot prices for the physical side and WTI futures prices for the hedge.

The saved analysis covers February 2015 through July 2026.

Public copies used for the saved results:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Continuous futures data

The futures history is a continuous front-month series.

A continuous series links several futures contracts together to create one long price history. That is useful for this analysis, but it is not the same as tracking the exact monthly contract a producer would trade.

A live hedge program would need contract-specific prices, expiration and roll dates, transaction costs, margin, production changes, and location or quality differences.
