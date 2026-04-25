import yfinance as yf

# Example: Checking Reliance on NSE
ticker = yf.Ticker("RELIANCE.NS")
print(ticker.info)

# Example: Checking TCS on BSE
ticker_bse = yf.Ticker("TCS.BO")
print(ticker_bse.financials)