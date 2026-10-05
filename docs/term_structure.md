# WTI Term Structure

## Business interpretation

WTI is not one price. Futures contracts for different delivery periods trade simultaneously.

Those prices form the **futures curve** or **term structure**.

For a producer, the curve matters because production expected in different months should be compared with different points on the hedge horizon.

## Core spreads

The project uses EIA historical Contract 1 through Contract 4 series.

```text
C1-C2 = Contract 1 - Contract 2
C1-C3 = Contract 1 - Contract 3
C1-C4 = Contract 1 - Contract 4
```

The primary historical spread is C1-C4.

## Curve classification

Project convention:

```text
C1-C4 > +$0.25/bbl -> backwardation
C1-C4 < -$0.25/bbl -> contango
otherwise           -> flat
```

The threshold is a project setting, not a universal market definition.

## Enhanced curve features

The project also calculates:

- slope per contract step,
- near-curve curvature,
- rolling C1-C4 mean,
- rolling C1-C4 standard deviation,
- rolling z-score,
- historical percentile rank of the C1-C4 spread.

### Curvature

A simple near-curve curvature measure is:

```text
Curvature = C1 - 2×C2 + C3
```

It helps distinguish a straight-sloping curve from one with a local bend.

### Z-score

```text
Z-score
= (current spread - rolling mean)
  / rolling standard deviation
```

This describes how unusual the spread is relative to its own recent history.

## Regime analysis

The project can summarize market behavior separately in:

- backwardation,
- flat,
- contango.

That creates a foundation for questions such as:

- Is front-month volatility different by curve regime?
- How persistent are extreme spreads?
- Does hedge behavior differ across regimes?

The regime label itself is descriptive and should not be treated as a standalone trading signal.

## Data limitation

The EIA historical NYMEX Contract 1-4 series used by the project ends in April 2024.

It is therefore a historical research dataset, not a live term-structure feed.
