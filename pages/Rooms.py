import streamlit as st

st.set_page_config(page_title="AI Rooms", layout="wide")

st.title("🏠 AI Rooms - Choose Your Assistant")

# Sample AI assistants for UI testing
rooms = {
    "Tech Assistant": "I can help with coding, debugging, and tech advice!",
    "Marketing Expert": "I provide insights on branding, SEO, and ads!",
    "Financial Advisor": "I analyze market trends and investment strategies.",
    "Creative Writer": "I assist with storytelling, poetry, and blog writing!"
}

selected_room = st.selectbox("Select an AI Persona:", list(rooms.keys()), index=0)

st.write(f"**{selected_room}**: {rooms[selected_room]}")

if st.button("Start Chat"):
    st.session_state.selected_room = selected_room
    st.switch_page("pages/Home.py")
