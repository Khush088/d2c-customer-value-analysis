-- SQL Query 5: Ideal Customer Profile (ICP) Extraction
-- Technical concepts used: High-Value Organic Sub-Group Aggregation & Profiling

WITH HighValueOrganic AS (
    SELECT *
    FROM customer_master
    WHERE strategic_segment = '1. High Value Organic'
)
SELECT 
    state,
    gender,
    observed_category,
    COUNT(customer_id) AS icp_customer_count,
    ROUND(AVG(age), 1) AS avg_age,
    ROUND(AVG(estimated_total_purchases), 2) AS avg_estimated_total_purchases,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_purchase_amount_usd,
    ROUND(AVG(net_margin_contribution), 2) AS avg_estimated_net_margin,
    ROUND(AVG(observed_promo_usage) * 100, 2) AS observed_promo_usage_pct
FROM HighValueOrganic
GROUP BY state, gender, observed_category
HAVING icp_customer_count >= 5
ORDER BY icp_customer_count DESC;
