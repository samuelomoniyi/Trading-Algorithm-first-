import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Define parameters
stock_symbol = 'AAPL'  # Example: Apple Inc.
interval = '1m'  # 1-minute intervals

# Indicator settings for short timeframes
rsi_period = 10
rsi_buy_threshold = 30
rsi_sell_threshold = 70
bollinger_window = 10
bollinger_std_dev = 2
stochastic_k_period = 10
stochastic_d_period = 3

def calculate_rsi(df, period=10):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_stochastic(df, k_period=10, d_period=3):
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=d_period).mean()
    return df['%K'], df['%D']

while True:
    # Fetch historical stock data with 1-minute intervals
    end_date = datetime.now().strftime('%Y-%m-%d')  # Today's date
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # One day before today for more data
    
    data = yf.download(stock_symbol, start=start_date, end=end_date, interval=interval)
    
    # Ensure all columns are numeric
    data = data.apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with NaN values (if any)
    data.dropna(inplace=True)
    
    # Calculate RSI
    data['RSI'] = calculate_rsi(data, period=rsi_period)
    
    # Calculate Bollinger Bands
    data['SMA_BB'] = data['Close'].rolling(window=bollinger_window).mean()
    data['Bollinger_Upper'] = data['SMA_BB'] + (data['Close'].rolling(window=bollinger_window).std() * bollinger_std_dev)
    data['Bollinger_Lower'] = data['SMA_BB'] - (data['Close'].rolling(window=bollinger_window).std() * bollinger_std_dev)
    
    # Generate Buy and Sell signals based on Bollinger Bands
    data['BB_Buy_Signal'] = data['Close'] < data['Bollinger_Lower']
    data['BB_Sell_Signal'] = data['Close'] > data['Bollinger_Upper']
    
    # Calculate Stochastic Oscillator
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
    
    # Get the most recent signal
    last_signal = data.iloc[-1]

    # Print current price
    print(f"Current Price: {last_signal['Close']} at {last_signal.name}")
    
    if last_signal['Final_Buy_Signal']:
        print(f"Buy Signal Detected at {last_signal.name} with price {last_signal['Close']}")
    
    if last_signal['Final_Sell_Signal']:
        print(f"Sell Signal Detected at {last_signal.name} with price {last_signal['Close']}")
    
    # Wait for the next interval
    time.sleep(60)  # Adjust the sleep time to match the interval (e.g., 60 seconds for 1-minute interval)
