import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic data with 'Close' prices and 'Volume'
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', periods=100)
close_prices = np.random.rand(len(dates)) * 100
volume = np.random.rand(len(dates)) * 1000  # Random volume data

# Create a DataFrame
data = pd.DataFrame({'Date': dates, 'Close': close_prices, 'Volume': volume})
data.set_index('Date', inplace=True)

# Define the Volume Oscillator function
def volume_oscillator(data, short_window=10, long_window=30):
    """
    Calculate the Volume Oscillator.
    """
    # Calculate short and long-term volume moving averages
    data['Vol_MA_Short'] = data['Volume'].rolling(window=short_window).mean()
    data['Vol_MA_Long'] = data['Volume'].rolling(window=long_window).mean()
    
    # Calculate the Volume Oscillator
    data['Vol_Oscillator'] = data['Vol_MA_Short'] - data['Vol_MA_Long']
    
    return data

# Set parameters
short_window = 10
long_window = 30

# Calculate the Volume Oscillator
data = volume_oscillator(data, short_window=short_window, long_window=long_window)

# Create subplots: one for Volume and one for Volume Oscillator
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Volume on the top subplot
ax1.bar(data.index, data['Volume'], color='blue', alpha=0.6)
ax1.set_ylabel('Volume')
ax1.set_title('Volume and Volume Oscillator')
ax1.grid(True)

# Plot Volume Oscillator on the bottom subplot
colors = np.where(data['Vol_Oscillator'] >= 0, 'green', 'red')
ax2.bar(data.index, data['Vol_Oscillator'], color=colors, alpha=0.6)
ax2.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax2.set_xlabel('Date')
ax2.set_ylabel('Volume Oscillator')
ax2.legend(loc='upper left')
ax2.grid(True)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
