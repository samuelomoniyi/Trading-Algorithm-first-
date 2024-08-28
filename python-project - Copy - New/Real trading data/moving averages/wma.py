import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Weighted Moving Average (WMA)
def calculate_wma(data, window=14):
    """
    Calculate the Weighted Moving Average (WMA).
    """
    weights = np.arange(1, window + 1)
    data['WMA'] = data['Close'].rolling(window=window).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    
    return data

# Set parameter
window = 14

# Calculate WMA
data = calculate_wma(data, window=window)

# Create subplots: one for Close Prices and one for WMA
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.plot(data.index, data['WMA'], label=f'WMA {window} days', color='orange')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Weighted Moving Average (WMA)')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
