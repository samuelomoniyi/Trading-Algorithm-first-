import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', periods=100)
prices = np.random.rand(len(dates)) * 100

# Create a DataFrame
data = pd.DataFrame({'Date': dates, 'Price': prices})
data.set_index('Date', inplace=True)

# Define the Stochastic Oscillator function
def stochastic_oscillator(data, window=14, smooth_window=3):
    """
    Calculate the Stochastic Oscillator (%K and %D lines).
    """
    # Calculate the rolling maximum and minimum
    high_max = data['Price'].rolling(window=window, min_periods=1).max()
    low_min = data['Price'].rolling(window=window, min_periods=1).min()
    
    # Calculate %K
    data['%K'] = ((data['Price'] - low_min) / (high_max - low_min)) * 100
    
    # Calculate %D as the moving average of %K
    data['%D'] = data['%K'].rolling(window=smooth_window).mean()
    
    return data

# Set parameters
window_size = 14
smooth_window = 3

# Calculate the Stochastic Oscillator
data = stochastic_oscillator(data, window=window_size, smooth_window=smooth_window)

# Plot the data
plt.figure(figsize=(14, 7))

# Plot %K and %D lines
plt.plot(data.index, data['%K'], label='%K', color='blue')
plt.plot(data.index, data['%D'], label='%D', color='red')

# Add horizontal lines for overbought and oversold levels
plt.axhline(80, color='gray', linestyle='--', label='Overbought')
plt.axhline(20, color='gray', linestyle='--', label='Oversold')

plt.title('Stochastic Oscillator')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
