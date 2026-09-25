# WTI Producer Hedge Simulator

A portfolio project that models how a crude-oil producer can use NYMEX WTI futures to reduce revenue volatility.

## Business question

> If a producer expects to sell 100,000 barrels of crude each month, how much revenue risk can be reduced by hedging 25%, 50%, 75%, or 100% of production with WTI futures?

This project reframes futures from a directional trading instrument into a commercial risk-management tool.

## What the project does

- Downloads public WTI spot-price data from FRED and a front-month WTI futures proxy (`CL=F`) from Yahoo Finance.
- Converts daily prices into monthly production and hedge observations.
- Simulates a short futures hedge for monthly crude production.
- Compares 0%, 25%, 50%, 75%, and 100% hedge ratios.
- Calculates physical revenue, futures P&L, combined hedged revenue, revenue volatility, downside revenue, minimum monthly revenue, and hedge effectiveness.
- Produces charts comparing unhedged and hedged revenue.
- Includes a simple stress-test function for crude-price shocks.

## Commercial intuition

A crude producer is naturally **long physical oil**: higher crude prices increase revenue, while lower prices reduce revenue.

To hedge that exposure, the producer can **short WTI futures**.

If WTI falls, physical revenue decreases while the short futures position gains value. If WTI rises, physical revenue increases while the short futures position loses value.

The objective is not to maximize trading profit. It is to stabilize commercial cash flow.

## Core hedge math

For monthly production volume `Q` and hedge ratio `h`:

```text
Hedged barrels = Q × h

Number of futures contracts =
Hedged barrels / 1,000
```

One NYMEX WTI futures contract represents 1,000 barrels.

For a short futures hedge:

```text
Futures P&L =
(Entry futures price - Exit futures price) × Hedged barrels
```

Total commercial revenue:

```text
Hedged revenue =
Physical revenue + Futures P&L
```

## Project structure

```text
wti-producer-hedge-simulator/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── run_analysis.py
├── data/
│   └── README.md
├── notebooks/
│   └── WTI_Producer_Hedge_Simulator.ipynb
└── src/
    └── hedge_engine.py
```

## Quick start

```bash
python -m venv .venv
pip install -r requirements.txt
python run_analysis.py
```

The script saves analysis tables, summary metrics, and charts into the `outputs/` folder.

## Important modeling note

This is a portfolio/educational model. Yahoo Finance's `CL=F` is used as a **continuous front-month WTI futures proxy**, not as a contract-specific historical settlement database.

A production trading/risk system would normally use individual futures contracts, explicit expiration and roll rules, contract-specific settlement prices, physical location and quality differentials, transaction costs, margin requirements, and credit/liquidity constraints.

That limitation is intentional and documented rather than hidden.

## Possible extensions

- Midland/Cushing basis risk
- WTI vs Brent cross-hedging
- minimum-variance hedge ratios
- rolling regression hedge ratios
- options/collars
- producer breakeven floors
- VaR and stress testing
- Streamlit dashboard
- storage / contango economics

## Why I built this

My interest is in the intersection of physical energy markets, futures, risk, and commercial decision-making. This project translates concepts familiar from active futures trading into the risk-management problem faced by a crude producer.

---

**Disclaimer:** Educational/portfolio use only. Not investment advice.
