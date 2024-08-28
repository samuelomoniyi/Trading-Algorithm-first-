import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
rsi_period = 14  # Period for RSI calculation
rsi_buy_threshold = 30
rsi_sell_threshold = 70

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate RSI
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data, period=rsi_period)

# Generate Buy and Sell signals
data['Buy_Signal'] = (data['RSI'] < rsi_buy_threshold) & (data['RSI'].shift(1) >= rsi_buy_threshold)
data['Sell_Signal'] = (data['RSI'] > rsi_sell_threshold) & (data['RSI'].shift(1) <= rsi_sell_threshold)

# Plotting
plt.figure(figsize=(14, 8))

# Plot closing price
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot RSI
plt.subplot(3, 1, 2)
plt.plot(data['RSI'], label='RSI', color='orange')
plt.axhline(y=rsi_buy_threshold, color='green', linestyle='--', label='Buy Threshold')
plt.axhline(y=rsi_sell_threshold, color='red', linestyle='--', label='Sell Threshold')
plt.title('Relative Strength Index (RSI)')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()

# Plot Buy and Sell signals on RSI
plt.subplot(3, 1, 3)
plt.plot(data['RSI'], label='RSI', color='orange')
plt.scatter(data.index[data['Buy_Signal']], data['RSI'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['RSI'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.axhline(y=rsi_buy_threshold, color='green', linestyle='--', label='Buy Threshold')
plt.axhline(y=rsi_sell_threshold, color='red', linestyle='--', label='Sell Threshold')
plt.title('RSI with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()

plt.tight_layout()
plt.show()

# Calculate Prediction Score
buy_signals = data['Buy_Signal'].sum()
sell_signals = data['Sell_Signal'].sum()

print(f'Total Buy Signals: {buy_signals}')
print(f'Total Sell Signals: {sell_signals}')
