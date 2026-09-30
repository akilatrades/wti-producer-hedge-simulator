"""Run Module 2: WTI futures term-structure analysis.

Run from the project root with:

    python run_term_structure.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.term_structure import (
    add_curve_metrics,
    load_eia_monthly_curve,
    select_example_curves,
    summarize_curve_regimes,
)

OUTPUT_DIR = Path("outputs")
SNAPSHOT_PATH = Path(
    "data/eia_wti_curve_monthly_2015_2024.csv"
)


def load_curve_data() -> pd.DataFrame:
    """Prefer EIA directly; fall back to the saved project snapshot."""
    try:
        print(
            "STEP 1 - Downloading historical WTI Contract 1-4 "
            "prices from EIA..."
        )
        return load_eia_monthly_curve(start="2015-01-01")
    except Exception as exc:
        if not SNAPSHOT_PATH.exists():
            raise

        print("EIA download was not available.")
        print(f"Reason: {exc}")
        print(
            "Using the saved EIA snapshot included in data/ instead.\n"
        )
        return pd.read_csv(
            SNAPSHOT_PATH,
            parse_dates=["date"],
            index_col="date",
        )


def make_charts(curve: pd.DataFrame) -> None:
    """Create two simple charts that explain the curve visually."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Chart 1:
    # Above zero = backwardation.
    # Below zero = contango.
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

    # Chart 2:
    # Show one strong backwardation month and one strong contango month.
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
        label = (
            f"{date:%b %Y} - "
            f"{row['curve_regime']}"
        )
        plt.plot(
            contract_numbers,
            prices,
            marker="o",
            label=label,
        )

    plt.xticks(
        contract_numbers,
        ["C1", "C2", "C3", "C4"],
    )
    plt.title("Examples of WTI Futures Curve Shapes")
    plt.xlabel("Delivery contract")
    plt.ylabel("Price ($/bbl)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "term_structure_curve_examples.svg"
    )
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    curve = load_curve_data()

    print("STEP 2 - Calculating calendar spreads...")
    print(
        "We calculate C1-C2, C1-C3, and C1-C4 by subtracting "
        "later prices from the nearest contract price.\n"
    )

    curve = add_curve_metrics(
        curve,
        flat_threshold=0.25,
    )

    print(
        "STEP 3 - Labeling each month as backwardation, "
        "contango, or flat..."
    )
    print(
        "Positive C1-C4 above $0.25/bbl = backwardation."
    )
    print(
        "Negative C1-C4 below -$0.25/bbl = contango."
    )
    print(
        "Anything in between is labeled flat.\n"
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

    print(
        "STEP 4 - Creating charts and saving output files..."
    )
    make_charts(curve)

    print("\nCurve-regime summary")
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

    print("\nSTEP 5 - Finished.")
    print(
        "Open outputs/TERM_STRUCTURE_README.md for the "
        "plain-English walkthrough."
    )


if __name__ == "__main__":
    main()
