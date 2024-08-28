import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Stochastic Oscillator
def stochastic_oscillator(data, period_k=14, period_d=3):
    """
    Calculate the Stochastic Oscillator %K and %D.
    """
    # Calculate the lowest low and highest high over the period
    data['Lowest_Low'] = data['Low'].rolling(window=period_k).min()
    data['Highest_High'] = data['High'].rolling(window=period_k).max()
    
    # Calculate %K
    data['%K'] = ((data['Close'] - data['Lowest_Low']) / (data['Highest_High'] - data['Lowest_Low'])) * 100
    
    # Calculate %D as the 3-day SMA of %K
    data['%D'] = data['%K'].rolling(window=period_d).mean()
    
    return data

# Set parameters
period_k = 14
period_d = 3

# Calculate the Stochastic Oscillator
data = stochastic_oscillator(data, period_k=period_k, period_d=period_d)

# Create subplots: one for Close Prices and one for Stochastic Oscillator
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.set_ylabel('Close Price')
ax1.set_title(f'{ticker} - Closing Prices and Stochastic Oscillator')
ax1.grid(True)

# Plot Stochastic Oscillator
ax2.plot(data.index, data['%K'], label='%K', color='blue')
ax2.plot(data.index, data['%D'], label='%D', color='red')
ax2.axhline(80, color='red', linestyle='--', label='Overbought (80)')
ax2.axhline(20, color='green', linestyle='--', label='Oversold (20)')
ax2.set_xlabel('Date')
ax2.set_ylabel('Stochastic Oscillator')
ax2.legend(loc='upper left')
ax2.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
