import streamlit as st
import pandas as pd
import time
import os
import certifi
import ssl
from nsetools import Nse

# Set SSL Certificate Path to Fix SSL Errors
os.environ["SSL_CERT_FILE"] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize NSE tool
nse = Nse()

# Function to fetch live stock alerts with error handling
def get_stock_alerts():
    stock_symbols = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK']
    alerts = []

    for stock in stock_symbols:
        try:
            quote = nse.get_quote(stock)
            alerts.append({
                'Stock': stock,
                'Buy Price (₹)': quote.get('buyPrice1', 'N/A'),
                'Sell Price (₹)': quote.get('sellPrice1', 'N/A')
            })
        except Exception:
            alerts.append({'Stock': stock, 'Buy Price (₹)': 'Error', 'Sell Price (₹)': 'Error'})
    
    return alerts

# Streamlit Page Config
st.set_page_config(page_title='Stock Alerts', layout='wide')

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stMarkdown h1 {
            text-align: center;
            color: white;
        }
        .stDataFrame {
            background: #1e1e1e;
            color: white;
        }
        .nav-container {
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: #d9534f;
            position: fixed;
            bottom: 0;
            width: 100%;
            box-shadow: 0px -2px 5px rgba(0,0,0,0.3);
        }
        .nav-button {
            color: white;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
        }
        .search-button {
            position: absolute;
            top: 20px;
            right: 20px;
            background: white;
            padding: 10px 15px;
            border-radius: 50px;
            color: red;
            font-weight: bold;
            cursor: pointer;
        }
        .search-button:hover {
            background: #ffdddd;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.markdown("<h1>📈 Bear Bull AI - Stock Alerts</h1>", unsafe_allow_html=True)

# Search Symbol Button with Functionality
if st.button("🔍 Search Symbol", key='search_button'):
    st.sidebar.text_input("Enter Stock Symbol:")

# Display New Stock Alerts
st.markdown("### 🆕 New Alerts")
new_alerts = get_stock_alerts()
df_new = pd.DataFrame(new_alerts)
st.dataframe(df_new, use_container_width=True)

# Display Previous Alerts (Simulated Historical Data)
st.markdown("### ⏳ Previous Alerts")
previous_alerts = get_stock_alerts()
df_previous = pd.DataFrame(previous_alerts)
st.dataframe(df_previous, use_container_width=True)

# Live Updates Simulation Without Blocking UI
def update_alerts():
    if st.button("🔄 Refresh Alerts"):
        time.sleep(2)
        st.experimental_rerun()

update_alerts()

# Bottom Navigation Bar
st.markdown(
    """
    <div class='nav-container'>
        <a class='nav-button' href='/' target='_self'>🏠 Home</a>
        <a class='nav-button' href='/Dashboard' target='_self'>📊 Dashboard</a>
        <a class='nav-button' href='/Alerts' target='_self'>🔔 Stock Alerts</a>
        <a class='nav-button' href='/AI_Chat' target='_self'>🤖 AI Chat</a>
        <a class='nav-button' href='/Portfolio' target='_self'>💼 Portfolio</a>
    </div>
    """,
    unsafe_allow_html=True,
)
