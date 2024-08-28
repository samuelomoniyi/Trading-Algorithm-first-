import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Volume Oscillator
def calculate_volume_oscillator(data, short_window=14, long_window=28):
    """
    Calculate the Volume Oscillator (VO).
    """
    # Calculate short and long volume moving averages
    data['Volume_SMA_Short'] = data['Volume'].rolling(window=short_window).mean()
    data['Volume_SMA_Long'] = data['Volume'].rolling(window=long_window).mean()
    
    # Calculate Volume Oscillator (VO)
    data['Volume_Oscillator'] = data['Volume_SMA_Short'] - data['Volume_SMA_Long']
    
    return data

# Set parameters
short_window = 14
long_window = 28

# Calculate Volume Oscillator
data = calculate_volume_oscillator(data, short_window=short_window, long_window=long_window)

# Create subplots: one for Volume and one for Volume Oscillator
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Volume
ax1.bar(data.index, data['Volume'], color='blue', alpha=0.6)
ax1.set_ylabel('Volume')
ax1.set_title(f'{ticker} - Volume and Volume Oscillator')
ax1.grid(True)

# Plot Volume Oscillator
colors = ['green' if value >= 0 else 'red' for value in data['Volume_Oscillator']]
ax2.bar(data.index, data['Volume_Oscillator'], color=colors, alpha=0.6)
ax2.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax2.set_xlabel('Date')
ax2.set_ylabel('Volume Oscillator')
ax2.legend(loc='upper left')
ax2.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
