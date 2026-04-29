import polars as pl
import duckdb

# 1. Update these paths
csv_path = "M:/nifty_500_cleaned.csv" # Point to your clean CSV
db_path = "M:/stocks.db"

# 2. Read the CSV (Much faster than Excel!)
df = pl.read_csv(csv_path)

# 3. Use 'OR REPLACE' to swap the old table with the clean one
with duckdb.connect(db_path) as con:
    con.execute("CREATE OR REPLACE TABLE nifty_500 AS SELECT * FROM df")
    print(f"✅ Successfully REPLACED with cleaned data in {db_path}")