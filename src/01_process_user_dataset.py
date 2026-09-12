import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path
from scipy import stats

# Pathlib relative BASE_DIR (one level up from src/)
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROC_DIR = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "database"
DASHBOARD_DIR = BASE_DIR / "dashboard"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROC_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

raw_csv_path = DATA_RAW_DIR / "real_shopping_trends.csv"

# Fallback check if raw CSV is at root data/
root_raw = BASE_DIR / "data" / "real_shopping_trends.csv"
if not raw_csv_path.exists() and root_raw.exists():
    df_temp = pd.read_csv(root_raw)
    df_temp.to_csv(raw_csv_path, index=False)

print("Executing Audit-Compliant Python Pipeline (Relative Paths & Single Source)...")

df = pd.read_csv(raw_csv_path)
total_rows = len(df)
unique_custs = df['Customer ID'].nunique()
unique_states = df['Location'].nunique()

print(f"Loaded {total_rows} customer records across {unique_states} U.S. states.")
assert total_rows == 3900, f"Expected 3900 rows, found {total_rows}"
assert unique_custs == 3900, f"Expected 3900 unique customers, found {unique_custs}"

df_clean = df.copy()
df_clean.rename(columns={
    'Customer ID': 'customer_id',
    'Age': 'age',
    'Gender': 'gender',
    'Item Purchased': 'item_purchased',
    'Category': 'category',
    'Purchase Amount (USD)': 'purchase_amount_usd',
    'Location': 'state',
    'Size': 'size',
    'Color': 'color',
    'Season': 'season',
    'Review Rating': 'satisfaction_score',
    'Subscription Status': 'subscription_status',
    'Shipping Type': 'shipping_type',
    'Discount Applied': 'discount_applied',
    'Promo Code Used': 'promo_code_used',
    'Previous Purchases': 'previous_purchases',
    'Payment Method': 'payment_method',
    'Frequency of Purchases': 'frequency_of_purchases'
}, inplace=True)

# Standardize Terminology & Behavioral Proxies
df_clean['observed_category'] = df_clean['category']
df_clean['estimated_total_purchases'] = df_clean['previous_purchases'] + 1
df_clean['observed_promo_usage'] = np.where(df_clean['promo_code_used'] == 'Yes', 1, 0)

freq_proxy_map = {
    'Weekly': 7, 'Bi-Weekly': 14, 'Fortnightly': 14, 'Monthly': 30,
    'Every 3 Months': 90, 'Quarterly': 90, 'Annually': 365
}
df_clean['frequency_proxy_days'] = df_clean['frequency_of_purchases'].map(freq_proxy_map).fillna(30)

# 20% DISCOUNT MODELING ASSUMPTION:
# The raw dataset provides 'Discount Applied' (Yes/No) but does not provide the actual discount percentage.
# We model an assumed 20% discount rate when Discount Applied == 'Yes' (gross_amount = purchase_amount_usd / 0.8).
df_clean['gross_amount'] = np.where(df_clean['discount_applied'] == 'Yes', df_clean['purchase_amount_usd'] / 0.8, df_clean['purchase_amount_usd'])
df_clean['gross_amount'] = round(df_clean['gross_amount'], 2)
df_clean['discount_amount'] = round(df_clean['gross_amount'] - df_clean['purchase_amount_usd'], 2)

# ESTIMATED MARGIN CONTRIBUTION ASSUMPTIONS:
# COGS (30%, 40%, 50%) and fulfillment ($5/order) are modeled scenario assumptions, not actual accounting entries.
FULFILLMENT_ESTIMATE = 5.0
df_clean['estimated_cogs_40'] = round(df_clean['gross_amount'] * 0.40, 2)
df_clean['net_margin_contribution'] = round(df_clean['purchase_amount_usd'] - df_clean['estimated_cogs_40'] - FULFILLMENT_ESTIMATE, 2)
df_clean['margin_cogs_30'] = round(df_clean['purchase_amount_usd'] - (df_clean['gross_amount'] * 0.30) - FULFILLMENT_ESTIMATE, 2)
df_clean['margin_cogs_50'] = round(df_clean['purchase_amount_usd'] - (df_clean['gross_amount'] * 0.50) - FULFILLMENT_ESTIMATE, 2)

# DECOUPLED LOYALTY DEFINITIONS (NON-CIRCULAR)
spend_75_pctile = df_clean['purchase_amount_usd'].quantile(0.75)  # $78.00
margin_75_pctile = df_clean['net_margin_contribution'].quantile(0.75) # $34.20
margin_median = df_clean['net_margin_contribution'].median() # $23.80

df_clean['loyalty_def_A_behavioral'] = (df_clean['previous_purchases'] >= 20) & (df_clean['purchase_amount_usd'] >= spend_75_pctile)
df_clean['loyalty_def_B_organic_margin'] = (df_clean['previous_purchases'] >= 15) & (df_clean['net_margin_contribution'] >= margin_75_pctile) & (df_clean['promo_code_used'] == 'No')

def_A_mask = df_clean['loyalty_def_A_behavioral'] == 1
def_B_mask = df_clean['loyalty_def_B_organic_margin'] == 1

loyalty_comparison = pd.DataFrame({
    'Metric': [
        'Customer Count',
        'Customer Share (%)',
        'Avg Purchase Amount ($)',
        'Avg Historical Purchases',
        'Avg Estimated Net Margin ($)',
        'Total Estimated Net Margin ($)',
        'Observed Promo Usage (%)'
    ],
    'Definition A (Behavioral)': [
        def_A_mask.sum(),
        round(def_A_mask.mean() * 100, 2),
        round(df_clean[def_A_mask]['purchase_amount_usd'].mean(), 2),
        round(df_clean[def_A_mask]['previous_purchases'].mean(), 2),
        round(df_clean[def_A_mask]['net_margin_contribution'].mean(), 2),
        round(df_clean[def_A_mask]['net_margin_contribution'].sum(), 2),
        round(df_clean[def_A_mask]['observed_promo_usage'].mean() * 100, 2)
    ],
    'Definition B (Economic/Organic)': [
        def_B_mask.sum(),
        round(def_B_mask.mean() * 100, 2),
        round(df_clean[def_B_mask]['purchase_amount_usd'].mean(), 2),
        round(df_clean[def_B_mask]['previous_purchases'].mean(), 2),
        round(df_clean[def_B_mask]['net_margin_contribution'].mean(), 2),
        round(df_clean[def_B_mask]['net_margin_contribution'].sum(), 2),
        round(df_clean[def_B_mask]['observed_promo_usage'].mean() * 100, 2)
    ]
})

# AUTHORITATIVE 4-TIER STRATEGIC SEGMENTATION
def get_authoritative_segment(row):
    if (row['net_margin_contribution'] > margin_median) and (row['promo_code_used'] == 'No') and (row['previous_purchases'] >= 10):
        return '1. High Value Organic'
    elif (row['purchase_amount_usd'] >= spend_75_pctile) and (row['promo_code_used'] == 'Yes'):
        return '2. High Spend Bargain Hunter'
    elif (row['promo_code_used'] == 'Yes'):
        return '3. Promo-Using Repeat'
    else:
        return '4. Mid-Tier Core'

df_clean['strategic_segment'] = df_clean.apply(get_authoritative_segment, axis=1)

# STATISTICAL TESTING (SAMPLE SIZES: Promo n=1794, Non-promo n=2106)
organic_m = df_clean[df_clean['promo_code_used'] == 'No']['net_margin_contribution']
promo_m = df_clean[df_clean['promo_code_used'] == 'Yes']['net_margin_contribution']

mean_diff = organic_m.mean() - promo_m.mean()
t_stat, p_val = stats.ttest_ind(organic_m, promo_m)

n1, n2 = len(organic_m), len(promo_m)
s1, s2 = organic_m.std(), promo_m.std()
se = np.sqrt((s1**2 / n1) + (s2**2 / n2))
ci_low = mean_diff - (1.96 * se)
ci_high = mean_diff + (1.96 * se)
pooled_sd = np.sqrt(((n1 - 1)*s1**2 + (n2 - 1)*s2**2) / (n1 + n2 - 2))
cohens_d = mean_diff / pooled_sd

print(f"\n--- Statistical Testing Output ---")
print(f"Non-Promo Group (n={n1}): Avg Margin = ${organic_m.mean():.2f}")
print(f"Promo Group     (n={n2}): Avg Margin = ${promo_m.mean():.2f}")
print(f"Mean Difference:          ${mean_diff:.2f} (95% CI: [${ci_low:.2f}, ${ci_high:.2f}])")
print(f"t-statistic:              {t_stat:.4f}, p-value: {p_val:.4e}")
print(f"Effect Size (Cohen's d):  {cohens_d:.4f} (Moderate Effect Size)")

# CALCULATED ICP COMPARISON TABLE
icp_mask = df_clean['strategic_segment'] == '1. High Value Organic'

icp_comparison = pd.DataFrame({
    'Attribute': [
        'Customer Count',
        'Average Age',
        'Average Purchase Amount ($)',
        'Avg Historical Purchases',
        'Avg Estimated Net Margin ($)',
        'Observed Promo Usage (%)',
        'Avg Satisfaction Rating',
        'Subscription Status (% Yes)',
        'Top Product Category',
        'Top Payment Method',
        'Top Shipping Method'
    ],
    'Preferred ICP (High Value Organic)': [
        icp_mask.sum(),
        round(df_clean[icp_mask]['age'].mean(), 1),
        round(df_clean[icp_mask]['purchase_amount_usd'].mean(), 2),
        round(df_clean[icp_mask]['previous_purchases'].mean(), 1),
        round(df_clean[icp_mask]['net_margin_contribution'].mean(), 2),
        "0.0% observed promo usage",
        round(df_clean[icp_mask]['satisfaction_score'].mean(), 2),
        round((df_clean[icp_mask]['subscription_status'] == 'Yes').mean() * 100, 1),
        df_clean[icp_mask]['category'].mode()[0],
        f"Most common payment method: {df_clean[icp_mask]['payment_method'].mode()[0]}",
        f"Most common shipping method: {df_clean[icp_mask]['shipping_type'].mode()[0]}"
    ],
    'Overall Population': [
        len(df_clean),
        round(df_clean['age'].mean(), 1),
        round(df_clean['purchase_amount_usd'].mean(), 2),
        round(df_clean['previous_purchases'].mean(), 1),
        round(df_clean['net_margin_contribution'].mean(), 2),
        f"{round(df_clean['observed_promo_usage'].mean() * 100, 1)}% observed promo usage",
        round(df_clean['satisfaction_score'].mean(), 2),
        round((df_clean['subscription_status'] == 'Yes').mean() * 100, 1),
        df_clean['category'].mode()[0],
        f"Most common payment method: {df_clean['payment_method'].mode()[0]}",
        f"Most common shipping method: {df_clean['shipping_type'].mode()[0]}"
    ]
})

# Canonical File Exports (NO DUPLICATE ROOT COPIES)
db_file = DATABASE_DIR / "retention_analytics.db"
conn = sqlite3.connect(db_file)
df_clean.to_sql("customer_master", conn, if_exists="replace", index=False)
loyalty_comparison.to_sql("loyalty_definitions_comparison", conn, if_exists="replace", index=False)
icp_comparison.to_sql("icp_comparison_summary", conn, if_exists="replace", index=False)
conn.close()

export_csv_proc = DATA_PROC_DIR / "engineered_customer_master.csv"
df_clean.to_csv(export_csv_proc, index=False)

loyalty_comparison.to_csv(DASHBOARD_DIR / "loyalty_definitions_comparison.csv", index=False)
icp_comparison.to_csv(DASHBOARD_DIR / "icp_comparison_summary.csv", index=False)

print(f"\nPipeline execution complete. Master table saved strictly to {export_csv_proc} and {db_file}.")
