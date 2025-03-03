import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(
    page_title="Home | AI Chat Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation
with st.sidebar:
    st.title("AI Chat Assistant")
    
    # User profile section
    st.subheader(f"Profile: {st.session_state.config['user_name']}")
    
    # Navigation
    st.subheader("Navigation")
    
    if st.button("🏠 Home", disabled=True):
        pass
    
    if st.button("💬 Chat"):
        switch_page("Chat")
    
    if st.button("🚪 Rooms"):
        switch_page("Rooms")
    
    if st.button("⚙️ Settings"):
        switch_page("Settings")
    
    # Display total cost
    st.sidebar.metric("Total Cost", f"${st.session_state.total_cost:.4f}")

# Main content - Welcome screen
st.title("Welcome to AI Chat Assistant")
st.markdown("""
### Your intelligent conversation partner

This AI Chat Assistant helps you:
- Chat with advanced AI models like GPT-4 and Claude
- Create and manage different chat rooms for specific topics
- Track your usage and costs
- Save and reuse your favorite prompts

Get started by clicking the button below or using the navigation sidebar.
""")

# Quick start button
if st.button("Go to Chat", type="primary", use_container_width=True):
    switch_page("Chat")

# Features showcase
st.subheader("Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 💬 Multiple Chat Rooms")
    st.markdown("Create dedicated spaces for different topics and projects")

with col2:
    st.markdown("#### 🤖 AI Model Selection")
    st.markdown("Choose from GPT-4, GPT-3.5, Claude and more")

with col3:
    st.markdown("#### 💾 Save Conversations")
    st.markdown("Never lose an important conversation again")

# Getting started guide
st.subheader("Getting Started")
st.markdown("""
1. **Navigate to Chat**: Start a conversation with the AI
2. **Explore Rooms**: Create specialized chat rooms for different topics
3. **Customize Settings**: Choose your preferred AI model and theme
4. **Save Prompts**: Store useful prompts for future use
""")