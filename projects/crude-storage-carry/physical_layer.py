"""Descriptive monthly carry / weekly Cushing inventory alignment."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen

import matplotlib.pyplot as plt
import pandas as pd

SOURCE = "https://www.eia.gov/dnav/pet/hist_xls/W_EPC0_SAX_YCUOK_MBBLw.xls"


def align_monthly(carry, stocks):
    stocks = stocks.copy()
    stocks["date"] = pd.to_datetime(stocks.date)
    if stocks.date.duplicated().any() or stocks.stocks_thousand_bbl.isna().any():
        raise ValueError("Unique dated inventory observations required")
    grouped = stocks.sort_values("date").set_index("date").stocks_thousand_bbl.resample("MS")
    monthly = pd.DataFrame({"mean_stocks_million_bbl": grouped.mean() / 1000,
                            "last_stocks_million_bbl": grouped.last() / 1000,
                            "weekly_observations": grouped.count()})
    monthly["stock_change_million_bbl"] = monthly.last_stocks_million_bbl.diff()
    carry = carry.copy()
    carry["date"] = pd.to_datetime(carry.date).dt.to_period("M").dt.to_timestamp()
    if carry.date.duplicated().any():
        raise ValueError("Only one carry observation per month is allowed")
    joined = carry.set_index("date").join(monthly, how="left")
    if joined.isna().any().any() or (joined.weekly_observations < 4).any():
        raise ValueError("Missing inventory coverage; do not interpolate")
    joined["carry_covers_costs"] = joined.net_carry > 0
    joined["stocks_build"] = joined.stock_change_million_bbl > 0
    return joined


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    data = Path("data/cushing_weekly_2014_2024.csv")
    out = Path("outputs/physical_layer")
    out.mkdir(parents=True, exist_ok=True)
    if args.download:
        with urlopen(SOURCE, timeout=60) as response:
            raw = response.read()
        frame = pd.read_excel(io.BytesIO(raw), sheet_name="Data 1", skiprows=2)
        frame = frame.iloc[:, :2]
        frame.columns = ["date", "stocks_thousand_bbl"]
        frame["date"] = pd.to_datetime(frame.date)
        frame = frame[(frame.date >= "2014-12-01") & (frame.date < "2024-04-01")]
        frame.to_csv(data, index=False)
        (out / "retrieval.json").write_text(json.dumps({"url": SOURCE,
            "download_sha256": hashlib.sha256(raw).hexdigest(),
            "retrieved_utc": pd.Timestamp.now(tz="UTC").isoformat()}, indent=2) + "\n")
    stocks = pd.read_csv(data)
    carry = pd.read_csv("outputs/carry_history.csv")
    aligned = align_monthly(carry, stocks)
    aligned.to_csv(out / "monthly_alignment.csv")
    aligned.loc["2020"].to_csv(out / "2020_detail.csv")
    rows = []
    for sample, frame in [("all", aligned), ("excluding_2020", aligned[aligned.index.year != 2020])]:
        for positive, group in frame.groupby("carry_covers_costs"):
            rows.append(dict(sample=sample, carry_covers_costs=bool(positive), months=len(group),
                             build_months=int(group.stocks_build.sum()), build_share=group.stocks_build.mean(),
                             mean_monthly_stock_change_million_bbl=group.stock_change_million_bbl.mean(),
                             mean_stocks_million_bbl=group.mean_stocks_million_bbl.mean()))
    pd.DataFrame(rows).to_csv(out / "regime_comparison.csv", index=False)
    metadata = dict(source=SOURCE, units="EIA thousand barrels converted to million barrels",
                    input_sha256=hashlib.sha256(data.read_bytes()).hexdigest(),
                    interpretation="Contemporaneous descriptive association; no causality or tradable signal claimed",
                    time_alignment="Monthly average C1/C4 vs monthly mean weekly stocks; change uses last weekly observation each month",
                    publication_warning="Stock dates are week-ending dates, not release timestamps. No point-in-time prediction or trading backtest.",
                    carry_stock_change_correlation=aligned.net_carry.corr(aligned.stock_change_million_bbl),
                    correlation_excluding_2020=aligned.loc[aligned.index.year != 2020, "net_carry"].corr(
                        aligned.loc[aligned.index.year != 2020, "stock_change_million_bbl"]))
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axes[0].plot(aligned.index, aligned.net_carry, color="#2563eb")
    axes[0].axhline(0, color="black", lw=.7)
    axes[0].set(ylabel="Net carry ($/bbl)", title="Storage incentives and Cushing stocks: descriptive monthly comparison")
    axes[1].plot(aligned.index, aligned.mean_stocks_million_bbl, color="#059669")
    axes[1].set(ylabel="Stocks (million bbl)")
    for ax in axes:
        ax.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2021-01-01"), color="gray", alpha=.15)
    fig.tight_layout()
    fig.savefig(out / "carry_and_cushing.svg")
    plt.close(fig)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
