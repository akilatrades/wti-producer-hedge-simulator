# WTI Producer Hedging & Market Risk Analytics

[![tests](https://github.com/akilatrades/wti-producer-hedge-simulator/actions/workflows/tests.yml/badge.svg)](https://github.com/akilatrades/wti-producer-hedge-simulator/actions/workflows/tests.yml)

Python-based analysis of crude-oil producer price exposure, WTI futures hedging, Midland-Cushing basis risk, hedge-ratio stability, and WTI term structure.

The project is designed as a compact energy-risk research framework: identify a physical exposure, apply a derivative hedge, measure residual risk, stress the assumptions, and validate the model.

> **One-line summary:** model a producer's WTI exposure and evaluate how fixed and statistically estimated futures hedges change revenue volatility, tail risk, basis exposure, and contract-level hedge requirements.

## Executive summary

The base case assumes **100,000 barrels of expected monthly production** and compares short NYMEX WTI futures hedges from 0% to 100%.

Historical saved results currently show:

| Metric | Result |
|---|---:|
| Unhedged revenue-surprise volatility | $711,294 |
| 75% hedge effectiveness | 90.3% |
| 100% hedge effectiveness | 96.0% |
| Static minimum-variance hedge ratio | 1.016 |
| Spot/futures monthly-change correlation | 0.983 |
| Rounded minimum-variance implementation | 102 CL contracts |
| Rounded minimum-variance variance reduction | 96.6% |

![Hedge effectiveness](outputs/hedge_effectiveness.svg)

These are historical model results, not hedge recommendations. A real producer would also consider production uncertainty, basis exposure, liquidity, margin, hedge limits, accounting treatment, and internal risk policy.

## What the project covers

### 1. Producer flat-price hedge

Compares 0%, 25%, 50%, 75%, and 100% futures hedges and measures:

- physical revenue,
- futures P&L,
- hedged revenue,
- residual revenue surprise,
- hedge effectiveness.

### 2. Market-risk metrics

Adds a risk-manager view of the same hedge strategies:

- monthly and annualized volatility,
- 95% and 99% historical Value at Risk,
- Expected Shortfall,
- downside deviation,
- worst historical modeled loss.

### 3. P&L attribution

Separates the result into:

```text
Physical flat-price effect
+ Futures hedge effect
= Residual flat-price result
```

The objective is to explain **why** the hedge result moved, not only whether it was positive or negative.

### 4. Midland-Cushing basis risk

Models the residual location risk created when a producer sells Midland crude but hedges with Cushing-linked WTI futures.

![Basis risk](outputs/basis_risk_stress.svg)

### 5. Minimum-variance hedge estimation

Estimates:

```text
h* = Cov(ΔSpot, ΔFutures) / Var(ΔFutures)
```

and compares the historical residual variance with fixed hedge ratios.

![Minimum-variance comparison](outputs/min_variance_comparison.svg)

### 6. Model validation

The project now tests the minimum-variance estimate using:

- rolling 24-month hedge ratios,
- walk-forward / out-of-sample testing,
- bootstrap confidence intervals.

The goal is to avoid presenting one in-sample hedge ratio as if it were a permanent constant.

### 7. Producer hedge ladder

Maps expected production across future months into:

- hedge percentages,
- whole CL contracts,
- hedged and unhedged barrels,
- futures notional.

This adds the contract-month dimension that a one-period hedge ratio cannot show.

### 8. Production uncertainty

Stress-tests actual production above and below forecast production and identifies:

- under-hedged barrels,
- over-hedged barrels,
- residual revenue effects.

This makes production-volume risk explicit.

### 9. WTI term structure

Analyzes historical EIA WTI Contract 1-4 prices using:

- C1-C2, C1-C3, and C1-C4 spreads,
- backwardation / contango / flat regimes,
- curve slope,
- curve curvature,
- rolling z-scores,
- historical spread percentiles.

![WTI term structure](outputs/term_structure_c1_c4_spread.svg)

### 10. Optional physical-market context

A separate module can join the curve data to EIA-style variables such as:

- commercial crude inventories,
- Cushing inventories,
- refinery utilization,
- crude production,
- imports,
- exports.

This module is descriptive and does not claim that one inventory print mechanically predicts the next WTI move.

## Architecture

```text
Public market data
      |
      v
Physical exposure assumptions
      |
      +--> Fixed hedge ratios
      |
      +--> Minimum-variance hedge estimate
      |
      +--> Basis-risk scenarios
      |
      +--> Production-volume scenarios
      |
      +--> Multi-month hedge ladder
      |
      v
Risk measurement
      |
      +--> Volatility / VaR / ES
      +--> P&L attribution
      +--> Walk-forward validation
      +--> Bootstrap uncertainty
      |
      v
WTI term-structure / physical-market context
```

## Repository structure

```text
.
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── run_analysis.py
├── src/
│   ├── hedge_engine.py
│   ├── basis_risk.py
│   ├── min_variance.py
│   ├── risk_metrics.py
│   ├── pnl_attribution.py
│   ├── hedge_ladder.py
│   ├── scenarios.py
│   ├── validation.py
│   ├── term_structure.py
│   └── fundamentals.py
├── docs/
│   ├── methodology.md
│   ├── hedge_model.md
│   ├── basis_risk.md
│   ├── risk_metrics.md
│   ├── hedge_book.md
│   ├── validation.md
│   ├── term_structure.md
│   ├── fundamentals.md
│   ├── data_dictionary.md
│   ├── limitations.md
│   └── glossary.md
├── data/
├── notebooks/
├── outputs/
└── tests/
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
python run_analysis.py
```

`run_analysis.py` refreshes the core tables and charts in `outputs/`.

The analysis attempts to download WTI spot and futures data. The historical EIA C1-C4 curve module uses the saved repository snapshot if the EIA table is unavailable.

## Generated analytical outputs

The expanded analysis can generate:

- `hedge_ratio_summary.csv`
- `monthly_analysis.csv`
- `risk_summary.csv`
- `pnl_attribution.csv`
- `basis_risk_scenarios.csv`
- `illustrative_hedge_ladder.csv`
- `production_uncertainty_scenarios.csv`
- `min_variance_summary.csv`
- `rolling_min_variance_ratio.csv`
- `walk_forward_validation.csv`
- `bootstrap_hedge_ratio_summary.csv`
- `term_structure_monthly.csv`
- `term_structure_regime_behavior.csv`
- `executive_summary.md`

See [outputs/README.md](outputs/README.md) for the reporting layer.

## Data

The project uses public market data and saved snapshots for reproducibility.

Primary sources / proxies include:

- FRED / EIA WTI Cushing spot data,
- Yahoo Finance `CL=F` as a continuous front-month WTI futures proxy,
- EIA historical NYMEX Contract 1-4 price tables.

See [data/README.md](data/README.md) for data provenance and caveats.

## Documentation

The README is intentionally written for a quick professional review.

For the full methodology:

- [Methodology](docs/methodology.md)
- [Producer hedge model](docs/hedge_model.md)
- [Basis risk](docs/basis_risk.md)
- [Risk metrics](docs/risk_metrics.md)
- [Hedge ladder](docs/hedge_book.md)
- [Validation](docs/validation.md)
- [Term structure](docs/term_structure.md)
- [Physical market context](docs/fundamentals.md)
- [Model limitations](docs/limitations.md)
- [Glossary](docs/glossary.md)

## Key limitations

This is an analytical research project, not an ETRM or production hedge-management system.

Important simplifications include:

- continuous futures rather than exact traded contracts,
- simplified month-end hedge timing,
- no transaction costs or margin modeling,
- simplified physical pricing,
- scenario-based Midland/Cushing basis analysis,
- no hedge-accounting or credit treatment,
- historical rather than live C1-C4 curve data.

A full discussion is in [docs/limitations.md](docs/limitations.md).

## Why this project exists

The project connects futures-market analysis with the economics of a physical energy business.

Instead of asking only whether WTI will rise or fall, it asks:

> What is the producer exposed to, which instrument offsets that risk, what remains after the hedge, and how stable is the model used to size it?

That is the core risk-management problem the repository is designed to demonstrate.

Educational and portfolio use only. Not investment advice.
