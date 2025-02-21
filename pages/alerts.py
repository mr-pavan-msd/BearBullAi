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
                'Price': quote.get('lastPrice', 'N/A'),
                'Change': quote.get('change', 'N/A')
            })
        except Exception as e:
            alerts.append({'Stock': stock, 'Price': 'Error', 'Change': 'Error'})
    
    return alerts

# Streamlit Page Config
st.set_page_config(page_title='Stock Alerts', layout='wide')

# App Title
st.markdown("<h1 style='text-align: center; color: white;'>📈 Bear Bull AI - Stock Alerts</h1>", unsafe_allow_html=True)

# Search Symbol Button
st.markdown("""
    <div style='position: absolute; top: 20px; right: 20px; background: white; padding: 10px 15px; border-radius: 50px; color: red; font-weight: bold;'>
        🔍 Search Symbol
    </div>
""", unsafe_allow_html=True)

# Display New Stock Alerts
st.markdown("### 🆕 New Alerts")
new_alerts = get_stock_alerts()
df_new = pd.DataFrame(new_alerts)
st.dataframe(df_new)

# Display Previous Alerts (Simulating Historical Data)
st.markdown("### ⏳ Previous Alerts")
previous_alerts = get_stock_alerts()
df_previous = pd.DataFrame(previous_alerts)
st.dataframe(df_previous)

# Live Updates Simulation (Real-time Stock Alerts)
def update_alerts():
    while True:
        time.sleep(5)  # Refresh every 5 seconds
        st.experimental_rerun()

# Bottom Navigation Bar
st.markdown("""
    <style>
        .nav-container {
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: #d9534f;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        .nav-button {
            color: white;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
    <div class='nav-container'>
        <a class='nav-button' href='/' target='_self'>🏠 Home</a>
        <a class='nav-button' href='/Dashboard' target='_self'>📊 Dashboard</a>
        <a class='nav-button' href='/Alerts' target='_self'>🔔 Stock Alerts</a>
        <a class='nav-button' href='/AI_Chat' target='_self'>🤖 AI Chat</a>
        <a class='nav-button' href='/Portfolio' target='_self'>💼 Portfolio</a>
    </div>
""", unsafe_allow_html=True)
