# WTI Producer Hedge Simulator

I trade futures myself, so I wanted to look at the market from the other side: how would an oil producer use futures to protect the value of oil it plans to sell later?

I built a Python model around a simple example — a producer selling 100,000 barrels of crude oil per month. The model compares different hedge sizes, adds Midland/Cushing basis risk, and tests a data-driven hedge ratio.

You don't need a background in futures or physical energy trading to follow it. I explain the terms as they come up.

## 30-second version

If the producer does nothing, falling oil prices directly reduce future revenue. A hedge uses a futures position to offset part of that price move.

In the historical sample from February 2015 through July 2026, a 75% hedge reduced the variance of monthly revenue surprise by 90.3%. A 100% hedge reduced it by 96.0%.

| Hedge | CL contracts short | Revenue-surprise std. dev. | Hedge effectiveness |
|---:|---:|---:|---:|
| 0% | 0 | $711,294 | 0.0% |
| 25% | 25 | $540,295 | 42.3% |
| 50% | 50 | $373,697 | 72.4% |
| 75% | 75 | $221,653 | 90.3% |
| 100% | 100 | $142,693 | 96.0% |

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

I also tested two things that matter beyond a simple fixed hedge. First, a Midland/Cushing basis move from -$1/bbl to -$5/bbl created a $400,000 modeled shortfall on 100,000 barrels when the basis was left unhedged. Second, the historical minimum-variance hedge ratio came out to 1.016, or about 102 CL contracts after rounding.

Those are model results, not trading recommendations.

## What is a futures contract?

A futures contract is a standardized contract tied to the future price of an asset.

For this project, the asset is WTI crude oil. The NYMEX WTI futures contract trades under the ticker CL, and one CL contract represents 1,000 barrels of crude oil. The contract is physically deliverable at Cushing, Oklahoma. Most traders close or roll their positions before delivery.

So if CL is trading at $75 per barrel, one contract represents 1,000 barrels at that market price.

CME's WTI contract overview:  
https://www.cmegroup.com/education/courses/event-contracts-underlying-markets/wti-overview

## What does hedging mean?

Hedging means taking one position to reduce the risk of another.

An oil producer is already exposed to oil prices because it owns future production. Higher prices help the producer. Lower prices hurt the producer.

To reduce the downside from falling prices, the producer can short WTI futures.

```text
Physical oil:
price up   -> physical revenue rises
price down -> physical revenue falls

Short futures:
price up   -> futures position loses
price down -> futures position gains
```

The futures position is not supposed to be judged by itself. The point is what happens after the futures P&L is combined with the physical oil revenue.

## A simple example

Assume the producer expects to sell 100,000 barrels next month and WTI is $75/bbl.

If oil falls to $60 with no hedge, the producer loses $15/bbl of value:

```text
$15 × 100,000 barrels = $1,500,000
```

Now assume the producer hedges 50% of production.

That is 50,000 barrels. Since one CL contract represents 1,000 barrels, the producer shorts 50 CL contracts.

If WTI falls from $75 to $60, the short futures hedge gains $15/bbl on those 50,000 hedged barrels:

```text
$15 × 50,000 barrels = $750,000 futures gain
```

The physical oil is still worth less, but the futures gain offsets part of the drop. That is the basic idea behind the model.

## How I measure whether the hedge worked

I needed a consistent way to compare the different hedge sizes.

At the start of each month, the futures price gives a market reference for the value of the producer's expected barrels. At the end of the month, I compare that starting benchmark with the producer's physical revenue plus futures P&L.

I call the difference revenue surprise.

A smaller revenue surprise means the producer ended up closer to the starting revenue benchmark. Hedge effectiveness measures how much the hedge reduced the variance of those monthly surprises compared with staying completely unhedged.

The chart below shows the monthly difference for several hedge sizes.

![Revenue surprise](outputs/revenue_surprise_history.svg)

## Letting the data choose a hedge size

Fixed hedge percentages are easy to understand, but I also wanted to ask a different question:

> Based on how WTI spot and futures prices moved together, what hedge size would have reduced price movement the most?

That is the idea behind a minimum-variance hedge ratio.

For this sample, the estimate was 1.016. On 100,000 barrels, that works out to about 102 CL contracts after rounding.

The rounded 1.02 hedge ratio reduced monthly price-change variance by 96.6% in the sample.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

I also estimated the ratio over rolling 24-month windows. It changed over time, which is a useful reminder that spot and futures relationships are not fixed forever.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

A real company would not automatically hedge 102% of expected production just because a historical calculation says so. Production uncertainty, hedge limits, liquidity, accounting treatment, and company risk policy all matter.

## Midland, Cushing, and basis risk

Cushing, Oklahoma is the delivery point for the NYMEX WTI futures contract and a major U.S. crude storage and pipeline hub.

Midland, Texas is a major crude pricing point in the Permian Basin.

Those prices are connected, but they are not always the same. Transportation, pipeline capacity, storage, and local supply and demand can cause one location to trade above or below another.

The difference between the two prices is called basis.

```text
Midland basis = Midland price - Cushing price
```

If Midland is $72 and Cushing is $75, the basis is -$3/bbl.

A producer selling crude in Midland can therefore hedge the main WTI price move with Cushing-based futures and still be exposed to a change in the Midland/Cushing price difference. That is basis risk.

CME background on U.S. crude grades and Midland/Cushing pricing:  
https://www.cmegroup.com/markets/energy/crude-oil/north-american-grades-futures-and-options.html

## Basis-risk example

I used a simple stress test.

The producer expects Midland to trade $1 below Cushing. Instead, the difference widens to $5 below Cushing.

That is a $4/bbl move against the producer:

```text
$4 × 100,000 barrels = $400,000
```

With no basis hedge, the modeled shortfall is $400,000. With a 50% basis hedge, it falls to about $200,000. In the simplified model, a full basis hedge offsets the basis move.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

This section is a scenario test, not a historical Midland cash-price backtest.

A basis hedge is separate from the main WTI futures hedge. The WTI hedge manages the overall oil-price move. A basis instrument manages the difference between locations.

## The math

Once the setup is clear, the core calculations are simple.

```text
Hedged barrels =
monthly production × hedge ratio

CL contracts =
hedged barrels / 1,000

Futures P&L =
(entry futures price - exit futures price) × hedged barrels

Total revenue =
physical oil revenue + futures P&L
```

The project then compares that total revenue across hedge sizes and measures how much uncertainty remains.

## Why I built it

I spend a lot of time trading and studying futures, but most of that experience starts with a market view: where price may go, where I am wrong, and how much risk I want to take.

This project made me work through a different question. If a company already has a real physical exposure, how can the futures market be used to manage that exposure instead of simply taking a directional trade?

That is what I wanted to learn from this project.

## Data and model limits

The project uses WTI Cushing spot prices from public FRED/EIA sources and a continuous front-month WTI futures series based on Yahoo Finance ticker `CL=F`.

The saved results use public copies of those series:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

The continuous futures series is useful for this project, but it is not the same as following the exact futures contract a producer would trade and roll each month.

A real hedge program would also have to handle specific contract months, roll timing, transaction costs, margin, liquidity, production changes, quality and location differences, accounting treatment, credit risk, and internal hedge limits.

<details>
<summary><strong>Glossary</strong></summary>

| Term | Plain-English meaning |
|---|---|
| WTI | West Texas Intermediate, a major U.S. crude-oil benchmark. |
| CL | The ticker for NYMEX WTI crude-oil futures. One contract represents 1,000 barrels. |
| Physical crude | The actual oil the producer owns and sells. |
| Spot price | The current cash-market price at a specific location. |
| Futures contract | A standardized contract tied to the price of an asset for a future delivery month. |
| Long | A position that generally benefits when price rises. |
| Short | A position that generally benefits when price falls. |
| Hedge | A position used to reduce another risk. |
| Hedge ratio | The percentage of expected production being hedged. |
| P&L | Profit and loss. |
| Basis | The price difference between two related crude prices or locations. |
| Basis risk | The risk that those two prices move differently. |
| Basis hedge | A hedge aimed at reducing the risk of that price difference. |
| Cushing | The Oklahoma delivery and pricing hub tied to NYMEX WTI futures. |
| Midland | A major crude-pricing location in the Permian Basin. |
| Revenue surprise | The difference between the starting revenue benchmark and modeled realized revenue. |
| Hedge effectiveness | How much the hedge reduced the variance of revenue surprise. |
| Minimum-variance hedge ratio | The historical hedge ratio that minimized residual price-change variance in the model. |
| Volatility | How much a price or revenue series moves around. |
| Stress test | A test of what happens during a large or unfavorable market move. |
| Continuous futures series | A price history created by linking multiple futures contracts over time. |
| ETRM | Energy Trading and Risk Management software used to track trades, positions, risk, and settlements. |

</details>

## Run it

```bash
python -m venv .venv
pip install -r requirements.txt
python run_analysis.py
```

Project files are organized into `src/` for the model logic, `notebooks/` for the walkthrough, and `outputs/` for the saved results and charts.

Educational and portfolio use only. Not investment advice.
