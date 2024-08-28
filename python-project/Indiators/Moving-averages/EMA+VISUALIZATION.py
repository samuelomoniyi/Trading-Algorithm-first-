import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_ema(data, span=14):
    """
    Calculate the Exponential Moving Average (EMA) for a given data series.

    Parameters:
    data (pd.Series): A pandas Series of price data.
    span (int): The span for the EMA calculation.

    Returns:
    pd.Series: The EMA values.
    """
    ema = data.ewm(span=span, adjust=False).mean()
    return ema

# Example usage
if __name__ == "__main__":
    # Sample data: Replace with your own data
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Close': np.random.rand(100) * 100  # Random closing prices
    }

    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)

    # Calculate 14-period EMA
    df['EMA_14'] = calculate_ema(df['Close'], span=14)

    # Print the resulting DataFrame with EMA
    print(df)

    # Plotting the Close price and EMA
    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['Close'], label='Close Price', color='blue')
    plt.plot(df.index, df['EMA_14'], label='14-period EMA', color='orange')

    plt.title('Close Price and 14-Period EMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    plt.show()
