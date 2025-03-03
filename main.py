"""
app.py
Main entry point for AI Assistant. Handles navigation between different pages.
"""

import streamlit as st

# App Configurations
st.set_page_config(page_title="AI Assistant", layout="wide")

# Sidebar Navigation
st.sidebar.image("logo.png", width=150)
st.sidebar.title("AMWAY ASSISTANT")
st.sidebar.markdown("## Navigation")

# Multipage Navigation
st.sidebar.page_link("pages/Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Chat.py", label="💬 Chat")
st.sidebar.page_link("pages/Rooms.py", label="📂 Rooms")
st.sidebar.page_link("pages/Settings.py", label="⚙️ Settings")

# Welcome Message
st.write("# Welcome to AI Assistant")
st.write("Navigate using the sidebar to start chatting or configure your settings.")
