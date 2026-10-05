# Documentation

This folder contains the detailed methodology and beginner explanations for the WTI Producer Hedging & Market Risk Analytics project.

The top-level `README.md` is intentionally concise. It is written for a recruiter, hiring manager, trader, risk manager, or engineer who wants to understand the project quickly. The pages here provide the technical detail behind that summary.

## Recommended reading order

1. [Methodology](methodology.md) — how the project is organized and how the analyses connect.
2. [Producer hedge model](hedge_model.md) — physical exposure, futures P&L, and hedge effectiveness.
3. [Basis risk](basis_risk.md) — Midland versus Cushing location exposure.
4. [Risk metrics](risk_metrics.md) — volatility, VaR, Expected Shortfall, and downside analysis.
5. [Hedge book and ladder](hedge_book.md) — mapping expected production to futures contracts.
6. [Model validation](validation.md) — walk-forward testing and bootstrap uncertainty.
7. [Term structure](term_structure.md) — C1-C4 spreads, curve regimes, slope, curvature, and z-scores.
8. [Physical market context](fundamentals.md) — optional EIA fundamental data and how it can be joined to the curve analysis.
9. [Data dictionary](data_dictionary.md) — field definitions.
10. [Limitations](limitations.md) — assumptions and what would be required for production use.
11. [Glossary](glossary.md) — plain-English definitions.

## Design principle

Each analytical section is written in two layers:

**Business interpretation** explains why the analysis matters to a producer, trader, or risk manager.

**Methodology** explains the calculation, assumptions, and implementation.

That keeps the project readable for a beginner without removing the detail needed by a technical reviewer.
