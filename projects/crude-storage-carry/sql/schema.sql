-- Tables for the crude-storage carry study (SQLite).
-- Prices are USD/bbl monthly averages of NYMEX WTI delivery positions C1-C4 (EIA).
-- Stocks are EIA weekly Cushing crude stocks excluding SPR, in thousand barrels.

DROP TABLE IF EXISTS wti_curve_monthly;
CREATE TABLE wti_curve_monthly (
    date        TEXT PRIMARY KEY,   -- month-end label, YYYY-MM-DD
    contract_1  REAL NOT NULL CHECK (contract_1 > 0),
    contract_2  REAL NOT NULL,
    contract_3  REAL NOT NULL,
    contract_4  REAL NOT NULL
);

DROP TABLE IF EXISTS cushing_weekly;
CREATE TABLE cushing_weekly (
    date                 TEXT PRIMARY KEY,   -- week-ending date, YYYY-MM-DD
    stocks_thousand_bbl  REAL NOT NULL
);

-- One row of cost assumptions, matching CarryCosts() in model.py.
DROP TABLE IF EXISTS carry_assumptions;
CREATE TABLE carry_assumptions (
    months                 REAL NOT NULL CHECK (months > 0),
    storage_per_month      REAL NOT NULL CHECK (storage_per_month >= 0),
    annual_financing_rate  REAL NOT NULL CHECK (annual_financing_rate >= 0),
    annual_insurance_rate  REAL NOT NULL CHECK (annual_insurance_rate >= 0),
    handling_round_trip    REAL NOT NULL CHECK (handling_round_trip >= 0)
);
