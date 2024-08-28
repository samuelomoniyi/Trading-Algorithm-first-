import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate EMA
def calculate_ema(data, short_window=12, long_window=26):
    """
    Calculate Exponential Moving Averages (EMA).
    """
    # Calculate short-term and long-term EMAs
    data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    return data

# Set parameters
short_window = 12
long_window = 26

# Calculate EMAs
data = calculate_ema(data, short_window=short_window, long_window=long_window)

# Create subplots: one for Close Prices and one for EMA
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.plot(data.index, data['EMA_Short'], label=f'EMA {short_window} days', color='orange')
ax1.plot(data.index, data['EMA_Long'], label=f'EMA {long_window} days', color='red')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Exponential Moving Averages (EMA)')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
