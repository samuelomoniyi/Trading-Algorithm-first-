import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
start_date = '2023-01-01'
end_date = '2024-01-01'
ao_fast_period = 5  # Fast period for Awesome Oscillator
ao_slow_period = 34  # Slow period for Awesome Oscillator

# Fetch historical stock data
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate Awesome Oscillator (AO)
data['AO'] = (data['Close'].rolling(window=ao_fast_period).mean() - data['Close'].rolling(window=ao_slow_period).mean())
data['AO_SMA_34'] = data['AO'].rolling(window=34).mean()

# Generate Buy and Sell signals
data['Buy_Signal'] = (data['AO'] > data['AO_SMA_34']) & (data['AO'].shift(1) <= data['AO_SMA_34'].shift(1))
data['Sell_Signal'] = (data['AO'] < data['AO_SMA_34']) & (data['AO'].shift(1) >= data['AO_SMA_34'].shift(1))

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

# Plot closing price with buy and sell signals
plt.subplot(3, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Awesome Oscillator Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot Awesome Oscillator and its SMA
plt.subplot(3, 1, 2)
plt.bar(data.index, data['AO'], color='gray', alpha=0.3, label='Awesome Oscillator')
plt.plot(data['AO_SMA_34'], label='AO 34-period SMA', color='orange')
plt.title('Awesome Oscillator and 34-period SMA')
plt.xlabel('Date')
plt.ylabel('AO Value')
plt.legend()

# Plot raw and filtered signals
plt.subplot(3, 1, 3)
plt.plot(data['AO'], label='Awesome Oscillator', color='blue')
plt.plot(data['AO_SMA_34'], label='AO 34-period SMA', color='orange')
plt.scatter(data.index[data['Buy_Signal']], data['AO'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['AO'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title('AO with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('AO Value')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
