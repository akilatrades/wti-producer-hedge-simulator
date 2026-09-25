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

START_DATE = "2018-01-01"
OUTPUT_DIR = Path("outputs")


def load_market_data():
    print("Downloading WTI spot data from FRED...")
    spot = web.DataReader("DCOILWTICO", "fred", START_DATE)["DCOILWTICO"]

    print("Downloading front-month WTI futures proxy from Yahoo Finance...")
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

    plt.figure(figsize=(10, 6))
    for ratio in [0.0, 0.5, 1.0]:
        sim = simulations[ratio]
        plt.plot(
            sim.index,
            sim["hedged_revenue"] / 1_000_000,
            label=f"{int(ratio * 100)}% hedged",
        )
    plt.title("Monthly Producer Revenue by Hedge Ratio")
    plt.ylabel("Revenue ($MM)")
    plt.xlabel("Month")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue_comparison.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 6))
    plt.plot(
        summary["hedge_ratio"] * 100,
        summary["monthly_revenue_std"] / 1_000_000,
        marker="o",
    )
    plt.title("Revenue Volatility vs Hedge Ratio")
    plt.xlabel("Hedge Ratio (%)")
    plt.ylabel("Monthly Revenue Std. Dev. ($MM)")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "revenue_volatility_by_hedge_ratio.png",
        dpi=180,
    )
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

    for ratio, sim in simulations.items():
        sim.to_csv(
            OUTPUT_DIR / f"simulation_{int(ratio * 100)}pct_hedged.csv"
        )

    make_charts(summary, simulations)

    cols = [
        "hedge_ratio",
        "contracts_short",
        "avg_monthly_revenue",
        "monthly_revenue_std",
        "p05_monthly_revenue",
        "minimum_monthly_revenue",
        "hedge_effectiveness",
    ]

    print("\nHedge comparison")
    print(summary[cols].to_string(index=False))


if __name__ == "__main__":
    main()
