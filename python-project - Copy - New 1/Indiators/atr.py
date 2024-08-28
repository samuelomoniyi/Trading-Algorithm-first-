import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic data with 'High', 'Low', and 'Close' prices
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', periods=100)
highs = np.random.rand(len(dates)) * 100 + 50
lows = highs - np.random.rand(len(dates)) * 10
closes = (highs + lows) / 2

# Create a DataFrame
data = pd.DataFrame({'Date': dates, 'High': highs, 'Low': lows, 'Close': closes})
data.set_index('Date', inplace=True)

# Define the ATR function
def atr(data, window=14):
    """
    Calculate the Average True Range (ATR).
    """
    # Calculate True Range (TR)
    data['TR1'] = data['High'] - data['Low']
    data['TR2'] = (data['High'] - data['Close'].shift(1)).abs()
    data['TR3'] = (data['Low'] - data['Close'].shift(1)).abs()
    data['True_Range'] = data[['TR1', 'TR2', 'TR3']].max(axis=1)
    
    # Calculate ATR as the rolling mean of True Range
    data['ATR'] = data['True_Range'].rolling(window=window).mean()
    
    return data

# Set parameters
window = 14

# Calculate the ATR
data = atr(data, window=window)

# Create subplots: one for ATR and one for Closing Prices
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot ATR
ax1.plot(data.index, data['ATR'], label='ATR', color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('ATR')
ax1.set_title('Average True Range (ATR) and Closing Prices')
ax1.grid(True)

# Add a second y-axis to the same plot for Close Prices
ax2 = ax1.twinx()
ax2.plot(data.index, data['Close'], label='Close Price', color='red', alpha=0.7)
ax2.set_ylabel('Close Price')

# Combine legends and adjust layout
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()

plt.show()
