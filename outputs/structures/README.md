# Producer hedge comparison

`revenue_comparison.csv` is a seeded **synthetic risk-neutral terminal distribution** under the parameters in `assumptions.json`. It reports total producer revenue, its standard deviation, fifth percentile and average worst-5% outcome. It is not a historical strategy backtest.

`payoffs.csv` and `payoffs.svg` show exact expiry outcomes, including negative terminal stress prices. The ordinary collar retains its reference-price floor; the three-way loses that floor below the sold put. Futures and swaps coincide only because settlement timing, collateral and funding are excluded.

`observed_benchmark_basis.csv` derives Cushing spot minus the front-month proxy from the original committed monthly history. `basis_summary.csv` summarizes that series. It is **not** Midland–Cushing location data. `basis_stress.csv` applies separately labeled, assumed location spreads to each hedge structure.

Reproduce with `python run_structures.py` from the repository root.
