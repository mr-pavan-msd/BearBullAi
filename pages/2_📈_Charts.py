import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fetch the selected stock from session state
if "chart_stock" not in st.session_state:
    st.switch_page("1_🏠_Main.py")  # Redirect to the main page if no stock is selected

selected_stock = st.session_state.chart_stock

# Function to fetch stock data
def fetch_stock_data(symbol):
    stock_data = yf.Ticker(symbol)
    hist_data = stock_data.history(period="3mo")  # Fetch 3 months of historical data
    return hist_data

# Fetch historical data for the selected stock
hist_data = fetch_stock_data(selected_stock)

# Display the stock symbol
st.write(f"### Charts for {selected_stock}")

# Chart type selection
chart_type = st.radio("Select Chart Type", ["Line Chart", "Candlestick Chart"])

# Time frame selection
time_frame = st.radio("Select Time Frame", ["1D", "1W", "1M", "3M"])

# Filter data based on time frame
if time_frame == "1D":
    filtered_data = hist_data.tail(1)  # Last day
elif time_frame == "1W":
    filtered_data = hist_data.tail(7)  # Last week
elif time_frame == "1M":
    filtered_data = hist_data.tail(30)  # Last month
elif time_frame == "3M":
    filtered_data = hist_data.tail(90)  # Last 3 months

# Plot the selected chart
if chart_type == "Line Chart":
    fig = px.line(
        filtered_data, 
        x=filtered_data.index, 
        y="Close", 
        title=f"{selected_stock} Stock Price ({time_frame})"
    )
elif chart_type == "Candlestick Chart":
    fig = go.Figure(data=[go.Candlestick(
        x=filtered_data.index,
        open=filtered_data["Open"],
        high=filtered_data["High"],
        low=filtered_data["Low"],
        close=filtered_data["Close"]
    )])
    fig.update_layout(title=f"{selected_stock} Candlestick Chart ({time_frame})")

st.plotly_chart(fig)

# Button to go back to the main page
if st.button("Back to Main Page"):
    st.switch_page("1_🏠_Main.py")