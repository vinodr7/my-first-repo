import duckdb
import polars as pl

# 1. Connect to your M: drive database
db_path = "M:/stocks.db"
con = duckdb.connect(db_path)

# 2. Pull the data into Polars (Polars handles 261 columns very fast)
df = con.execute("SELECT * FROM nifty_500").pl()

# 3. Identify and remove duplicate column names
# Python sets don't allow duplicates, so we use them to filter
cols = df.columns
unique_cols = []
seen = set()

for col in cols:
    # We use .lower() to catch 'Revenue' vs 'revenue'
    clean_name = col.strip().lower()
    if clean_name not in seen:
        seen.add(clean_name)
        unique_cols.append(col)

# 4. Create the cleaned DataFrame
df_clean = df.select(unique_cols)

# 5. Overwrite the table in DuckDB
con.execute("DROP TABLE IF EXISTS nifty_500")
con.execute("CREATE TABLE nifty_500 AS SELECT * FROM df_clean")

print(f"✅ Clean-up Complete!")
print(f"Original columns: {len(cols)}")
print(f"Unique columns kept: {len(unique_cols)}")