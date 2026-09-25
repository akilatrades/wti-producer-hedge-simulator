from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from pandas_datareader import data as web

from src.hedge_engine import (
    HedgeAssumptions,
    compare_hedge_ratios,
    prepare_monthly_market_data,
)

START_DATE = "2015-01-01"
OUTPUT_DIR = Path("outputs")


def load_market_data():
    print("Downloading WTI spot data from FRED...")
    spot = web.DataReader("DCOILWTICO", "fred", START_DATE)["DCOILWTICO"]

    print("Downloading continuous front-month WTI futures proxy...")
    futures = yf.download(
        "CL=F",
        start=START_DATE,
        auto_adjust=False,
        progress=False,
    )

    if isinstance(futures.columns, pd.MultiIndex):
        close = futures["Close"].iloc[:, 0]
    else:
        close = futures["Close"]

    close.name = "CL=F"
    return spot, close


def make_charts(summary, simulations):
    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(11, 6))
    for ratio in [0.0, 0.5, 1.0]:
        sim = simulations[ratio]
        plt.plot(
            sim.index,
            sim["revenue_surprise"] / 1_000_000,
            label=f"{int(ratio * 100)}% hedged",
        )
    plt.axhline(0, linewidth=1)
    plt.title("Monthly Revenue Surprise: Unhedged vs Hedged")
    plt.ylabel("Revenue Surprise ($MM)")
    plt.xlabel("Month")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue_surprise.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 6))
    plt.plot(
        summary["hedge_ratio"] * 100,
        summary["hedge_effectiveness"] * 100,
        marker="o",
    )
    plt.title("Hedge Effectiveness by Hedge Ratio")
    plt.xlabel("Hedge Ratio (%)")
    plt.ylabel("Variance Reduction (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "hedge_effectiveness.png", dpi=180)
    plt.close()


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    spot, futures = load_market_data()
    market = prepare_monthly_market_data(spot, futures)

    assumptions = HedgeAssumptions(monthly_production_bbl=100_000)
    summary, simulations = compare_hedge_ratios(
        market,
        hedge_ratios=(0, 0.25, 0.50, 0.75, 1.00),
        assumptions=assumptions,
    )

    summary.to_csv(OUTPUT_DIR / "hedge_ratio_summary.csv", index=False)
    market.to_csv(OUTPUT_DIR / "monthly_market_data.csv")
    make_charts(summary, simulations)

    print("\nHedge comparison")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
