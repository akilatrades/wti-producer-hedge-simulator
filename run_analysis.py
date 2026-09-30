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
from src.term_structure import (
    add_curve_metrics,
    load_eia_monthly_curve,
    select_example_curves,
    summarize_curve_regimes,
)

START_DATE = "2015-01-01"
OUTPUT_DIR = Path("outputs")
CURVE_SNAPSHOT = Path(
    "data/eia_wti_curve_monthly_2015_2024.csv"
)


def load_market_data():
    """Load the spot and continuous futures data used by the hedge model."""
    print("Downloading WTI spot data from FRED...")
    spot = web.DataReader(
        "DCOILWTICO",
        "fred",
        START_DATE,
    )["DCOILWTICO"]

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


def load_curve_data():
    """Load historical C1-C4 WTI futures prices.

    The project first tries the EIA historical tables. If that request is not
    available, it uses the saved project snapshot so the analysis can still
    be reproduced.
    """
    print("Loading historical WTI futures-curve data...")

    try:
        return load_eia_monthly_curve(start=START_DATE)
    except Exception as exc:
        if not CURVE_SNAPSHOT.exists():
            raise

        print(
            "EIA curve download was unavailable; "
            "using the saved project snapshot."
        )
        print(f"Reason: {exc}")

        return pd.read_csv(
            CURVE_SNAPSHOT,
            parse_dates=["date"],
            index_col="date",
        )


def make_hedge_charts(summary, simulations):
    """Create the main hedge-effectiveness charts."""
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
    plt.savefig(
        OUTPUT_DIR / "monthly_revenue_surprise.png",
        dpi=180,
    )
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
    plt.savefig(
        OUTPUT_DIR / "hedge_effectiveness.png",
        dpi=180,
    )
    plt.close()


def make_curve_charts(curve):
    """Create charts showing the shape of the WTI futures curve."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # C1-C4 through time:
    # positive = C1 above C4
    # negative = C1 below C4
    plt.figure(figsize=(12, 6))
    plt.plot(
        curve.index,
        curve["c1_c4_spread"],
        linewidth=1.6,
    )
    plt.axhline(0, linewidth=1)
    plt.title(
        "WTI Term Structure: Contract 1 Minus Contract 4"
    )
    plt.ylabel("C1 - C4 Spread ($/bbl)")
    plt.xlabel("Month")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "term_structure_c1_c4_spread.svg"
    )
    plt.close()

    # Compare one strong backwardation observation with one strong contango
    # observation so the two shapes can be seen directly.
    examples = select_example_curves(curve)
    contract_numbers = [1, 2, 3, 4]

    plt.figure(figsize=(9, 6))

    for date, row in examples.iterrows():
        prices = [
            row["contract_1"],
            row["contract_2"],
            row["contract_3"],
            row["contract_4"],
        ]

        plt.plot(
            contract_numbers,
            prices,
            marker="o",
            label=f"{date:%b %Y} - {row['curve_regime']}",
        )

    plt.xticks(
        contract_numbers,
        ["C1", "C2", "C3", "C4"],
    )
    plt.title("Examples of WTI Futures Curve Shapes")
    plt.xlabel("Delivery position")
    plt.ylabel("Price ($/bbl)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "term_structure_curve_examples.svg"
    )
    plt.close()


def run_hedge_analysis():
    """Run the producer hedge comparison."""
    spot, futures = load_market_data()
    market = prepare_monthly_market_data(
        spot,
        futures,
    )

    assumptions = HedgeAssumptions(
        monthly_production_bbl=100_000
    )

    summary, simulations = compare_hedge_ratios(
        market,
        hedge_ratios=(0, 0.25, 0.50, 0.75, 1.00),
        assumptions=assumptions,
    )

    summary.to_csv(
        OUTPUT_DIR / "hedge_ratio_summary.csv",
        index=False,
    )
    market.to_csv(
        OUTPUT_DIR / "monthly_market_data.csv"
    )

    make_hedge_charts(
        summary,
        simulations,
    )

    print("\nHedge comparison")
    print(summary.to_string(index=False))


def run_curve_analysis():
    """Run the WTI futures-curve analysis."""
    curve = load_curve_data()

    curve = add_curve_metrics(
        curve,
        flat_threshold=0.25,
    )

    summary = summarize_curve_regimes(curve)
    examples = select_example_curves(curve)

    curve.to_csv(
        OUTPUT_DIR / "term_structure_monthly.csv"
    )
    summary.to_csv(
        OUTPUT_DIR / "term_structure_regime_summary.csv",
        index=False,
    )
    examples.to_csv(
        OUTPUT_DIR / "term_structure_example_curves.csv"
    )

    make_curve_charts(curve)

    print("\nWTI futures-curve summary")
    display = summary.copy()
    display["share_of_sample"] = (
        display["share_of_sample"] * 100
    ).round(1)
    display["average_c1_c4_spread"] = (
        display["average_c1_c4_spread"].round(2)
    )
    display["average_front_month_price"] = (
        display["average_front_month_price"].round(2)
    )
    print(display.to_string(index=False))


def main():
    """Run the project analyses and refresh the saved outputs."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    run_hedge_analysis()
    run_curve_analysis()


if __name__ == "__main__":
    main()
