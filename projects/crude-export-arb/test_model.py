import pandas as pd
import pytest
from model import ExportCosts, export_economics, monthly_prices

NO_COSTS = ExportCosts(0, 0, 0, 0, 0, 0)


def test_spread_with_no_costs():
    x = export_economics(80, 76, NO_COSTS)
    assert x["brent_wti_spread"] == 4
    assert x["arb_margin"] == 4
    assert x["breakeven_freight"] == 4


def test_hand_computed_default_month():
    # Brent 80, WTI 75: losses 0.15, financing 75 x (e^(0.06 x 45/365) - 1)
    x = export_economics(80, 75)
    financing = 75 * (2.718281828459045 ** (0.06 * 45 / 365) - 1)
    assert x["financing"] == pytest.approx(financing)
    assert x["losses_and_insurance"] == pytest.approx(0.15)
    assert x["total_delivered_cost"] == pytest.approx(1 + 0.5 + 3 + 0.15 + financing)
    assert x["arb_margin"] == pytest.approx(5 - x["total_delivered_cost"])


def test_breakeven_freight_closes_the_arb():
    x = export_economics(84.2, 78.9)
    at_breakeven = ExportCosts(freight_gulf_to_europe=x["breakeven_freight"])
    assert export_economics(84.2, 78.9, at_breakeven)["arb_margin"] == pytest.approx(0)


def test_higher_freight_lowers_margin_one_for_one():
    a = export_economics(80, 75)
    b = export_economics(80, 75, ExportCosts(freight_gulf_to_europe=4.25))
    assert a["arb_margin"] - b["arb_margin"] == pytest.approx(1.25)


def test_bad_inputs():
    with pytest.raises(ValueError):
        ExportCosts(freight_gulf_to_europe=-1)
    with pytest.raises(ValueError):
        export_economics(float("nan"), 70)
    with pytest.raises(ValueError):
        export_economics(70, -37.63)


def _daily(column, start, periods):
    dates = pd.bdate_range(start, periods=periods)
    return pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), column: 50.0})


def test_monthly_average_and_thin_month_fails():
    brent = _daily("brent", "2020-01-01", 45)
    wti = _daily("wti_cushing", "2020-01-01", 45)
    monthly = monthly_prices(brent, wti)
    assert monthly.brent.iloc[0] == 50
    assert monthly.brent_days.iloc[0] == 23  # business days in January 2020
    gappy = wti[~wti.date.str.match(r"2020-01-[12]")]  # 9 January days remain
    with pytest.raises(ValueError):
        monthly_prices(brent, gappy)
