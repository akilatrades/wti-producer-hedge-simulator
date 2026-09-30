# Module 2 — WTI Futures Curve / Term Structure

This guide is written for someone who is **brand new to commodity futures**.

You do not need to know what a futures curve, calendar spread, backwardation, contango, or roll means before starting. Each term is explained before it is used.

---

## What are we trying to learn?

The original project asks:

> How can an oil producer use WTI futures to reduce price risk?

This module adds a second question:

> How are WTI futures prices different across delivery months?

That matters because an oil producer does not produce all of its oil today. Production happens over time.

A producer expecting oil in January, February, March, and April may want to understand the futures prices connected to those different delivery periods.

The line-up of futures prices across delivery months is called the **futures curve** or **term structure**.

---

# Start with one simple idea

Imagine four WTI futures prices are shown at the same time:

```text
Contract 1 = $80
Contract 2 = $79
Contract 3 = $78
Contract 4 = $77
```

These are **not four prices for the exact same delivery month**.

They represent four successive delivery positions in the futures market.

In this historical EIA dataset:

```text
C1 = nearest delivery contract in the dataset
C2 = next delivery contract
C3 = next one after that
C4 = fourth delivery contract
```

So the curve is simply:

```text
C1 -> C2 -> C3 -> C4
80    79    78    77
```

The prices fall as delivery moves farther into the future.

Now compare that with:

```text
C1 -> C2 -> C3 -> C4
70    71    72    73
```

Here, prices rise as delivery moves farther into the future.

Those two shapes have different names. We will get to those names only after the math is clear.

---

# The full workflow before we begin

This module does seven basic things:

1. **Load** historical C1, C2, C3, and C4 WTI futures prices.
2. **Line up** the four prices for each month.
3. **Subtract** later contracts from the nearest contract to create calendar spreads.
4. **Label** each month as backwardation, contango, or flat.
5. **Summarize** how often each curve shape appeared.
6. **Chart** the spread through time and show example curves.
7. **Connect** the curve back to a physical producer and hedging decisions.

Nothing more complicated than that is required to understand the module.

---

# Step 1 — Load the four futures prices

The project uses historical WTI futures data from the U.S. Energy Information Administration, or EIA.

The saved project file contains:

- `contract_1`
- `contract_2`
- `contract_3`
- `contract_4`

The file is:

`data/eia_wti_curve_monthly_2015_2024.csv`

Each row is one month.

A simplified row might look like this:

| Month | C1 | C2 | C3 | C4 |
|---|---:|---:|---:|---:|
| Example month | $80 | $79 | $78 | $77 |

### What does C1 mean?

C1 means the **nearest delivery contract in the EIA series for that observation**.

It does **not** mean one fixed futures contract forever.

As time moves forward, the contract considered C1 changes.

That is important. C1 is a position on the curve — "nearest contract" — rather than one permanent contract symbol.

### Why do we use four contracts?

Four contracts are enough to show whether the front of the WTI curve is generally above, below, or close to the later part of the curve.

It is a simple starting point.

A professional trading desk may look at many more delivery months.

---

# Step 2 — Line up the prices for the same observation

Before comparing contracts, the prices must refer to the same observation period.

For each month, the code places C1, C2, C3, and C4 on one row.

Example:

```text
Month: January

C1 = $80
C2 = $79
C3 = $78
C4 = $77
```

Now we can compare the near contract with later contracts.

This is important because comparing a January C1 observation with a March C4 observation would mix different points in time.

The code avoids that by aligning the contracts by date first.

---

# Step 3 — Calculate calendar spreads

A **calendar spread** in this project is simply a price difference between two futures delivery positions.

The main calculations are:

```text
C1-C2 spread = C1 price - C2 price
C1-C3 spread = C1 price - C3 price
C1-C4 spread = C1 price - C4 price
```

We use C1 minus the later contract.

## Example A — positive spread

Assume:

```text
C1 = $80
C4 = $77
```

Then:

```text
C1-C4 = $80 - $77
      = +$3/bbl
```

The result is positive.

That means the nearest contract is $3 per barrel **more expensive** than C4.

## Example B — negative spread

Assume:

```text
C1 = $70
C4 = $73
```

Then:

```text
C1-C4 = $70 - $73
      = -$3/bbl
```

The result is negative.

That means the nearest contract is $3 per barrel **cheaper** than C4.

## The easiest way to remember the sign

```text
Positive C1-C4:
near price > later price

Negative C1-C4:
near price < later price
```

That sign is what we use in the next step.

---

# Step 4 — Give the curve shape a name

Once we know whether C1 is above or below C4, we can label the curve.

The project uses this simple rule:

```text
C1-C4 > +$0.25/bbl  -> backwardation
C1-C4 < -$0.25/bbl  -> contango
between -$0.25 and +$0.25 -> flat
```

The $0.25 threshold is a project setting. It prevents tiny differences from being treated as an important curve shape.

It is **not** a universal market rule.

## Backwardation

Backwardation means nearby futures prices are above later futures prices.

Example:

```text
C1 = $80
C2 = $79
C3 = $78
C4 = $77
```

The curve slopes downward as we move to later delivery.

The C1-C4 spread is:

```text
$80 - $77 = +$3/bbl
```

That is positive, so the project labels this month **backwardation**.

### Plain-English interpretation

The market is pricing the nearer delivery higher than the later delivery.

That can be consistent with stronger value being placed on near-term barrels, but this project does **not** assume one single cause.

Do not read backwardation as:

> "WTI must go up next."

That is not what the label means.

---

## Contango

Contango means later futures prices are above nearby futures prices.

Example:

```text
C1 = $70
C2 = $71
C3 = $72
C4 = $73
```

The curve slopes upward as we move to later delivery.

The C1-C4 spread is:

```text
$70 - $73 = -$3/bbl
```

That is negative, so the project labels this month **contango**.

### Plain-English interpretation

The market is pricing later delivery above nearer delivery.

That can be consistent with storage and carrying costs or weaker pressure for immediate barrels, but the curve alone does not prove why the shape exists.

Do not read contango as:

> "WTI must go down next."

Again, the label describes the relationship between delivery months, not a guaranteed future price direction.

---

## Flat curve

If C1 and C4 are very close, the project labels the curve **flat**.

Example:

```text
C1 = $75.00
C4 = $75.10

C1-C4 = -$0.10/bbl
```

Because -$0.10 falls between -$0.25 and +$0.25, the project calls the curve flat.

---

# Step 5 — Calculate a simple curve slope

The module also calculates:

```text
Curve slope per contract = (C4 - C1) / 3
```

Why divide by 3?

Because there are three steps between C1 and C4:

```text
C1 -> C2 -> C3 -> C4
  1     2     3
```

## Example

If:

```text
C1 = $70
C4 = $73
```

Then:

```text
($73 - $70) / 3
= $1 per contract step
```

That tells us the curve increased by about $1 per barrel for each contract step from C1 to C4.

### Important sign difference

The slope formula is written as:

```text
C4 - C1
```

But the calendar spread is written as:

```text
C1 - C4
```

So the signs point in opposite directions.

That is not an error.

We keep C1-C4 as the main beginner measure because it makes this rule easy:

```text
positive spread = backwardation
negative spread = contango
```

You can understand the entire module without using the slope.

---

# Step 6 — Repeat the calculation for every month

The code does the same calculations for every monthly observation.

For each month it creates columns like:

| Column | Meaning |
|---|---|
| `contract_1` | nearest futures price |
| `contract_2` | next futures price |
| `contract_3` | third futures price |
| `contract_4` | fourth futures price |
| `c1_c2_spread` | C1 minus C2 |
| `c1_c3_spread` | C1 minus C3 |
| `c1_c4_spread` | C1 minus C4 |
| `curve_slope_per_contract` | average price change per contract step |
| `curve_regime` | backwardation, contango, or flat |

The full file is saved as:

`outputs/term_structure_monthly.csv`

This is the most detailed output from the module.

---

# Step 7 — Summarize the historical curve regimes

After every month receives a label, the code counts how many months were:

- backwardation,
- contango,
- flat.

It also calculates:

- average C1-C4 spread in each regime,
- average C1 price in each regime,
- share of the sample represented by each regime.

The result is saved as:

`outputs/term_structure_regime_summary.csv`

For the saved January 2015 through April 2024 sample, using the project's simple +/- $0.25 threshold:

```text
Backwardation: 48 months
Contango:      54 months
Flat:          10 months
```

These counts are descriptive.

They do not mean one regime was "better" than another.

---

# Step 8 — Read the first chart

The first chart is:

`outputs/term_structure_c1_c4_spread.svg`

It plots the C1-C4 spread through time.

Read it this way:

```text
Line above zero
-> C1 > C4
-> backwardation

Line below zero
-> C1 < C4
-> contango

Line near zero
-> C1 and C4 are close
-> relatively flat curve
```

The farther the line is from zero, the larger the difference between the near contract and C4.

This chart answers:

> How did the front-versus-later relationship change through time?

---

# Step 9 — Read the example-curve chart

The second chart is:

`outputs/term_structure_curve_examples.svg`

The code selects:

- the month with the largest positive C1-C4 spread,
- the month with the largest negative C1-C4 spread.

Then it draws the actual C1, C2, C3, and C4 prices for those months.

This makes the curve shape easier to see.

### If the line falls from left to right

```text
C1 high -> C4 lower
```

That is backwardation.

### If the line rises from left to right

```text
C1 low -> C4 higher
```

That is contango.

The chart is meant to help you connect the math to the picture.

---

# Step 10 — Connect this back to a physical oil producer

This is the most important business reason for adding Module 2.

The original hedge project uses a continuous front-month futures series.

That is useful for learning, but a real producer has physical production arriving in different months.

Example:

```text
January production
February production
March production
April production
```

Those future barrels do not all have the same timing.

A real hedge program therefore needs to think about questions like:

- Which futures contract best matches the month when the physical oil will be sold?
- Is the producer hedging January production with a January-related contract or with something much later?
- What happens if the futures curve is steep?
- What happens when the curve changes shape before the hedge is rolled?
- Does moving the hedge from one contract month to another create additional cost or risk?

Module 2 does not solve all of those questions yet.

It creates the market-structure foundation needed to study them properly.

---

# Why this matters to a trading desk

A trader or analyst may care about the curve because it shows that WTI is not just one price.

There is a different price for different delivery periods.

That matters to:

- producers,
- refiners,
- storage operators,
- physical traders,
- hedgers,
- market-risk teams,
- quantitative analysts.

For example, storage economics depend partly on the difference between near and later prices.

A producer's hedge can also be affected by which delivery month is used.

So the curve gives more information than looking at front-month WTI alone.

---

# What this module does NOT prove

This section is important.

The project does **not** prove that:

- backwardation guarantees WTI will rise,
- contango guarantees WTI will fall,
- one curve regime is always profitable,
- the C1-C4 spread alone is a complete trading signal,
- the historical EIA curve is a live trading feed,
- four contracts capture the entire WTI forward curve.

The module is a **descriptive market-structure analysis**.

Later modules can test whether curve shape is related to hedge performance, returns, inventories, volatility, or other variables.

---

# Common beginner mistakes

## Mistake 1 — Thinking C1 is one permanent contract

It is not.

C1 means the nearest delivery position in the historical series.

As time passes, the exact contract represented by C1 changes.

## Mistake 2 — Thinking backwardation means "bullish"

Backwardation describes the relationship between delivery months.

It is not automatically a directional price forecast.

## Mistake 3 — Thinking contango means "bearish"

Same issue.

Contango is a curve shape, not a guaranteed prediction.

## Mistake 4 — Forgetting the subtraction order

This project uses:

```text
C1 - C4
```

So:

```text
positive = C1 above C4
negative = C1 below C4
```

If you reverse the formula to C4-C1, the signs reverse too.

## Mistake 5 — Treating the $0.25 threshold as a market law

It is only a simple classification setting used by this project.

You could test a different threshold later.

## Mistake 6 — Assuming monthly data captures every intraday move

It does not.

This module uses monthly historical observations to study broad curve structure.

A trading desk may use daily, hourly, or live contract-level data.

---

# What happens when you run the script?

Run:

```bash
python run_term_structure.py
```

The script walks through the work in plain English.

It:

1. loads EIA curve data,
2. explains what C1-C4 mean,
3. calculates the spreads,
4. labels the curve,
5. summarizes the historical regimes,
6. selects example months,
7. creates the output files and charts.

The script first tries to read the EIA historical tables directly.

If that is unavailable, it uses the saved project snapshot:

`data/eia_wti_curve_monthly_2015_2024.csv`

That fallback makes the project reproducible.

---

# Output files explained

| File | What it is for |
|---|---|
| `data/eia_wti_curve_monthly_2015_2024.csv` | Saved input data containing C1-C4 prices. |
| `outputs/term_structure_monthly.csv` | Every monthly observation plus spreads, slope, and curve label. |
| `outputs/term_structure_regime_summary.csv` | Counts and averages for backwardation, contango, and flat months. |
| `outputs/term_structure_example_curves.csv` | The two historical example months selected by the code. |
| `outputs/term_structure_c1_c4_spread.svg` | Chart of C1-C4 through time. |
| `outputs/term_structure_curve_examples.svg` | Chart showing example backwardation and contango curves. |

---

# Data limitation

The EIA historical NYMEX futures series used here is not available after April 5, 2024.

That means the saved term-structure sample is used for **historical learning and research**.

It is not a current WTI futures-curve feed.

A production trading system would need current contract-level data, exact contract symbols, expiration dates, roll rules, transaction costs, and liquidity information.

---

# How this module improves the overall project

Before Module 2, the project mostly asked:

> How much of the producer's oil should be hedged?

Now it also asks:

> What does the WTI market look like across different delivery months?

That is a meaningful step toward a more realistic commodity-trading and hedging framework.

The next natural research question is:

> Does the producer's hedge behave differently when the WTI curve is in backwardation versus contango?

That would directly connect this module back to hedge performance.

---

# How to explain Module 2 in an interview

### Short version

> "I extended my WTI producer hedge model to study the futures curve. I used the first four WTI futures delivery positions, calculated calendar spreads such as C1-C4, and classified historical observations as backwardation, contango, or flat. I then visualized how the curve changed over time and connected the curve structure back to contract-month selection for a physical producer."

### If they ask why it matters

> "A producer has physical exposure across future months, not just today. Looking at the curve helps me think about which futures contract matches each production period and what additional risk can appear when the hedge is moved from one delivery month to another."

### If they ask whether backwardation is bullish

> "Not automatically. In this project, backwardation only describes nearby futures being priced above later futures. I treat it as market-structure information, not as a guaranteed directional signal."

---

# Beginner glossary

| Term | Plain-English meaning |
|---|---|
| WTI | West Texas Intermediate, a major U.S. crude-oil benchmark. |
| Futures contract | A standardized contract tied to a price for a future delivery month. |
| Delivery month | The month connected to a specific futures contract. |
| Futures curve | Several futures prices arranged from nearer delivery to later delivery. |
| Term structure | Another name for the futures curve. |
| C1 | The nearest delivery position in the historical EIA series. It changes through time. |
| C2 | The delivery position after C1. |
| C3 | The delivery position after C2. |
| C4 | The fourth delivery position in the series. |
| Front / near contract | The nearest futures delivery position. |
| Deferred contract | A futures contract with delivery farther into the future. |
| Calendar spread | The difference between two futures delivery-month prices. |
| C1-C4 spread | C1 price minus C4 price. The main curve measure used here. |
| Positive spread | C1 is priced above the later contract. |
| Negative spread | C1 is priced below the later contract. |
| Backwardation | Nearby futures are priced above later futures. |
| Contango | Later futures are priced above nearby futures. |
| Flat curve | Nearby and later prices are very close. |
| Curve slope | A simple measure of how much the curve rises or falls across delivery positions. |
| Curve regime | The project's label for backwardation, contango, or flat. |
| Threshold | A cutoff used to decide which label to assign. Here it is +/- $0.25/bbl. |
| Prompt barrels | Physical oil needed or delivered in the near term. |
| Carry | Costs/economics associated with holding a commodity through time, such as storage and financing. |
| Roll | Moving a futures position from a nearer contract into a later contract. |
| Roll risk | Risk or cost caused by the price difference between the contract being exited and the new contract being entered. |
| Historical sample | The past data used for the analysis. |
| Live market data | Current, continuously updating market prices. |

Educational and portfolio use only. This is not a trading recommendation.
