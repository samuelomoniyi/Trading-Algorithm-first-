import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Fetch historical data
ticker = 'AAPL'  # Example ticker symbol for Apple Inc.
data = yf.download(ticker, start='2023-01-01', end='2024-08-28', interval='1d')

# Feature Engineering
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['Price_Change'] = data['Close'].diff()
data['Target'] = np.where(data['Price_Change'].shift(-1) > 0, 1, 0)  # 1 if price goes up, 0 if down

# Drop rows with NaN values
data = data.dropna()

# Define features and labels
X = data[['SMA_20', 'SMA_50', 'Price_Change']]
y = data['Target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Add predictions to the original dataset for visualization
data['Predicted'] = np.nan
data.loc[X_test.index, 'Predicted'] = y_pred

# Plot actual vs predicted movements
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Close Prices
ax1.plot(data.index, data['Close'], label='Close Price', color='blue')

# Plot Predicted Buy/Sell Points
buy_signals = data[data['Predicted'] == 1]
sell_signals = data[data['Predicted'] == 0]

ax1.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
ax1.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', alpha=1)

ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{ticker} - Actual vs Predicted Movements')
ax1.legend(loc='upper left')
ax1.grid(True)

# Adjust layout
plt.tight_layout()

plt.show()
