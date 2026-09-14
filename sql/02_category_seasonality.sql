-- SQL Query 2: Category Value & Promo Reliance Analysis
-- Technical concepts used: Category-Level Aggregation, Margin & Promo Usage Breakdown

SELECT 
    category AS product_category,
    COUNT(customer_id) AS total_buyers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customer_master), 2) AS buyer_share_pct,
    ROUND(AVG(estimated_total_purchases), 2) AS avg_estimated_total_purchases,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_purchase_amount_usd,
    ROUND(AVG(net_margin_contribution), 2) AS avg_estimated_net_margin,
    ROUND(AVG(observed_promo_usage) * 100, 2) AS observed_promo_usage_pct
FROM customer_master
GROUP BY category
ORDER BY avg_estimated_net_margin DESC;
