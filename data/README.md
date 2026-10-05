# Data

The project uses public market data and saved snapshots so the analysis can be reproduced and its limitations can be reviewed explicitly.

## 1. WTI Cushing spot

The main hedge model uses WTI Cushing spot as a simplified physical-price proxy.

The analysis runner downloads the FRED/EIA series:

```text
DCOILWTICO
```

This is not the same as a producer's realized Midland price or netback.

## 2. WTI futures proxy

The main hedge history uses Yahoo Finance ticker:

```text
CL=F
```

as a continuous front-month WTI futures proxy.

A continuous futures series is useful for long historical analysis but is **not** the same as following exact contract months, roll dates, transaction costs, and exchange settlement conventions.

That distinction is important when interpreting the hedge backtest.

## 3. Saved WTI term-structure snapshot

File:

`eia_wti_curve_monthly_2015_2024.csv`

The project uses four historical EIA WTI futures delivery positions:

```text
C1 = nearest delivery position
C2 = second delivery position
C3 = third delivery position
C4 = fourth delivery position
```

C1 is not one permanent contract. The specific futures contract represented by C1 changes over time.

The saved snapshot allows the term-structure analysis to run even when the source webpage is unavailable.

EIA notes that this historical NYMEX Contract 1-4 dataset is not available after April 5, 2024, so the curve module is a historical research example rather than a live curve feed.

## 4. Optional physical-market fundamentals

Template:

`fundamentals_template.csv`

Expected fields:

- commercial crude stocks,
- Cushing stocks,
- refinery utilization,
- crude production,
- imports,
- exports.

To use the optional fundamentals module, create:

`data/eia_physical_fundamentals.csv`

using the documented schema.

The project intentionally does not ship made-up fundamental observations. The template contains column names only.

See [physical market context](../docs/fundamentals.md).

## Data governance principles used in the project

The repository tries to distinguish clearly between:

- downloaded source data,
- saved reproducibility snapshots,
- illustrative scenario assumptions,
- generated analytical outputs.

Illustrative hedge-ladder prices and production forecasts are not labeled as historical observations.

## Primary limitations

A production hedge model would need:

- exact futures contract identifiers,
- exchange expiration calendars,
- roll timing,
- transaction costs,
- margin and liquidity,
- realized physical production,
- actual location/quality pricing,
- settlement conventions.

See [model limitations](../docs/limitations.md).
