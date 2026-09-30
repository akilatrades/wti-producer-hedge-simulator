# Data

The project uses two main price series: WTI Cushing spot prices for the physical side and WTI futures prices for the hedge.

The saved analysis covers February 2015 through July 2026.

Public copies used for the saved results:

- [WTI spot dataset](https://github.com/datasets/oil-prices)
- [WTI futures history](https://github.com/JavierLuqueGarcia/Crude-oil-Backtest)

## Continuous futures data

The futures history is a continuous front-month series.

A continuous series links several futures contracts together to create one long price history. That is useful for this analysis, but it is not the same as tracking the exact monthly contract a producer would trade.

A live hedge program would need contract-specific prices, expiration and roll dates, transaction costs, margin, production changes, and location or quality differences.

## WTI futures-curve data

The project also uses four historical WTI futures delivery positions from the U.S. Energy Information Administration (EIA).

The easiest way to read them is:

```text
Contract 1 / C1 = nearest delivery position in the EIA history
Contract 2 / C2 = next delivery position
Contract 3 / C3 = next one after that
Contract 4 / C4 = fourth delivery position
```

C1 is **not one permanent contract**. It means the nearest position at each point in the historical series, so the exact contract represented by C1 changes through time.

The saved file is:

`eia_wti_curve_monthly_2015_2024.csv`

Each row contains C1, C2, C3, and C4 prices for the same monthly observation. Keeping the four prices on the same row lets us compare nearer and later delivery without mixing different dates.

The project keeps this saved snapshot for reproducibility. If the EIA webpage is temporarily unavailable, the analysis can still run from the CSV.

Important limitation: EIA notes that this NYMEX futures-price history is not available after April 5, 2024. This dataset is therefore used for historical learning and research, not as a live WTI curve feed.

Sources:

- https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm
- https://www.eia.gov/dnav/pet/TblDefs/pet_pri_fut_tbldef2.asp

