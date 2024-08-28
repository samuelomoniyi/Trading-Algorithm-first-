import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
short_window = 14  # Short-term window for volume moving average
long_window = 28   # Long-term window for volume moving average

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate Volume Moving Averages
data['Short_MA_Volume'] = data['Volume'].rolling(window=short_window).mean()
data['Long_MA_Volume'] = data['Volume'].rolling(window=long_window).mean()

# Calculate Volume Oscillator
data['Volume_Oscillator'] = data['Short_MA_Volume'] - data['Long_MA_Volume']

# Generate Buy and Sell signals
data['Buy_Signal'] = (data['Volume_Oscillator'] > 0) & (data['Volume_Oscillator'].shift(1) <= 0)
data['Sell_Signal'] = (data['Volume_Oscillator'] < 0) & (data['Volume_Oscillator'].shift(1) >= 0)

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

# Plot closing price with volume oscillator signals
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Volume Oscillator Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot Volume Oscillator
plt.subplot(3, 1, 2)
plt.plot(data['Volume_Oscillator'], label='Volume Oscillator', color='purple')
plt.axhline(y=0, color='black', linestyle='--')
plt.title('Volume Oscillator')
plt.xlabel('Date')
plt.ylabel('Oscillator Value')
plt.legend()

# Plot volume moving averages
plt.subplot(3, 1, 3)
plt.plot(data['Volume'], label='Volume', color='blue', alpha=0.5)
plt.plot(data['Short_MA_Volume'], label='Short MA Volume', color='green', linestyle='--')
plt.plot(data['Long_MA_Volume'], label='Long MA Volume', color='red', linestyle='--')
plt.title('Volume and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
