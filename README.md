# WTI Producer Hedge Simulator

I built this project to connect futures trading with a real energy problem.

The setup is simple: assume a crude oil producer expects to sell **100,000 barrels per month**. If oil prices fall before that oil is sold, revenue falls too. I wanted to see how much of that risk could be reduced by shorting WTI futures.

## What I tested

I started by comparing a few simple hedge sizes: 0%, 25%, 50%, 75%, and 100% of expected production.

For each one, I combined the producer's physical oil revenue with the profit or loss from the futures hedge. Then I compared how stable the total revenue was.

Using historical data from **February 2015 through July 2026**, I got these results:

| Hedge ratio | CL contracts short | Revenue volatility | Hedge effectiveness |
|---:|---:|---:|---:|
| 0% | 0 | $711,294 | 0.0% |
| 25% | 25 | $540,295 | 42.3% |
| 50% | 50 | $373,697 | 72.4% |
| 75% | 75 | $221,653 | 90.3% |
| 100% | 100 | $142,693 | 96.0% |

The main takeaway was pretty clear. In this sample, a **75% hedge cut modeled revenue risk by about 90%**. A full hedge reduced it by about **96%**.

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

![Revenue surprise](outputs/revenue_surprise_history.svg)

## Finding a better hedge size

After testing fixed hedge sizes, I wanted to see what the data itself would suggest.

I used the historical relationship between WTI spot prices and WTI futures prices to estimate a hedge size that would have reduced price swings the most.

That estimate came out to **1.016**, which is about **102 CL contracts** for 100,000 barrels of production.

Using that hedge size reduced monthly price-change variance by about **96.6%** in the sample.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

I also looked at the hedge ratio over rolling 24-month periods. It moved over time, which makes sense because market relationships are not always constant.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

I would not treat 102 contracts as a real-world recommendation. A real trading or risk desk would also have to think about production uncertainty, hedge limits, liquidity, accounting rules, and company risk policy.

## Midland vs. Cushing basis risk

The next piece I wanted to understand was basis risk.

A producer may sell crude in **Midland, Texas** while using WTI futures tied to **Cushing, Oklahoma**. Those two prices are related, but they are not always the same.

In this model:

```text
Midland basis = Midland price - Cushing price
```

So even if the producer hedges the main WTI price move, the Midland price can still weaken compared with Cushing.

Here is the example I used. The producer expects Midland to trade at **-$1/bbl** versus Cushing, but the actual basis ends up at **-$5/bbl**. That is a **$4/bbl move against the producer**.

On 100,000 barrels, that works out to:

```text
$4 × 100,000 barrels = $400,000
```

With no basis hedge, the modeled shortfall is $400,000. With a 50% basis hedge, it drops to about $200,000. In the simplified model, a full basis hedge offsets that move.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

This part is a stress-test example, not a historical Midland cash-price backtest.

For background on the pricing and the use of Midland differential hedges:

- [EIA: WTI Cushing spot-market definition](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
- [SEC/EOG disclosure: Midland Differential basis swaps](https://www.sec.gov/Archives/edgar/data/821189/000082118919000020/a2019033110-q.htm)

## How the hedge works

A producer is naturally exposed to falling oil prices because it owns future production.

If the producer shorts WTI futures and oil prices fall, the physical oil is worth less, but the short futures position gains. If oil prices rise, the physical oil is worth more, but the futures hedge loses.

The point is not to make the most money on the futures trade. The point is to make total revenue less sensitive to oil-price swings.

The basic math is:

```text
Hedged barrels = monthly production × hedge ratio

CL contracts = hedged barrels / 1,000

Futures P&L =
(entry futures price - exit futures price) × hedged barrels

Total revenue =
physical oil revenue + futures P&L
```

## Why I built this

I trade futures, and I wanted to take that interest beyond a directional trade and apply it to a physical energy business.

This gave me a way to work through hedge sizing, physical revenue, futures P&L, basis risk, and risk reduction in one model.

It also helped me get more comfortable using Python for a trading and risk problem instead of only looking at charts or individual trades.

## Data

The model uses WTI Cushing spot-price data from public FRED/EIA sources and a continuous front-month WTI futures series based on Yahoo Finance ticker `CL=F`.

The saved results use public mirrors of those series:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Glossary

| Term | What I mean by it |
|---|---|
| **WTI** | West Texas Intermediate, a major U.S. crude oil benchmark. |
| **CL** | NYMEX WTI crude oil futures. One CL contract represents 1,000 barrels. |
| **Physical crude** | The actual oil the producer sells. |
| **Futures contract** | A contract tied to the future price of oil. |
| **Hedge** | A position used to reduce price risk. |
| **Short futures** | Selling futures so the position can gain if oil prices fall. |
| **Hedge ratio** | The percentage of expected production being hedged. |
| **P&L** | Profit and loss. |
| **Basis** | The price difference between two related crude prices or locations. |
| **Basis risk** | The risk that those two prices do not move together. |
| **Basis swap** | A contract used to hedge that price difference. |
| **Cushing** | The Oklahoma delivery point tied to NYMEX WTI futures. |
| **Midland** | A major Permian Basin crude pricing location. |
| **Revenue surprise** | How far actual modeled revenue ends up from the starting expectation. |
| **Hedge effectiveness** | How much the hedge reduced revenue risk. |
| **Minimum-variance hedge ratio** | The hedge size that reduced price swings the most in the historical sample. |
| **Volatility** | How much prices or revenue move around. |
| **Stress test** | A simple test of what happens under a large market move. |
| **Continuous futures series** | A price history that links multiple futures contracts together over time. |
| **ETRM** | A system used by energy companies to track trades, positions, risk, and settlements. |

## Limitations

This is a portfolio model, not a live producer hedge book.

The futures data is a continuous front-month series, so it does not track the exact contract a real producer would hold each month. A real implementation would also need contract roll dates, transaction costs, margin, production uncertainty, location and quality differences, and counterparty risk.

## Project files

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

## Run it

```bash
python -m venv .venv
pip install -r requirements.txt
python run_analysis.py
```

**Disclaimer:** Educational and portfolio use only. Not investment advice.
