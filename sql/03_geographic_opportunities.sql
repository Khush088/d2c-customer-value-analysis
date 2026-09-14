-- SQL Query 3: Geographic Opportunity Mapping (Organic vs Promo-Driven Volume)
-- Technical concepts used: Aggregations, Normalized Multi-Factor Index, Business Sample Rule Filter

WITH StateMetrics AS (
    SELECT 
        state,
        COUNT(DISTINCT customer_id) AS customer_count,
        SUM(estimated_total_purchases) AS total_estimated_orders,
        SUM(purchase_amount_usd) AS total_net_revenue,
        SUM(discount_amount) AS total_discount_given,
        SUM(net_margin_contribution) AS total_net_margin,
        AVG(net_margin_contribution) AS avg_margin_per_cust,
        AVG(observed_promo_usage) AS avg_promo_usage_rate,
        AVG(purchase_amount_usd) AS avg_purchase_amount
    FROM customer_master
    GROUP BY state
    HAVING customer_count >= 50  -- Minimum sample-size business rule filter
),
MinMaxStats AS (
    SELECT 
        MIN(avg_margin_per_cust) AS min_margin, MAX(avg_margin_per_cust) AS max_margin,
        MIN(customer_count) AS min_vol, MAX(customer_count) AS max_vol
    FROM StateMetrics
)
SELECT 
    s.state,
    s.customer_count,
    s.total_estimated_orders,
    ROUND(s.total_net_revenue, 2) AS total_net_revenue,
    ROUND(s.total_net_margin, 2) AS total_net_margin,
    ROUND(s.avg_margin_per_cust, 2) AS avg_margin_per_cust,
    ROUND(s.avg_promo_usage_rate * 100, 2) AS observed_promo_usage_pct,
    ROUND(s.avg_purchase_amount, 2) AS avg_purchase_amount,
    -- Normalized Composite Score = 40% Norm Margin + 30% Norm Volume + 30% Norm Non-Promo Rate
    ROUND(
        (0.40 * (s.avg_margin_per_cust - m.min_margin) / (m.max_margin - m.min_margin + 0.001) * 100) +
        (0.30 * (s.customer_count - m.min_vol) / (m.max_vol - m.min_vol + 0.001) * 100) +
        (0.30 * (1 - s.avg_promo_usage_rate) * 100),
    2) AS normalized_organic_score
FROM StateMetrics s, MinMaxStats m
ORDER BY normalized_organic_score DESC;
