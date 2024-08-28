# import yfinance as yf
# import pandas as pd
# import matplotlib.pyplot as plt

# # Define parameters
# stock_symbol = 'AAPL'  # Example: Apple Inc.
# start_date = '2024-01-01'
# end_date = '2024-01-02'  # Short time frame for intraday data
# interval = '15m'  # 10-minute intervals
# rsi_period = 14  # RSI period
# rsi_buy_threshold = 30
# rsi_sell_threshold = 70
# ema_period = 50  # EMA period
# sma_period = 200  # SMA period

# # Fetch historical stock data with 10-minute intervals
# data = yf.download(stock_symbol, start=start_date, end=end_date, interval=interval)

# # Calculate RSI
# def calculate_rsi(df, period=14):
#     delta = df['Close'].diff()
#     gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
#     rs = gain / loss
#     rsi = 100 - (100 / (1 + rs))
#     return rsi

# data['RSI'] = calculate_rsi(data, period=rsi_period)

# # Generate RSI Buy and Sell signals
# data['RSI_Buy_Signal'] = (data['RSI'] < rsi_buy_threshold) & (data['RSI'].shift(1) >= rsi_buy_threshold)
# data['RSI_Sell_Signal'] = (data['RSI'] > rsi_sell_threshold) & (data['RSI'].shift(1) <= rsi_sell_threshold)

# # Calculate EMA and SMA
# data['EMA'] = data['Close'].ewm(span=ema_period, adjust=False).mean()
# data['SMA'] = data['Close'].rolling(window=sma_period).mean()

# # Generate EMA/SMA Buy and Sell signals
# data['EMA_Buy_Signal'] = (data['Close'] > data['EMA']) & (data['Close'].shift(1) <= data['EMA'].shift(1))
# data['EMA_Sell_Signal'] = (data['Close'] < data['EMA']) & (data['Close'].shift(1) >= data['EMA'].shift(1))

# data['SMA_Buy_Signal'] = (data['Close'] > data['SMA']) & (data['Close'].shift(1) <= data['SMA'].shift(1))
# data['SMA_Sell_Signal'] = (data['Close'] < data['SMA']) & (data['Close'].shift(1) >= data['SMA'].shift(1))

# # Combine RSI and EMA/SMA Signals
# data['Buy_Signal'] = data['RSI_Buy_Signal'] & data['EMA_Buy_Signal'] & data['SMA_Buy_Signal']
# data['Sell_Signal'] = data['RSI_Sell_Signal'] & data['EMA_Sell_Signal'] & data['SMA_Sell_Signal']

# # Calculate prediction accuracy
# correct_predictions = 0
# total_signals = 0

# # Evaluate Buy Signals
# for i in range(1, len(data) - 1):
#     if data['Buy_Signal'].iloc[i]:
#         total_signals += 1
#         if data['Close'].iloc[i + 1] > data['Close'].iloc[i]:
#             correct_predictions += 1

# # Evaluate Sell Signals
# for i in range(1, len(data) - 1):
#     if data['Sell_Signal'].iloc[i]:
#         total_signals += 1
#         if data['Close'].iloc[i + 1] < data['Close'].iloc[i]:
#             correct_predictions += 1

# # Calculate prediction accuracy
# if total_signals > 0:
#     prediction_accuracy = correct_predictions / total_signals
# else:
#     prediction_accuracy = 0

# # Plotting
# plt.figure(figsize=(14, 12))

# # Plot closing price with buy and sell signals
# plt.subplot(4, 1, 1)
# plt.plot(data['Close'], label='Close Price', color='blue')
# plt.plot(data['EMA'], label='EMA', color='orange', linestyle='--')
# plt.plot(data['SMA'], label='SMA', color='purple', linestyle='--')
# plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
# plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
# plt.title(f'{stock_symbol} Price with Combined RSI, EMA, and SMA Signals')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend()

# # Plot RSI
# plt.subplot(4, 1, 2)
# plt.plot(data['RSI'], label='RSI', color='orange')
# plt.axhline(y=rsi_buy_threshold, color='green', linestyle='--', label='Buy Threshold')
# plt.axhline(y=rsi_sell_threshold, color='red', linestyle='--', label='Sell Threshold')
# plt.title('RSI')
# plt.xlabel('Date')
# plt.ylabel('RSI')
# plt.legend()

# # Plot EMA and SMA
# plt.subplot(4, 1, 3)
# plt.plot(data['EMA'], label='EMA', color='orange')
# plt.plot(data['SMA'], label='SMA', color='purple')
# plt.title('EMA and SMA')
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.legend()

# # Plot Buy and Sell signals on EMA/SMA
# plt.subplot(4, 1, 4)
# plt.plot(data['EMA'], label='EMA', color='orange')
# plt.plot(data['SMA'], label='SMA', color='purple')
# plt.scatter(data.index[data['Buy_Signal']], data['EMA'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
# plt.scatter(data.index[data['Sell_Signal']], data['EMA'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
# plt.title('EMA/SMA with Buy and Sell Signals')
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.legend()

# plt.tight_layout()
# plt.show()

# # Print Prediction Score and Accuracy
# print(f'Total Signals: {total_signals}')
# print(f'Correct Predictions: {correct_predictions}')
# print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')



import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
interval = '15m'  # 15-minute intervals
rsi_period = 14  # RSI period
rsi_buy_threshold = 30
rsi_sell_threshold = 70
ema_period = 10  # EMA period
sma_period = 10  # SMA period

# Calculate dates
end_date = datetime.now().strftime('%Y-%m-%d')  # Today's date
start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # One day before today

# Fetch historical stock data with 15-minute intervals
data = yf.download(stock_symbol, start=start_date, end=end_date, interval=interval)

# Calculate RSI
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data, period=rsi_period)

# Generate RSI Buy and Sell signals
data['RSI_Buy_Signal'] = (data['RSI'] < rsi_buy_threshold) & (data['RSI'].shift(1) >= rsi_buy_threshold)
data['RSI_Sell_Signal'] = (data['RSI'] > rsi_sell_threshold) & (data['RSI'].shift(1) <= rsi_sell_threshold)

# Calculate EMA and SMA
data['EMA'] = data['Close'].ewm(span=ema_period, adjust=False).mean()
data['SMA'] = data['Close'].rolling(window=sma_period).mean()

# Generate EMA/SMA Buy and Sell signals
data['EMA_Buy_Signal'] = (data['Close'] > data['EMA']) & (data['Close'].shift(1) <= data['EMA'].shift(1))
data['EMA_Sell_Signal'] = (data['Close'] < data['EMA']) & (data['Close'].shift(1) >= data['EMA'].shift(1))

data['SMA_Buy_Signal'] = (data['Close'] > data['SMA']) & (data['Close'].shift(1) <= data['SMA'].shift(1))
data['SMA_Sell_Signal'] = (data['Close'] < data['SMA']) & (data['Close'].shift(1) >= data['SMA'].shift(1))

# Combine RSI and EMA/SMA Signals
data['Buy_Signal'] = data['RSI_Buy_Signal'] & data['EMA_Buy_Signal'] & data['SMA_Buy_Signal']
data['Sell_Signal'] = data['RSI_Sell_Signal'] & data['EMA_Sell_Signal'] & data['SMA_Sell_Signal']

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
plt.plot(data['EMA'], label='EMA', color='orange', linestyle='--')
plt.plot(data['SMA'], label='SMA', color='purple', linestyle='--')
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal', alpha=1)
plt.title(f'{stock_symbol} Price with Combined RSI, EMA, and SMA Signals')
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

# Plot EMA and SMA
plt.subplot(3, 1, 3)
plt.plot(data['EMA'], label='EMA', color='orange')
plt.plot(data['SMA'], label='SMA', color='purple')
plt.title('EMA and SMA')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()

plt.tight_layout()
plt.show()

# Print Prediction Score and Accuracy
print(f'Total Signals: {total_signals}')
print(f'Correct Predictions: {correct_predictions}')
print(f'Prediction Accuracy: {prediction_accuracy * 100:.2f}%')
