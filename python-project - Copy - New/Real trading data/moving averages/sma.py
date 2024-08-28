import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate SMA
def calculate_sma(data, short_window=20, long_window=50):
    """
    Calculate Simple Moving Averages (SMA).
    """
    # Calculate short-term and long-term SMAs
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    
    return data

# Set parameters
short_window = 20
long_window = 50

# Calculate SMAs
data = calculate_sma(data, short_window=short_window, long_window=long_window)

# Create subplots: one for Close Prices and one for SMA
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.plot(data.index, data['SMA_Short'], label=f'SMA {short_window} days', color='orange')
ax1.plot(data.index, data['SMA_Long'], label=f'SMA {long_window} days', color='red')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Simple Moving Averages (SMA)')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
