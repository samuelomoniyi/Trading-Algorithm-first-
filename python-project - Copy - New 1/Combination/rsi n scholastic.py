import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
interval = '5m'  # 30-minute intervals

# Indicator settings for short timeframes
rsi_period = 10
rsi_buy_threshold = 30
rsi_sell_threshold = 70
stochastic_k_period = 10
stochastic_d_period = 3
future_period = 1  # Number of intervals to look ahead for prediction accuracy

# Calculate dates
end_date = datetime.now().strftime('%Y-%m-%d')  # Today's date
start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # 30 days before today

# Fetch historical stock data with 30-minute intervals
data = yf.download(stock_symbol, start=start_date, end=end_date, interval=interval)

# Ensure all columns are numeric
data = data.apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values (if any)
data.dropna(inplace=True)

# Calculate RSI
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data, period=rsi_period)

# Calculate Stochastic Oscillator
data['Low_Min'] = data['Low'].rolling(window=stochastic_k_period).min()
data['High_Max'] = data['High'].rolling(window=stochastic_k_period).max()
data['%K'] = 100 * (data['Close'] - data['Low_Min']) / (data['High_Max'] - data['Low_Min'])
data['%D'] = data['%K'].rolling(window=stochastic_d_period).mean()

# Generate Buy and Sell signals
data['Buy_Signal'] = (data['RSI'] < rsi_buy_threshold) & (data['%K'] > data['%D'])
data['Sell_Signal'] = (data['RSI'] > rsi_sell_threshold) & (data['%K'] < data['%D'])

# Initialize counters for accuracy calculation
correct_predictions = 0
total_signals = 0

# Evaluate Buy Signals
for i in range(len(data) - future_period):
    if data['Buy_Signal'].iloc[i]:
        total_signals += 1
        if data['Close'].iloc[i + future_period] > data['Close'].iloc[i]:
            correct_predictions += 1

# Evaluate Sell Signals
for i in range(len(data) - future_period):
    if data['Sell_Signal'].iloc[i]:
        total_signals += 1
        if data['Close'].iloc[i + future_period] < data['Close'].iloc[i]:
            correct_predictions += 1

# Calculate prediction accuracy
if total_signals > 0:
    prediction_accuracy = correct_predictions / total_signals
else:
    prediction_accuracy = 0

# Plotting
plt.figure(figsize=(14, 12))

# Plot closing price with Buy and Sell signals
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
plt.title('RSI')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()

# Plot Stochastic Oscillator
plt.subplot(3, 1, 3)
plt.plot(data['%K'], label='%K', color='blue')
plt.plot(data['%D'], label='%D', color='orange')
plt.title('Stochastic Oscillator')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()

plt.tight_layout()
plt.show()

# Print Signal Summary
print(f'Total Buy Signals: {data["Buy_Signal"].sum()}')
print(f'Total Sell Signals: {data["Sell_Signal"].sum()}')
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
