# WTI Producer Hedge Simulator

A Python portfolio project modeling how a crude-oil producer can use NYMEX WTI futures to reduce revenue risk.

## Business question

> If a producer expects to sell **100,000 barrels of crude per month**, how much price risk can be reduced by hedging 25%, 50%, 75%, or 100% of expected production with WTI futures?

The project reframes futures from a directional trading instrument into a **commercial risk-management tool**.

## Historical result

Using a historical sample from **February 2015 through July 2026**, the model finds that increasing the hedge ratio materially reduces the variance of monthly revenue surprise versus the prior-month WTI futures benchmark.

| Hedge ratio | CL contracts short | Revenue-surprise std. dev. | 5th percentile surprise | Hedge effectiveness |
|---:|---:|---:|---:|---:|
| 0% | 0 | $711,294 | $-1,064,650 | 0.0% |
| 25% | 25 | $540,295 | $-793,675 | 42.3% |
| 50% | 50 | $373,697 | $-507,900 | 72.4% |
| 75% | 75 | $221,653 | $-237,000 | 90.3% |
| 100% | 100 | $142,693 | $-27,300 | 96.0% |

A **75% hedge** reduced revenue-surprise variance by **90.3%** and lowered monthly surprise volatility from about **$711,294** unhedged to **$221,653**. A **100% benchmark hedge** reduced variance by **96.0%**, although residual spot/futures basis and continuous-contract effects remain.

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

![Revenue surprise](outputs/revenue_surprise_history.svg)

## Commercial intuition

A crude producer is naturally **long physical oil**. Falling crude prices reduce the value of future production.

To reduce that exposure, the producer can **short WTI futures**:

- if WTI falls, physical revenue falls but the short futures position gains;
- if WTI rises, physical revenue rises but the short futures position loses.

The objective is not to maximize trading P&L. The objective is to make commercial cash flow more predictable.

## Model

For monthly production volume `Q` and hedge ratio `h`:

```text
Hedged barrels = Q × h

CL contracts = hedged barrels / 1,000
```

For the short futures position:

```text
Futures P&L =
(entry futures price - exit futures price) × hedged barrels
```

Commercial revenue:

```text
Hedged revenue =
physical revenue + futures P&L
```

The key risk measure is **revenue surprise**:

```text
Benchmark locked revenue =
futures entry price × total monthly production

Revenue surprise =
hedged revenue - benchmark locked revenue
```

Hedge effectiveness is:

```text
1 - Var(hedged revenue surprise) / Var(unhedged revenue surprise)
```

## What the project demonstrates

- physical commodity exposure translated into futures hedge sizing;
- WTI contract sizing at 1,000 barrels per CL contract;
- physical revenue + derivatives P&L;
- partial versus full hedging;
- downside-risk analysis;
- hedge effectiveness;
- basis/proxy risk;
- stress testing;
- Python time-series analysis and visualization.

## Project structure

```text
wti-producer-hedge-simulator/
├── README.md
├── requirements.txt
├── run_analysis.py
├── src/
│   └── hedge_engine.py
├── notebooks/
│   └── WTI_Producer_Hedge_Simulator.ipynb
├── data/
│   └── README.md
└── outputs/
    ├── README.md
    ├── hedge_ratio_summary.csv
    ├── monthly_analysis.csv
    ├── hedge_effectiveness.svg
    └── revenue_surprise_history.svg
```

## Quick start

```bash
python -m venv .venv
pip install -r requirements.txt
python run_analysis.py
```

## Data

The runtime script refreshes WTI Cushing spot from **FRED/EIA** and the continuous front-month WTI proxy from **Yahoo Finance (`CL=F`)**.

The committed historical snapshot uses public mirrors of those series for reproducibility:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Important limitation

This is an educational/portfolio risk model, not a production ETRM system. A continuous front-month futures series can contain roll effects and does not represent a single contract held from hedge initiation to physical settlement.

An institutional implementation would use contract-specific settlements, explicit roll rules, physical location/quality differentials, transaction costs, margin/liquidity constraints, and counterparty/credit considerations.

## Next extensions

- Midland/Cushing basis risk
- minimum-variance hedge ratio
- rolling hedge ratios
- WTI/Brent cross-hedging
- producer collars and put options
- VaR and stress testing
- Streamlit risk dashboard

## Why I built this

My interest is in the intersection of physical energy markets, futures, risk, and commercial decision-making. This project applies futures concepts to the cash-flow problem faced by a crude producer rather than to directional speculation.

---

**Disclaimer:** Educational and portfolio use only. Not investment advice.
