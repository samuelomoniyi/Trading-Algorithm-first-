import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
k_period = 14  # Stochastic Oscillator %K period
d_period = 3   # Stochastic Oscillator %D period (moving average of %K)

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate Stochastic Oscillator
data['L14'] = data['Low'].rolling(window=k_period).min()
data['H14'] = data['High'].rolling(window=k_period).max()
data['%K'] = 100 * ((data['Close'] - data['L14']) / (data['H14'] - data['L14']))
data['%D'] = data['%K'].rolling(window=d_period).mean()

# Generate Buy and Sell signals based solely on %K and %D crossovers
data['Buy_Signal'] = (data['%K'] > data['%D']) & (data['%K'].shift(1) <= data['%D'].shift(1))
data['Sell_Signal'] = (data['%K'] < data['%D']) & (data['%K'].shift(1) >= data['%D'].shift(1))

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

# Plot Stochastic Oscillator %K and %D
plt.subplot(3, 1, 2)
plt.plot(data['%K'], label='%K', color='orange')
plt.plot(data['%D'], label='%D', color='blue')
plt.title('Stochastic Oscillator')
plt.xlabel('Date')
plt.ylabel('%K and %D')
plt.legend()

# Plot Buy and Sell signals on Stochastic Oscillator
plt.subplot(3, 1, 3)
plt.plot(data['%K'], label='%K', color='orange')
plt.plot(data['%D'], label='%D', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['%K'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['%K'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title('Stochastic Oscillator with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('%K and %D')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
