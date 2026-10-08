from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from pandas_datareader import data as web

from src.basis_risk import compare_basis_scenarios
from src.fundamentals import (
    join_curve_and_fundamentals,
    prepare_fundamentals,
    summarize_fundamentals_by_regime,
)
from src.hedge_engine import (
    HedgeAssumptions,
    compare_hedge_ratios,
    prepare_monthly_market_data,
)
from src.hedge_ladder import build_hedge_ladder, policy_schedule
from src.min_variance import (
    contracts_for_hedge_ratio,
    hedge_ratio_diagnostics,
    minimum_variance_hedge_ratio,
    rolling_minimum_variance_hedge_ratio,
)
from src.pnl_attribution import attribute_flat_price
from src.risk_metrics import compare_hedge_risk
from src.scenarios import production_volume_scenarios
from src.term_structure import (
    add_curve_features,
    add_curve_metrics,
    load_eia_monthly_curve,
    select_example_curves,
    summarize_curve_regimes,
    summarize_regime_behavior,
)
from src.validation import (
    bootstrap_minimum_variance_ratio,
    summarize_walk_forward,
    walk_forward_min_variance,
)

START_DATE = "2015-01-01"
OUTPUT_DIR = Path("outputs")
CURVE_SNAPSHOT = Path("data/eia_wti_curve_monthly_2015_2024.csv")
FUNDAMENTALS_FILE = Path("data/eia_physical_fundamentals.csv")


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
    """Load historical C1-C4 WTI futures prices with snapshot fallback."""
    print("Loading historical WTI futures-curve data...")

    try:
        return load_eia_monthly_curve(start=START_DATE)
    except Exception as exc:
        if not CURVE_SNAPSHOT.exists():
            raise

        print("EIA curve download was unavailable; using the saved project snapshot.")
        print(f"Reason: {exc}")

        return pd.read_csv(
            CURVE_SNAPSHOT,
            parse_dates=["date"],
            index_col="date",
        )


def make_hedge_charts(summary, simulations):
    """Create hedge-effectiveness and revenue-surprise charts."""
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
    plt.savefig(OUTPUT_DIR / "revenue_surprise_history.svg")
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
    plt.savefig(OUTPUT_DIR / "hedge_effectiveness.svg")
    plt.close()


def make_risk_chart(risk_summary):
    """Compare historical 95% VaR and Expected Shortfall by hedge ratio."""
    plt.figure(figsize=(9, 6))
    x = risk_summary["hedge_ratio"] * 100
    plt.plot(
        x,
        risk_summary["historical_var_95"] / 1_000,
        marker="o",
        label="95% VaR",
    )
    plt.plot(
        x,
        risk_summary["historical_es_95"] / 1_000,
        marker="o",
        label="95% ES",
    )
    plt.title("Historical Downside Risk by Hedge Ratio")
    plt.xlabel("Hedge Ratio (%)")
    plt.ylabel("Modeled Monthly Loss ($000)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "risk_tail_comparison.svg")
    plt.close()


def make_min_variance_charts(comparison, rolling):
    """Create minimum-variance comparison and rolling-ratio charts."""
    plt.figure(figsize=(9, 6))
    plt.plot(
        comparison["hedge_ratio"] * 100,
        comparison["residual_price_std"],
        marker="o",
    )
    plt.title("Residual Monthly Price Risk by Hedge Ratio")
    plt.xlabel("Hedge Ratio (%)")
    plt.ylabel("Residual Price-Change Std. Dev. ($/bbl)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "min_variance_comparison.svg")
    plt.close()

    plt.figure(figsize=(11, 6))
    plt.plot(rolling.index, rolling.values)
    plt.axhline(1.0, linewidth=1)
    plt.title("Rolling 24-Month Minimum-Variance Hedge Ratio")
    plt.xlabel("Month")
    plt.ylabel("Estimated Hedge Ratio")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rolling_min_variance_ratio.svg")
    plt.close()


def make_curve_charts(curve):
    """Create charts showing WTI term-structure behavior."""
    plt.figure(figsize=(12, 6))
    plt.plot(curve.index, curve["c1_c4_spread"], linewidth=1.6)
    plt.axhline(0, linewidth=1)
    plt.title("WTI Term Structure: Contract 1 Minus Contract 4")
    plt.ylabel("C1 - C4 Spread ($/bbl)")
    plt.xlabel("Month")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "term_structure_c1_c4_spread.svg")
    plt.close()

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

    plt.xticks(contract_numbers, ["C1", "C2", "C3", "C4"])
    plt.title("Examples of WTI Futures Curve Shapes")
    plt.xlabel("Delivery Position")
    plt.ylabel("Price ($/bbl)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "term_structure_curve_examples.svg")
    plt.close()


def run_hedge_analysis(market):
    """Run fixed-ratio hedging, risk metrics, attribution, and scenarios."""
    assumptions = HedgeAssumptions(monthly_production_bbl=100_000)
    ratios = (0, 0.25, 0.50, 0.75, 1.00)

    summary, simulations = compare_hedge_ratios(
        market,
        hedge_ratios=ratios,
        assumptions=assumptions,
    )

    summary.to_csv(OUTPUT_DIR / "hedge_ratio_summary.csv", index=False)

    monthly = market.copy()
    for ratio in ratios:
        label = f"revenue_surprise_{int(ratio * 100)}pct"
        monthly[label] = simulations[ratio]["revenue_surprise"]
    monthly.index.name = "month"
    monthly.to_csv(OUTPUT_DIR / "monthly_analysis.csv")

    risk_summary = compare_hedge_risk(simulations)
    risk_summary.to_csv(OUTPUT_DIR / "risk_summary.csv", index=False)

    attribution_rows = []
    for ratio in ratios:
        attributed = attribute_flat_price(simulations[ratio]).copy()
        attributed.insert(0, "hedge_ratio", ratio)
        attribution_rows.append(attributed)
    attribution = pd.concat(attribution_rows).sort_index()
    attribution.to_csv(OUTPUT_DIR / "pnl_attribution.csv")

    production_scenarios = production_volume_scenarios(
        expected_production_bbl=100_000,
        hedge_ratio=0.75,
        spot_exit=60.0,
        futures_entry=75.0,
        futures_exit=60.0,
    )
    production_scenarios.to_csv(
        OUTPUT_DIR / "production_uncertainty_scenarios.csv",
        index=False,
    )

    months = pd.date_range("2027-01-31", periods=6, freq="ME")
    ladder_input = policy_schedule(
        production_months=months,
        expected_production_bbl=[
            100_000,
            100_000,
            98_000,
            96_000,
            95_000,
            95_000,
        ],
        hedge_ratios=[0.80, 0.70, 0.60, 0.40, 0.40, 0.40],
        futures_contracts=[
            "CLG27",
            "CLH27",
            "CLJ27",
            "CLK27",
            "CLM27",
            "CLN27",
        ],
        futures_prices=[70.0, 70.4, 70.8, 71.1, 71.4, 71.6],
    )
    ladder = build_hedge_ladder(ladder_input)
    ladder.to_csv(
        OUTPUT_DIR / "illustrative_hedge_ladder.csv",
        index=False,
    )

    make_hedge_charts(summary, simulations)
    make_risk_chart(risk_summary)

    print("\nFixed-ratio hedge comparison")
    print(summary.to_string(index=False))

    return summary, simulations, risk_summary


def run_basis_analysis():
    """Run simplified Midland/Cushing basis stress scenarios."""
    basis = compare_basis_scenarios()
    basis.to_csv(OUTPUT_DIR / "basis_risk_scenarios.csv", index=False)

    print("\nBasis-risk scenarios")
    display_cols = [
        "basis_hedge_ratio",
        "realized_midland_basis",
        "residual_revenue_risk",
    ]
    print(basis[display_cols].to_string(index=False))

    return basis


def run_min_variance_analysis(market):
    """Estimate, validate, and stress the minimum-variance hedge ratio."""
    static_ratio = minimum_variance_hedge_ratio(market)
    rounded_contracts = contracts_for_hedge_ratio(100_000, static_ratio)
    rounded_ratio = rounded_contracts * 1_000 / 100_000

    static_diag = hedge_ratio_diagnostics(market, static_ratio)
    rounded_diag = hedge_ratio_diagnostics(market, rounded_ratio)

    summary = pd.DataFrame(
        [
            ["observations", static_diag["observations"]],
            [
                "spot_futures_change_correlation",
                static_diag["spot_futures_change_correlation"],
            ],
            ["static_min_variance_hedge_ratio", static_ratio],
            ["rounded_cl_contracts_for_100000_bbl", rounded_contracts],
            ["rounded_hedge_ratio", rounded_ratio],
            [
                "unhedged_monthly_price_change_std",
                static_diag["unhedged_price_change_std"],
            ],
            [
                "rounded_optimal_residual_std",
                rounded_diag["residual_price_change_std"],
            ],
            [
                "rounded_optimal_variance_reduction",
                rounded_diag["variance_reduction"],
            ],
        ],
        columns=["metric", "value"],
    )
    summary.to_csv(
        OUTPUT_DIR / "min_variance_summary.csv",
        index=False,
    )

    comparison_ratios = [0.0, 0.50, 0.75, 1.00, rounded_ratio]
    comparison_rows = []
    for ratio in comparison_ratios:
        diag = hedge_ratio_diagnostics(market, ratio)
        comparison_rows.append(
            {
                "hedge_ratio": ratio,
                "contracts_short": contracts_for_hedge_ratio(
                    100_000,
                    ratio,
                ),
                "residual_price_std": diag["residual_price_change_std"],
                "variance_reduction": diag["variance_reduction"],
            }
        )

    comparison = (
        pd.DataFrame(comparison_rows)
        .drop_duplicates(subset=["hedge_ratio"])
        .sort_values("hedge_ratio")
    )
    comparison.to_csv(
        OUTPUT_DIR / "min_variance_comparison.csv",
        index=False,
    )

    rolling = rolling_minimum_variance_hedge_ratio(
        market,
        window=24,
    )
    rolling.to_csv(
        OUTPUT_DIR / "rolling_min_variance_ratio.csv",
        header=True,
    )

    walk = walk_forward_min_variance(market, window=24)
    walk.to_csv(OUTPUT_DIR / "walk_forward_validation.csv")
    walk_summary = pd.DataFrame([summarize_walk_forward(walk)])
    walk_summary.to_csv(
        OUTPUT_DIR / "walk_forward_validation_summary.csv",
        index=False,
    )

    bootstrap_summary, bootstrap_samples = bootstrap_minimum_variance_ratio(
        market,
        n_bootstrap=5_000,
        confidence=0.95,
        seed=42,
    )
    bootstrap_summary.to_csv(
        OUTPUT_DIR / "bootstrap_hedge_ratio_summary.csv",
        index=False,
    )
    bootstrap_samples.to_csv(
        OUTPUT_DIR / "bootstrap_hedge_ratio_samples.csv",
        index=False,
    )

    make_min_variance_charts(comparison, rolling)

    print("\nMinimum-variance hedge ratio")
    print(summary.to_string(index=False))

    return summary, comparison, walk_summary, bootstrap_summary


def run_curve_analysis():
    """Run descriptive WTI term-structure and curve-regime analysis."""
    curve = load_curve_data()
    curve = add_curve_metrics(curve, flat_threshold=0.25)
    curve = add_curve_features(curve, zscore_window=24)

    regime_summary = summarize_curve_regimes(curve)
    regime_behavior = summarize_regime_behavior(curve)
    examples = select_example_curves(curve)

    curve.to_csv(OUTPUT_DIR / "term_structure_monthly.csv")
    regime_summary.to_csv(
        OUTPUT_DIR / "term_structure_regime_summary.csv",
        index=False,
    )
    regime_behavior.to_csv(
        OUTPUT_DIR / "term_structure_regime_behavior.csv",
        index=False,
    )
    examples.to_csv(OUTPUT_DIR / "term_structure_example_curves.csv")

    make_curve_charts(curve)

    print("\nWTI futures-curve summary")
    display = regime_summary.copy()
    display["share_of_sample"] = (display["share_of_sample"] * 100).round(1)
    display["average_c1_c4_spread"] = display["average_c1_c4_spread"].round(2)
    display["average_front_month_price"] = display["average_front_month_price"].round(2)
    print(display.to_string(index=False))

    return curve, regime_summary, regime_behavior


def run_optional_fundamentals(curve):
    """Join optional physical-market data if a populated file is present."""
    if not FUNDAMENTALS_FILE.exists():
        print(
            "\nOptional fundamentals file not found; "
            "skipping physical-market context module."
        )
        return None

    raw = pd.read_csv(
        FUNDAMENTALS_FILE,
        parse_dates=["date"],
    )
    if raw.empty:
        print(
            "\nOptional fundamentals file is empty; "
            "skipping physical-market context module."
        )
        return None

    prepared = prepare_fundamentals(raw)
    combined = join_curve_and_fundamentals(curve, prepared)
    summary = summarize_fundamentals_by_regime(combined)

    prepared.to_csv(OUTPUT_DIR / "physical_fundamentals_features.csv")
    combined.to_csv(OUTPUT_DIR / "curve_and_fundamentals.csv")
    summary.to_csv(
        OUTPUT_DIR / "fundamentals_by_curve_regime.csv",
        index=False,
    )
    return summary


def write_executive_summary(
    hedge_summary,
    min_variance_summary,
    walk_summary,
    bootstrap_summary,
):
    """Write a concise management-style summary using generated results."""
    row_75 = hedge_summary.loc[hedge_summary["hedge_ratio"].sub(0.75).abs().idxmin()]
    row_100 = hedge_summary.loc[hedge_summary["hedge_ratio"].sub(1.00).abs().idxmin()]

    min_values = dict(
        zip(
            min_variance_summary["metric"],
            min_variance_summary["value"],
        )
    )
    boot = bootstrap_summary.iloc[0]
    walk = walk_summary.iloc[0]

    text = f"""# Executive Summary

## Objective

Evaluate how WTI futures can reduce monthly price risk for an illustrative producer with 100,000 barrels of expected monthly production, while making residual basis, volume, curve, and model risk explicit.

## Key historical findings

- 75% fixed hedge effectiveness: **{row_75["hedge_effectiveness"]:.1%}** variance reduction.
- 100% fixed hedge effectiveness: **{row_100["hedge_effectiveness"]:.1%}** variance reduction.
- Static minimum-variance hedge ratio: **{min_values["static_min_variance_hedge_ratio"]:.3f}**.
- Rounded minimum-variance implementation: **{int(min_values["rounded_cl_contracts_for_100000_bbl"])} CL contracts**.
- Rounded minimum-variance variance reduction: **{min_values["rounded_optimal_variance_reduction"]:.1%}**.
- 95% bootstrap interval for the hedge ratio: **[{boot["lower_bound"]:.3f}, {boot["upper_bound"]:.3f}]**.
- Walk-forward residual volatility using trailing estimates: **{walk["model_residual_std"]:.3f} $/bbl**.
- Walk-forward residual volatility using a 1.0 hedge benchmark: **{walk["one_to_one_residual_std"]:.3f} $/bbl**.

## Risk interpretation

The historical sample shows that WTI futures can materially reduce flat-price variability, but a producer remains exposed to other risks:

- Midland/Cushing basis can move independently of the Cushing-linked futures hedge.
- Actual production can differ from forecast production, creating under- or over-hedged volume.
- The statistically estimated hedge ratio is not constant through time.
- The WTI futures curve changes between backwardation, contango, and relatively flat regimes.

## Governance / model-use note

The results are analytical benchmarks, not trading or hedge recommendations. A production hedge program would also require contract-specific execution, liquidity and margin constraints, policy limits, credit, accounting treatment, and ETRM controls.

See the top-level README and `docs/` for methodology and limitations.
"""

    (OUTPUT_DIR / "executive_summary.md").write_text(text)


def main():
    """Run the project analyses and refresh saved outputs."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    spot, futures = load_market_data()
    market = prepare_monthly_market_data(spot, futures)

    hedge_summary, simulations, risk_summary = run_hedge_analysis(market)
    run_basis_analysis()

    (
        min_summary,
        comparison,
        walk_summary,
        bootstrap_summary,
    ) = run_min_variance_analysis(market)

    curve, regime_summary, regime_behavior = run_curve_analysis()
    run_optional_fundamentals(curve)

    write_executive_summary(
        hedge_summary,
        min_summary,
        walk_summary,
        bootstrap_summary,
    )

    print("\nAnalysis complete. See outputs/ for generated results.")


if __name__ == "__main__":
    main()
