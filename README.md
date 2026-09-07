# D2C Customer Value & Promotional Strategy Analysis

## Decoding Customer Value: A SQL-Driven Retention Strategy

**Domain:** D2C E-Commerce / Retail Analytics
**Tools:** Python, SQL, Power BI
**Dataset:** Shopping Trends customer-level dataset
**Customers:** 3,900
**Geographic Coverage:** 43 U.S. states

---

## 1. Project Overview

For a D2C fashion brand, growing sales is only part of the challenge. Customers who spend more are not necessarily more valuable if their purchases depend heavily on discounts.

This project analyzes customer-level purchasing behavior to understand **customer value, repeat purchasing, promotional dependence, and geographic opportunities**.

The analysis focuses on five business questions:

* Which customers represent the strongest long-term value?
* Are high-spending customers also generating strong margins?
* How does promotional usage relate to customer profitability?
* Which states present opportunities for organic growth?
* What does the brand's highest-value customer profile look like?

The final output combines **Python-based feature engineering, SQL analysis, statistical testing, and Power BI visualization** to translate customer behavior into actionable business recommendations.

---

## 2. Business Questions

### Customer Value

* Which customers have both high spending and strong repeat-purchase behavior?
* How do organic customers compare with customers who frequently use promotions?

### Promotions

* Are promotional customers generating lower estimated margins?
* Is there evidence that promotional purchasing is associated with lower customer value?

### Geography

* Which states have a combination of customer volume, margin, and lower promotional dependence?
* Where could the brand focus future acquisition efforts?

### Customer Profile

* What characteristics are common among high-value organic customers?
* How does this segment differ from the overall customer base?

### Strategy

* How could the brand reduce unnecessary discount dependence while protecting sales?
* What experiment could be used to validate a new promotional strategy?

---

## 3. Dataset

The analysis uses a customer-level version of the **Shopping Trends** dataset containing 3,900 customer records.

Each row represents an individual customer and includes variables such as:

* Customer ID
* Age
* Gender
* Item Purchased
* Category
* Purchase Amount
* Location
* Size
* Color
* Season
* Review Rating
* Subscription Status
* Shipping Type
* Discount Applied
* Promo Code Used
* Previous Purchases
* Payment Method
* Frequency of Purchases

The dataset does not contain individual order timestamps, so the analysis focuses on **customer-level purchasing behavior rather than true longitudinal retention or cohort analysis**.

---

## 4. Analytical Approach

The project follows this workflow:

```text
Raw Customer Dataset
        ↓
Python Data Cleaning & Feature Engineering
        ↓
Engineered Customer Master
        ↓
SQLite Database
        ↓
SQL Analysis
        ↓
CSV Analysis Outputs
        ↓
Power BI Dashboard
        ↓
Business Recommendations
```

### Python

Python was used for:

* Data cleaning and validation
* Feature engineering
* Customer segmentation
* Margin calculations
* Statistical testing
* Geographic opportunity scoring
* Preparing datasets for SQL and Power BI

Main libraries:

* Pandas
* NumPy

### SQL

SQLite was used to perform the main analytical queries using:

* CTEs
* Aggregations
* CASE statements
* Window functions
* Percentiles / threshold-based segmentation
* Customer-level comparisons
* Geographic and category analysis

### Power BI

Power BI was used to build an executive dashboard covering:

* Customer value segments
* Promotional behavior
* Estimated margin
* Geographic opportunities
* Category performance
* Repeat-purchase behavior

---

## 5. Customer Value Segmentation

Customers were divided into four strategic segments using purchasing behavior, spend, and promotional usage.

| Segment                   | Customers | Share | Avg. Previous Purchases | Avg. Purchase Amount | Avg. Est. Net Margin |
| ------------------------- | --------: | ----: | ----------------------: | -------------------: | -------------------: |
| High Value Organic        |       940 | 24.1% |                    29.8 |               $77.00 |               $41.20 |
| High Spend Bargain Hunter |       477 | 12.2% |                    29.1 |               $88.40 |               $40.04 |
| Promo-Using Repeat        |     1,317 | 33.8% |                    24.2 |               $49.30 |               $16.58 |
| Mid-Tier Core             |     1,166 | 29.9% |                    23.8 |               $54.10 |               $27.46 |

### Key observation

The **High Spend Bargain Hunter** segment spends more on average than the High Value Organic segment, but its estimated margin is slightly lower.

This highlights an important business distinction:

> **Higher spending does not automatically mean higher customer value.**

Customers who repeatedly purchase without relying on promotions can be more attractive from a margin perspective.

---

## 6. Loyalty Analysis

Rather than defining loyalty using a single arbitrary metric, two different customer definitions were evaluated.

### Definition 1 — Behavioral Loyalty

Customers were considered behaviorally loyal when they had:

* At least 20 previous purchases
* Purchase amount at or above the 75th percentile ($78)

This identified **639 customers**.

| Metric                    |  Result |
| ------------------------- | ------: |
| Customers                 |     639 |
| Avg. Purchase Amount      |  $89.21 |
| Avg. Estimated Net Margin |  $44.43 |
| Promo Usage               |   46.0% |
| Total Estimated Margin    | $28,392 |

This definition captures customers who demonstrate both **repeat behavior and high spending**, but it does not distinguish between organic buyers and customers who rely heavily on promotions.

### Definition 2 — Economic / Organic Loyalty

A stricter definition was also tested:

* At least 15 previous purchases
* Estimated net margin of at least $34.20
* No observed promo-code usage

This identified **502 customers**.

| Metric                    |  Result |
| ------------------------- | ------: |
| Customers                 |     502 |
| Avg. Purchase Amount      |  $86.60 |
| Avg. Estimated Net Margin |  $46.96 |
| Promo Usage               |    0.0% |
| Total Estimated Margin    | $23,574 |

For the strategic analysis, this second definition is used to identify **high-margin organic customers**, because it explicitly separates repeat behavior from promotional dependence.

Importantly, these are **analytical definitions**, not claims that the customers are permanently loyal or will remain active in the future.

---

## 7. Promotional Behavior & Margin

One of the main findings is the difference in estimated margin between customers who used promotions and those who did not.

| Customer Group      | Customers | Avg. Estimated Net Margin |
| ------------------- | --------: | ------------------------: |
| Promo Users         |     1,794 |                    $24.66 |
| Non-Promo Customers |     2,106 |                    $30.36 |

The difference is approximately **$5.70 per customer**.

A two-sample t-test was conducted to assess whether the observed difference in estimated margins was statistically significant.

**Result:**

* Mean difference: **$5.70**
* 95% confidence interval: **$4.90 – $6.50**
* t-statistic: **13.77**
* p-value: **< 0.001**
* Cohen's d: **0.44**

The result indicates a statistically significant difference in estimated margin between the two groups, with a moderate standardized effect size.

### Important interpretation

This analysis is **observational**.

It does not establish that promotions caused the lower margins. Customers who use promotions may already differ from non-promo customers in ways that are not captured in the dataset.

Therefore, the finding should be interpreted as:

> **Promo users are associated with lower estimated margins in this dataset, but the analysis does not establish causality.**

A controlled experiment would be required to measure the causal impact of changing promotional policy.

---

## 8. Geographic Opportunity

States were evaluated using three factors:

* Estimated margin
* Customer volume
* Non-promo customer rate

A composite opportunity score was created using:

```text
40% → Normalized Margin
30% → Normalized Customer Volume
30% → Normalized Non-Promo Rate
```

States with fewer than 50 customers were excluded from the final opportunity ranking to avoid over-interpreting very small samples.

### Highest-ranked opportunities

| Rank | State       | Opportunity Score |
| ---: | ----------- | ----------------: |
|    1 | Mississippi |             68.86 |
|    2 | Alaska      |             68.66 |
|    3 | Illinois    |             66.85 |
|    4 | Missouri    |             65.96 |
|    5 | Delaware    |             65.57 |

These states should be viewed as **candidate markets for further investigation**, rather than definitive expansion recommendations.

Before allocating significant marketing spend, the brand should validate these opportunities using additional information such as acquisition cost, market size, competition, and historical sales trends.

---

## 9. Category Analysis

Customer distribution and purchasing behavior were also analyzed across the four major product categories.

| Category    | Customers | Share | Avg. Purchase Amount | Avg. Previous Purchases |
| ----------- | --------: | ----: | -------------------: | ----------------------: |
| Clothing    |     1,659 | 42.5% |               $59.70 |                    25.5 |
| Accessories |     1,240 | 31.8% |               $59.69 |                    25.4 |
| Footwear    |       692 | 17.7% |               $60.30 |                    25.4 |
| Outerwear   |       309 |  7.9% |               $57.20 |                    25.9 |

Clothing represents the largest share of customers, while purchase frequency is relatively similar across categories.

This suggests that category differences in customer value are more nuanced than simply looking at sales volume.

---

## 10. Ideal Customer Profile

The analysis uses **High Value Organic** customers as the preferred ICP for strategic comparison.

### High Value Organic vs. Overall Customer Base

| Metric                  | High Value Organic | Overall |       Difference |
| ----------------------- | -----------------: | ------: | ---------------: |
| Customers               |                940 |   3,900 |    24.1% of base |
| Avg. Purchase Amount    |             $77.00 |  $59.12 |           +30.2% |
| Avg. Previous Purchases |               29.8 |    25.5 |             +4.3 |
| Avg. Est. Net Margin    |             $41.20 |  $27.74 |           +48.5% |
| Observed Promo Usage    |                 0% |   46.0% | Lower dependence |

### Profile characteristics

The segment is characterized by:

* Higher average spending
* More historical purchases
* Higher estimated margins
* No observed promo-code usage
* A greater concentration of credit-card payments
* A greater concentration of 2-Day Shipping

The purpose of the ICP is not to describe a demographic stereotype, but to identify **behavioral characteristics associated with higher customer value** in this dataset.

---

## 11. Key Business Insights

### 1. Revenue alone is not enough

The highest-spending customers are not necessarily the most profitable customers.

The High Spend Bargain Hunter segment has higher average spending than the High Value Organic segment, but slightly lower estimated margin.

---

### 2. Organic repeat customers are particularly attractive

High Value Organic customers combine:

* Strong historical purchase behavior
* Higher average order value
* Higher estimated margin
* No observed promotional usage

This makes them a useful benchmark for customer acquisition and retention strategies.

---

### 3. Promotions are associated with lower estimated margins

Promo users have lower average estimated margins than non-promo customers.

However, because the data is observational, this should be treated as an **association rather than a causal conclusion**.

---

### 4. Promotional strategy should focus on efficiency, not simply elimination

The goal should not be to remove discounts for every customer.

Instead, the brand could test whether some customers can be moved from percentage-based discounts toward alternatives such as:

* Free shipping above a minimum basket value
* Threshold-based offers
* Loyalty rewards
* Personalized incentives
* Non-monetary benefits

This could potentially protect conversion while improving economics.

---

### 5. Geographic opportunities require validation

The geographic scoring model identifies states with attractive combinations of volume, margin, and organic purchasing behavior.

These states provide a shortlist for further investigation rather than a final market-expansion decision.

---

## 12. Promotional Strategy Experiment

To move from observational analysis to causal measurement, a controlled experiment is proposed.

### Test

Compare:

**Control:** Existing promotional strategy

**Treatment:** Free shipping above a defined order-value threshold (e.g. $75)

Customers would be randomly assigned to the two groups.

### Primary Metric

**Net Margin Per User (NMPU)**

This metric is preferred over revenue alone because the objective is to improve customer economics rather than simply increase sales.

### Guardrail Metric

**Conversion Rate**

A potential decision rule is to investigate or stop the treatment if conversion falls by more than **5% relative to the control group**.

Additional metrics should include:

* Average order value
* Revenue per user
* Estimated margin per order
* Promo redemption rate
* Repeat purchase behavior

The experiment should be powered using an appropriate sample-size calculation before launch.

---

## 13. Cost & Margin Modeling

The original dataset does not provide accounting-level cost data or actual discount percentages.

Therefore, estimated margin is based on explicit modeling assumptions.

### Discount assumption

For customers with `Discount Applied = Yes`, gross purchase value is estimated as:

```text
Estimated Gross Amount = Purchase Amount / 0.80
```

This assumes a 20% discount.

### Cost assumptions

The analysis uses scenario assumptions for:

* COGS: 30%, 40%, or 50%
* Fulfillment: $5 per order

These values are **analytical assumptions and not actual company accounting figures**.

The resulting margin should therefore be interpreted as **estimated contribution margin under the modeled assumptions**, not reported financial margin.

---

## 14. Limitations

### No order-level timestamps

The dataset is customer-level and does not contain complete historical order dates.

Therefore, the project cannot accurately calculate:

* Monthly retention
* M1 / M3 / M6 retention
* Cohort retention curves
* Actual churn dates
* Time between purchases

`Previous Purchases` is treated as a historical purchase-count variable rather than a timestamp-based retention measure.

### Promotional causality

Customers were not randomly assigned to promotions.

Therefore, the statistical test identifies an association between promo usage and estimated margin, not a causal effect.

### Modeled economics

Discounts, COGS, and fulfillment costs are assumptions used for analytical purposes.

Actual business decisions should use accounting and transaction-level data.

### Customer-level dataset

Because each record represents a customer rather than a complete order history, the analysis cannot evaluate detailed order sequences or product-level purchase journeys.

### Geographic scoring

The opportunity score is a prioritization framework rather than a direct forecast of incremental revenue.

---

## 15. Project Structure

```text
project/
│
├── data/
│   ├── raw/
│   │   └── real_shopping_trends.csv
│   │
│   └── processed/
│       └── engineered_customer_master.csv
│
├── database/
│   └── retention_analytics.db
│
├── src/
│   ├── 01_process_user_dataset.py
│   └── 03_run_sql_analysis.py
│
├── sql/
│   └── *.sql
│
├── dashboard/
│   ├── *.csv
│   └── customer_value.pbix
│
├── deliverables/
│   └── retention_playbook.md
│
└── README.md
```

---

## 16. Dashboard

The Power BI dashboard provides an executive view of:

### KPI Summary

* Total Customers
* Purchase Amount
* Estimated Net Margin
* Promo Usage
* Average Purchase Amount

### Customer Value

* Segment distribution
* Spend vs. estimated margin
* Repeat purchasing behavior

### Promotional Analysis

* Promo vs. non-promo customers
* Estimated margin comparison
* Customer segment and promotion patterns

### Geographic Analysis

* State-level customer distribution
* Margin performance
* Organic customer opportunity

### Category Analysis

* Customer distribution
* Average purchase amount
* Historical purchase behavior

---

## 17. Final Takeaway

The central finding from this analysis is that **customer value cannot be evaluated using revenue alone**.

A smaller group of customers who spend consistently without relying on promotions can generate stronger estimated economics than customers with similar or higher spending but greater promotional dependence.

The recommended strategy is therefore not simply to reduce discounts. Instead, the brand should:

1. Identify and retain high-value organic customers.
2. Understand which customers genuinely require incentives.
3. Shift from broad discounts toward targeted or threshold-based offers.
4. Prioritize promising geographic markets for further testing.
5. Validate promotional changes through randomized experimentation.
6. Optimize for **margin and customer value alongside revenue and conversion**.

This creates a more sustainable retention strategy focused on **profitable customer relationships rather than sales volume alone**.
