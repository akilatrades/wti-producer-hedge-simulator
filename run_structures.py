"""Reproduce an assumption-based hedge comparison and observed benchmark basis."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.options import costless_ceiling, producer_revenues


def main():
    out = Path("outputs/structures")
    out.mkdir(parents=True, exist_ok=True)
    config = dict(
        forward=70.0,
        floor=60.0,
        subfloor=45.0,
        maturity=1.0,
        volatility=0.40,
        rate=0.04,
        barrels=100_000,
        seed=42,
        scenarios=100_000,
    )
    f, k, low, t, vol, r = [
        config[x]
        for x in ("forward", "floor", "subfloor", "maturity", "volatility", "rate")
    ]
    ceiling = costless_ceiling(f, k, t, vol, r)
    three = costless_ceiling(f, k, t, vol, r, subfloor=low)
    rng = np.random.default_rng(config["seed"])
    terminal = f * np.exp(
        -0.5 * vol**2 * t + vol * np.sqrt(t) * rng.normal(size=config["scenarios"])
    )
    # This is a risk-neutral illustrative distribution, not a forecast/backtest.
    revenues = producer_revenues(terminal, 0, f, k, ceiling, three, low)
    rows = []
    for name, values in revenues.items():
        q = np.quantile(values, 0.05)
        rows.append(
            dict(
                strategy=name,
                mean_revenue=values.mean(),
                std_revenue=values.std(ddof=1),
                p05_revenue=q,
                worst_5pct_mean_revenue=values[values <= q + 1e-8].mean(),
                probability_below_6m=float(np.mean(values < 6_000_000 - 1e-6)),
            )
        )
    pd.DataFrame(rows).to_csv(out / "revenue_comparison.csv", index=False)
    grid = np.linspace(-20, 150, 400)
    payoffs = producer_revenues(grid, 0, f, k, ceiling, three, low)
    pd.DataFrame({"terminal_price": grid, **payoffs}).to_csv(
        out / "payoffs.csv", index=False
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, values in payoffs.items():
        if name != "fixed_price_swap":
            ax.plot(grid, values / 1e6, label=name.replace("_", " "))
    ax.set(
        xlabel="Terminal reference price ($/bbl)",
        ylabel="Producer revenue ($m)",
        title="Three-way collar gives up protection below the sold put",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "payoffs.svg")
    plt.close(fig)
    # Reuse the checked-in public-source historical output, not invented location prices.
    history = pd.read_csv("outputs/monthly_analysis.csv")
    history["cushing_spot_minus_front_proxy"] = history.spot_exit - history.futures_exit
    history[
        ["month", "spot_exit", "futures_exit", "cushing_spot_minus_front_proxy"]
    ].to_csv(out / "observed_benchmark_basis.csv", index=False)
    basis = history.cushing_spot_minus_front_proxy
    pd.DataFrame(
        [
            dict(
                observations=len(basis),
                mean=basis.mean(),
                std=basis.std(),
                p05=basis.quantile(0.05),
                p95=basis.quantile(0.95),
                minimum=basis.min(),
                maximum=basis.max(),
            )
        ]
    ).to_csv(out / "basis_summary.csv", index=False)
    stress = []
    for price in [20.0, 45.0, 60.0, 70.0, 100.0]:
        for spread in [-15.0, -5.0, 0.0, 5.0]:
            values = producer_revenues(price, spread, f, k, ceiling, three, low)
            stress.append(
                {
                    "terminal_price": price,
                    "assumed_location_basis": spread,
                    **{n: float(v) for n, v in values.items()},
                }
            )
    pd.DataFrame(stress).to_csv(out / "basis_stress.csv", index=False)
    (out / "assumptions.json").write_text(
        json.dumps(
            {
                **config,
                "ceiling": ceiling,
                "three_way_ceiling": three,
                "data_class": "synthetic terminal scenarios; historical benchmark basis in separate CSV",
                "distribution": "risk-neutral lognormal; zero location basis in distribution comparison",
            },
            indent=2,
        )
        + "\n"
    )
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
