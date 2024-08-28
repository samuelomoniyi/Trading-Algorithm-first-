import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate RSI
def rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI).
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Calculate RSI and add it to the DataFrame
data['RSI'] = rsi(data)

# Create subplots: one for Close Prices and one for RSI
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.set_ylabel('Close Price')
ax1.set_title(f'{ticker} - Closing Prices and RSI')
ax1.grid(True)

# Plot RSI
ax2.plot(data.index, data['RSI'], label='RSI', color='orange')
ax2.axhline(70, color='red', linestyle='--', label='Overbought (70)')
ax2.axhline(30, color='green', linestyle='--', label='Oversold (30)')
ax2.set_xlabel('Date')
ax2.set_ylabel('RSI')
ax2.legend(loc='upper left')
ax2.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
