# Changelog

## 1.0.0

Stable v1 release. The planned core scope is complete and active feature development is paused.

### Finalized

- core producer-hedging, basis-risk, term-structure, risk-metric, and validation workflow
- saved headline results and plain-language interpretation on the project landing page
- automated validation across supported Python versions
- version metadata aligned to the stable v1 release
- future work reserved for maintenance, data refreshes, or clearly scoped extensions

## 0.2.0

Major project upgrade focused on market-risk analysis and reproducibility.

### Added

- historical VaR and Expected Shortfall
- downside-risk comparison across hedge ratios
- flat-price P&L attribution
- multi-month producer hedge ladder
- production-volume uncertainty and over-hedging scenarios
- walk-forward minimum-variance validation
- bootstrap confidence intervals for hedge ratios
- curve curvature, rolling z-score, and percentile features
- curve-regime behavior summaries
- optional physical-market fundamentals framework
- modular documentation under `docs/`
- pytest test suite
- GitHub Actions CI
- project metadata in `pyproject.toml`

### Documentation

- redesigned the top-level README for a concise review of the business question, methods, results, and limitations
- added a five-minute project review path and concise skills summary
- moved the original combined notebook into `notebooks/archive/` so the guided notebooks are the canonical review path
- kept detailed methodology and supporting explanations under `docs/`
