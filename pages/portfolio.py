import streamlit as st

# Set page layout
st.set_page_config(page_title="Bear Bull AI", layout="wide")

# Custom CSS for styling
st.markdown(
    """
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
    .header {
        text-align: center;
        background: linear-gradient(90deg, #FF416C, #FF4B2B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        margin: 0 auto; /* Center the header */
        font-weight: 600;
    }

    /* Styling for holdings section */
    .holdings-section {
        background: linear-gradient(135deg, #f0f2f6, #e0e0e0);
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Styling for cards */
    .card {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        color: white;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Styling for the bottom navigation bar */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #333;
        padding: 10px;
        text-align: center;
        z-index: 100;
        display: flex;
        justify-content: space-around;
    }
    .nav-button {
        color: white;
        background: linear-gradient(135deg, #FF416C, #FF4B2B);
        border: none;
        padding: 10px 15px;
        cursor: pointer;
        border-radius: 25px;
        font-size: 14px;
        font-weight: bold;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background: linear-gradient(135deg, #FF4B2B, #FF416C);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
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