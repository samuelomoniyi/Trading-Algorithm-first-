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

# Define the Stochastic Oscillator function
def stochastic_oscillator(data, window=14, smooth_window=3):
    """
    Calculate the Stochastic Oscillator (%K and %D lines).
    """
    # Calculate the rolling maximum and minimum
    high_max = data['Close'].rolling(window=window, min_periods=1).max()
    low_min = data['Close'].rolling(window=window, min_periods=1).min()
    
    # Calculate %K
    data['%K'] = ((data['Close'] - low_min) / (high_max - low_min)) * 100
    
    # Calculate %D as the moving average of %K
    data['%D'] = data['%K'].rolling(window=smooth_window).mean()
    
    return data

# Set parameters
window_size = 14
smooth_window = 3

# Calculate the Stochastic Oscillator
data = stochastic_oscillator(data, window=window_size, smooth_window=smooth_window)

# Create subplots: one for Close Prices and one for Stochastic Oscillator
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plot Close prices on the top subplot
ax1.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.5)
ax1.set_ylabel('Close Price')
ax1.legend(loc='upper left')
ax1.grid(True)

# Plot Stochastic Oscillator on the bottom subplot
ax2.plot(data.index, data['%K'], label='%K', color='green')  # Changed color for %K
ax2.plot(data.index, data['%D'], label='%D', color='red')
ax2.axhline(80, color='gray', linestyle='--', label='Overbought')
ax2.axhline(20, color='gray', linestyle='--', label='Oversold')
ax2.set_xlabel('Date')
ax2.set_ylabel('Stochastic Oscillator')
ax2.legend(loc='upper left')
ax2.grid(True)

# Add a title and adjust layout
fig.suptitle('Close Prices and Stochastic Oscillator')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
