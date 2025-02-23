import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Configure Streamlit page
st.set_page_config(page_title="Bear Bull AI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for animations and styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* Apply Poppins font to all elements */
    * {
        font-family: 'Poppins', sans-serif;
    }

    /* Fade-in animation for components */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton > button, .stTextInput > div > div > input, .stDataFrame, .stPlotlyChart, .stMetric, .stInfo {
        animation: fadeIn 0.5s ease-in-out;
    }

    /* Gradient background for the header */
    .stMarkdown h1 {
        text-align: center;
        background: linear-gradient(90deg, #FF416C, #FF4B2B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        margin-bottom: 20px;
        font-weight: 600;
    }

    /* Hover effects for buttons */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Styling for text input */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 10px;
        font-size: 16px;
        border: 2px solid #4CAF50;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF416C;
        box-shadow: 0 0 10px rgba(255, 65, 108, 0.5);
    }

    /* Styling for dataframes */
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Styling for metrics */
    .stMetric {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        border-radius: 10px;
        padding: 15px;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Styling for news cards */
    .stInfo {
        background: linear-gradient(135deg, #ff9a9e, #fad0c4);
        border-radius: 10px;
        padding: 15px;
        color: black;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Styling for radio buttons */
    .stRadio > div {
        display: flex;
        gap: 10px;
        background: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stRadio > div > label {
        background: white;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stRadio > div > label:hover {
        background: #4CAF50;
        color: white;
        transform: scale(1.05);
    }

    /* Styling for the chart selection and timeframe selection */
    .chart-selection {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .chart-selection > div {
        flex: 1;
        background: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .chart-selection h3 {
        margin-bottom: 10px;
        color: #4CAF50;
        font-weight: 600;
    }

    /* Styling for top gainers and losers */
    .gainers-losers {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .gainers-losers > div {
        flex: 1;
        background: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .gainers-losers h3 {
        margin-bottom: 10px;
        color: #4CAF50;
        font-weight: 600;
    }

    /* Styling for the bottom navigation bar */
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #333;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .nav-button {
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background: #45a049;
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to fetch real-time stock data
@st.cache_data(ttl=60)  # Cache for 60 seconds to reduce API calls
def get_realtime_stock_data(stock_symbol, interval):
    try:
        ticker = yf.Ticker(stock_symbol)
        data = ticker.history(period="1d", interval=interval)
        if data.empty:
            st.warning(f"⚠ No data found for {stock_symbol}.")
            return None
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"❌ Error fetching real-time stock data: {e}")
        return None

# Function to fetch top gainers and losers
def get_market_movers():
    gainers = {"RELIANCE.NS": [2800, "+2.5%"], "TATASTEEL.NS": [125, "+1.8%"], "AXISBANK.NS": [950, "+1.2%"]}
    losers = {"ITC.NS": [410, "-2.1%"], "HCLTECH.NS": [1230, "-1.5%"], "WIPRO.NS": [590, "-1.1%"]}
    return gainers, losers

# Function to fetch market news
def get_market_news():
    news = [
        {"title": "Stock Market Hits New Highs", "source": "Economic Times"},
        {"title": "Tech Stocks Rally Amid AI Boom", "source": "Bloomberg"},
        {"title": "Investors Shift Focus to Renewable Energy", "source": "CNBC"}
    ]
    return news

# Function to plot candlestick chart
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
        xaxis_rangeslider_visible=False, template="plotly_dark",
        transition_duration=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Function to plot trending chart
def plot_trending_chart(df, stock_symbol):
    if df is None or df.empty:
        st.warning(f"⚠ No data available for {stock_symbol}.")
        return
    
    fig = px.line(df, x="Datetime", y="Close", title=f"📊 {stock_symbol} - Trending Chart", markers=True)
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# UI: Header & Stock Search
st.markdown("""
    <h1>🐻 Bear Bull <span style='color: #FF416C;'>AI</span></h1>
""", unsafe_allow_html=True)

stock_symbol = st.text_input("Enter stock symbol:", "RELIANCE.NS")

# Fetch & Display Real-Time Stock Data
if stock_symbol:
    st.write("### ⏳ Real-Time Stock Data")
    df = get_realtime_stock_data(stock_symbol, "1m")  # Default to 1m interval
    if df is not None:
        st.dataframe(df.tail(10), use_container_width=True)
        
        # Chart Selection and Timeframe Selection
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Chart Type")
            tab_option = st.radio("", ("Candlestick Chart", "Trending Chart"), key="chart_type", horizontal=True)
        with col2:
            st.markdown("#### ⏰ Timeframe")
            timeframe = st.radio("", ["1m", "5m", "15m", "30m", "1h", "1d"], key="timeframe", horizontal=True)
        
        df = get_realtime_stock_data(stock_symbol, timeframe)
        if df is not None:
            if tab_option == "Candlestick Chart":
                plot_candlestick_chart(df, stock_symbol, True, True)
            else:
                plot_trending_chart(df, stock_symbol)

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
