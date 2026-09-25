# WTI Producer Hedge Simulator

I built this project because I wanted to connect the way I think about futures with a real energy-market problem.

The example is a crude producer selling 100,000 barrels per month. The producer knows the oil will be sold later, so there is price risk between now and then. I wanted to see how much of that risk could be reduced with WTI futures, and what kinds of risk would still remain after the hedge was in place.

## Hedge comparison

I started with a straightforward comparison of five hedge levels: 0%, 25%, 50%, 75%, and 100% of expected production.

For each hedge level, I combined the producer's physical oil revenue with the gain or loss on the futures position. I then compared how much total monthly revenue moved around.

The historical sample runs from February 2015 through July 2026.

| Hedge ratio | CL contracts short | Revenue volatility | Hedge effectiveness |
|---:|---:|---:|---:|
| 0% | 0 | $711,294 | 0.0% |
| 25% | 25 | $540,295 | 42.3% |
| 50% | 50 | $373,697 | 72.4% |
| 75% | 75 | $221,653 | 90.3% |
| 100% | 100 | $142,693 | 96.0% |

In this sample, the 75% hedge reduced modeled revenue risk by about 90%. The 100% hedge reduced it by about 96%.

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

![Revenue surprise](outputs/revenue_surprise_history.svg)

## Hedge sizing from the data

After comparing fixed hedge levels, I wanted to see what the historical relationship between spot and futures prices would suggest.

I estimated a minimum-variance hedge ratio using WTI spot and futures price changes. The result was 1.016, which works out to roughly 102 CL contracts for 100,000 barrels of production.

That hedge size reduced monthly price-change variance by about 96.6% in the sample.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

I also calculated the same hedge ratio over rolling 24-month windows. The result moved over time, which is useful because the relationship between spot and futures prices is not perfectly stable.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

I would not use 102 contracts as a real-world recommendation by itself. A producer would also have to consider expected production, company hedge limits, liquidity, accounting treatment, and internal risk policy.

## Midland and Cushing basis risk

The next part of the project looks at basis risk.

A producer may sell crude in Midland while hedging with WTI futures tied to Cushing. Those prices are related, but they do not always move by the same amount.

In this project:

```text
Midland basis = Midland price - Cushing price
```

I used a simple stress test to show what happens if that difference moves against the producer.

If the producer expects Midland to trade $1 below Cushing, but the actual difference widens to $5 below Cushing, the producer is $4 per barrel worse off than expected. On 100,000 barrels, that is a $400,000 difference.

```text
$4 × 100,000 barrels = $400,000
```

With no basis hedge, the full $400,000 remains. A 50% basis hedge cuts that amount to about $200,000. In the simplified model, a full basis hedge offsets the move.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

This section is a scenario test, not a historical Midland cash-price backtest.

For background:

- [EIA: WTI Cushing spot-market definition](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
- [SEC/EOG disclosure: Midland Differential basis swaps](https://www.sec.gov/Archives/edgar/data/821189/000082118919000020/a2019033110-q.htm)

## How the hedge works

A crude producer is naturally exposed to falling oil prices because the producer owns future production.

If the producer shorts WTI futures and oil prices fall, the physical oil is worth less, but the short futures position gains. If oil prices rise, the physical oil is worth more, while the futures hedge loses.

The purpose of the hedge is not to make money from the futures trade on its own. It is to make the producer's overall revenue less sensitive to oil-price moves.

The basic math is:

```text
Hedged barrels = monthly production × hedge ratio

CL contracts = hedged barrels / 1,000

Futures P&L =
(entry futures price - exit futures price) × hedged barrels

Total revenue =
physical oil revenue + futures P&L
```

## Why I built it

I trade futures, and I wanted to use that experience in a way that was closer to how futures are used in the energy industry.

This project gave me a reason to work through physical revenue, hedge sizing, futures P&L, basis risk, and risk reduction in the same model. It also gave me more experience using Python for a market problem instead of only using charts and discretionary trade ideas.

## Data

The model uses WTI Cushing spot-price data from public FRED/EIA sources and a continuous front-month WTI futures series based on Yahoo Finance ticker `CL=F`.

The saved results use public copies of those series:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Glossary

| Term | Meaning |
|---|---|
| WTI | West Texas Intermediate, a major U.S. crude oil benchmark. |
| CL | NYMEX WTI crude oil futures. One CL contract represents 1,000 barrels. |
| Physical crude | The actual oil the producer sells. |
| Futures contract | A contract tied to the future price of oil. |
| Hedge | A position used to reduce price risk. |
| Short futures | Selling futures so the position can gain if oil prices fall. |
| Hedge ratio | The percentage of expected production being hedged. |
| P&L | Profit and loss. |
| Basis | The price difference between two related crude prices or locations. |
| Basis risk | The risk that those two prices do not move together. |
| Basis swap | A contract used to hedge that price difference. |
| Cushing | The Oklahoma delivery point tied to NYMEX WTI futures. |
| Midland | A major Permian Basin crude pricing location. |
| Revenue surprise | The difference between expected revenue and modeled revenue. |
| Hedge effectiveness | How much the hedge reduced revenue risk. |
| Minimum-variance hedge ratio | The hedge size that reduced price swings the most in the historical sample. |
| Volatility | How much prices or revenue move around. |
| Stress test | A test of what happens under a large market move. |
| Continuous futures series | A price history that links several futures contracts together over time. |
| ETRM | A system used by energy companies to track trades, positions, risk, and settlements. |

## Limitations

This is a portfolio model, not a live producer hedge book.

The futures data is a continuous front-month series, so it does not track the exact contract a producer would hold each month. A real implementation would also need contract roll dates, transaction costs, margin, production uncertainty, location and quality differences, and counterparty risk.

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
