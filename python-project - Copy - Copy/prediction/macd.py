import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
fast_period = 12  # MACD fast period (e.g., 12 days)
slow_period = 26  # MACD slow period (e.g., 26 days)
signal_period = 9  # MACD signal line period (e.g., 9 days)

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate MACD and Signal line
data['EMA_12'] = data['Close'].ewm(span=fast_period, adjust=False).mean()
data['EMA_26'] = data['Close'].ewm(span=slow_period, adjust=False).mean()
data['MACD'] = data['EMA_12'] - data['EMA_26']
data['Signal_Line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()

# Generate Buy and Sell signals based on MACD crossovers
data['Buy_Signal'] = (data['MACD'] > data['Signal_Line']) & (data['MACD'].shift(1) <= data['Signal_Line'].shift(1))
data['Sell_Signal'] = (data['MACD'] < data['Signal_Line']) & (data['MACD'].shift(1) >= data['Signal_Line'].shift(1))

# Calculate prediction accuracy
correct_predictions = 0
total_signals = 0

# Evaluate Buy Signals
for i in range(1, len(data) - 1):
    if data['Buy_Signal'].iloc[i]:
        total_signals += 1
        if data['Close'].iloc[i + 1] > data['Close'].iloc[i]:
            correct_predictions += 1

# Evaluate Sell Signals
for i in range(1, len(data) - 1):
    if data['Sell_Signal'].iloc[i]:
        total_signals += 1
        if data['Close'].iloc[i + 1] < data['Close'].iloc[i]:
            correct_predictions += 1

# Calculate prediction accuracy
if total_signals > 0:
    prediction_accuracy = correct_predictions / total_signals
else:
    prediction_accuracy = 0

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

# Plot MACD and Signal Line
plt.subplot(3, 1, 2)
plt.plot(data['MACD'], label='MACD', color='orange')
plt.plot(data['Signal_Line'], label='Signal Line', color='blue')
plt.title('MACD and Signal Line')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()

# Plot Buy and Sell signals on MACD
plt.subplot(3, 1, 3)
plt.plot(data['MACD'], label='MACD', color='orange')
plt.plot(data['Signal_Line'], label='Signal Line', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['MACD'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['MACD'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title('MACD with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('MACD Value')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
