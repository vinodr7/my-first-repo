### Capture the ROE of the stock
import yfinance as yf

stock_aapl = yf.Ticker("AAPL")
roe_aapl = stock_aapl.info.get("returnOnEquity")

stock_msft = yf.Ticker("MSFT")
roe_msft = stock_msft.info.get("returnOnEquity")

stock_googl = yf.Ticker("GOOGL")
roe_googl = stock_googl.info.get("returnOnEquity")

print(f"ROE of AAPL: {roe_aapl}")
print(f"ROE of MSFT: {roe_msft}")
print(f"ROE of GOOGL: {roe_googl}")