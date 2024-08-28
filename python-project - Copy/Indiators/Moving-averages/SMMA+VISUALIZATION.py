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

# Define the SMMA function
def smoothed_moving_average(prices, window):
    smma = np.zeros(len(prices))
    smma[window-1] = np.mean(prices[:window])
    for i in range(window, len(prices)):
        smma[i] = (smma[i-1] * (window - 1) + prices[i]) / window
    return smma

# Set the window size
window_size = 10

# Calculate SMMA
data['SMMA'] = smoothed_moving_average(data['Price'].values, window_size)

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Price'], label='Price', color='blue', alpha=0.5)
plt.plot(data.index, data['SMMA'], label='SMMA', color='green')
plt.title('Price and Smoothed Moving Average')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
