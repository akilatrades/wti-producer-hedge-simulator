# Model Limitations

A credible risk project should state clearly what the model does **not** capture.

## Market-data limitations

### Continuous futures proxy

The main hedge history uses a continuous front-month WTI futures proxy.

A continuous series is useful for long historical analysis, but it is not identical to a sequence of actual producer hedge trades.

A production hedge would require contract-specific:

- trade dates,
- settlement prices,
- expiration dates,
- roll dates,
- liquidity,
- transaction costs.

### Spot-price proxy

WTI Cushing spot is used as a simplified physical-price proxy.

A real producer may realize a price based on:

- Midland or another location,
- crude quality,
- transport agreements,
- timing conventions,
- marketing deductions.

### Historical C1-C4 data

The EIA Contract 1-4 history used in the term-structure module ends in April 2024.

The module is therefore historical rather than a live curve monitor.

## Hedge-model limitations

The base hedge model assumes:

- known monthly production,
- simplified month-end timing,
- no transaction costs,
- no margin or liquidity constraints,
- no credit charges,
- no hedge-accounting effects,
- no tax effects,
- no execution slippage.

The production-uncertainty module relaxes the first assumption, but it remains a scenario model.

## Basis-risk limitations

The Midland/Cushing analysis is a scenario stress test.

It is not a historical backtest of a specific Midland basis futures or swap contract.

## Statistical limitations

The minimum-variance hedge ratio is estimated from historical covariance.

Potential issues include:

- structural change,
- sampling error,
- sensitivity to the chosen window,
- non-normal returns,
- changing physical/futures relationships.

The rolling, walk-forward, and bootstrap analyses are included specifically to make these limitations visible.

## VaR limitations

Historical VaR and Expected Shortfall depend on the sample.

They do not capture every possible future event and should not be interpreted as worst-case loss estimates.

## Curve-regime limitations

Backwardation and contango classifications are descriptive.

The chosen +/- $0.25/bbl threshold is a project convention.

The curve label alone is not a forecast of future WTI direction.

## Production-use gap

A production-grade commercial hedging system would require an ETRM or equivalent control environment covering:

- trade capture,
- confirmations,
- settlements,
- position limits,
- market data governance,
- independent valuation,
- P&L explain,
- risk limits,
- credit,
- audit trails,
- hedge accounting.

This repository is an analytical portfolio/research project rather than an ETRM.
