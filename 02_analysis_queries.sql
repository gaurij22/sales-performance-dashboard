-- ============================================================
-- Sales Performance Dashboard - Core Analytical Queries
-- Author: Gauri Joshi
-- Description: KPI, trend, and variance analysis queries
-- ============================================================


-- ─────────────────────────────────────────────
-- 1. MONTHLY REVENUE vs TARGET (Variance Analysis)
-- ─────────────────────────────────────────────
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.revenue)                                          AS actual_revenue,
    MAX(t.target_revenue)                                   AS target_revenue,
    SUM(f.revenue) - MAX(t.target_revenue)                  AS variance,
    ROUND(
        (SUM(f.revenue) - MAX(t.target_revenue))
        / NULLIF(MAX(t.target_revenue), 0) * 100, 2
    )                                                        AS variance_pct
FROM fact_sales f
JOIN dim_date    d ON f.date_id   = d.date_id
JOIN fact_targets t ON f.region_id = t.region_id
                   AND d.year      = t.year
                   AND d.month     = t.month
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


-- ─────────────────────────────────────────────
-- 2. REGIONAL PERFORMANCE SUMMARY
-- ─────────────────────────────────────────────
SELECT
    r.region_name,
    COUNT(DISTINCT f.sale_id)                               AS total_transactions,
    SUM(f.quantity)                                         AS units_sold,
    ROUND(SUM(f.revenue), 2)                                AS total_revenue,
    ROUND(SUM(f.profit),  2)                                AS total_profit,
    ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount_pct), 2)                           AS avg_discount_pct
FROM fact_sales   f
JOIN dim_regions  r ON f.region_id = r.region_id
GROUP BY r.region_name
ORDER BY total_revenue DESC;


-- ─────────────────────────────────────────────
-- 3. TOP 10 PRODUCTS BY REVENUE
-- ─────────────────────────────────────────────
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity)                                         AS units_sold,
    ROUND(SUM(f.revenue), 2)                                AS total_revenue,
    ROUND(SUM(f.profit),  2)                                AS total_profit,
    ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS margin_pct
FROM fact_sales   f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- ─────────────────────────────────────────────
-- 4. SALES REP PERFORMANCE LEADERBOARD
-- ─────────────────────────────────────────────
SELECT
    sr.rep_name,
    r.region_name,
    COUNT(DISTINCT f.sale_id)                               AS deals_closed,
    ROUND(SUM(f.revenue), 2)                                AS total_revenue,
    ROUND(AVG(f.revenue), 2)                                AS avg_deal_size,
    ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS margin_pct,
    RANK() OVER (ORDER BY SUM(f.revenue) DESC)              AS revenue_rank
FROM fact_sales      f
JOIN dim_sales_reps  sr ON f.rep_id    = sr.rep_id
JOIN dim_regions      r ON sr.region_id = r.region_id
GROUP BY sr.rep_name, r.region_name
ORDER BY total_revenue DESC;


-- ─────────────────────────────────────────────
-- 5. CONVERSION RATE & DISCOUNT IMPACT
-- ─────────────────────────────────────────────
SELECT
    p.category,
    ROUND(AVG(f.discount_pct), 2)                           AS avg_discount_pct,
    COUNT(f.sale_id)                                        AS num_sales,
    ROUND(SUM(f.revenue), 2)                                AS total_revenue,
    ROUND(SUM(f.profit),  2)                                AS total_profit,
    ROUND(
        SUM(f.quantity * f.unit_price) - SUM(f.revenue), 2
    )                                                        AS revenue_lost_to_discount
FROM fact_sales   f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue_lost_to_discount DESC;


-- ─────────────────────────────────────────────
-- 6. QUARTER-OVER-QUARTER GROWTH
-- ─────────────────────────────────────────────
WITH quarterly AS (
    SELECT
        d.year,
        d.quarter,
        ROUND(SUM(f.revenue), 2) AS revenue
    FROM fact_sales f
    JOIN dim_date   d ON f.date_id = d.date_id
    GROUP BY d.year, d.quarter
)
SELECT
    year,
    quarter,
    revenue                                                  AS current_revenue,
    LAG(revenue) OVER (ORDER BY year, quarter)               AS prev_quarter_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year, quarter))
        / NULLIF(LAG(revenue) OVER (ORDER BY year, quarter), 0) * 100, 2
    )                                                        AS qoq_growth_pct
FROM quarterly
ORDER BY year, quarter;


-- ─────────────────────────────────────────────
-- 7. UNDERPERFORMING REGIONS (Below 80% of Target)
-- ─────────────────────────────────────────────
SELECT
    r.region_name,
    t.year,
    t.month,
    ROUND(SUM(f.revenue), 2)                                AS actual_revenue,
    t.target_revenue,
    ROUND(SUM(f.revenue) / t.target_revenue * 100, 2)       AS achievement_pct
FROM fact_sales   f
JOIN dim_regions  r ON f.region_id  = r.region_id
JOIN dim_date     d ON f.date_id    = d.date_id
JOIN fact_targets t ON t.region_id  = r.region_id
                   AND t.year       = d.year
                   AND t.month      = d.month
GROUP BY r.region_name, t.year, t.month, t.target_revenue
HAVING ROUND(SUM(f.revenue) / t.target_revenue * 100, 2) < 80
ORDER BY achievement_pct ASC;
