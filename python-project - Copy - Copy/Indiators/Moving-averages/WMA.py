import pandas as pd
import numpy as np

# Example data: Replace with your own data
data = {'Close': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]}
df = pd.DataFrame(data)

# Custom function to calculate Weighted Moving Average
def wma(series, window):
    weights = np.arange(1, window + 1)
    return series.rolling(window).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

# Calculate 3-period WMA
df['WMA_3'] = wma(df['Close'], 3)

print(df)
