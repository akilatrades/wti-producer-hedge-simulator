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

## WTI term-structure data

Module 2 adds the first four historical WTI futures contracts from the U.S. Energy Information Administration (EIA).

The EIA labels them Contract 1 through Contract 4. Contract 1 is the nearest delivery contract in the historical series and Contracts 2-4 are the successive delivery months.

The project keeps a monthly snapshot in `eia_wti_curve_monthly_2015_2024.csv` so the analysis remains reproducible if the EIA webpage is temporarily unavailable.

Important limitation: EIA notes that its NYMEX futures-price history is not available after April 5, 2024. This dataset is therefore used for historical term-structure research, not as a live WTI curve feed.

Sources:

- https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm
- https://www.eia.gov/dnav/pet/TblDefs/pet_pri_fut_tbldef2.asp

