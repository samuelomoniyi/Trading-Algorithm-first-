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

# Define the CMA function
def cumulative_moving_average(prices):
    cma = np.cumsum(prices) / np.arange(1, len(prices) + 1)
    return cma

# Calculate CMA
data['CMA'] = cumulative_moving_average(data['Price'].values)

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Price'], label='Price', color='blue', alpha=0.5)
plt.plot(data.index, data['CMA'], label='CMA', color='orange')
plt.title('Price and Cumulative Moving Average')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
