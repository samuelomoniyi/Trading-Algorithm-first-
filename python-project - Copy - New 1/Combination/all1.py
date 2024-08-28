import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
interval = '1m'  # 5-minute intervals

# Indicator settings for short timeframes
rsi_period = 10
rsi_buy_threshold = 30
rsi_sell_threshold = 70
bollinger_window = 10
bollinger_std_dev = 2
stochastic_k_period = 10
stochastic_d_period = 3

# Calculate dates
end_date = datetime.now().strftime('%Y-%m-%d')  # Today's date
start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # One day before today for more data

# Fetch historical stock data with 5-minute intervals
data = yf.download(stock_symbol, start=start_date, end=end_date, interval=interval)

# Calculate RSI
def calculate_rsi(df, period=10):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data, period=rsi_period)

# Calculate Bollinger Bands
data['SMA_BB'] = data['Close'].rolling(window=bollinger_window).mean()
data['Bollinger_Upper'] = data['SMA_BB'] + (data['Close'].rolling(window=bollinger_window).std() * bollinger_std_dev)
data['Bollinger_Lower'] = data['SMA_BB'] - (data['Close'].rolling(window=bollinger_window).std() * bollinger_std_dev)

# Generate Buy and Sell signals based on Bollinger Bands
data['BB_Buy_Signal'] = data['Close'] < data['Bollinger_Lower']
data['BB_Sell_Signal'] = data['Close'] > data['Bollinger_Upper']

# Calculate Stochastic Oscillator
def calculate_stochastic(df, k_period=10, d_period=3):
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=d_period).mean()
    return df['%K'], df['%D']

data['%K'], data['%D'] = calculate_stochastic(data, k_period=stochastic_k_period, d_period=stochastic_d_period)

# Generate Buy and Sell signals based on Stochastic Oscillator
data['Stochastic_Buy_Signal'] = (data['%K'] > data['%D']) & (data['%K'].shift(1) <= data['%D'].shift(1))
data['Stochastic_Sell_Signal'] = (data['%K'] < data['%D']) & (data['%K'].shift(1) >= data['%D'].shift(1))

# Generate Buy and Sell signals based on RSI
data['RSI_Buy_Signal'] = (data['RSI'] < rsi_buy_threshold)
data['RSI_Sell_Signal'] = (data['RSI'] > rsi_sell_threshold)

# Combine all signals
data['Final_Buy_Signal'] = data['BB_Buy_Signal'] & data['Stochastic_Buy_Signal'] & data['RSI_Buy_Signal']
data['Final_Sell_Signal'] = data['BB_Sell_Signal'] & data['Stochastic_Sell_Signal'] & data['RSI_Sell_Signal']

# Calculate prediction accuracy
correct_predictions = 0
total_signals = 0

# Evaluate Buy Signals
for i in range(1, len(data) - 1):
    if data['Final_Buy_Signal'].iloc[i]:
        total_signals += 1
        if data['Close'].iloc[i + 1] > data['Close'].iloc[i]:
            correct_predictions += 1

# Evaluate Sell Signals
for i in range(1, len(data) - 1):
    if data['Final_Sell_Signal'].iloc[i]:
        total_signals += 1
        if data['Close'].iloc[i + 1] < data['Close'].iloc[i]:
            correct_predictions += 1

# Calculate prediction accuracy
if total_signals > 0:
    prediction_accuracy = correct_predictions / total_signals
else:
    prediction_accuracy = 0

# Plotting
plt.figure(figsize=(14, 12))

# Plot closing price with buy and sell signals
plt.subplot(4, 1, 1)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['Bollinger_Upper'], label='Bollinger Upper', color='red', linestyle='--')
plt.plot(data['Bollinger_Lower'], label='Bollinger Lower', color='green', linestyle='--')
plt.scatter(data.index[data['Final_Buy_Signal']], data['Close'][data['Final_Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Final_Sell_Signal']], data['Close'][data['Final_Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Combined Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot RSI
plt.subplot(4, 1, 2)
plt.plot(data['RSI'], label='RSI', color='orange')
plt.axhline(y=rsi_buy_threshold, color='green', linestyle='--', label='Buy Threshold')
plt.axhline(y=rsi_sell_threshold, color='red', linestyle='--', label='Sell Threshold')
plt.title('RSI')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()

# Plot Bollinger Bands
plt.subplot(4, 1, 3)
plt.plot(data['Bollinger_Upper'], label='Bollinger Upper', color='red')
plt.plot(data['Bollinger_Lower'], label='Bollinger Lower', color='green')
plt.fill_between(data.index, data['Bollinger_Lower'], data['Bollinger_Upper'], color='gray', alpha=0.2)
plt.title('Bollinger Bands')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Plot Stochastic Oscillator
plt.subplot(4, 1, 4)
plt.plot(data['%K'], label='%K', color='blue')
plt.plot(data['%D'], label='%D', color='red')
plt.axhline(y=80, color='gray', linestyle='--', label='Overbought')
plt.axhline(y=20, color='gray', linestyle='--', label='Oversold')
plt.title('Stochastic Oscillator')
plt.xlabel('Date')
plt.ylabel('%K / %D')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
