-- Monthly Cushing inventory from weekly observations, matching align_monthly() in
-- physical_layer.py:
--   * level  = mean of the month's weekly stocks, in million barrels
--   * change = last weekly observation this month minus last observation last month
-- The December 2014 rows exist only to give January 2015 a prior month.

DROP VIEW IF EXISTS monthly_inventory;
CREATE VIEW monthly_inventory AS
WITH weekly AS (
    SELECT
        substr(date, 1, 7) AS month,
        date,
        stocks_thousand_bbl / 1000.0 AS stocks_million_bbl,
        ROW_NUMBER() OVER (PARTITION BY substr(date, 1, 7) ORDER BY date DESC) AS rank_from_end
    FROM cushing_weekly
),
by_month AS (
    SELECT
        month,
        AVG(stocks_million_bbl) AS mean_stocks_million_bbl,
        MAX(CASE WHEN rank_from_end = 1 THEN stocks_million_bbl END) AS last_stocks_million_bbl,
        COUNT(*) AS weekly_observations
    FROM weekly
    GROUP BY month
)
SELECT
    month,
    mean_stocks_million_bbl,
    last_stocks_million_bbl,
    weekly_observations,
    last_stocks_million_bbl
        - LAG(last_stocks_million_bbl) OVER (ORDER BY month) AS stock_change_million_bbl
FROM by_month;
