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

## Minimum-variance hedge ratio

Instead of choosing a hedge ratio only by policy (25%, 50%, 75%, 100%), the project now estimates a **minimum-variance hedge ratio** from historical monthly WTI spot and futures price changes:

```text
h* = Cov(ΔSpot, ΔFutures) / Var(ΔFutures)
```

For the historical sample, the estimated static ratio is **1.016**. For 100,000 barrels/month, that rounds to **102 CL contracts**, or roughly **1.02× production exposure**.

Monthly spot/futures changes had a correlation of **0.983**. Using the rounded minimum-variance ratio reduced monthly price-change variance by **96.6%**, with residual volatility of about **$1.35/bbl** versus **$7.29/bbl** unhedged.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

The model also calculates a **24-month rolling hedge ratio** to show that the statistically optimal ratio changes through time rather than remaining fixed.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

This is a statistical risk-minimization result, not a recommendation to over-hedge physical production. A commercial desk would also consider production uncertainty, hedge limits, liquidity, basis risk, accounting treatment, and risk policy.

## Basis risk extension: Midland vs Cushing

A producer may sell physical crude in **Midland, Texas** while using NYMEX WTI futures referenced to **Cushing, Oklahoma**. That introduces **location basis risk**:

```text
Midland basis = Midland physical price - Cushing price
```

A flat-price WTI futures hedge can neutralize much of the outright crude-price move while leaving the producer exposed to the Midland/Cushing differential.

The project now includes an **illustrative basis stress test** with a basis initially locked at **-$1/bbl**. The producer is assumed to hedge 100% of flat-price exposure with WTI futures while separately testing 0%, 50%, and 100% basis-swap coverage.

Example: if realized Midland basis widens from **-$1/bbl to -$5/bbl**, a 100,000 bbl/month producer has a **$400,000 location-basis shortfall** even though the outright WTI price is fully hedged. A 50% basis hedge cuts that residual to **$200,000**; a 100% basis swap offsets the modeled basis move.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

This is intentionally a **scenario analysis, not a claimed historical Midland cash backtest**. Reliable institutional basis datasets are often proprietary. The commercial mechanism is real: public EOG disclosures describe using Midland Differential basis swaps to fix the difference between Midland and Cushing pricing.

- [EIA: WTI Cushing spot-market definition](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
- [SEC/EOG disclosure: Midland Differential basis swaps](https://www.sec.gov/Archives/edgar/data/821189/000082118919000020/a2019033110-q.htm)

### Why this matters

This separates two risks that are easy to blur together:

```text
Outright price risk → hedge with WTI futures

Location basis risk → hedge with a Midland/Cushing basis instrument
```

A producer can therefore be **100% hedged on flat price and still lose money versus its expected realized price if local basis weakens**.

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
- explicit Midland/Cushing location basis risk;
- basis-swap scenario hedging;
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
│   ├── hedge_engine.py
│   ├── basis_risk.py
│   └── min_variance.py
├── notebooks/
│   └── WTI_Producer_Hedge_Simulator.ipynb
├── data/
│   └── README.md
└── outputs/
    ├── README.md
    ├── hedge_ratio_summary.csv
    ├── monthly_analysis.csv
    ├── hedge_effectiveness.svg
    ├── revenue_surprise_history.svg
    ├── basis_risk_scenarios.csv
    ├── basis_risk_stress.svg
    ├── min_variance_summary.csv
    ├── min_variance_comparison.svg
    └── rolling_min_variance_ratio.svg
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

- historical contract-specific Midland basis data
- rolling hedge ratios
- WTI/Brent cross-hedging
- producer collars and put options
- VaR and stress testing
- Streamlit risk dashboard

## Why I built this

My interest is in the intersection of physical energy markets, futures, risk, and commercial decision-making. This project applies futures concepts to the cash-flow problem faced by a crude producer rather than to directional speculation.

---

**Disclaimer:** Educational and portfolio use only. Not investment advice.
