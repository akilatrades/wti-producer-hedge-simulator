"""Run from this directory. Uses the committed EIA daily spot snapshot."""

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from model import ExportCosts, export_economics, monthly_prices

BRENT = Path("data/eia_brent_daily_2016_2026.csv")
WTI = Path("data/eia_wti_cushing_daily_2016_2026.csv")


def arb_history(monthly, costs=None):
    rows = [
        {
            "month": month.strftime("%Y-%m"),
            "brent": row.brent,
            "wti_cushing": row.wti_cushing,
            **export_economics(row.brent, row.wti_cushing, costs),
        }
        for month, row in monthly.iterrows()
    ]
    return pd.DataFrame(rows)


def main():
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    monthly = monthly_prices(pd.read_csv(BRENT), pd.read_csv(WTI))
    # The final month in the snapshot is partial; keep full months only.
    partial = monthly.index[-1]
    monthly = monthly.iloc[:-1]
    costs = ExportCosts()
    history = arb_history(monthly, costs)
    history.to_csv(out / "arb_history.csv", index=False)

    annual = history.assign(year=history.month.str[:4]).groupby("year")
    annual = pd.DataFrame(
        {
            "months": annual.size(),
            "mean_brent_wti_spread": annual.brent_wti_spread.mean(),
            "mean_delivered_cost": annual.total_delivered_cost.mean(),
            "open_months": annual.arb_margin.apply(lambda x: int((x > 0).sum())),
            "mean_breakeven_freight": annual.breakeven_freight.mean(),
        }
    )
    annual.to_csv(out / "annual_summary.csv")

    sensitivity = []
    for pipeline in [0.0, 0.50, 1.00, 1.50]:
        for freight in [1.50, 2.00, 3.00, 4.00, 5.00, 6.00]:
            case = ExportCosts(
                pipeline_cushing_to_gulf=pipeline, freight_gulf_to_europe=freight
            )
            margin = arb_history(monthly, case).arb_margin
            sensitivity.append(
                {
                    "pipeline_cushing_to_gulf": pipeline,
                    "freight_gulf_to_europe": freight,
                    "open_months": int((margin > 0).sum()),
                    "months": len(margin),
                    "mean_arb_margin": margin.mean(),
                }
            )
    pd.DataFrame(sensitivity).to_csv(out / "cost_sensitivity.csv", index=False)

    (out / "assumptions.json").write_text(
        json.dumps(
            {
                **asdict(costs),
                "brent_sha256": hashlib.sha256(BRENT.read_bytes()).hexdigest(),
                "wti_sha256": hashlib.sha256(WTI.read_bytes()).hexdigest(),
                "data_class": "EIA daily spot prices averaged by month; assumed constant costs",
                "sample_start": history.month.iloc[0],
                "sample_end": history.month.iloc[-1],
                "excluded": f"Partial month {partial:%Y-%m}; 2015 and earlier "
                "(US crude export ban lifted December 2015)",
            },
            indent=2,
        )
        + "\n"
    )

    dates = pd.to_datetime(history.month)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(dates, history.brent_wti_spread, label="Brent minus WTI Cushing")
    ax.plot(
        dates,
        history.total_delivered_cost,
        label="Assumed cost to deliver Cushing crude to Europe",
    )
    ax.fill_between(
        dates,
        history.total_delivered_cost,
        history.brent_wti_spread,
        where=history.arb_margin > 0,
        alpha=0.2,
        label="Arb open",
    )
    ax.set(ylabel="USD/bbl", title="When does Brent pay for exporting Cushing crude?")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "arb_history.svg")
    plt.close(fig)

    print(
        f"{len(history)} months; open {(history.arb_margin > 0).sum()}; "
        f"median breakeven freight {history.breakeven_freight.median():.2f}"
    )
    print(annual.round(2).to_string())


if __name__ == "__main__":
    main()
