# Producer Hedge Book and Hedge Ladder

## Business interpretation

A producer does not produce all future barrels on one date.

Expected production is distributed across months, so the hedge should also be mapped across delivery periods.

The project represents this as a simple **hedge ladder**.

Example:

| Production month | Expected barrels | Hedge ratio | Futures contract | Contracts short |
|---|---:|---:|---|---:|
| Jan | 100,000 | 80% | CL Feb | 80 |
| Feb | 100,000 | 70% | CL Mar | 70 |
| Mar | 95,000 | 60% | CL Apr | 57 |

The contract mapping is illustrative. A real hedge book would use actual contract calendars, expiry rules, physical pricing windows, and company policy.

## Why a ladder is better than one hedge ratio

A single 75% hedge ratio hides the timing dimension.

Commercial hedge policies often reduce hedge percentages farther into the future because:

- production forecasts become less certain,
- liquidity can change by contract month,
- management may preserve upside exposure,
- policy limits may differ by horizon.

## Hedge-policy scenarios

The project can compare policies such as:

### Conservative

```text
Month 1: 80%
Month 2: 70%
Month 3: 60%
Months 4-6: 40%
```

### Balanced

```text
Month 1: 70%
Month 2: 60%
Month 3: 50%
Months 4-6: 30%
```

### Light hedge

```text
Month 1: 50%
Month 2: 40%
Month 3: 30%
Months 4-6: 20%
```

The code converts each production month into:

- hedged barrels,
- whole CL contracts,
- residual unhedged barrels,
- futures notional.

## Production uncertainty and over-hedging

Expected production can differ from actual production.

If a producer hedges 100,000 expected barrels but only produces 80,000 barrels, part of the futures position is no longer offset by physical production.

The scenario module tracks:

```text
Over-hedged barrels
= max(hedged barrels - actual production, 0)
```

This makes the risk of aggressive hedge ratios visible rather than leaving it as a footnote.

## Production-use requirements

A real hedge book would also require:

- contract identifiers,
- exchange expiry dates,
- roll rules,
- trade dates,
- transaction costs,
- credit/margin usage,
- realized physical volumes,
- settlement data,
- approval limits,
- hedge-accounting metadata.
