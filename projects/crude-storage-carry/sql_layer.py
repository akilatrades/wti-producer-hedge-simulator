"""SQL version of the storage-carry study. Run from this directory.

Loads the committed EIA CSVs into SQLite, computes net carry, monthly Cushing
inventory and the regime comparison with the queries in sql/, and saves the
results to outputs/sql/. test_sql_layer.py checks they match the pandas outputs.
"""

import math
import sqlite3
from dataclasses import astuple
from pathlib import Path

import pandas as pd
from model import CarryCosts

SQL = Path("sql")
CURVE = Path("data/eia_wti_curve_monthly_2015_2024.csv")
STOCKS = Path("data/cushing_weekly_2014_2024.csv")


def build_database(costs=None, path=":memory:"):
    costs = costs or CarryCosts()
    con = sqlite3.connect(path)
    # Not every SQLite build ships math functions; register exp() explicitly.
    con.create_function("exp", 1, math.exp, deterministic=True)
    con.executescript((SQL / "schema.sql").read_text())
    curve = pd.read_csv(CURVE)
    stocks = pd.read_csv(STOCKS)
    con.executemany(
        "INSERT INTO wti_curve_monthly VALUES (?, ?, ?, ?, ?)",
        curve[
            ["date", "contract_1", "contract_2", "contract_3", "contract_4"]
        ].itertuples(index=False, name=None),
    )
    con.executemany(
        "INSERT INTO cushing_weekly VALUES (?, ?)",
        stocks[["date", "stocks_thousand_bbl"]].itertuples(index=False, name=None),
    )
    con.execute("INSERT INTO carry_assumptions VALUES (?, ?, ?, ?, ?)", astuple(costs))
    for view in ["net_carry.sql", "monthly_inventory.sql"]:
        con.executescript((SQL / view).read_text())
    con.commit()
    return con


def check_coverage(con):
    """Fail, rather than interpolate, if a carry month lacks inventory data."""
    gaps = con.execute(
        """
        SELECT n.date
        FROM net_carry AS n
        LEFT JOIN monthly_inventory AS i ON i.month = substr(n.date, 1, 7)
        WHERE i.weekly_observations IS NULL
           OR i.weekly_observations < 4
           OR i.stock_change_million_bbl IS NULL
        """
    ).fetchall()
    if gaps:
        raise ValueError(f"Missing inventory coverage for {len(gaps)} month(s)")


def run(con):
    check_coverage(con)
    carry = pd.read_sql_query("SELECT * FROM net_carry ORDER BY date", con)
    regimes = pd.read_sql_query((SQL / "regime_comparison.sql").read_text(), con)
    regimes["carry_covers_costs"] = regimes.carry_covers_costs.astype(bool)
    return carry, regimes


def main():
    out = Path("outputs/sql")
    out.mkdir(parents=True, exist_ok=True)
    con = build_database()
    carry, regimes = run(con)
    carry.to_csv(out / "net_carry_sql.csv", index=False)
    regimes.to_csv(out / "regime_comparison_sql.csv", index=False)
    print(
        f"{len(carry)} months; contango {(carry.gross_spread > 0).sum()}; "
        f"positive net carry {(carry.net_carry > 0).sum()}"
    )
    print(regimes.to_string(index=False))


if __name__ == "__main__":
    main()
