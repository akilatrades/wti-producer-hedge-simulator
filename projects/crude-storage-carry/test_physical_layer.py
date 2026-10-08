import pandas as pd
import pytest
from physical_layer import align_monthly


def test_month_change_uses_prior_month_last_not_average():
    stocks = pd.DataFrame(
        {
            "date": pd.date_range("2019-12-06", "2020-02-28", freq="W-FRI"),
            "stocks_thousand_bbl": range(10000, 23000, 1000),
        }
    )
    carry = pd.DataFrame({"date": ["2020-01-31", "2020-02-29"], "net_carry": [1, -1]})
    result = align_monthly(carry, stocks)
    assert result.stock_change_million_bbl.tolist() == [5, 4]
    assert result.carry_covers_costs.tolist() == [True, False]
    assert result.weekly_observations.tolist() == [5, 4]
    with pytest.raises(ValueError):
        align_monthly(carry, stocks[stocks.date >= "2020-01-01"])
