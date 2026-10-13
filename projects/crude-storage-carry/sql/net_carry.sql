-- Buy at C1, store for the assumed number of months, sell at C4.
-- Same economics as storage_economics() in model.py, in USD/bbl:
--   net carry = C4 - C1 - storage - financing - insurance - handling
-- Financing is continuously compounded on the C1 acquisition price.
-- April 2024 is excluded because EIA stopped the series on April 5, 2024.

DROP VIEW IF EXISTS net_carry;
CREATE VIEW net_carry AS
WITH costs AS (
    SELECT
        c.date,
        c.contract_1 AS near,
        c.contract_4 AS deferred,
        c.contract_4 - c.contract_1 AS gross_spread,
        a.months * a.storage_per_month AS storage_cost,
        c.contract_1 * (exp(a.annual_financing_rate * a.months / 12.0) - 1) AS financing_cost,
        c.contract_1 * a.annual_insurance_rate * a.months / 12.0 AS insurance_cost,
        a.handling_round_trip AS handling_cost,
        a.months
    FROM wti_curve_monthly AS c
    CROSS JOIN carry_assumptions AS a
    WHERE c.date < '2024-04-01'
)
SELECT
    date,
    near,
    deferred,
    gross_spread,
    storage_cost,
    financing_cost,
    insurance_cost,
    handling_cost,
    storage_cost + financing_cost + insurance_cost + handling_cost AS total_carry_cost,
    gross_spread - storage_cost - financing_cost - insurance_cost - handling_cost AS net_carry,
    (gross_spread - financing_cost - insurance_cost - handling_cost) / months
        AS breakeven_monthly_storage
FROM costs;
