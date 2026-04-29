import duckdb

# 1. Connect to your M: drive
db_path = "M:/stocks.db"
con = duckdb.connect(db_path)

# 2. Get all column names from your table
columns = [row[0] for row in con.execute("DESCRIBE nifty_500").fetchall()]

# 3. Build a dynamic SQL query to calculate stats for every column
subqueries = []
for col in columns:
    safe_col = f'"{col}"'  # Handles spaces and (%) 
    q = f"""
    SELECT 
        '{col}' as column_name,
        COUNT({safe_col}) as total_count,
        COUNT(*) - COUNT({safe_col}) as null_count,
        AVG(TRY_CAST({safe_col} AS DOUBLE)) as mean,
        MIN(TRY_CAST({safe_col} AS DOUBLE)) as min,
        MAX(TRY_CAST({safe_col} AS DOUBLE)) as max
    FROM nifty_500
    """
    subqueries.append(q)

# 4. Combine and execute
full_query = " UNION ALL ".join(subqueries)
con.execute("DROP TABLE IF EXISTS univariate_analysis")
con.execute(f"CREATE TABLE univariate_analysis AS {full_query}")

print("✅ Univariate Analysis complete! Data stored in 'univariate_analysis' table.")
con.close()