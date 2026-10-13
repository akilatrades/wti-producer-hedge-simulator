"""The SQL queries must reproduce the pandas model exactly."""

import sqlite3

import pandas as pd
import pytest
from model import CarryCosts, storage_economics
from physical_layer import align_monthly
from sql_layer import SQL, build_database, check_coverage, run


@pytest.fixture(scope="module")
def results():
    return run(build_database())


def test_net_carry_matches_python_model(results):
    carry, _ = results
    curve = pd.read_csv("data/eia_wti_curve_monthly_2015_2024.csv")
    curve = curve[curve.date < "2024-04-01"]
    assert len(carry) == len(curve) == 111
    for sql_row, price in zip(carry.itertuples(), curve.itertuples()):
        expected = storage_economics(price.contract_1, price.contract_4)
        for column, value in expected.items():
            assert getattr(sql_row, column) == pytest.approx(value, abs=1e-12)


def test_headline_counts(results):
    carry, _ = results
    assert (carry.gross_spread > 0).sum() == 59
    assert (carry.net_carry > 0).sum() == 12


def test_regime_comparison_matches_physical_layer(results):
    carry, regimes = results
    stocks = pd.read_csv("data/cushing_weekly_2014_2024.csv")
    aligned = align_monthly(carry[["date", "net_carry"]], stocks)
    for sample, frame in [
        ("all", aligned),
        ("excluding_2020", aligned[aligned.index.year != 2020]),
    ]:
        for positive, group in frame.groupby("carry_covers_costs"):
            row = regimes[
                (regimes["sample"] == sample)
                & (regimes.carry_covers_costs == bool(positive))
            ].iloc[0]
            assert row.months == len(group)
            assert row.build_months == group.stocks_build.sum()
            assert row.build_share == pytest.approx(group.stocks_build.mean())
            assert row.mean_monthly_stock_change_million_bbl == pytest.approx(
                group.stock_change_million_bbl.mean()
            )
            assert row.mean_stocks_million_bbl == pytest.approx(
                group.mean_stocks_million_bbl.mean()
            )
    covered = regimes[(regimes["sample"] == "all") & regimes.carry_covers_costs].iloc[0]
    assert (covered.months, covered.build_months) == (12, 10)


def test_hand_computed_month():
    con = sqlite3.connect(":memory:")
    con.executescript((SQL / "schema.sql").read_text())
    con.execute("INSERT INTO wti_curve_monthly VALUES ('2020-01-31', 70, 71, 72, 73)")
    con.execute("INSERT INTO carry_assumptions VALUES (3, 0, 0, 0, 0)")
    con.executescript((SQL / "net_carry.sql").read_text())
    net, breakeven = con.execute(
        "SELECT net_carry, breakeven_monthly_storage FROM net_carry"
    ).fetchone()
    assert (net, breakeven) == (3, 1)


def test_cost_assumptions_flow_through():
    base = run(build_database())[0]
    pricier = run(build_database(CarryCosts(storage_per_month=1.0)))[0]
    assert (base.net_carry - pricier.net_carry).tolist() == pytest.approx([1.5] * 111)


def test_missing_inventory_fails():
    con = build_database()
    con.execute("DELETE FROM cushing_weekly WHERE date LIKE '2018-06%'")
    with pytest.raises(ValueError):
        check_coverage(con)
