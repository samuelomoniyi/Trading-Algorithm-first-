import pandas as pd

# Example data: Replace with your own data
data = {'Close': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]}
df = pd.DataFrame(data)

# Calculate 3-period SMA
df['SMA_3'] = df['Close'].rolling(window=3).mean()

print(df)
