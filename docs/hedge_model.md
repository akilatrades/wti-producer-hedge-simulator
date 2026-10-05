# Producer Hedge Model

## Business interpretation

A crude-oil producer is naturally **long oil price exposure** because future revenue rises when crude prices rise and falls when crude prices fall.

A short WTI futures position can offset part of that price exposure.

The objective of the model is not to make the futures position profitable by itself. The objective is to reduce uncertainty in the combined physical-plus-derivative result.

## Illustrative hedge mechanics

Assume:

- expected production: 100,000 barrels,
- WTI futures entry price: $75/bbl,
- hedge ratio: 50%,
- CL contract size: 1,000 barrels.

The hedge covers:

```text
100,000 × 50% = 50,000 barrels
```

Required contracts:

```text
50,000 / 1,000 = 50 CL contracts short
```

If futures fall from $75 to $60:

```text
Futures P&L
= ($75 - $60) × 50,000
= +$750,000
```

The physical barrels are worth less, but the short futures position offsets part of the decline.

## Model fields

For each month, the hedge engine tracks:

- spot exit price,
- futures entry price,
- futures exit price,
- expected production,
- hedge ratio,
- contracts short,
- hedged barrels,
- physical revenue,
- futures P&L,
- hedged revenue,
- benchmark locked revenue,
- residual revenue surprise.

## Revenue surprise

The project uses the prior futures entry price as a simple benchmark for the monthly revenue that could have been approximately locked for the full expected volume.

```text
Revenue surprise
= Hedged revenue - benchmark locked revenue
```

A smaller and less volatile revenue surprise means the hedge kept realized modeled revenue closer to that starting benchmark.

## Fixed hedge ratios

The base analysis compares:

- 0%,
- 25%,
- 50%,
- 75%,
- 100%.

This provides an intuitive risk frontier: as the hedge ratio rises, flat-price exposure generally falls, but participation in favorable price increases also falls.

## P&L attribution

The project separates the monthly result into:

```text
Physical flat-price effect
+ Futures hedge effect
= Residual flat-price result
```

A separate basis module can add location-basis effects.

This decomposition matters because a risk manager should be able to explain **why** the total result moved, not only whether it was positive or negative.

## Commercial interpretation

A statistically effective hedge is not automatically the correct operational hedge.

A commercial policy can be constrained by:

- expected production uncertainty,
- internal hedge limits,
- liquidity,
- margin requirements,
- accounting treatment,
- credit limits,
- location and quality differences,
- contract-month matching.

Those issues are treated explicitly in the ladder, scenario, and limitations documentation.
