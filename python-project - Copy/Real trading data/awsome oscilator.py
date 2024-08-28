import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Awesome Oscillator
def awesome_oscillator(data, short_window=5, long_window=34):
    """
    Calculate the Awesome Oscillator (AO).
    """
    # Calculate Median Price
    data['Median_Price'] = (data['High'] + data['Low']) / 2
    
    # Calculate short and long SMAs of the Median Price
    data['SMA_Short'] = data['Median_Price'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Median_Price'].rolling(window=long_window).mean()
    
    # Calculate AO Line
    data['AO'] = data['SMA_Short'] - data['SMA_Long']
    
    return data

# Set parameters
short_window = 5
long_window = 34

# Calculate AO
data = awesome_oscillator(data, short_window=short_window, long_window=long_window)

# Create subplots: one for Close Prices and one for Awesome Oscillator
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.set_ylabel('Close Price')
ax1.set_title(f'{ticker} - Awesome Oscillator and Close Price')
ax1.grid(True)

# Plot Awesome Oscillator
colors = ['green' if value >= 0 else 'red' for value in data['AO']]
ax2.bar(data.index, data['AO'], color=colors, alpha=0.6)
ax2.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax2.set_xlabel('Date')
ax2.set_ylabel('AO')
ax2.legend(loc='upper left')
ax2.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
