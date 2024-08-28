import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    """
    Calculate Bollinger Bands.
    """
    # Calculate the rolling mean (Middle Band)
    data['Middle_Band'] = data['Close'].rolling(window=window).mean()
    
    # Calculate the rolling standard deviation
    data['Rolling_Std'] = data['Close'].rolling(window=window).std()
    
    # Calculate the Upper Band and Lower Band
    data['Upper_Band'] = data['Middle_Band'] + (num_std_dev * data['Rolling_Std'])
    data['Lower_Band'] = data['Middle_Band'] - (num_std_dev * data['Rolling_Std'])
    
    return data

# Set parameters
window = 20
num_std_dev = 2

# Calculate Bollinger Bands
data = calculate_bollinger_bands(data, window=window, num_std_dev=num_std_dev)

# Create subplots: one for Close Prices and one for Bollinger Bands
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.plot(data.index, data['Middle_Band'], label='Middle Band (SMA)', color='orange')
ax1.plot(data.index, data['Upper_Band'], label='Upper Band', color='green')
ax1.plot(data.index, data['Lower_Band'], label='Lower Band', color='red')
ax1.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='lightgrey', alpha=0.5)
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Bollinger Bands')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
