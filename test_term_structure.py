import pandas as pd

from src.term_structure import (
    add_curve_metrics,
    select_example_curves,
    summarize_curve_regimes,
)

# Small made-up dataset used only to test the math.
curve = pd.DataFrame(
    {
        "contract_1": [80.0, 70.0, 75.0],
        "contract_2": [79.0, 71.0, 75.1],
        "contract_3": [78.0, 72.0, 75.1],
        "contract_4": [77.0, 73.0, 75.2],
    },
    index=pd.to_datetime(
        [
            "2024-01-31",
            "2024-02-29",
            "2024-03-31",
        ]
    ),
)

result = add_curve_metrics(
    curve,
    flat_threshold=0.25,
)

# January: C1 ($80) > C4 ($77) -> +$3 -> backwardation.
assert (
    result.loc["2024-01-31", "c1_c4_spread"]
    == 3.0
)
assert (
    result.loc["2024-01-31", "curve_regime"]
    == "backwardation"
)

# February: C1 ($70) < C4 ($73) -> -$3 -> contango.
assert (
    result.loc["2024-02-29", "c1_c4_spread"]
    == -3.0
)
assert (
    result.loc["2024-02-29", "curve_regime"]
    == "contango"
)

# March is within the +/- $0.25 flat threshold.
assert round(
    result.loc["2024-03-31", "c1_c4_spread"],
    2,
) == -0.20
assert (
    result.loc["2024-03-31", "curve_regime"]
    == "flat"
)

summary = summarize_curve_regimes(result)
assert summary["months"].sum() == 3

examples = select_example_curves(result)
assert len(examples) == 2

print("Term-structure math checks passed.")
