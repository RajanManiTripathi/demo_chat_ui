import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import yaml
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Settings | AI Chat Assistant",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to save config
def save_config():
    with open("config.yaml", "w") as file:
        yaml.dump(st.session_state.config, file)
    st.success("Settings saved successfully!")

# Sidebar for navigation
with st.sidebar:
    st.title("AI Chat Assistant")
    
    # User profile section
    st.subheader(f"Profile: {st.session_state.config['user_name']}")
    
    # Navigation
    st.subheader("Navigation")
    
    if st.button("🏠 Home"):
        switch_page("Home")
    
    if st.button("💬 Chat"):
        switch_page("Chat")
    
    if st.button("🚪 Rooms"):
        switch_page("Rooms")
    
    if st.button("⚙️ Settings", disabled=True):
        pass
    
    if st.button("🧠 Personas"):
        switch_page("Personas")
    
    if st.button("📝 Prompts"):
        switch_page("Prompts")
    
    # Display total cost
    st.sidebar.metric("Total Cost", f"${st.session_state.total_cost:.4f}")

# Main content
st.title("Settings")
st.markdown("Configure your AI Chat Assistant preferences and view usage statistics.")

# Settings tabs
tab1, tab2, tab3, tab4 = st.tabs(["User Settings", "AI Models", "Usage Statistics", "Advanced"])

with tab1:
    st.subheader("User Profile")
    
    # User name
    user_name = st.text_input("Your Name", value=st.session_state.config["user_name"])
    if user_name != st.session_state.config["user_name"]:
        st.session_state.config["user_name"] = user_name
    
    # Theme selection
    theme_options = ["light", "dark"]
    selected_theme = st.selectbox(
        "Theme",
        theme_options,
        index=theme_options.index(st.session_state.config.get("theme", "light"))
    )
    if selected_theme != st.session_state.config.get("theme", "light"):
        st.session_state.config["theme"] = selected_theme
    
    # UI preferences
    st.subheader("UI Preferences")
    
    # Chat message style
    chat_style_options = ["Bubbles", "Cards", "Simple"]
    selected_chat_style = st.selectbox(
        "Chat Message Style",
        chat_style_options,
        index=0
    )
    
    # Save button
    if st.button("Save User Settings"):
        save_config()

with tab2:
    st.subheader("AI Model Settings")
    
    # Default model selection
    model_options = list(st.session_state.config["models"].keys())
    default_model = st.selectbox(
        "Default AI Model",
        model_options,
        index=model_options.index(st.session_state.config["default_model"]),
        format_func=lambda x: st.session_state.config["models"][x]["name"]
    )
    if default_model != st.session_state.config["default_model"]:
        st.session_state.config["default_model"] = default_model
    
    # Model pricing information
    st.subheader("Model Pricing")
    
    for model_id, model_info in st.session_state.config["models"].items():
        with st.expander(f"{model_info['name']} Settings"):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_name = st.text_input(
                    "Display Name",
                    value=model_info["name"],
                    key=f"name_{model_id}"
                )
                if new_name != model_info["name"]:
                    st.session_state.config["models"][model_id]["name"] = new_name
            
            with col2:
                new_cost = st.number_input(
                    "Cost per 1K tokens ($)",
                    min_value=0.0,
                    max_value=10.0,
                    value=model_info["cost_per_1k_tokens"],
                    step=0.001,
                    key=f"cost_{model_id}"
                )
                if new_cost != model_info["cost_per_1k_tokens"]:
                    st.session_state.config["models"][model_id]["cost_per_1k_tokens"] = new_cost
    
    # Add new model
    st.subheader("Add New Model")
    
    with st.form("add_model_form"):
        new_model_id = st.text_input("Model ID (e.g., 'gpt-4-turbo')")
        new_model_name = st.text_input("Display Name (e.g., 'GPT-4 Turbo')")
        new_model_cost = st.number_input("Cost per 1K tokens ($)", min_value=0.0, max_value=10.0, value=0.01, step=0.001)
        
        submit_button = st.form_submit_button("Add Model")
        
        if submit_button and new_model_id and new_model_name:
            if new_model_id not in st.session_state.config["models"]:
                st.session_state.config["models"][new_model_id] = {
                    "name": new_model_name,
                    "cost_per_1k_tokens": new_model_cost
                }
                st.success(f"Model '{new_model_name}' added!")
                save_config()
                st.experimental_rerun()
            else:
                st.error(f"Model ID '{new_model_id}' already exists!")
    
    # Save button
    if st.button("Save Model Settings"):
        save_config()

with tab3:
    st.subheader("Usage Statistics")
    
    # Total cost
    st.metric("Total Cost", f"${st.session_state.total_cost:.4f}")
    
    # Messages per room
    st.subheader("Messages per Room")
    
    # Create a bar chart of message counts
    room_names = []
    message_counts = []
    
    for room_name, room_data in st.session_state.rooms.items():
        room_names.append(room_name)
        message_counts.append(len(room_data.get("messages", [])))
    
    # Display as a bar chart
    st.bar_chart({
        "Messages": message_counts
    }, x=room_names)
    
    # Cost breakdown by model
    st.subheader("Cost by Model")
    
    # Calculate costs by model
    model_costs = {}
    
    for room_data in st.session_state.rooms.values():
        for message in room_data.get("messages", []):
            if message["role"] == "assistant":
                model = message.get("model", "gpt-3.5-turbo")
                cost = message.get("cost", 0)
                
                if model not in model_costs:
                    model_costs[model] = 0
                
                model_costs[model] += cost
    
    # Display costs by model
    for model, cost in model_costs.items():
        model_name = st.session_state.config["models"][model]["name"]
        st.metric(model_name, f"${cost:.4f}")
    
    # Reset statistics
    if st.button("Reset Usage Statistics"):
        st.session_state.total_cost = 0.0
        st.success("Usage statistics reset successfully!")

with tab4:
    st.subheader("Advanced Settings")
    
    # API Configuration
    st.subheader("API Configuration")
    st.markdown("In a production environment, you would configure API keys here.")
    
    # Sample API key input (not functional in this demo)
    openai_api_key = st.text_input("OpenAI API Key", type="password", value="sk-...")
    anthropic_api_key = st.text_input("Anthropic API Key", type="password", value="sk-ant-...")
    
    st.caption("Note: API keys are not saved or used in this demo application.")
    
    # Export/Import data
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export All Data", use_container_width=True):
            # In a real app, this would generate a downloadable file
            export_data = {
                "config": st.session_state.config,
                "rooms": st.session_state.rooms,
                "personas": st.session_state.personas,
                "sample_prompts": st.session_state.sample_prompts,
                "saved_prompts": st.session_state.saved_prompts,
                "total_cost": st.session_state.total_cost
            }
            
            # Display the data as JSON
            st.code(json.dumps(export_data, indent=2))
            st.info("In a production app, this would download a file with all your data.")
    
    with col2:
        if st.button("Clear All Data", use_container_width=True):
            # Show confirmation
            st.warning("This will delete all chat history and reset all settings. Are you sure?")
            if st.button("Yes, Clear Everything"):
                # Reset session state
                for room_name in st.session_state.rooms:
                    st.session_state.rooms[room_name]["messages"] = []
                st.session_state.total_cost = 0.0
                st.session_state.saved_prompts = []
                st.success("All data cleared successfully!")
                st.experimental_rerun()