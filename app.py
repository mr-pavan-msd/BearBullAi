import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import os
import hashlib
import bcrypt
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from collections import deque
from streamlit_cookies_manager import EncryptedCookieManager

# Set page configuration immediately after imports!
st.set_page_config(page_title="Bear Bull AI - Home", layout="wide")

# Load API Key
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Initialize cookie manager (replace "CHANGE_ME" with a strong secret in production)
cookies = EncryptedCookieManager(prefix="bearbull_", password="CHANGE_ME")
if not cookies.ready():
    st.stop()
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def verify_password(password, hashed_password):
    # Verify the password against the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)

# Example usage
hashed_password = hash_password("password123")
print(hashed_password)  # Output: b'$2b$12$...'

# Verify the password
is_valid = verify_password("password123", hashed_password)
print(is_valid)  # Output: True
# Initialize session state for login using cookies for persistence
if "logged_in" not in st.session_state:
    if cookies.get("logged_in", False):
        st.session_state.logged_in = True
        st.session_state.username = cookies.get("username", "")
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""

# Custom CSS for UI enhancements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    * { font-family: 'Poppins', sans-serif; }

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
        margin: 0 auto;
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

    /* Styling for the bottom navigation bar */
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
        background: linear-gradient(135deg, #FF416C, #FF4B2B);
        padding: 10px 20px;
        margin: 5px;
        text-decoration: none;
        font-weight: bold;
        border-radius: 25px;
        transition: all 0.3s ease;
    }
    .fixed-bottom a:hover {
        background: linear-gradient(135deg, #FF4B2B, #FF416C);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Styling for market indexes */
    .market-indexes {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .market-indexes > div {
        flex: 1;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        border-radius: 10px;
        padding: 15px;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Styling for recommended stocks */
    .recommended-stocks {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .recommended-stocks > div {
        flex: 1;
        background: linear-gradient(135deg, #ff9a9e, #fad0c4);
        border-radius: 10px;
        padding: 15px;
        color: black;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Custom CSS for square-shaped popup */
    .square-popup {
        width: 400px;
        height: 400px;
        border: 1px solid #ccc;
        padding: 10px;
        margin: auto;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    </style>
    """, unsafe_allow_html=True)

# Persist login state using cookies
if not st.session_state.logged_in:
    st.title("Login Required")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login", key="login_button")

    # Simple login validation (replace with real authentication logic)
    if login_button:
        if email == "user@example.com" and password == "password123":
            st.session_state.logged_in = True
            st.session_state.username = email
            # Persist login state in cookies
            cookies["logged_in"] = True
            cookies["username"] = email
            cookies.save()
            st.success("Login successful!")
            st.experimental_rerun()  # Refresh the page to load app content
        else:
            st.error("Invalid credentials. Please try again.")
    st.stop()  # Stop further execution until login is successful
else:
    st.title(f"Welcome to the App, {st.session_state.username}!")
    st.write("You have successfully logged in.")
    if st.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        cookies["logged_in"] = False
        cookies["username"] = ""
        cookies.save()
        st.experimental_rerun()
def hash_password(password: str) -> str:
    # Create a SHA-256 hash of the password
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Example usage:
stored_hashed_password = hash_password("password123")  # This would be stored in your database
print("Hashed password:", stored_hashed_password)
# Function to fetch stock suggestions
def get_stock_suggestions(query):
    if len(query) < 3:
        return []
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url).json()
        matches = response.get("bestMatches", [])
        return [match["1. symbol"] for match in matches]
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return []

# Function to fetch stock prices with fallback
def get_stock_price(symbol):
    try:
        if not symbol.endswith((".NS", ".BO")):
            symbol += ".NS"
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            return f"₹{data['Close'].iloc[-1]:.2f}"
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url).json()
        quote = response.get("Global Quote", {})
        if quote:
            return f"₹{float(quote.get('05. price', 0)):.2f}"
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    return "Data Unavailable"

# Function to fetch market indexes with fallback to Yahoo Finance
def get_market_indexes():
    indexes = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "NIFTY BANK": "^NSEBANK"
    }
    results = {}
    for name, symbol in indexes.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                price = data['Close'].iloc[-1]
                prev_close = data['Close'].iloc[-2] if len(data) > 1 else price
                change = price - prev_close
                change_pct = (change / prev_close) * 100
                results[name] = f"₹{price:.2f} ({change_pct:.2f}%)"
                continue
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url).json()
            print(f"Alpha Vantage Response for {name}: {response}")
            quote = response.get("Global Quote", {})
            if quote:
                price = float(quote.get("05. price", 0))
                change = float(quote.get("09. change", 0))
                change_pct = float(quote.get("10. change percent", "0%").rstrip('%'))
                results[name] = f"₹{price:.2f} ({change_pct:.2f}%)"
            else:
                results[name] = "Data Unavailable"
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            results[name] = "Data Unavailable"
    return results

# Function to fetch stock details with improved error handling
def get_stock_details(symbol):
    try:
        if not symbol.endswith((".NS", ".BO")):
            symbol += ".NS"
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d", interval="1m")
        return {
            "name": info.get("longName", info.get("shortName", symbol)),
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "change_percent": info.get("regularMarketChangePercent", 0),
            "open": history["Open"].iloc[-1] if not history.empty else 0,
            "high": history["High"].max() if not history.empty else 0,
            "low": history["Low"].min() if not history.empty else 0,
            "prev_close": info.get("previousClose", 0),
            "history": history
        }
    except Exception as e:
        print(f"Error fetching details for {symbol}: {e}")
        return None

# Fetch recommended stocks
def get_recommended_stocks():
    stocks = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "RELIANCE.NS", "HINDUNILVR.NS"]
    return {stock: get_stock_price(stock) for stock in stocks}

# Sidebar settings
with st.sidebar:
    st.title("⚙ Settings")
    refresh_rate = st.slider("Auto-refresh interval (seconds):", 10, 300, 60, key="refresh_rate_slider")

# Auto-refresh
st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")

# UI: Header & Search
st.markdown("<h1>🐻 Bear Bull <span style='color: #FF416C;'>AI</span></h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    st.button("👤 Profile", key="profile_button")
with col2:
    search_query = st.text_input("Search stocks...", "", key="search_input")
    if search_query:
        suggestions = get_stock_suggestions(search_query)
        if suggestions:
            selected_stock = st.selectbox("Suggested Stocks:", suggestions, key="stock_selectbox")
            search_query = selected_stock

# Store recent searches
if 'search_history' not in st.session_state:
    st.session_state.search_history = deque(maxlen=5)
if search_query and search_query not in st.session_state.search_history:
    st.session_state.search_history.appendleft(search_query)

# Display recent searches
if st.session_state.search_history:
    st.markdown("### 🔄 Recent Searches")
    cols = st.columns(min(4, len(st.session_state.search_history)))
    for i, stock in enumerate(st.session_state.search_history):
        with cols[i % 4]:
            if st.button(stock, key=f"recent_search_{i}"):
                search_query = stock

# Show selected stock price
if search_query:
    price = get_stock_price(search_query)
    st.markdown(f"### 📈 {search_query} Price: {price}")

# Market Indexes Section
st.markdown("### 📊 Indian Market Indexes")
indexes = get_market_indexes()
cols = st.columns(len(indexes))
for (name, value), col in zip(indexes.items(), cols):
    with col:
        st.metric(label=name, value=value)

# Recommended Stocks Section
st.markdown("### 📌 Recommended Stocks")
recommended = get_recommended_stocks()
cols = st.columns(3)
for (stock, price), col in zip(list(recommended.items())[:3], cols):
    with col:
        st.metric(label=stock, value=price)
        if st.button(f"View {stock}", key=f"view_{stock}"):
            st.experimental_set_query_params(page="chart", stock=stock)

if st.button("Show More Recommendations", key="show_more_button"):
    cols = st.columns(3)
    for (stock, price), col in zip(list(recommended.items())[3:6], cols):
        with col:
            st.metric(label=stock, value=price)
            if st.button(f"View {stock} ", key=f"view_more_{stock}"):
                st.experimental_set_query_params(page="chart", stock=stock)

# Placeholder Cards Section
st.markdown("### 📂 Searched Stocks")
if 'placeholder_cards' not in st.session_state:
    st.session_state.placeholder_cards = deque(maxlen=6)
if search_query and search_query not in st.session_state.placeholder_cards:
    st.session_state.placeholder_cards.appendleft(search_query)

cols = st.columns(3)
for i in range(0, 6, 3):
    row_cols = st.columns(3)
    for j in range(3):
        idx = i + j
        if idx < len(st.session_state.placeholder_cards):
            stock = st.session_state.placeholder_cards[idx]
            with row_cols[j]:
                if stock:
                    if st.button(f"📈 {stock}", key=f"placeholder_{stock}"):
                        details = get_stock_details(stock)
                        if details:
                            with st.expander(f"Details: {stock}", expanded=True):
                                st.markdown("<div class='square-popup'>", unsafe_allow_html=True)
                                st.write(f"**Name:** {details['name']}")
                                st.write(f"**Price:** ₹{details['price']:.2f}")
                                st.write(f"**Change:** ₹{details['change']:.2f} ({details['change_percent']:.2f}%)")
                                st.write(f"**Open:** ₹{details['open']:.2f}")
                                st.write(f"**High:** ₹{details['high']:.2f}")
                                st.write(f"**Low:** ₹{details['low']:.2f}")
                                st.write(f"**Prev Close:** ₹{details['prev_close']:.2f}")
                                st.line_chart(details['history'][['Open', 'High', 'Low', 'Close']])
                                if st.button("View Charts", key=f"chart_{stock}"):
                                    st.experimental_set_query_params(page="chart", stock=stock)
                                st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.error("Failed to load details")
                else:
                    st.markdown("""
                        <div class='stInfo' style='padding:20px;border-radius:10px;'>
                            <h4 style='color:black'>Empty Slot</h4>
                            <p style='color:black'>Search stocks to fill</p>
                        </div>
                    """, unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
    <div class='fixed-bottom'>
        <a href='#'>🏠 Home</a>
        <a href='#'>📊 Dashboard</a>
        <a href='#'>🔔 Alerts</a>
        <a href='#'>🤖 AI Chat</a>
        <a href='#'>💼 Portfolio</a>
    </div>
""", unsafe_allow_html=True)
