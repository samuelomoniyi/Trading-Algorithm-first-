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

# Define the Awesome Oscillator function
def awesome_oscillator(data, short_window=5, long_window=34):
    """
    Calculate the Awesome Oscillator.
    """
    # Calculate the median price
    data['Median'] = (data['Close'].rolling(window=1).mean())  # Median price equivalent for single-period
    
    # Calculate short and long moving averages of the median price
    data['SMA_Short'] = data['Median'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Median'].rolling(window=long_window).mean()
    
    # Calculate the Awesome Oscillator
    data['AO'] = data['SMA_Short'] - data['SMA_Long']
    
    return data

# Set parameters
short_window = 5
long_window = 34

# Calculate the Awesome Oscillator
data = awesome_oscillator(data, short_window=short_window, long_window=long_window)

# Create subplots: one for Close Prices and one for Awesome Oscillator
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Close prices on the top subplot
ax1.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.5)
ax1.set_ylabel('Close Price')
ax1.legend(loc='upper left')
ax1.grid(True)

# Plot Awesome Oscillator on the bottom subplot
ax2.bar(data.index, data['AO'], label='AO', color='green', alpha=0.6)
ax2.axhline(0, color='gray', linestyle='--', label='Zero Line')
ax2.set_xlabel('Date')
ax2.set_ylabel('Awesome Oscillator')
ax2.legend(loc='upper left')
ax2.grid(True)

# Add a title and adjust layout
fig.suptitle('Close Prices and Awesome Oscillator')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
