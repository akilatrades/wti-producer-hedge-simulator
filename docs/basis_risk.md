# Midland-Cushing Basis Risk

## Business interpretation

NYMEX WTI futures are tied to Cushing, Oklahoma. A Permian producer may sell physical crude at Midland.

Those two prices can move differently.

The location difference is:

```text
Midland basis = Midland price - Cushing price
```

A producer can therefore hedge the broad WTI price move and still lose revenue if Midland weakens relative to Cushing.

That residual exposure is **basis risk**.

## Example

Expected basis:

```text
Midland - Cushing = -$1/bbl
```

Realized basis:

```text
Midland - Cushing = -$5/bbl
```

Basis deterioration:

```text
-$5 - (-$1) = -$4/bbl
```

For 100,000 barrels, the revenue impact is:

```text
-$4 × 100,000 = -$400,000
```

A Cushing futures hedge does not automatically remove that $400,000 location loss.

## Basis hedge representation

The project models a simplified basis swap:

```text
Basis swap P&L
= (locked basis - realized basis)
  × basis-hedged barrels
```

If the producer locked -$1/bbl and realized -$5/bbl, the swap pays +$4/bbl on the hedged basis volume.

## Why this module matters

The module demonstrates an important commercial principle:

> Flat-price risk and location-basis risk are different exposures.

A trader or risk analyst should be able to identify which exposure is being hedged by which instrument.

## Limitation

The current saved basis analysis is a scenario model, not a historical backtest of Midland cash prices or Midland-Cushing basis instruments.

For production use, the model would require contract-specific basis data, settlement conventions, liquidity assumptions, and actual realized physical pricing.
