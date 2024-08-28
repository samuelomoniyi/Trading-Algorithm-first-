import pandas as pd
import numpy as np


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
    # Sample data: Replace with your own data
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Close': np.random.rand(100) * 100  # Random closing prices
    }

    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)

    df['RSI'] = calculate_rsi(df['Close'])

    # Print the resulting DataFrame with RSI
    print(df)

    # Optional: Plot the RSI
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['RSI'], label='RSI', color='orange')
    plt.axhline(70, color='red', linestyle='--', label='Overbought Threshold')
    plt.axhline(30, color='green', linestyle='--', label='Oversold Threshold')
    plt.title('RSI and Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
