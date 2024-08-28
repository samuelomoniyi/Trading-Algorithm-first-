import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic data with 'Close' prices
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', periods=100)
close_prices = np.random.rand(len(dates)) * 100

# Create a DataFrame
data = pd.DataFrame({'Date': dates, 'Close': close_prices})
data.set_index('Date', inplace=True)

# Define the MACD function
def macd(data, short_ema=12, long_ema=26, signal_ema=9):
    """
    Calculate the MACD line, Signal line, and MACD Histogram.
    """
    # Calculate the short and long EMAs
    data['EMA_Short'] = data['Close'].ewm(span=short_ema, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=long_ema, adjust=False).mean()
    
    # Calculate the MACD Line
    data['MACD_Line'] = data['EMA_Short'] - data['EMA_Long']
    
    # Calculate the Signal Line
    data['Signal_Line'] = data['MACD_Line'].ewm(span=signal_ema, adjust=False).mean()
    
    # Calculate the MACD Histogram
    data['MACD_Histogram'] = data['MACD_Line'] - data['Signal_Line']
    
    return data

# Set parameters
short_ema = 12
long_ema = 26
signal_ema = 9

# Calculate the MACD
data = macd(data, short_ema=short_ema, long_ema=long_ema, signal_ema=signal_ema)

# Create subplots: one for MACD and Histogram, and one for Close Prices
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 12), sharex=True)

# Plot MACD Line, Signal Line, and MACD Histogram on the top subplot
ax1.plot(data.index, data['MACD_Line'], label='MACD Line', color='blue', linewidth=1.5)
ax1.plot(data.index, data['Signal_Line'], label='Signal Line', color='red', linewidth=1.5)
hist_colors = np.where(data['MACD_Histogram'] >= data['MACD_Histogram'].shift(1), 'green', 'red')
ax1.bar(data.index, data['MACD_Histogram'], color=hist_colors, alpha=0.6)
ax1.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax1.set_ylabel('MACD')
ax1.legend(loc='upper left')
ax1.grid(True)

# Plot Close prices on the bottom subplot
ax2.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.7)
ax2.set_xlabel('Date')
ax2.set_ylabel('Close Price')
ax2.legend(loc='upper left')
ax2.grid(True)

# Add a title and adjust layout
fig.suptitle('MACD, MACD Histogram, and Close Prices')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
