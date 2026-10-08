"""Run from this directory. Uses the committed EIA historical monthly snapshot."""

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from model import CarryCosts, storage_economics


def main():
    source = Path("data/eia_wti_curve_monthly_2015_2024.csv")
    prices = pd.read_csv(source)
    # EIA discontinued this series on April 5, 2024; omit partial April average.
    prices = prices[prices.date < "2024-04-01"].copy()
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    costs = CarryCosts()
    rows = [
        dict(
            date=row.date,
            near=row.contract_1,
            deferred=row.contract_4,
            **storage_economics(row.contract_1, row.contract_4, costs),
        )
        for row in prices.itertuples()
    ]
    frame = pd.DataFrame(rows)
    frame.to_csv(out / "carry_history.csv", index=False)
    sensitivity = []
    for storage in [0.25, 0.50, 0.75, 1.00]:
        for rate in [0.03, 0.06, 0.10]:
            assumption = CarryCosts(
                storage_per_month=storage, annual_financing_rate=rate
            )
            net = [
                storage_economics(x.contract_1, x.contract_4, assumption)["net_carry"]
                for x in prices.itertuples()
            ]
            sensitivity.append(
                dict(
                    storage_per_month=storage,
                    financing_rate=rate,
                    positive_months=sum(x > 0 for x in net),
                    observations=len(net),
                    mean_net_carry=sum(net) / len(net),
                )
            )
    pd.DataFrame(sensitivity).to_csv(out / "cost_sensitivity.csv", index=False)
    (out / "assumptions.json").write_text(
        json.dumps(
            {
                **asdict(costs),
                "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "data_class": "historical monthly average curve; assumed constant costs",
                "sample_start": frame.date.iloc[0],
                "sample_end": frame.date.iloc[-1],
                "excluded": "April 2024 partial-month data; all months thereafter unavailable",
            },
            indent=2,
        )
        + "\n"
    )
    dates = pd.to_datetime(frame.date)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(dates, frame.gross_spread, label="C4 minus C1")
    ax.plot(dates, frame.net_carry, label="After assumed carry costs")
    ax.axhline(0, color="black", linewidth=0.7)
    ax.set(
        ylabel="$/bbl",
        title="Contango must cover storage, financing, insurance and handling",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "carry_history.svg")
    plt.close(fig)
    print(
        f"{len(frame)} months; contango {(frame.gross_spread > 0).sum()}; positive net carry {(frame.net_carry > 0).sum()}"
    )


if __name__ == "__main__":
    main()
