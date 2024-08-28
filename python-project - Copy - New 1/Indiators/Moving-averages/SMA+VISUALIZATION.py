import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_sma(data, window=14):
    """
    Calculate the Simple Moving Average (SMA) for a given data series.

    Parameters:
    data (pd.Series): A pandas Series of price data.
    window (int): The look-back period for SMA calculation.

    Returns:
    pd.Series: The SMA values.
    """
    sma = data.rolling(window=window).mean()
    return sma

# Example usage
if __name__ == "__main__":
    # Sample data: Replace with your own data
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Close': np.random.rand(100) * 100  # Random closing prices
    }

    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)

    # Calculate 14-period SMA
    df['SMA_14'] = calculate_sma(df['Close'], window=14)

    # Print the resulting DataFrame with SMA
    print(df)

    # Plotting the Close price and SMA
    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['Close'], label='Close Price', color='blue')
    plt.plot(df.index, df['SMA_14'], label='14-period SMA', color='green')

    plt.title('Close Price and 14-Period SMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    plt.show()
