-- SQL Query 1: Authoritative Customer Value & Promo Dependency Segmentation
-- Technical concepts used: Aggregation, Exact Strategic Segment Summaries, Ratio Math

SELECT 
    strategic_segment,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customer_master), 2) AS customer_pct,
    ROUND(AVG(estimated_total_purchases), 2) AS avg_estimated_total_purchases,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_purchase_amount_usd,
    ROUND(AVG(net_margin_contribution), 2) AS avg_estimated_net_margin,
    ROUND(AVG(observed_promo_usage) * 100, 2) AS observed_promo_usage_pct,
    ROUND(AVG(frequency_proxy_days), 1) AS avg_frequency_proxy_days
FROM customer_master
GROUP BY strategic_segment
ORDER BY avg_estimated_net_margin DESC;
