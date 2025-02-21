import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Configure Streamlit page
st.set_page_config(page_title="Bear Bull AI - Home", layout="wide")

# Function to fetch market index data
def get_market_indexes():
    indexes = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "BANK NIFTY": "^NSEBANK"}
    market_data = {}
    for name, symbol in indexes.items():
        data = yf.Ticker(symbol).history(period="1d")
        if not data.empty:
            market_data[name] = round(data["Close"].iloc[-1], 2)
    return market_data

# Function to fetch top stock news
def get_market_news():
    try:
        news_api = "https://newsapi.org/v2/top-headlines?category=business&country=in&apiKey=YOUR_NEWSAPI_KEY"
        response = requests.get(news_api).json()
        articles = response.get("articles", [])[:5]
        return [f"[{a['title']}]({a['url']})" for a in articles]
    except:
        return ["Unable to fetch news at the moment"]

# Function to recommend stocks (dummy data for now)
def get_recommended_stocks():
    return {"TCS.NS": "₹3850", "INFY.NS": "₹1550", "HDFCBANK.NS": "₹1520", "ICICIBANK.NS": "₹950"}

# Sidebar Settings
with st.sidebar:
    st.title("⚙ Settings")
    refresh_rate = st.slider("Auto-refresh interval (seconds):", 10, 300, 60)

# Auto-refresh
st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")

# UI: Header & Search
st.markdown("""
    <h1 style='text-align: center; color: white;'>🐻 Bear Bull <span style='color: red;'>AI</span></h1>
""", unsafe_allow_html=True)
col1, col2 = st.columns([1, 3])
with col1:
    st.button("👤 Profile")
with col2:
    search = st.text_input("Search stocks...", "Reliance")

# Market Indexes Section
st.markdown("### 📊 Market Indexes")
market_data = get_market_indexes()
cols = st.columns(len(market_data))
for i, (index, value) in enumerate(market_data.items()):
    with cols[i]:
        st.metric(label=index, value=f"₹{value}")

# Market News Section
st.markdown("### 📰 Today’s Market News")
news_articles = get_market_news()
for article in news_articles:
    st.markdown(f"- {article}")

# Recommended Stocks Section
st.markdown("### 📌 Recommended Stocks")
recommended = get_recommended_stocks()
cols = st.columns(len(recommended))
for i, (stock, price) in enumerate(recommended.items()):
    with cols[i]:
        if st.button(stock):
            search = stock  # Update stock selection
        st.metric(label=stock, value=price)

# 🔹 Quick Navigation (Using Streamlit's `st.page_link()`)
st.markdown("---")
st.write("### 🌎 Quick Navigation")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link("app.py", label="🏠 Home", icon="🏠")
with col2:
    st.page_link("pages/dashboard.py", label="📊 Dashboard", icon="📊")
with col3:
    st.page_link("pages/alerts.py", label="🔔 Alerts", icon="🔔")
with col4:
    st.page_link("pages/ai_chat.py", label="🤖 AI Chat", icon="🤖")
with col5:
    st.page_link("pages/portfolio.py", label="💼 Portfolio", icon="💼")

# 🔹 Sticky Bottom Navigation Bar
st.markdown("""
    <style>
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #333;
        padding: 10px;
        text-align: center;
        z-index: 100;
    }
    .fixed-bottom a {
        color: white;
        background-color: #FF5733;
        padding: 10px 20px;
        margin: 5px;
        text-decoration: none;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='fixed-bottom'>
        <a href='home' target='_self'>🏠 Home</a>
        <a href='dashboard' target='_self'>📊 Dashboard</a>
        <a href='alerts' target='_self'>🔔 Alerts</a>
        <a href='ai_chat' target='_self'>🤖 AI Chat</a>
        <a href='portfolio' target='_self'>💼 Portfolio</a>
    </div>
""", unsafe_allow_html=True)

