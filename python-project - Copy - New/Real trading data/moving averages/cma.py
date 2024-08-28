import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Cumulative Moving Average (CMA)
def calculate_cma(data):
    """
    Calculate the Cumulative Moving Average (CMA).
    """
    data['CMA'] = data['Close'].expanding().mean()
    return data

# Calculate CMA
data = calculate_cma(data)

# Create subplots: one for Close Prices and one for CMA
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.plot(data.index, data['CMA'], label='Cumulative Moving Average', color='orange')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Cumulative Moving Average (CMA)')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
