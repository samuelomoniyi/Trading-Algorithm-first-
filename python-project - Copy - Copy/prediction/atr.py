import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
atr_period = 14  # Period for ATR calculation
atr_multiplier = 1.5  # Multiplier to determine buy/sell thresholds

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate True Range (TR)
data['TR'] = pd.concat([
    data['High'] - data['Low'],
    (data['High'] - data['Close'].shift(1)).abs(),
    (data['Low'] - data['Close'].shift(1)).abs()
], axis=1).max(axis=1)

# Calculate ATR
data['ATR'] = data['TR'].rolling(window=atr_period).mean()

# Calculate Buy and Sell thresholds
data['Buy_Threshold'] = data['Close'].rolling(window=atr_period).max() - atr_multiplier * data['ATR']
data['Sell_Threshold'] = data['Close'].rolling(window=atr_period).min() + atr_multiplier * data['ATR']

# Generate Buy and Sell signals
data['Buy_Signal'] = data['Close'] < data['Buy_Threshold']
data['Sell_Signal'] = data['Close'] > data['Sell_Threshold']

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
plt.figure(figsize=(14, 10))

# Plot closing price with ATR thresholds
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['Buy_Threshold'], label='Buy Threshold', color='green', linestyle='--')
plt.plot(data['Sell_Threshold'], label='Sell Threshold', color='red', linestyle='--')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with ATR-Based Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot ATR
plt.subplot(3, 1, 2)
plt.plot(data['ATR'], label='ATR', color='orange')
plt.title('Average True Range (ATR)')
plt.xlabel('Date')
plt.ylabel('ATR Value')
plt.legend()

# Plot raw and filtered signals
plt.subplot(3, 1, 3)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title('Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
