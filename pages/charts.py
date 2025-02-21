import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(page_title="Stock Chart", layout="wide")

# Function to fetch real-time stock data
@st.cache_data(ttl=60)  # Cache for 60 seconds to reduce API calls
def get_realtime_stock_data(stock_symbol):
    try:
        ticker = yf.Ticker(stock_symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            st.warning(f"⚠ No data found for {stock_symbol}.")
            return None
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"❌ Error fetching real-time stock data: {e}")
        return None

# Function to plot candlestick chart with SMA & EMA
def plot_candlestick_chart(df, stock_symbol):
    if df is None or df.empty:
        st.warning(f"⚠ No data available for {stock_symbol}.")
        return
    
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["EMA_10"] = df["Close"].ewm(span=10, adjust=False).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df["Datetime"], open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        increasing=dict(line=dict(color="green")),
        decreasing=dict(line=dict(color="red")),
        name="Candlestick Chart"
    ))
    
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["SMA_20"], mode='lines', name='SMA 20', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["EMA_10"], mode='lines', name='EMA 10', line=dict(color='orange')))
    
    fig.update_layout(
        title=f"📈 {stock_symbol} - Live Candlestick Chart",
        xaxis_title="Time", yaxis_title="Price (INR)",
        xaxis_rangeslider_visible=False, template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True, key=f"candlestick_{stock_symbol}")

# Get stock from session state
if "selected_stock" in st.session_state:
    stock_symbol = st.session_state["selected_stock"]
else:
    st.warning("⚠ No stock selected. Returning to Home Page.")
    st.switch_page("app.py")

# UI Header
st.markdown(f"## 📊 {stock_symbol} - Stock Chart & Data")

# Fetch & Display Real-Time Stock Data
df = get_realtime_stock_data(stock_symbol)
if df is not None:
    st.write("### ⏳ Real-Time Stock Data")
    st.dataframe(df.tail(10))
    plot_candlestick_chart(df, stock_symbol)

# Back Button
if st.button("🔙 Back to Home"):
    st.switch_page("app.py")
