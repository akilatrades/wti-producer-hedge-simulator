# Module 2 — WTI Futures Term Structure

This module studies the **shape of the WTI futures curve**.

If you are completely new to commodity markets, start here. You do not need to know what backwardation, contango, or calendar spreads mean before reading this guide.

## The entire module in one sentence

We line up the prices of four WTI futures contracts, measure the differences between them, and use those differences to describe whether the market is pricing nearby oil above or below oil delivered several months later.

## Why a commodity trader cares

A crude-oil trader does not look only at one WTI price.

There are many WTI futures contracts, each tied to a different delivery month. Those prices together form the **futures curve**.

The shape of that curve contains information about how the market is pricing oil across time. It can also matter to producers, refiners, storage operators, physical traders, and hedgers because the contract chosen for a hedge may trade differently from another delivery month.

This module does **not** claim that curve shape alone predicts the next WTI price move. It is a market-structure tool that can later be combined with inventories, production, refinery demand, volatility, and other fundamentals.

---

## Step 1 — Understand the four prices

The EIA historical dataset labels the first four WTI futures contracts as:

- **Contract 1 (C1):** the nearest delivery contract in the EIA series.
- **Contract 2 (C2):** the next delivery month after C1.
- **Contract 3 (C3):** the next delivery month after C2.
- **Contract 4 (C4):** the next delivery month after C3.

Imagine the prices are:

```text
C1 = $80
C2 = $79
C3 = $78
C4 = $77
```

Nearby oil is priced higher than oil delivered later.

Now imagine:

```text
C1 = $70
C2 = $71
C3 = $72
C4 = $73
```

Nearby oil is priced lower than oil delivered later.

Those are two very different curve shapes.

---

## Step 2 — Calculate calendar spreads

A **calendar spread** is just one delivery-month price minus another delivery-month price.

This module calculates:

```text
C1-C2 spread = Contract 1 price - Contract 2 price
C1-C3 spread = Contract 1 price - Contract 3 price
C1-C4 spread = Contract 1 price - Contract 4 price
```

Example:

```text
C1 = $80
C4 = $77

C1-C4 = $80 - $77 = +$3/bbl
```

The positive number tells us the near contract is more expensive than Contract 4.

Another example:

```text
C1 = $70
C4 = $73

C1-C4 = $70 - $73 = -$3/bbl
```

The negative number tells us Contract 4 is more expensive than the near contract.

---

## Step 3 — Label the curve

We use the C1-C4 spread as a simple curve-shape indicator.

### Backwardation

If C1 is meaningfully above C4, the curve is labeled **backwardation**.

Example:

```text
C1 = $80
C4 = $77
C1-C4 = +$3
```

The front of the curve is higher than the later part.

Backwardation is often associated with a market placing more value on prompt barrels than future barrels, but the curve should not be treated as proof of one specific supply-and-demand story by itself.

### Contango

If C1 is meaningfully below C4, the curve is labeled **contango**.

Example:

```text
C1 = $70
C4 = $73
C1-C4 = -$3
```

Later delivery is priced above nearby delivery.

Contango can be consistent with storage/carry economics or a market with less pressure for immediate barrels, but again, the curve alone does not prove the cause.

### Flat

Small differences are labeled **flat**.

This project uses a +/- $0.25 per barrel threshold:

```text
C1-C4 > +$0.25  -> backwardation
C1-C4 < -$0.25  -> contango
between those   -> flat
```

Why use a threshold? Because calling a $0.03 difference a major market regime would give tiny changes too much meaning.

---

## Step 4 — Measure the slope

The project also calculates:

```text
Curve slope per contract = (C4 - C1) / 3
```

There are three contract steps from C1 to C4:

```text
C1 -> C2 -> C3 -> C4
```

The slope is therefore an easy way to describe how quickly the curve rises or falls across those steps.

You do not need the slope to understand the module. The C1-C4 spread is the main beginner-friendly measure.

---

## Step 5 — Look at the historical regimes

For every month in the dataset, the program:

1. reads C1 through C4,
2. calculates the spreads,
3. calculates the slope,
4. labels the month backwardation, contango, or flat,
5. saves the result to `term_structure_monthly.csv`.

It then counts how many months fall into each regime and saves that table to `term_structure_regime_summary.csv`.

This lets us answer questions such as:

- How often was the curve backwardated in the sample?
- How often was it in contango?
- How large was the average C1-C4 spread in each regime?
- What was the average front-month price in each regime?

These are descriptive statistics. They do not automatically mean one regime is bullish or bearish.

---

## Step 6 — Read the first chart

`term_structure_c1_c4_spread.svg` plots the C1-C4 spread through time.

Interpret it like this:

```text
Above zero -> C1 is above C4 -> backwardation
Below zero -> C1 is below C4 -> contango
Near zero  -> relatively flat curve
```

The farther the line moves away from zero, the larger the price difference between nearby and later delivery.

---

## Step 7 — Read the example-curve chart

`term_structure_curve_examples.svg` shows two historical curve shapes selected by the code:

- the month with the largest positive C1-C4 spread,
- the month with the largest negative C1-C4 spread.

This is meant to make the terms visual.

If the plotted line slopes **down** from C1 toward C4, nearby contracts are more expensive: backwardation.

If the plotted line slopes **up** from C1 toward C4, later contracts are more expensive: contango.

---

## Step 8 — Why this improves the hedge project

The original hedge model mostly asks:

> How much production should be hedged?

Term structure adds another question:

> Which part of the WTI curve are we looking at, and what does the relationship between delivery months look like?

That matters because a physical producer has future production arriving at different dates. A professional hedge program should eventually think about **which contract month matches which production month**, not just one continuous front-month price series.

This module is therefore a bridge from a simple hedge simulator toward a more realistic commodity-risk framework.

---

## What the output files mean

| File | Plain-English purpose |
|---|---|
| `term_structure_monthly.csv` | The full monthly C1-C4 dataset plus spreads, slope, and regime label. |
| `term_structure_regime_summary.csv` | Counts and averages for backwardation, contango, and flat months. |
| `term_structure_example_curves.csv` | The strongest backwardation and contango examples selected by the code. |
| `term_structure_c1_c4_spread.svg` | Shows how the C1-C4 spread changed over time. |
| `term_structure_curve_examples.svg` | Shows what backwardation and contango look like as actual curves. |

---

## How to run this module

From the main project folder:

```bash
pip install -r requirements.txt
python run_term_structure.py
```

The script prints each step as it runs.

It first tries to read EIA's historical tables directly. If that download is unavailable, it falls back to the saved EIA snapshot in `data/eia_wti_curve_monthly_2015_2024.csv`.

---

## Data limitation you should know

The EIA NYMEX futures-price history used here stops after April 5, 2024. That means this module is a **historical research example**, not a live futures-curve dashboard.

The saved monthly snapshot in this repository covers January 2015 through April 2024.

A production trading system would use a current contract-level market-data feed and exact futures symbols, expiration dates, and roll rules.

---

## How to explain this module in an interview

A simple answer:

> "I extended my WTI producer hedge project to analyze the futures term structure. I pulled the first four WTI delivery contracts, calculated calendar spreads such as C1-C4, classified historical months as backwardation, contango, or flat, and built visualizations showing how the curve changed over time. The goal was to move beyond a single continuous futures price and start thinking about contract-month selection and curve risk in a physical hedging program."

If they ask why it matters:

> "A producer does not produce all of its crude today. Future production occurs across different months, so the relationship between futures delivery months matters when deciding which contracts best match the physical exposure."

---

## Beginner glossary for this module

| Term | Plain-English meaning |
|---|---|
| Futures curve | Several futures prices lined up by delivery month. |
| Term structure | Another name for how futures prices are arranged across delivery dates. |
| Front / near contract | The nearest delivery contract in the dataset. Here that is C1. |
| Deferred contract | A futures contract with delivery farther in the future. |
| Calendar spread | The price of one delivery month minus another delivery month. |
| C1-C4 spread | Contract 1 price minus Contract 4 price. The main curve measure in this module. |
| Backwardation | Nearby futures are priced above later futures. |
| Contango | Later futures are priced above nearby futures. |
| Flat curve | Nearby and later futures prices are very close. |
| Curve slope | A simple measure of how quickly prices rise or fall across contract months. |
| Prompt barrels | Physical oil needed or delivered in the near term. |
| Carry | The economics of holding a commodity through time, including items such as storage and financing. |
| Curve regime | The label used here for backwardation, contango, or flat. |
| Roll | Moving a futures position from an expiring contract into a later contract. |
| Roll risk | The risk/cost created because the new contract may trade at a different price from the expiring one. |

Educational and portfolio use only. This is not a trading recommendation.
