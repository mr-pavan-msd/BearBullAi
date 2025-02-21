import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Configure Streamlit page
st.set_page_config(page_title="Bear Bull AI", layout="wide")

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

# Function to fetch top gainers and losers (Static data for now)
def get_market_movers():
    gainers = {"RELIANCE.NS": [2800, "+2.5%"], "TATASTEEL.NS": [125, "+1.8%"], "AXISBANK.NS": [950, "+1.2%"]}
    losers = {"ITC.NS": [410, "-2.1%"], "HCLTECH.NS": [1230, "-1.5%"], "WIPRO.NS": [590, "-1.1%"]}
    return gainers, losers

# Function to plot candlestick chart with SMA & EMA
def plot_candlestick_chart(df, stock_symbol, show_sma, show_ema):
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
    
    if show_sma:
        fig.add_trace(go.Scatter(x=df["Datetime"], y=df["SMA_20"], mode='lines', name='SMA 20', line=dict(color='blue')))
    if show_ema:
        fig.add_trace(go.Scatter(x=df["Datetime"], y=df["EMA_10"], mode='lines', name='EMA 10', line=dict(color='orange')))
    
    fig.update_layout(
        title=f"📈 {stock_symbol} - Live Candlestick Chart",
        xaxis_title="Time", yaxis_title="Price (INR)",
        xaxis_rangeslider_visible=False, template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Sidebar Settings
with st.sidebar:
    st.title("⚙ Settings")
    refresh_rate = st.slider("Auto-refresh interval (seconds):", 10, 300, 60)
    show_sma = st.checkbox("Show SMA 20", True)
    show_ema = st.checkbox("Show EMA 10", True)

# UI: Header & Stock Search
st.markdown("""
    <h1 style='text-align: center; color: white;'>🐻 Bear Bull <span style='color: red;'>AI</span></h1>
""", unsafe_allow_html=True)
stock_symbol = st.text_input("Enter stock symbol:", "RELIANCE.NS")

# Auto-refresh
st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")

# Fetch & Display Real-Time Stock Data
if stock_symbol:
    st.write("### ⏳ Real-Time Stock Data")
    df = get_realtime_stock_data(stock_symbol)
    if df is not None:
        st.dataframe(df.tail(10))
        plot_candlestick_chart(df, stock_symbol, show_sma, show_ema)

# Market Gainers & Losers
st.markdown("### 📈 Today’s Gainers & Losers")
gainers, losers = get_market_movers()
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🚀 Top Gainers")
    for stock, details in gainers.items():
        st.metric(label=stock, value=f"₹{details[0]}", delta=details[1])
with col2:
    st.markdown("#### 📉 Top Losers")
    for stock, details in losers.items():
        st.metric(label=stock, value=f"₹{details[0]}", delta=details[1])

# Multi-Stock Watchlist
st.markdown("### 📌 Multi-Stock Watchlist")
watchlist = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
cols = st.columns(len(watchlist))
for i, stock in enumerate(watchlist):
    with cols[i]:
        if st.button(stock, key=f"watchlist_{stock}"):
            stock_symbol = stock

# Fixed Bottom Navigation
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Home", key="nav_home"):
        st.switch_page("Home")
with col2:
    if st.button("📊 Dashboard", key="nav_dashboard"):
        st.switch_page("Dashboard")
with col3:
    if st.button("🔔 Stock Alerts", key="nav_alerts"):
        st.switch_page("Alerts")
with col4:
    if st.button("🤖 AI Chat", key="nav_chat"):
        st.switch_page("AI Chat")
with col5:
    if st.button("💼 Portfolio", key="nav_portfolio"):
        st.switch_page("Portfolio")
