import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Calculate MACD, Signal Line, and MACD Histogram.
    """
    # Calculate the short and long EMA
    data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    # Calculate the MACD Line
    data['MACD_Line'] = data['EMA_Short'] - data['EMA_Long']
    
    # Calculate the Signal Line
    data['Signal_Line'] = data['MACD_Line'].ewm(span=signal_window, adjust=False).mean()
    
    # Calculate the MACD Histogram
    data['MACD_Histogram'] = data['MACD_Line'] - data['Signal_Line']
    
    return data

# Set parameters
short_window = 12
long_window = 26
signal_window = 9

# Calculate MACD components
data = calculate_macd(data, short_window=short_window, long_window=long_window, signal_window=signal_window)

# Create subplots: one for Close Prices, one for MACD Line and Signal Line, and one for MACD Histogram
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(14, 12), sharex=True)

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.set_ylabel('Close Price')
ax1.set_title(f'{ticker} - MACD and Close Price')
ax1.grid(True)

# Plot MACD Line and Signal Line
ax2.plot(data.index, data['MACD_Line'], label='MACD Line', color='blue')
ax2.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
ax2.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax2.set_ylabel('MACD')
ax2.legend(loc='upper left')
ax2.grid(True)

# Plot MACD Histogram
colors = np.where(data['MACD_Histogram'] >= 0, 'green', 'red')
ax3.bar(data.index, data['MACD_Histogram'], color=colors, alpha=0.6)
ax3.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax3.set_xlabel('Date')
ax3.set_ylabel('MACD Histogram')
ax3.legend(loc='upper left')
ax3.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
