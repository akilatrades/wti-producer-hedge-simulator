# WTI Producer Hedge Simulator

I trade futures, and I wanted to understand how the same market can be used by an oil producer for something very different: protecting revenue.

This project uses a simple example. The producer expects to sell 100,000 barrels of crude oil each month. The oil will be sold later, so the price can move before the producer gets paid. If oil falls, revenue falls with it.

The question I wanted to answer was:

> How much of that price risk can be reduced with WTI futures?

I also wanted to see what a futures hedge does not protect against.

## Starting with a simple hedge

A hedge is just a position used to reduce another risk.

In this case, the producer owns future oil production. That means the producer benefits from higher oil prices and gets hurt by lower prices.

To offset some of that downside, the producer can short WTI futures.

If oil falls, the physical oil is worth less, but the short futures position gains. If oil rises, the physical oil is worth more, while the futures hedge loses.

The goal is not for the futures trade to make money by itself. The goal is to make the producer's total revenue more stable.

I tested five hedge levels: 0%, 25%, 50%, 75%, and 100% of expected production.

The historical sample runs from February 2015 through July 2026.

| Hedge ratio | CL contracts short | Revenue volatility | Hedge effectiveness |
|---:|---:|---:|---:|
| 0% | 0 | $711,294 | 0.0% |
| 25% | 25 | $540,295 | 42.3% |
| 50% | 50 | $373,697 | 72.4% |
| 75% | 75 | $221,653 | 90.3% |
| 100% | 100 | $142,693 | 96.0% |

The result was straightforward. In this sample, the 75% hedge reduced modeled revenue risk by about 90%. The 100% hedge reduced it by about 96%.

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

The chart below shows the same idea month by month. The hedged revenue moves around less than the unhedged revenue.

![Revenue surprise](outputs/revenue_surprise_history.svg)

## Letting the data choose the hedge size

After testing fixed hedge levels, I asked a different question:

> Based on the way WTI spot and futures prices moved together, what hedge size would have reduced price movement the most?

That is what the minimum-variance hedge ratio is trying to answer.

The estimate for this sample was 1.016. For 100,000 barrels of production, that is about 102 CL contracts.

That hedge size reduced monthly price-change variance by about 96.6% in the sample.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

I also recalculated the hedge ratio using rolling 24-month windows. It changed over time, which is important. The relationship between spot and futures prices is not fixed forever.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

I would not treat 102 contracts as a recommendation to hedge more than production. In a real business, hedge size would also depend on expected production, company limits, liquidity, accounting treatment, and risk policy.

## Midland and Cushing do not always move together

A WTI futures hedge can reduce the main oil-price risk and still leave another problem.

A producer might sell crude in Midland, Texas, while the WTI futures contract is tied to Cushing, Oklahoma. Midland and Cushing prices are related, but they are not always equal.

The difference between them is called basis.

```text
Midland basis = Midland price - Cushing price
```

I used a simple example.

The producer expects Midland to trade $1 below Cushing. Later, Midland is trading $5 below Cushing instead.

The producer is now $4 per barrel worse off than expected.

On 100,000 barrels:

```text
$4 × 100,000 barrels = $400,000
```

With no basis hedge, that $400,000 difference remains. With a 50% basis hedge, the modeled difference falls to about $200,000. In this simplified example, a full basis hedge offsets the move.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

This is a stress-test example. It is not a historical Midland cash-price backtest.

For background on the pricing and the type of hedge used here:

- [EIA: WTI Cushing spot-market definition](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
- [SEC/EOG disclosure: Midland Differential basis swaps](https://www.sec.gov/Archives/edgar/data/821189/000082118919000020/a2019033110-q.htm)

## The math behind the model

One CL futures contract represents 1,000 barrels of WTI crude.

If the producer wants to hedge part of its monthly production:

```text
Hedged barrels = monthly production × hedge ratio

CL contracts = hedged barrels / 1,000
```

Because the producer is short futures, the futures P&L is:

```text
Futures P&L =
(entry futures price - exit futures price) × hedged barrels
```

The model then combines that with the physical oil revenue:

```text
Total revenue =
physical oil revenue + futures P&L
```

That is the core of the project. The rest is measuring how much risk is left after the hedge.

## Why I built this

I trade futures myself, so I am used to thinking about entries, exits, price direction, and risk on a trade.

I wanted to look at futures from the other side.

For a producer, futures are not only a way to take a market view. They can also be used to protect the economics of a physical business.

Building this helped me connect futures trading with physical energy markets, hedge sizing, basis risk, and Python-based risk analysis.

## Data

The project uses WTI Cushing spot-price data from public FRED/EIA sources and a continuous front-month WTI futures series based on Yahoo Finance ticker `CL=F`.

The saved results use public copies of those series:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Glossary

| Term | Plain-English meaning |
|---|---|
| WTI | West Texas Intermediate, one of the main U.S. crude-oil price benchmarks. |
| CL | The ticker for NYMEX WTI crude-oil futures. One contract represents 1,000 barrels. |
| Physical crude | The actual oil the producer owns and sells. |
| Futures contract | A contract whose value moves with the future price of oil. |
| Hedge | A position used to reduce another risk. |
| Short futures | Selling futures so the position can gain when oil prices fall. |
| Hedge ratio | The percentage of expected production being hedged. |
| P&L | Profit and loss. |
| Basis | The price difference between two related crude prices or locations. |
| Basis risk | The risk that those two prices move differently. |
| Basis swap | A contract used to hedge that price difference. |
| Cushing | The Oklahoma delivery point tied to NYMEX WTI futures. |
| Midland | A major crude-pricing location in the Permian Basin. |
| Revenue surprise | The difference between expected revenue and modeled revenue. |
| Hedge effectiveness | How much the hedge reduced revenue risk. |
| Minimum-variance hedge ratio | The hedge size that reduced price movement the most in the historical sample. |
| Volatility | How much a price or revenue number moves around. |
| Stress test | A simple test of what happens during a large or unfavorable market move. |
| Continuous futures series | A price history made by linking futures contracts together over time. |
| ETRM | An Energy Trading and Risk Management system used to track trades, positions, risk, and settlements. |

## Limits of the project

This is a portfolio model, not a live producer hedge book.

The futures data is a continuous front-month series, so it does not follow the exact contract a producer would trade and roll each month.

A real hedge program would also have to deal with contract rolls, transaction costs, margin, production changes, location and quality differences, liquidity, and counterparty risk.

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

Educational and portfolio use only. Not investment advice.
