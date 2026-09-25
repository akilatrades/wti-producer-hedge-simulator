# WTI Producer Hedge Simulator

A Python project that models how a crude oil producer can use WTI futures to reduce price risk on future production.

The example assumes the producer expects to sell 100,000 barrels of crude oil each month. Because that oil will be sold later, the final selling price is still unknown. If oil prices fall before the sale, revenue falls with them.

This project looks at three questions:

1. How much can a futures hedge reduce that price risk?
2. What happens when Midland and Cushing prices move differently?
3. Can historical spot and futures data help estimate a better hedge size?

No background in futures or physical energy trading is required. The terms are explained as they come up.

## 30-second summary

A producer that expects to sell oil in the future is exposed to falling prices. Short WTI futures can offset part of that risk.

Using historical data from February 2015 through July 2026, the model compares several hedge levels:

| Hedge ratio | CL contracts short | Revenue-surprise std. dev. | Hedge effectiveness |
|---:|---:|---:|---:|
| 0% | 0 | $711,294 | 0.0% |
| 25% | 25 | $540,295 | 42.3% |
| 50% | 50 | $373,697 | 72.4% |
| 75% | 75 | $221,653 | 90.3% |
| 100% | 100 | $142,693 | 96.0% |

In this sample, a 75% hedge reduces the variance of monthly revenue surprise by 90.3%. A 100% hedge reduces it by 96.0%.

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

The model also tests Midland/Cushing basis risk and estimates a minimum-variance hedge ratio from historical spot and futures price changes.

## What is a futures contract?

A futures contract is a standardized contract tied to the price of an asset for a future delivery month.

For this project, the asset is WTI crude oil.

WTI crude oil futures trade under the ticker CL on NYMEX/CME. One CL contract represents 1,000 barrels of crude oil.

If CL is trading at $75 per barrel, one contract represents:

```text
1,000 barrels × $75 = $75,000 of crude oil value
```

Futures are margined products, so a trader does not pay the full $75,000 to enter the position. Instead, collateral is posted to support the trade.

WTI futures are physically deliverable at Cushing, Oklahoma. Most financial traders close or roll their positions before delivery.

CME contract overview:  
https://www.cmegroup.com/education/courses/event-contracts-underlying-markets/wti-overview

## What does hedging mean?

Hedging means taking one position to reduce the risk of another.

An oil producer is already exposed to oil prices because it owns future production.

Higher oil prices help the producer. Lower oil prices hurt the producer.

To reduce the downside from falling prices, the producer can short WTI futures.

```text
Physical oil:
price up   -> physical revenue rises
price down -> physical revenue falls

Short futures:
price up   -> futures position loses
price down -> futures position gains
```

The futures position is not judged by itself. The important result is what happens after futures P&L is combined with physical oil revenue.

## A simple hedge example

Assume the producer expects to sell 100,000 barrels next month and WTI is trading at $75 per barrel.

If oil falls to $60 with no hedge, the producer loses $15 per barrel of value:

```text
$15 × 100,000 barrels = $1,500,000
```

Now assume the producer hedges 50% of production.

That equals 50,000 barrels. Since one CL contract represents 1,000 barrels, the producer shorts 50 CL contracts.

If WTI falls from $75 to $60, the short futures position gains $15 per barrel on those 50,000 hedged barrels:

```text
$15 × 50,000 barrels = $750,000 futures gain
```

The physical oil is still worth less, but the futures gain offsets part of the decline.

That is the basic idea behind the model.

## How the model compares hedge sizes

The model tests 0%, 25%, 50%, 75%, and 100% hedge ratios.

A 0% hedge means the producer stays fully exposed to the market price.

A 50% hedge means half of expected production is covered with futures.

A 100% hedge means the full expected production amount is matched with futures.

For each hedge level, the model combines:

```text
Physical oil revenue
+
Futures profit or loss
=
Total modeled revenue
```

The result is then compared with the revenue level implied by the futures price at the start of the month.

The difference is called revenue surprise.

A smaller revenue surprise means realized modeled revenue stayed closer to that starting benchmark.

![Revenue surprise](outputs/revenue_surprise_history.svg)

Hedge effectiveness measures how much the hedge reduces the variance of those revenue surprises compared with staying unhedged.

In plain English, higher hedge effectiveness means more stable revenue in the model.

## Using the data to estimate hedge size

Fixed hedge percentages are easy to compare, but the project also estimates a minimum-variance hedge ratio.

The idea is simple:

> Based on how WTI spot and futures prices moved together, what hedge size would have reduced price movement the most?

For this sample, the estimated ratio is 1.016.

For 100,000 barrels of production, that equals about 102 CL contracts after rounding.

The rounded 1.02 hedge ratio reduces monthly price-change variance by 96.6% in the historical sample.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

The ratio is also calculated over rolling 24-month windows.

That result changes over time, which shows that the relationship between spot and futures prices is not constant.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

The 102-contract result is a statistical estimate, not a recommendation to hedge more than expected production. A real company would also consider production uncertainty, hedge limits, liquidity, accounting treatment, and internal risk policy.

## What are Cushing and Midland?

Cushing, Oklahoma is the delivery point for the NYMEX WTI futures contract and a major U.S. crude storage and pipeline hub.

Midland, Texas is a major crude pricing point in the Permian Basin.

Both locations are important to U.S. crude trading, but their prices do not always match.

Transportation costs, pipeline capacity, storage, and local supply and demand can cause one location to trade above or below another.

That price difference is called basis.

```text
Midland basis = Midland price - Cushing price
```

If Midland is $72 and Cushing is $75:

```text
$72 - $75 = -$3/bbl
```

Midland is trading $3 below Cushing.

CME background on U.S. crude grades:  
https://www.cmegroup.com/markets/energy/crude-oil/north-american-grades-futures-and-options.html

## What is basis risk?

A producer can hedge the overall WTI price move and still have basis risk.

Suppose the producer sells crude in Midland but hedges with WTI futures tied to Cushing.

The Cushing-based futures hedge may reduce the main oil-price risk, but Midland can still become cheaper relative to Cushing.

That remaining location-price difference is basis risk.

The project uses a simple stress test.

The producer expects Midland to trade $1 below Cushing. Instead, the difference widens to $5 below Cushing.

That is a $4 per barrel move against the producer:

```text
$4 × 100,000 barrels = $400,000
```

With no basis hedge, the modeled shortfall is $400,000.

With a 50% basis hedge, the shortfall falls to about $200,000.

In the simplified model, a full basis hedge offsets the basis move.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

This is a stress-test example, not a historical Midland cash-price backtest.

A basis hedge is separate from the main WTI futures hedge. The futures hedge manages the overall crude-price move. A basis instrument manages the price difference between locations.

## Core math

Once the setup is clear, the calculations are straightforward.

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

The model then compares total revenue across hedge sizes and measures how much uncertainty remains.

## Why I built this

I trade futures myself, so most of my experience starts with a market view: where price may go, where the trade is wrong, and how much risk to take.

This project looks at futures from a different angle.

For a producer, futures are not only a way to take a market view. They can also protect the economics of a physical business.

Building the model helped connect futures trading with physical energy markets, hedge sizing, basis risk, and Python-based risk analysis.

## Data and limitations

The project uses WTI Cushing spot prices from public FRED/EIA sources and a continuous front-month WTI futures series based on Yahoo Finance ticker `CL=F`.

The saved results use public copies of those series:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

A continuous futures series links several futures contracts together to create one long price history. That is useful for this project, but it is not the same as following the exact contract a producer would trade and roll each month.

A live hedge program would also need specific contract months, roll timing, transaction costs, margin, liquidity, production changes, quality and location differences, accounting treatment, credit risk, and internal hedge limits.

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
