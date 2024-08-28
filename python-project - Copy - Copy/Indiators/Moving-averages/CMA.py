import pandas as pd

# Example data: Replace with your own data
data = {'Close': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]}
df = pd.DataFrame(data)

# Calculate CMA
df['CMA'] = df['Close'].expanding().mean()

print(df)
