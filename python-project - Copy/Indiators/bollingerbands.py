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

# Define the Bollinger Bands function
def bollinger_bands(data, window=20, num_sd=2):
    """
    Calculate Bollinger Bands.
    """
    # Calculate the rolling mean (Middle Band)
    data['Middle_Band'] = data['Close'].rolling(window=window).mean()
    
    # Calculate the rolling standard deviation
    data['Rolling_Std'] = data['Close'].rolling(window=window).std()
    
    # Calculate the Upper and Lower Bands
    data['Upper_Band'] = data['Middle_Band'] + (data['Rolling_Std'] * num_sd)
    data['Lower_Band'] = data['Middle_Band'] - (data['Rolling_Std'] * num_sd)
    
    return data

# Set parameters
window = 20
num_sd = 2

# Calculate the Bollinger Bands
data = bollinger_bands(data, window=window, num_sd=num_sd)

# Create a plot: one for Closing Prices and Bollinger Bands
fig, ax = plt.subplots(figsize=(14, 7))

# Plot Close prices
ax.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.7)

# Plot Bollinger Bands
ax.plot(data.index, data['Middle_Band'], label='Middle Band (SMA)', color='black', linestyle='--')
ax.plot(data.index, data['Upper_Band'], label='Upper Band', color='red', linestyle='--')
ax.plot(data.index, data['Lower_Band'], label='Lower Band', color='green', linestyle='--')

# Fill the area between the Upper and Lower Bands
ax.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.2)

# Add labels, legend, and grid
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Bollinger Bands and Closing Prices')
ax.legend(loc='upper left')
ax.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
