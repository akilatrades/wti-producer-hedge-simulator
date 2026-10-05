# Physical Market Context

## Business interpretation

Futures curves are financial prices, but crude-oil term structure is connected to the physical market.

The project includes an optional framework for joining curve observations with EIA-style physical-market variables such as:

- U.S. commercial crude inventories,
- Cushing inventories,
- refinery utilization,
- crude production,
- imports,
- exports.

The purpose is **context**, not an automatic trading signal.

## Suggested input schema

A fundamentals file can contain:

| Field | Unit | Meaning |
|---|---|---|
| `date` | date | observation date |
| `commercial_crude_stocks_kb` | thousand barrels | U.S. commercial crude inventory |
| `cushing_stocks_kb` | thousand barrels | Cushing inventory |
| `refinery_utilization_pct` | percent | refinery utilization |
| `crude_production_kbd` | thousand bbl/day | U.S. crude production |
| `imports_kbd` | thousand bbl/day | crude imports |
| `exports_kbd` | thousand bbl/day | crude exports |

A header-only template is stored in `data/fundamentals_template.csv`.

## Derived features

The fundamentals module can calculate:

- weekly changes,
- percentage changes where appropriate,
- rolling z-scores,
- net imports:

```text
Net imports = imports - exports
```

These features can then be joined with term-structure data.

## Example research questions

- Do unusually low Cushing inventories coincide with stronger backwardation?
- Does refinery utilization change alongside the front of the curve?
- How does net import dependence vary across curve regimes?
- Are large inventory changes associated with unusual C1-C4 z-scores?

## Important limitation

This module is deliberately descriptive.

The project does not claim that an inventory change mechanically predicts the next WTI price move.

Any predictive use would require a separate research design with announcement timing, expectations/surprises, transaction costs, and out-of-sample validation.
