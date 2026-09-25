# WTI Producer Hedge Simulator

I trade futures, and I built this project because I wanted to understand how the same market can be used by an oil producer to protect revenue.

You don't need a background in futures or physical energy trading to follow this project. I explain the concepts as they come up.

The example is a crude oil producer that expects to sell 100,000 barrels of oil each month.

The basic problem is simple: the producer has oil that will be sold later, but the price can change before the sale happens. If oil prices fall, the producer earns less money.

This project asks:

> Can WTI futures reduce that risk, and what risk is still left after the hedge?

---

## First: what is a futures contract?

A futures contract is an agreement tied to the price of something that will be bought or sold in the future.

In this project, that "something" is crude oil.

WTI crude oil futures trade under the ticker **CL** on NYMEX/CME. One CL contract represents 1,000 barrels of crude oil.

So if WTI futures are trading at $75 per barrel, one contract represents:

```text
1,000 barrels × $75 = $75,000 of crude oil value
```

A trader does not need to pay $75,000 in cash to enter the contract. Futures are margined products, so the trader posts collateral instead.

WTI futures are also physically deliverable. If a position is held into the delivery process, the contract can result in actual crude oil being delivered at Cushing, Oklahoma. Most financial traders close or roll their positions before that point.

For this project, I am using the futures price as a hedge for the producer's future oil revenue.

[CME: WTI Crude Oil futures overview](https://www.cmegroup.com/education/courses/event-contracts-underlying-markets/wti-overview)

---

## What does "hedging" mean?

Hedging just means taking one position to reduce the risk of another position.

The producer already has exposure to oil prices because it expects to sell oil in the future.

If oil prices go up, that is good for the producer.

If oil prices go down, that is bad for the producer.

In trading terms, the producer is already naturally "long" oil because the value of its future production rises and falls with oil prices.

To protect against a price drop, the producer can take the opposite position in the futures market and short WTI futures.

That creates two sides:

```text
Physical oil:
Higher oil price = better
Lower oil price = worse

Short futures hedge:
Higher oil price = loss
Lower oil price = gain
```

The two positions partially offset each other.

The producer is not trying to make money from the futures position by itself. The goal is to make total revenue more stable.

---

## A simple example

Assume the producer expects to sell 100,000 barrels next month.

WTI is currently $75 per barrel.

Without any hedge, the producer is fully exposed to whatever oil price exists next month.

If oil falls to $60, the value of the production falls by $15 per barrel.

```text
$15 drop × 100,000 barrels = $1,500,000 less physical revenue
```

Now assume the producer hedged 50% of production.

50% of 100,000 barrels is 50,000 barrels.

Because one CL contract represents 1,000 barrels:

```text
50,000 hedged barrels / 1,000 = 50 CL contracts
```

The producer would short 50 futures contracts.

If WTI falls from $75 to $60, the short futures position gains $15 per barrel on those 50,000 hedged barrels:

```text
$15 × 50,000 barrels = $750,000 futures gain
```

The producer still loses money on the physical oil because the market price fell, but the futures gain offsets part of that loss.

That is the basic idea behind the whole project.

---

## What I tested

I tested five different hedge sizes:

0%, 25%, 50%, 75%, and 100% of expected monthly production.

A 0% hedge means the producer does nothing in the futures market.

A 50% hedge means half of expected production is protected with futures.

A 100% hedge means the full expected production amount is matched with futures.

For each hedge size, I combine physical oil revenue with futures profit or loss and then measure how much the total revenue moves around.

The historical sample runs from February 2015 through July 2026.

| Hedge ratio | CL contracts short | Revenue volatility | Hedge effectiveness |
|---:|---:|---:|---:|
| 0% | 0 | $711,294 | 0.0% |
| 25% | 25 | $540,295 | 42.3% |
| 50% | 50 | $373,697 | 72.4% |
| 75% | 75 | $221,653 | 90.3% |
| 100% | 100 | $142,693 | 96.0% |

In this sample, the 75% hedge reduced modeled revenue risk by about 90%.

The 100% hedge reduced it by about 96%.

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

The chart below shows the same idea over time. The hedged revenue moves around less than the unhedged revenue.

![Revenue surprise](outputs/revenue_surprise_history.svg)

---

## What does "hedge effectiveness" mean?

I needed a way to measure whether the hedge actually helped.

The project compares how much monthly revenue moves away from the amount the producer could roughly expect based on the futures price at the start of the month.

I call that difference "revenue surprise."

If the result is close to zero, revenue stayed close to the starting expectation.

If the result is very positive or very negative, revenue moved farther away from that expectation.

Hedge effectiveness measures how much the hedge reduced the variance of those revenue surprises compared with having no hedge at all.

In plain English:

> Higher hedge effectiveness means the hedge made revenue more predictable.

---

## Letting the data choose a hedge size

The fixed hedge tests are easy to understand, but I also wanted to know if the historical data suggested a better hedge size.

This is where the minimum-variance hedge ratio comes in.

The name sounds more complicated than the idea.

I am asking:

> Based on how WTI spot prices and WTI futures prices moved together, what hedge size would have reduced price movement the most?

The calculation is:

```text
Minimum-variance hedge ratio =
Covariance of spot and futures changes
divided by
Variance of futures changes
```

You do not need the formula to understand the result.

For this sample, the estimated hedge ratio was 1.016.

For 100,000 barrels of production, that works out to roughly 102 CL contracts.

The modeled result reduced monthly price-change variance by about 96.6%.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

I also recalculated that hedge ratio using rolling 24-month windows.

Why?

Because markets change.

A hedge relationship that worked one year may not work exactly the same way a few years later.

![Rolling minimum-variance hedge ratio](outputs/rolling_min_variance_ratio.svg)

I would not treat 102 contracts as a real-world recommendation to hedge more than production. A real company would also consider expected production, company limits, liquidity, accounting rules, and internal risk policy.

---

## What are Midland and Cushing?

This part confused me at first too, because "WTI" can sound like one single oil price.

It is not that simple.

Crude oil is produced and traded in different locations. The location matters because oil has to be stored and transported.

### Cushing, Oklahoma

Cushing is a major U.S. crude oil storage and pipeline hub.

It is also the delivery point tied to the NYMEX WTI futures contract.

That makes Cushing very important to WTI pricing.

The WTI futures price is closely connected to the value of crude delivered into Cushing.

[EIA: Cushing is the delivery and pricing point for WTI](https://www.eia.gov/state/analysis.php?sid=OK)

### Midland, Texas

Midland is in the Permian Basin area of West Texas, one of the largest oil-producing regions in the United States.

WTI Midland reflects crude pricing in that production region.

Oil produced around Midland may eventually move by pipeline toward other markets, including the Gulf Coast.

[EIA: WTI Midland and Permian crude pricing](https://www.eia.gov/todayinenergy/detail.php?id=38832)

---

## Why can Midland and Cushing have different prices?

Because location has value.

Imagine oil is worth $75 in Cushing but only $72 in Midland.

The crude itself may be similar, but the Midland barrel has to be transported somewhere else. Pipeline capacity, storage, local supply, demand, and transportation problems can all affect the local price.

The difference between the two prices is called basis.

In this project:

```text
Midland basis = Midland price - Cushing price
```

If Midland is $72 and Cushing is $75:

```text
$72 - $75 = -$3 basis
```

That means Midland is trading $3 below Cushing.

---

## What is basis risk?

A producer can hedge WTI price risk and still have basis risk.

That is important.

Suppose the producer sells oil in Midland but hedges using WTI futures tied to Cushing.

The futures hedge may work perfectly against the Cushing price.

But if Midland gets cheaper compared with Cushing, the producer may still receive less money for the physical oil.

That remaining difference is basis risk.

I used a simple stress test.

The producer expects Midland to trade $1 below Cushing.

Later, Midland is trading $5 below Cushing.

The basis moved from -$1 to -$5.

That is a $4 per barrel move against the producer.

On 100,000 barrels:

```text
$4 × 100,000 barrels = $400,000
```

So even if the main WTI price was hedged, the producer could still be $400,000 worse off because the local Midland price weakened relative to Cushing.

![Midland-Cushing basis risk stress test](outputs/basis_risk_stress.svg)

---

## What is a basis hedge?

A basis hedge is separate from the main WTI futures hedge.

The WTI futures hedge protects against the overall move in crude prices.

The basis hedge protects against the difference between two prices.

In this project, I use an illustrative Midland/Cushing basis swap.

If the producer hedges 50% of the basis exposure, the $400,000 modeled basis shortfall falls to about $200,000.

If the producer fully hedges the basis in this simplified example, the basis move is offset.

This section is a scenario test, not a historical Midland cash-price backtest.

For an example of producers using Midland differential swaps:

[SEC/EOG disclosure: Midland Differential basis swaps](https://www.sec.gov/Archives/edgar/data/821189/000082118919000020/a2019033110-q.htm)

---

## The math behind the model

Once the basic ideas are clear, the math is pretty simple.

### Step 1: decide how many barrels to hedge

```text
Hedged barrels =
monthly production × hedge ratio
```

Example:

```text
100,000 barrels × 75% = 75,000 hedged barrels
```

### Step 2: convert barrels into CL contracts

One CL contract represents 1,000 barrels.

```text
CL contracts =
hedged barrels / 1,000
```

Example:

```text
75,000 / 1,000 = 75 CL contracts
```

### Step 3: calculate futures profit or loss

Because the producer is short futures:

```text
Futures P&L =
(entry futures price - exit futures price)
× hedged barrels
```

If the futures price falls, that number is positive.

If the futures price rises, that number is negative.

### Step 4: add futures P&L to physical revenue

```text
Total revenue =
physical oil revenue + futures P&L
```

Then I compare that result across the different hedge sizes.

---

## Why I built this

I trade futures myself, so I am used to thinking about entries, exits, price direction, and risk on an individual trade.

I wanted to understand the other side of the market.

For an oil producer, futures are not only a tool for betting on whether oil will go up or down. They can be used to protect the economics of an actual physical business.

Building this project helped me connect futures trading with physical energy markets, hedge sizing, basis risk, and Python-based risk analysis.

---

## Data

The project uses two main price series.

The first is WTI Cushing spot price data from public FRED/EIA sources.

The second is a continuous front-month WTI futures series based on Yahoo Finance ticker `CL=F`.

The saved results use public copies of those series:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

---

## Glossary

| Term | Plain-English meaning |
|---|---|
| WTI | West Texas Intermediate, one of the main U.S. crude-oil price benchmarks. |
| CL | The ticker for NYMEX WTI crude-oil futures. One contract represents 1,000 barrels. |
| Physical crude | The actual oil the producer owns and sells. |
| Spot price | The current cash-market price of the oil. |
| Futures contract | A standardized contract tied to the price of oil for a future delivery month. |
| Long | A position that generally benefits when price rises. |
| Short | A position that generally benefits when price falls. |
| Hedge | A position used to reduce another risk. |
| Hedge ratio | The percentage of expected production being hedged. |
| P&L | Profit and loss. |
| Basis | The price difference between two related crude prices or locations. |
| Basis risk | The risk that those two prices move differently. |
| Basis swap | A contract used to hedge the price difference between two locations or benchmarks. |
| Cushing | The Oklahoma storage and delivery hub tied to NYMEX WTI futures. |
| Midland | A major crude-pricing location in the Permian Basin of West Texas. |
| Revenue surprise | The difference between expected revenue and the revenue produced by the model. |
| Hedge effectiveness | How much the hedge reduced revenue risk. |
| Minimum-variance hedge ratio | The hedge size that reduced price movement the most in the historical sample. |
| Volatility | How much a price or revenue number moves around. |
| Stress test | A test of what happens during a large or unfavorable market move. |
| Continuous futures series | A price history made by linking several futures contracts together over time. |
| ETRM | An Energy Trading and Risk Management system used to track trades, positions, risk, and settlements. |

---

## Limits of the project

This is a portfolio model, not a live producer hedge book.

The futures data is a continuous front-month series. That means it links multiple futures contracts together to create one long price history.

A real producer would trade specific monthly contracts and manage when those contracts expire or roll forward.

A live hedge program would also have to deal with transaction costs, margin, liquidity, production changes, location and quality differences, accounting treatment, credit risk, and company hedge limits.

---

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

## Run the project

```bash
python -m venv .venv
pip install -r requirements.txt
python run_analysis.py
```

Educational and portfolio use only. Not investment advice.
