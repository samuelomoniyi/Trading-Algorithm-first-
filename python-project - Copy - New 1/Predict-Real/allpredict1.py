import yfinance as yf

# Define the ticker symbol for EUR/USD
ticker = 'EURUSD=X'

# Fetch the data from Yahoo Finance
data = yf.Ticker(ticker)

# Get the most recent market data
latest_data = data.history(period='1d')

# Get the current price (most recent closing price)
current_price = latest_data['Close'].iloc[-1]

# Print the current price
print(f"Current EUR/USD price: {current_price}")
