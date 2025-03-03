import streamlit as st
import time
from litellm_handler import generate_response

st.set_page_config(page_title="Chat Assistant", layout="wide")

# Sample chat history for testing UI
SAMPLE_CHAT_HISTORY = [
    ("🧑 You", "Hello"),
    ("🤖 AI", "Hi there! How can I assist you today?"),
    ("🧑 You", "What is AI?"),
    ("🤖 AI", "AI stands for Artificial Intelligence, which simulates human intelligence in machines.")
]

# Load sample chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = SAMPLE_CHAT_HISTORY

st.title("💬 Chat Assistant")

# Display chat messages
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        role, text = chat
        css_class = "user-message" if role == "🧑 You" else "ai-message"
        st.markdown(f"<div class='message-container {css_class}'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Type your message...")
if st.button("Send") and user_input:
    st.session_state.chat_history.append(("🧑 You", user_input))
    
    # Get AI response using LiteLLM or sample data
    ai_response = generate_response(user_input)
    st.session_state.chat_history.append(("🤖 AI", ai_response))

    st.rerun()
