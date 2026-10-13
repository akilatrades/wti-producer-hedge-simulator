-- Do months where carry covers costs coincide with Cushing builds?
-- Joins each carry month to its inventory month and summarizes both regimes,
-- for the full sample and excluding 2020. Matches regime_comparison.csv.

WITH joined AS (
    SELECT
        n.date,
        n.net_carry,
        i.mean_stocks_million_bbl,
        i.stock_change_million_bbl,
        i.weekly_observations,
        n.net_carry > 0 AS carry_covers_costs,
        i.stock_change_million_bbl > 0 AS stocks_build
    FROM net_carry AS n
    JOIN monthly_inventory AS i
        ON i.month = substr(n.date, 1, 7)
),
samples AS (
    SELECT 'all' AS sample, * FROM joined
    UNION ALL
    SELECT 'excluding_2020' AS sample, * FROM joined WHERE substr(date, 1, 4) <> '2020'
)
SELECT
    sample,
    carry_covers_costs,
    COUNT(*) AS months,
    SUM(stocks_build) AS build_months,
    AVG(stocks_build) AS build_share,
    AVG(stock_change_million_bbl) AS mean_monthly_stock_change_million_bbl,
    AVG(mean_stocks_million_bbl) AS mean_stocks_million_bbl
FROM samples
GROUP BY sample, carry_covers_costs
ORDER BY sample, carry_covers_costs;
