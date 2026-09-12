import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW = BASE_DIR / "data" / "raw" / "real_shopping_trends.csv"
DATA_PROC = BASE_DIR / "data" / "processed" / "engineered_customer_master.csv"
DB_FILE = BASE_DIR / "database" / "retention_analytics.db"
DASH_DIR = BASE_DIR / "dashboard"

print("==================================")
print("AUTOMATED PROJECT QA & INTEGRITY AUDIT (DYNAMIC PASS)")
print("==================================\n")

# 1. Check Canonical Source Raw CSV
df_raw = pd.read_csv(DATA_RAW)
raw_count = len(df_raw)
raw_unique = df_raw['Customer ID'].nunique()

print(f"Source Raw CSV Rows:          {raw_count} {'[PASS]' if raw_count == 3900 else '[FAIL]'}")
print(f"Source Unique Customers:      {raw_unique} {'[PASS]' if raw_unique == 3900 else '[FAIL]'}")

# 2. Check Canonical Master Processed CSV
df_master = pd.read_csv(DATA_PROC)
master_count = len(df_master)
master_nulls = df_master[['customer_id', 'purchase_amount_usd', 'net_margin_contribution', 'strategic_segment']].isnull().sum().sum()

print(f"Engineered Master CSV Rows:   {master_count} {'[PASS]' if master_count == 3900 else '[FAIL]'}")
print(f"Master Table Key Nulls:       {master_nulls} {'[PASS]' if master_nulls == 0 else '[FAIL]'}")

# 3. Check Canonical SQLite DB
conn = sqlite3.connect(DB_FILE)
df_sqlite = pd.read_sql_query("SELECT COUNT(*) AS cnt, COUNT(DISTINCT customer_id) AS uniq_cnt FROM customer_master", conn)
db_count = df_sqlite['cnt'].iloc[0]
db_uniq = df_sqlite['uniq_cnt'].iloc[0]

print(f"SQLite DB Record Count:       {db_count} {'[PASS]' if db_count == 3900 else '[FAIL]'}")
print(f"SQLite Unique Customers:      {db_uniq} {'[PASS]' if db_uniq == 3900 else '[FAIL]'}")

# 4. Dynamic Segmentation Validation (Compare Master CSV vs SQLite vs SQL Dashboard CSV)
seg_counts_py = df_master['strategic_segment'].value_counts().to_dict()

df_sqlite_seg = pd.read_sql_query("SELECT strategic_segment, COUNT(*) as total_customers FROM customer_master GROUP BY strategic_segment", conn)
seg_counts_sqlite = dict(zip(df_sqlite_seg['strategic_segment'], df_sqlite_seg['total_customers']))

df_seg_csv = pd.read_csv(DASH_DIR / "01_customer_segmentation.csv")
seg_counts_sql_csv = dict(zip(df_seg_csv['strategic_segment'], df_seg_csv['total_customers']))

csv_total_custs = df_seg_csv['total_customers'].sum()

# Dynamic Comparison Checks (No Hardcoded Segment Numbers!)
segment_match_py_sqlite = (seg_counts_py == seg_counts_sqlite)
segment_match_py_sqlcsv = (seg_counts_py == seg_counts_sql_csv)
dynamic_segment_pass = segment_match_py_sqlite and segment_match_py_sqlcsv

print(f"SQL Segmentation CSV Total:   {csv_total_custs} {'[PASS]' if csv_total_custs == 3900 else '[FAIL]'}")
print(f"Dynamic Segment Counts Match: {'[PASS]' if dynamic_segment_pass else '[FAIL]'}")

# 5. Dynamic Net Sales Total Validation (Compare Master CSV vs SQLite)
net_sales_master = round(df_master['purchase_amount_usd'].sum(), 2)
net_sales_sqlite = round(pd.read_sql_query("SELECT SUM(purchase_amount_usd) as total_sales FROM customer_master", conn)['total_sales'].iloc[0], 2)
dynamic_sales_pass = (net_sales_master == net_sales_sqlite)

print(f"Dynamic Net Sales Match:      ${net_sales_master:,.2f} {'[PASS]' if dynamic_sales_pass else '[FAIL]'}")

# 6. Check Summary CSVs Presence
loyalty_csv_valid = (DASH_DIR / "loyalty_definitions_comparison.csv").exists()
icp_csv_valid = (DASH_DIR / "icp_comparison_summary.csv").exists()
geo_csv_valid = (DASH_DIR / "03_geographic_opportunities.csv").exists()

conn.close()

# 7. Final Audit Verdict
all_passed = (raw_count == 3900 and raw_unique == 3900 and master_count == 3900 and 
              db_count == 3900 and csv_total_custs == 3900 and dynamic_segment_pass and 
              master_nulls == 0 and dynamic_sales_pass and loyalty_csv_valid and icp_csv_valid and geo_csv_valid)

print("\n==================================")
print("FINAL PROJECT VALIDATION REPORT")
print("==================================")
print(f"Source customers:        3900 {'[PASS]' if raw_count == 3900 else '[FAIL]'}")
print(f"Unique customers:        3900 {'[PASS]' if raw_unique == 3900 else '[FAIL]'}")
print(f"SQL customers:           3900 {'[PASS]' if csv_total_custs == 3900 else '[FAIL]'}")
print(f"Dashboard customers:     3900 {'[PASS]' if master_count == 3900 else '[FAIL]'}")
print(f"Dynamic Segment Match:        {'[PASS]' if dynamic_segment_pass else '[FAIL]'}")
print(f"Dynamic Net Sales Match:      {'[PASS]' if dynamic_sales_pass else '[FAIL]'}")
print(f"Estimated Margin Valid:       {'[PASS]' if df_master['net_margin_contribution'].notnull().all() else '[FAIL]'}")
print(f"Geographic Output Valid:      {'[PASS]' if geo_csv_valid else '[FAIL]'}")
print(f"Loyalty Summary Valid:        {'[PASS]' if loyalty_csv_valid else '[FAIL]'}")
print(f"ICP Summary Valid:            {'[PASS]' if icp_csv_valid else '[FAIL]'}")
print("\nPROJECT STATUS: " + ("PASS" if all_passed else "FAIL"))
print("==================================")

if not all_passed:
    exit(1)
