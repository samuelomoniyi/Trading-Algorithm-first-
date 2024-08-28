import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
stochastic_k_window = 14  # %K period
stochastic_d_window = 3   # %D period
rsi_window = 14          # RSI period
rsi_overbought_threshold = 70
rsi_oversold_threshold = 30
overbought_threshold = 80
oversold_threshold = 20

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate RSI
delta = data['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=rsi_window).mean()
avg_loss = loss.rolling(window=rsi_window).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# Calculate %K and %D for Stochastic Oscillator
data['Lowest_Low'] = data['Low'].rolling(window=stochastic_k_window).min()
data['Highest_High'] = data['High'].rolling(window=stochastic_k_window).max()
data['%K'] = 100 * (data['Close'] - data['Lowest_Low']) / (data['Highest_High'] - data['Lowest_Low'])
data['%D'] = data['%K'].rolling(window=stochastic_d_window).mean()

# Generate Buy and Sell signals based on RSI and Stochastic Oscillator
data['RSI_Buy_Signal'] = (data['RSI'] < rsi_oversold_threshold)
data['RSI_Sell_Signal'] = (data['RSI'] > rsi_overbought_threshold)
data['Stochastic_Buy_Signal'] = (data['%K'] > data['%D']) & (data['%K'] < overbought_threshold)
data['Stochastic_Sell_Signal'] = (data['%K'] < data['%D']) & (data['%K'] > oversold_threshold)

# Combined Buy and Sell Signals
data['Buy_Signal'] = data['RSI_Buy_Signal'] & data['Stochastic_Buy_Signal']
data['Sell_Signal'] = data['RSI_Sell_Signal'] & data['Stochastic_Sell_Signal']

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
plt.figure(figsize=(14, 14))

# Plot closing price with buy and sell signals
plt.subplot(4, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Combined RSI and Stochastic Oscillator Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot RSI
plt.subplot(4, 1, 2)
plt.plot(data['RSI'], label='RSI', color='purple')
plt.axhline(y=rsi_overbought_threshold, color='red', linestyle='--', label='Overbought Threshold')
plt.axhline(y=rsi_oversold_threshold, color='green', linestyle='--', label='Oversold Threshold')
plt.title('RSI')
plt.xlabel('Date')
plt.ylabel('RSI Value')
plt.legend()

# Plot Stochastic Oscillator %K and %D
plt.subplot(4, 1, 3)
plt.plot(data['%K'], label='%K', color='blue')
plt.plot(data['%D'], label='%D', color='orange')
plt.axhline(y=overbought_threshold, color='red', linestyle='--', label='Overbought Threshold')
plt.axhline(y=oversold_threshold, color='green', linestyle='--', label='Oversold Threshold')
plt.title('Stochastic Oscillator %K and %D')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()

# Plot Buy and Sell Signals on %K
plt.subplot(4, 1, 4)
plt.scatter(data.index[data['Buy_Signal']], data['%K'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['%K'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title('Buy and Sell Signals on %K')
plt.xlabel('Date')
plt.ylabel('Stochastic %K Value')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
