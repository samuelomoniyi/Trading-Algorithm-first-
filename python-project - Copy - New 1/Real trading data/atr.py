import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Average True Range (ATR)
def calculate_atr(data, window=14):
    """
    Calculate the Average True Range (ATR).
    """
    # Calculate True Range (TR)
    data['Prev_Close'] = data['Close'].shift(1)
    data['TR'] = pd.concat([
        data['High'] - data['Low'],
        abs(data['High'] - data['Prev_Close']),
        abs(data['Low'] - data['Prev_Close'])
    ], axis=1).max(axis=1)
    
    # Calculate ATR
    data['ATR'] = data['TR'].rolling(window=window).mean()
    
    return data

# Set parameter
window = 14

# Calculate ATR
data = calculate_atr(data, window=window)

# Create subplots: one for Close Prices and one for ATR
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.set_ylabel('Close Price')
ax1.set_title(f'{ticker} - ATR and Close Price')
ax1.grid(True)

# Plot ATR
ax2.plot(data.index, data['ATR'], label='ATR', color='orange')
ax2.set_xlabel('Date')
ax2.set_ylabel('ATR')
ax2.legend(loc='upper left')
ax2.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
