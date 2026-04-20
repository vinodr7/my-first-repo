import yfinance as yf
import polars as pl
from colorama import Fore, Style, init

init(autoreset=True)

def analyze_stock(symbol):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}🔍 ANALYZING: {symbol}")
    ticker = yf.Ticker(symbol)
    
    # 1. Pull Financials
    fin = ticker.financials.T
    if fin.empty:
        print(Fore.RED + "Error: Data not found.")
        return
    
    # Convert to Polars and handle missing data
    # .fill_null(0) replaces 'None' with 0 so the math doesn't break
    df = pl.from_pandas(fin.reset_index()).fill_null(0)
    
    # 2. Get Revenue and Profit (Oldest to Newest)
    revenues = df["Total Revenue"].to_list()[::-1]
    profits = df["Net Income"].to_list()[::-1]
    
    # 3. Flexible Growth Logic: Compare Latest vs. 3 Years Ago
    # This is less "brittle" than checking every single year
    rev_growth = ((revenues[-1] / revenues[0]) - 1) * 100 if revenues[0] != 0 else 0
    
    # 4. Red Flag Check: Debt-to-Equity (Crucial for stability)
    info = ticker.info
    debt_equity = info.get('debtToEquity', 0)
    
    # 5. The "Investable" Verdict
    is_growing = rev_growth > 10  # Looking for >10% growth over 3 years
    no_debt_flag = debt_equity < 200 # Standard threshold (2.0 or 200%)
    
    if is_growing and no_debt_flag:
        print(Fore.GREEN + f"✅ QUALITY BUSINESS: {rev_growth:.1f}% Growth | Debt/Equity: {debt_equity}")
    else:
        status = []
        if not is_growing: status.append("Low Growth")
        if not no_debt_flag: status.append("High Debt")
        print(Fore.YELLOW + f"⚠️ STABILITY CHECK: {', '.join(status)}")

    print(f"Latest Revenue: ${revenues[-1]:,.0f}")

# TEST
for t in ["MSFT", "AAPL", "GOOGL","NVDA", "AMZN", "TSLA", "META", "NFLX","AVGO", "MU", "JPM","MS","GS"]:
    analyze_stock(t)