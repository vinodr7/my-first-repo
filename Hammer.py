import polars as pl
import duckdb

# 1. Keep the .xlsx path
excel_path = "M:/2026-04-26-nifty-500.xlsx"
db_path = "M:/stocks.db"

# 2. Use read_excel instead of read_csv
# We use openpyxl because it's the one Windows didn't block
df = pl.read_excel(excel_path, engine="openpyxl")

# 3. Connect and FORCE the clean-up
with duckdb.connect(db_path) as con:
    con.execute("DROP TABLE IF EXISTS nifty_500")
    con.execute("CREATE TABLE nifty_500 AS SELECT * FROM df")
    
    # Final Verification
    count = con.execute("SELECT count(*) FROM information_schema.columns WHERE table_name = 'nifty_500'").fetchone()[0]
    print(f"✅ Success! Database now has {count} columns.")