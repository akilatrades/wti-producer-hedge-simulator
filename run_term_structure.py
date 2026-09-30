"""Run Module 2: WTI futures-curve analysis.

This script prints each stage of the analysis as it runs, from raw C1-C4 prices to the final curve labels.

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
    """Load historical C1-C4 prices.

    The script first tries the EIA website. If that is unavailable, it uses
    the saved CSV snapshot in this repository.
    """
    print("=" * 72)
    print("MODULE 2 - WTI FUTURES CURVE / TERM STRUCTURE")
    print("=" * 72)
    print()
    print("What are we doing?")
    print(
        "We are comparing four WTI futures delivery positions at the "
        "same point in time."
    )
    print(
        "C1 is the nearest delivery position in the EIA history. "
        "C2, C3, and C4 are the next three positions."
    )
    print(
        "The goal is to see whether nearby WTI is priced above, below, "
        "or close to later delivery."
    )
    print()

    try:
        print("STEP 1 - Load the historical C1, C2, C3, and C4 prices.")
        print(
            "Trying to read the EIA historical tables directly..."
        )
        curve = load_eia_monthly_curve(start="2015-01-01")
        print("EIA data loaded successfully.")
        print()
        return curve
    except Exception as exc:
        if not SNAPSHOT_PATH.exists():
            raise

        print("The live EIA download was not available.")
        print(f"Technical reason: {exc}")
        print(
            "That is okay. We will use the saved EIA snapshot included "
            "with the project instead."
        )
        print()
        return pd.read_csv(
            SNAPSHOT_PATH,
            parse_dates=["date"],
            index_col="date",
        )


def explain_first_row(curve: pd.DataFrame) -> None:
    """Show one real row before any spread calculations are added."""
    first_date = curve.index[0]
    first = curve.iloc[0]

    print("STEP 2 - Look at one row before doing any math.")
    print()
    print(f"Example month: {first_date:%B %Y}")
    print(f"C1 price: USD {first['contract_1']:.2f}/bbl")
    print(f"C2 price: USD {first['contract_2']:.2f}/bbl")
    print(f"C3 price: USD {first['contract_3']:.2f}/bbl")
    print(f"C4 price: USD {first['contract_4']:.2f}/bbl")
    print()
    print(
        "These are four different delivery positions observed for the "
        "same month. We can now compare them."
    )
    print()


def explain_spread_math(curve_with_metrics: pd.DataFrame) -> None:
    """Walk through the C1-C4 subtraction using the first row."""
    first_date = curve_with_metrics.index[0]
    first = curve_with_metrics.iloc[0]

    c1 = first["contract_1"]
    c4 = first["contract_4"]
    spread = first["c1_c4_spread"]

    print("STEP 3 - Calculate calendar spreads.")
    print()
    print("The main spread in this module is:")
    print("    C1-C4 = C1 price - C4 price")
    print()
    print(f"Using {first_date:%B %Y}:")
    print(
        f"    USD {c1:.2f} - USD {c4:.2f} "
        f"= USD {spread:.2f}/bbl"
    )
    print()

    if spread > 0:
        print(
            "The result is positive, so C1 is more expensive than C4."
        )
    elif spread < 0:
        print(
            "The result is negative, so C1 is cheaper than C4."
        )
    else:
        print("The result is zero, so C1 and C4 have the same price.")

    print()
    print(
        "The script repeats this calculation for every month in the "
        "historical sample."
    )
    print()


def explain_regime_rule() -> None:
    """Explain how the spread is translated into a curve label."""
    print("STEP 4 - Turn the C1-C4 spread into a simple curve label.")
    print()
    print("This project uses the following classification rule:")
    print("    C1-C4 > +USD 0.25/bbl  -> backwardation")
    print("    C1-C4 < -USD 0.25/bbl  -> contango")
    print("    otherwise               -> flat")
    print()
    print(
        "The USD 0.25 threshold is only a project setting. It is not a "
        "universal market rule."
    )
    print()
    print(
        "Backwardation means nearby futures are above later futures."
    )
    print(
        "Contango means later futures are above nearby futures."
    )
    print(
        "These labels describe the curve shape. They are not guaranteed "
        "predictions of where WTI will move next."
    )
    print()


def make_charts(curve: pd.DataFrame) -> None:
    """Create two charts that connect the math to a picture."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Positive C1-C4 = near contract above C4 = backwardation.
    # Negative C1-C4 = near contract below C4 = contango.
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
    plt.xlabel("Delivery position")
    plt.ylabel("Price ($/bbl)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "term_structure_curve_examples.svg"
    )
    plt.close()


def print_summary(summary: pd.DataFrame) -> None:
    """Print the historical regime summary with beginner-friendly labels."""
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

    print("STEP 5 - Count how often each curve shape appeared.")
    print()
    print(display.to_string(index=False))
    print()
    print(
        "This table is descriptive. It tells us what the historical "
        "sample looked like; it does not say which regime is 'best'."
    )
    print()


def print_example_curves(examples: pd.DataFrame) -> None:
    """Explain why the example months were selected."""
    back_date = examples["c1_c4_spread"].idxmax()
    cont_date = examples["c1_c4_spread"].idxmin()

    strongest_backwardation = examples.loc[back_date]
    strongest_contango = examples.loc[cont_date]

    print("STEP 6 - Pick two examples so the curve shape is easy to see.")
    print()
    print(
        f"Strong backwardation example: {back_date:%B %Y}, "
        f"C1-C4 = USD "
        f"{strongest_backwardation['c1_c4_spread']:.2f}/bbl"
    )
    print(
        f"Strong contango example: {cont_date:%B %Y}, "
        f"C1-C4 = USD "
        f"{strongest_contango['c1_c4_spread']:.2f}/bbl"
    )
    print()
    print(
        "These are examples chosen from the historical sample. They are "
        "not trading recommendations."
    )
    print()


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    curve = load_curve_data()
    explain_first_row(curve)

    curve = add_curve_metrics(
        curve,
        flat_threshold=0.25,
    )
    explain_spread_math(curve)
    explain_regime_rule()

    summary = summarize_curve_regimes(curve)
    examples = select_example_curves(curve)

    print_summary(summary)
    print_example_curves(examples)

    print("STEP 7 - Save the tables and charts.")
    print()

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
    make_charts(curve)

    print("Created:")
    print("  outputs/term_structure_monthly.csv")
    print("  outputs/term_structure_regime_summary.csv")
    print("  outputs/term_structure_example_curves.csv")
    print("  outputs/term_structure_c1_c4_spread.svg")
    print("  outputs/term_structure_curve_examples.svg")
    print()
    print("FINAL TAKEAWAY")
    print(
        "WTI is not one single futures price. Different delivery periods "
        "can trade at different prices."
    )
    print(
        "This module measures those differences so we can describe the "
        "shape of the curve before connecting it to producer hedging."
    )
    print()
    print(
        "For the full beginner lesson, read "
        "outputs/TERM_STRUCTURE_README.md."
    )


if __name__ == "__main__":
    main()
