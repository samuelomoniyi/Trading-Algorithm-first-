import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
ema_period = 12  # Period for EMA calculation
sma_period = 26  # Period for SMA calculation

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate EMA and SMA
data['EMA'] = data['Close'].ewm(span=ema_period, adjust=False).mean()
data['SMA'] = data['Close'].rolling(window=sma_period).mean()

# Generate Buy and Sell signals
data['Buy_Signal'] = (data['EMA'] > data['SMA']) & (data['EMA'].shift(1) <= data['SMA'].shift(1))
data['Sell_Signal'] = (data['EMA'] < data['SMA']) & (data['EMA'].shift(1) >= data['SMA'].shift(1))

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

# Plot closing price with EMA and SMA crossovers
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['EMA'], label=f'EMA {ema_period}', color='orange')
plt.plot(data['SMA'], label=f'SMA {sma_period}', color='green')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with EMA and SMA Crossover Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot EMA and SMA
plt.subplot(3, 1, 2)
plt.plot(data['EMA'], label=f'EMA {ema_period}', color='orange')
plt.plot(data['SMA'], label=f'SMA {sma_period}', color='green')
plt.title('EMA and SMA')
plt.xlabel('Date')
plt.ylabel('Moving Average')
plt.legend()

# Plot Buy and Sell Signals
plt.subplot(3, 1, 3)
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
