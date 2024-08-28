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

# Define the WMA function
def weighted_moving_average(prices, window):
    weights = np.arange(1, window + 1)
    wma = np.convolve(prices, weights[::-1] / weights.sum(), mode='valid')
    return wma

# Set the window size
window_size = 10

# Calculate WMA
data['WMA'] = pd.Series(weighted_moving_average(data['Price'], window_size), index=data.index[window_size-1:])

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Price'], label='Price', color='blue', alpha=0.5)
plt.plot(data.index, data['WMA'], label='WMA', color='red')
plt.title('Price and Weighted Moving Average')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
