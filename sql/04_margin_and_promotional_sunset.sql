-- SQL Query 4: Promotional Sunset Scenario & Margin Recovery Modeling
-- Technical concepts used: Segment Aggregations, Scenario Analysis (25%, 50%, 75% Sunset Models)

SELECT 
    strategic_segment,
    COUNT(customer_id) AS total_customers,
    SUM(estimated_total_purchases) AS total_orders,
    ROUND(SUM(gross_amount), 2) AS total_gross_spend,
    ROUND(SUM(discount_amount), 2) AS total_discount_given,
    ROUND(SUM(purchase_amount_usd), 2) AS total_net_spend,
    ROUND(SUM(net_margin_contribution), 2) AS total_net_margin_base_cogs40,
    ROUND(AVG(observed_promo_usage) * 100, 2) AS observed_promo_usage_pct,
    -- Modeled Sunset Recovery Scenarios (25%, 50%, 75%)
    ROUND(SUM(discount_amount) * 0.25, 2) AS modeled_recovery_25pct_sunset,
    ROUND(SUM(discount_amount) * 0.50, 2) AS modeled_recovery_50pct_sunset,
    ROUND(SUM(discount_amount) * 0.75, 2) AS modeled_recovery_75pct_sunset
FROM customer_master
GROUP BY strategic_segment
ORDER BY total_discount_given DESC;
