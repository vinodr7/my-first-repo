import duckdb
import polars as pl

# 1. Connect to your M: drive
con = duckdb.connect("M:/stocks.db")

# 2. Select the columns you want to "profile"
# Using quotes inside the string to handle the (%) and spaces
query = """
SELECT 
    "ROE Annual %", 
    "Net Profit Annual YoY Growth %",
    "Market Capitalization"
FROM nifty_500
"""

# 3. Fetch data and run Univariate Analysis
df = con.execute(query).pl()

# The .describe() method is the standard way to do Univariate Analysis in one line
print(df.describe())