import streamlit as st

# Set page layout
st.set_page_config(page_title="Bear Bull AI", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: black;
        }
        .header {
            font-size: 30px;
            font-weight: bold;
            font-style: italic;
            color: white;
            text-align: center;
        }
        .holdings-section {
            background-color: #E0E0E0;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        }
        .card {
            background-color: #4285F4;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            color: white;
            font-size: 18px;
        }
        .nav-bar {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #E0E0E0;
            text-align: center;
            padding: 10px;
            display: flex;
            justify-content: space-around;
        }
        .nav-button {
            color: white;
            background-color: #FF5733;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 50%;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<div class='header'>🐻 Bear Bull AI</div>", unsafe_allow_html=True)
st.markdown("<h4 style='font-style:italic;'>Holdings</h4>", unsafe_allow_html=True)

# Tabs for Overview, Equity, Mutual Funds
tab1, tab2, tab3 = st.tabs(["Overview", "Equity", "Mutual Funds"])

with tab1:
    st.markdown("### Overview Section")

with tab2:
    st.markdown("### Equity Section")

with tab3:
    st.markdown("### Mutual Funds Section")

# Holdings Section
st.markdown("<div class='holdings-section'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'>Invested Value<br>₹ 1000</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'>Overall Gain/Loss<br>₹ 1000</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='card'>Today's Gain/Loss<br>₹ 1000</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Assets Section
st.markdown("<div class='holdings-section'>", unsafe_allow_html=True)
st.markdown("### Assets")
st.markdown("**Equity**")
st.markdown("<div class='card'>📊 Equity</div>", unsafe_allow_html=True)
st.markdown("**Mutual Funds**")
st.markdown("<div class='card'>💰 Mutual Funds</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Extra Buttons Section
st.markdown("<div class='holdings-section'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'>📈 Profit & Loss</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'>💹 Trades & Charges</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='card'>⚙️ Manage Account</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Bottom Navigation Bar
st.markdown(
    """
    <div class='nav-bar'>
        <a href='/Home' class='nav-button'>🏠 Home</a>
        <a href='/Dashboard' class='nav-button'>📊 Dashboard</a>
        <a href='/StockAlerts' class='nav-button'>🔔 Stock Alerts</a>
        <a href='/AI_Chat' class='nav-button'>🤖 AI Chat</a>
        <a href='/Portfolio' class='nav-button'>💼 Portfolio</a>
    </div>
    """,
    unsafe_allow_html=True
)
