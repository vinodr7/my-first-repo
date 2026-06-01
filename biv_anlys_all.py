import duckdb
import polars as pl

con = duckdb.connect("M:/stocks.db", read_only=True)

# 1. Fetch data
columns = ['"Revenue Growth Annual YoY %"', '"Net Profit Annual YoY Growth %"']
df = con.execute(f"SELECT {', '.join(columns)} FROM nifty_500").pl()

# 2. CLEANING: Remove Nulls + Filter Outliers
# We remove the 10,000% jumps so they don't break the math
df_clean = (
    df.drop_nulls()
    .filter(
        (pl.col(df.columns[0]) > -100) & (pl.col(df.columns[0]) < 500) &
        (pl.col(df.columns[1]) > -100) & (pl.col(df.columns[1]) < 500)
    )
)

# 3. Calculate Correlation
matrix = df_clean.corr()

print(f"--- BIVARIATE CORRELATION (Outliers Removed) ---")
print(f"Rows analyzed: {len(df_clean)} of 500")
print(matrix)