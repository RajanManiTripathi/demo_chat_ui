import streamlit as st
import time

# Placeholder functions for backend integration
def fetch_chat_history():
    return st.session_state.get("chat_history", {})

def save_chat_history(chat_name, messages):
    st.session_state.chat_history[chat_name] = messages

def fetch_saved_prompts():
    return st.session_state.get("saved_prompts", [])

def save_new_prompt(prompt):
    st.session_state.saved_prompts.append(prompt)

def get_ai_response(user_input, model):
    time.sleep(1)
    return f"🤖 {model}: Processing your request..."

# Streamlit App Configuration
st.set_page_config(layout="wide", page_title="Amway Chat Assistant")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "cost" not in st.session_state:
    st.session_state.cost = 0.00
if "saved_prompts" not in st.session_state:
    st.session_state.saved_prompts = []

# Top Navigation Bar
st.markdown(
    """
    <style>
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background-color: #2E4A2E;
        color: white;
    }
    .nav-button {
        background-color: #4CAF50;
        padding: 8px 16px;
        border-radius: 5px;
        color: white;
        text-decoration: none;
        margin-right: 10px;
    }
    </style>
    <div class="top-bar">
        <div>
            <a class="nav-button" href="#">Assistants Gallery</a>
            <a class="nav-button" href="#">Personas</a>
        </div>
        <div>
            <span>Profile: User</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Main Layout
col1, col2 = st.columns([3, 1])

# Left Column - Chat UI
with col1:
    st.subheader("💬 Amway Assistant Chat")
    chat_container = st.container()

    with chat_container:
        st.markdown('<div style="max-height: 65vh; overflow-y: auto;">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            role, text = msg["role"], msg["content"]
            st.markdown(f'<div style="padding: 10px; margin: 5px; border-radius: 10px; background-color: {"#DCF8C6" if role == "user" else "#EAEAEA"};">{text}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.text_input("Type a message...")
    if st.button("Send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        ai_response = get_ai_response(user_input, "GPT-4")
        st.session_state.messages.append({"role": "ai", "content": ai_response})
        st.session_state.cost += 0.05
        save_chat_history(f"Chat {len(st.session_state.chat_history) + 1}", st.session_state.messages.copy())
        st.rerun()

# Right Column - Sidebar with Chat History, Model, Profile
with col2:
    st.markdown("### 🔍 Chat History")
    chat_names = list(fetch_chat_history().keys()) or ["No Previous Chats"]
    selected_chat = st.selectbox("Select a Chat", chat_names)
    if selected_chat != "No Previous Chats":
        st.session_state.messages = st.session_state.chat_history[selected_chat]

    st.markdown("### 🤖 AI Model")
    model = st.selectbox("Select Model", ["GPT-4", "Claude", "Llama-2", "Custom"])

    st.markdown(f"💰 **Cost Used:** ${st.session_state.cost:.2f}")

    st.markdown("### 📌 Saved Prompts")
    saved_prompts = ["No Saved Prompts"] + fetch_saved_prompts()
    selected_prompt = st.selectbox("Select Prompt", saved_prompts)
    if selected_prompt != "No Saved Prompts":
        st.session_state.messages.append({"role": "user", "content": selected_prompt})
    
    new_prompt = st.text_input("Save New Prompt")
    if st.button("Save Prompt") and new_prompt:
        save_new_prompt(new_prompt)

# Rooms Section
st.markdown("### 🏢 Assistants Rooms")
room_col1, room_col2 = st.columns(2)

with room_col1:
    st.markdown("#### Public Room")
    st.button("Translation Assistant")
    st.button("Catalog Writing Assistant")
    st.button("Email Drafting Assistant")

with room_col2:
    st.markdown("#### HR Room")
    st.button("Interview Summary Assistant")
    st.button("Candidate Filtering and Scoring")
    
st.button("➕ Add a New Assistant")
