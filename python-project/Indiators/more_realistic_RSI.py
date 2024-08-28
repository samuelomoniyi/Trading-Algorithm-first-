import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given data series.

    Parameters:
    data (pd.Series): A pandas Series of price data.
    window (int): The look-back period for RSI calculation.

    Returns:
    pd.Series: The RSI values.
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Example usage
if __name__ == "__main__":
    np.random.seed(0)
    # Simulate more realistic closing prices with trends
    trend = np.cumsum(np.random.randn(100))  # Cumulative sum to create trends
    noise = np.random.normal(0, 5, 100)  # Adding some noise
    close_prices = 50 + trend + noise  # Creating a closing price series

    data = {
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Close': close_prices
    }

    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)

    # Calculate RSI
    df['RSI'] = calculate_rsi(df['Close'])

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle('Close Price and RSI')

    # Plot the Close Price
    ax1.plot(df.index, df['Close'], label='Close Price', color='blue')
    ax1.set_ylabel('Close Price')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Plot the RSI
    ax2.plot(df.index, df['RSI'], label='RSI', color='orange')
    ax2.axhline(70, color='red', linestyle='--', label='Overbought Threshold')
    ax2.axhline(30, color='green', linestyle='--', label='Oversold Threshold')
    ax2.set_ylabel('RSI')
    ax2.set_xlabel('Date')
    ax2.legend(loc='upper left')
    ax2.grid(True)

    # Display the plot
    plt.show()
