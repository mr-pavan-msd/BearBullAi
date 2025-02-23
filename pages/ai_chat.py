import streamlit as st
import time
import speech_recognition as sr
from nsepython import nsefetch, nse_eq

# Set page config
st.set_page_config(page_title="Bear Bull AI - Chat", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .chat-container {
            max-width: 600px;
            margin: auto;
        }
        .user-msg, .bot-msg {
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            display: flex;
            align-items: center;
        }
        .user-msg {
            background-color: #d1ecf1;
            justify-content: flex-end;
        }
        .bot-msg {
            background-color: #f8f9fa;
            justify-content: flex-start;
        }
        .chat-input {
            width: 100%;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        .send-button, .mic-button {
            background-color: #FF5733;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            margin-left: 10px;
        }
        .nav-container {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #333;
            text-align: center;
            padding: 10px;
            display: flex;
            justify-content: space-around;
        }
        .nav-button {
            color: white;
            background-color: #FF5733;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            border-radius: 50px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("""<h1 style='text-align: center;'>🐻 Bear Bull AI Chat</h1>""", unsafe_allow_html=True)

# Chat display
chat_container = st.container()
with chat_container:
    for role, text in st.session_state["messages"]:
        st.markdown(f"<div class='{role}-msg'><strong>{role.capitalize()}:</strong> {text}</div>", unsafe_allow_html=True)

# Voice input function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Speech recognition service unavailable"

# Input field & buttons
col1, col2, col3 = st.columns([7, 1, 1])
with col1:
    user_input = st.text_input("Type your message...", key="chat_input")
with col2:
    if st.button("➤", key="send_button") and user_input:
        st.session_state["messages"].append(("user", user_input))
        st.rerun()
with col3:
    if st.button("🎙️", key="mic_button"):
        voice_text = recognize_speech()
        if voice_text:
            st.session_state["messages"].append(("user", voice_text))
            st.rerun()

# Simulate AI response
if st.session_state["messages"] and st.session_state["messages"][-1][0] == "user":
    time.sleep(1)  # Simulating API delay
    bot_response = "Hello! How can I assist you in stock trading today?"
    st.session_state["messages"].append(("bot", bot_response))
    st.rerun()

# Function to fetch Indian stock data
def get_indian_stock_data(symbol):
    try:
        data = nse_eq(symbol)
        return data
    except Exception as e:
        return f"Error fetching data for {symbol}: {e}"

# Search symbol and fetch real-time data for Indian stocks
st.sidebar.title("Search Indian Stock Symbol")
symbol = st.sidebar.text_input("Enter Indian stock symbol (e.g., TCS, INFY):")
if symbol:
    stock_data = get_indian_stock_data(symbol)
    if isinstance(stock_data, dict):
        st.sidebar.write(f"Data for {symbol}:")
        st.sidebar.write(stock_data)
    else:
        st.sidebar.error(stock_data)

# Bottom navigation bar
st.markdown(
    """
    <div class='nav-container'>
        <button class='nav-button' onclick="window.location.href='/Home'">🏠 Home</button>
        <button class='nav-button' onclick="window.location.href='/Dashboard'">📊 Dashboard</button>
        <button class='nav-button' onclick="window.location.href='/Alerts'">🔔 Stock Alerts</button>
        <button class='nav-button' onclick="window.location.href='/AI_Chat'">🤖 AI Chat</button>
        <button class='nav-button' onclick="window.location.href='/Portfolio'">💼 Portfolio</button>
    </div>
    """,
    unsafe_allow_html=True,
)
