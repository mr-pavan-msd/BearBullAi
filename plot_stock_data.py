import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Load stock data
ticker = input("Enter stock ticker (e.g., AAPL): ").upper()
df = pd.read_csv(f"{ticker}_stock.csv", parse_dates=True, index_col="Date")

# Basic Line Chart - Stock Prices
plt.figure(figsize=(12, 5))
sns.lineplot(x=df.index, y=df["Close"], label="Close Price", color="blue")
plt.title(f"{ticker} Stock Price Over Time")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()
plt.grid()
plt.show()

# Candlestick Chart - Interactive
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
)])
fig.update_layout(title=f"{ticker} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
fig.show()

