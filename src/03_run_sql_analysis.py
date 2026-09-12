import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "retention_analytics.db"
SQL_DIR = BASE_DIR / "sql"
DASH_DIR = BASE_DIR / "dashboard"

conn = sqlite3.connect(DB_PATH)

sql_files = {
    '01_customer_segmentation.csv': '01_customer_segmentation.sql',
    '02_category_seasonality.csv': '02_category_seasonality.sql',
    '03_geographic_opportunities.csv': '03_geographic_opportunities.sql',
    '04_margin_promotional_sunset.csv': '04_margin_and_promotional_sunset.sql',
    '05_ideal_customer_profile.csv': '05_ideal_customer_profile.sql'
}

print("Running SQL Analytical Query Suite against SQLite Database (Canonical DB)...\n")

for csv_name, sql_name in sql_files.items():
    sql_file_path = SQL_DIR / sql_name
    with open(sql_file_path, 'r') as f:
        query = f.read()
        
    print(f"==================================================")
    print(f"Executing: {sql_name}")
    print(f"==================================================")
    
    df_result = pd.read_sql_query(query, conn)
    print(df_result.head(10))
    print("\n")
    
    export_path = DASH_DIR / csv_name
    df_result.to_csv(export_path, index=False)

# Export Loyalty Comparison & ICP Comparison summary tables to dashboard/
df_loyalty = pd.read_sql_query("SELECT * FROM loyalty_definitions_comparison", conn)
df_loyalty.to_csv(DASH_DIR / "loyalty_definitions_comparison.csv", index=False)

df_icp = pd.read_sql_query("SELECT * FROM icp_comparison_summary", conn)
df_icp.to_csv(DASH_DIR / "icp_comparison_summary.csv", index=False)

conn.close()
print("All SQL queries and summary tables executed successfully and exported to dashboard/ folder!")
