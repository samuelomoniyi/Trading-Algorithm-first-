import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch real-time data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Calculate Smoothed Moving Average (SMMA)
def calculate_smma(data, window=14):
    """
    Calculate the Smoothed Moving Average (SMMA).
    """
    # Calculate initial SMMA (SMA of the first 'window' periods)
    data['SMA_Initial'] = data['Close'].rolling(window=window).mean()
    
    # Initialize SMMA with the SMA value
    data['SMMA'] = data['SMA_Initial']
    
    # Calculate subsequent SMMA values
    for i in range(window, len(data)):
        data['SMMA'].iloc[i] = (data['SMMA'].iloc[i - 1] * (window - 1) + data['Close'].iloc[i]) / window

    # Drop the initial SMA column
    data.drop(columns=['SMA_Initial'], inplace=True)
    
    return data

# Set parameter
window = 14

# Calculate SMMA
data = calculate_smma(data, window=window)

# Create subplots: one for Close Prices and one for SMMA
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
ax1.plot(data.index, data['SMMA'], label=f'SMMA {window} days', color='orange')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Smoothed Moving Average (SMMA)')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
