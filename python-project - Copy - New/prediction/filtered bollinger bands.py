import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
bollinger_window = 20  # Default period for Bollinger Bands
bollinger_std = 2  # Default number of standard deviations
trend_window = 50  # Additional trend filter window

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate Bollinger Bands
data['SMA'] = data['Close'].rolling(window=bollinger_window).mean()
data['Bollinger_Upper'] = data['SMA'] + (bollinger_std * data['Close'].rolling(window=bollinger_window).std())
data['Bollinger_Lower'] = data['SMA'] - (bollinger_std * data['Close'].rolling(window=bollinger_window).std())

# Calculate additional trend indicator (Simple Moving Average)
data['Trend_SMA'] = data['Close'].rolling(window=trend_window).mean()

# Generate Buy and Sell signals with additional filtering
data['Raw_Buy_Signal'] = data['Close'] < data['Bollinger_Lower']
data['Raw_Sell_Signal'] = data['Close'] > data['Bollinger_Upper']
data['Buy_Signal'] = data['Raw_Buy_Signal'] & (data['Close'] > data['Trend_SMA'])
data['Sell_Signal'] = data['Raw_Sell_Signal'] & (data['Close'] < data['Trend_SMA'])

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

# Plot closing price with Bollinger Bands and trend indicator
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['Bollinger_Upper'], label='Upper Bollinger Band', color='orange')
plt.plot(data['Bollinger_Lower'], label='Lower Bollinger Band', color='orange')
plt.plot(data['Trend_SMA'], label='Trend SMA', color='green', linestyle='--')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Refined Bollinger Bands Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot Bollinger Bands and Trend SMA
plt.subplot(3, 1, 2)
plt.plot(data['Bollinger_Upper'], label='Upper Bollinger Band', color='orange')
plt.plot(data['Bollinger_Lower'], label='Lower Bollinger Band', color='orange')
plt.plot(data['Trend_SMA'], label='Trend SMA', color='green', linestyle='--')
plt.title('Bollinger Bands and Trend SMA')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()

# Plot raw and filtered signals
plt.subplot(3, 1, 3)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.scatter(data.index[data['Raw_Buy_Signal']], data['Close'][data['Raw_Buy_Signal']], marker='^', color='gray', label='Raw Buy Signal', alpha=0.5)
plt.scatter(data.index[data['Raw_Sell_Signal']], data['Close'][data['Raw_Sell_Signal']], marker='v', color='gray', label='Raw Sell Signal', alpha=0.5)
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Filtered Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Filtered Sell Signal', alpha=1)
plt.title('Raw vs. Filtered Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
