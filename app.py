import streamlit as st
from utils.prompt_manager import load_prompt, save_prompt
from utils.conversation import load_conversation, save_conversation
from utils.settings_manager import load_settings, save_settings, update_setting
from models import LocalModel, LitellmModel

# Set up page layout
st.set_page_config(page_title="Prompt Chat Agent", layout="wide")

# Global conversation history storage
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = "Local Model"  # Default model

# Load settings from YAML
settings = load_settings()

def display_prompt_page():
    st.title("Prompt Agent")
    st.subheader("Upload or Load Prompt YAML")

    # Upload Prompt YAML file
    uploaded_file = st.file_uploader("Choose a YAML file", type="yaml")
    if uploaded_file:
        prompt = load_prompt(uploaded_file)
        st.session_state['current_prompt'] = prompt
        st.write("Prompt Loaded:")
        st.json(prompt)

    # Save modified prompt
    if st.session_state.get('current_prompt', None):
        if st.button("Save Prompt"):
            save_prompt(st.session_state['current_prompt'])
            st.success("Prompt Saved!")

    # Display available models
    models = ["Local Model", "Litellm Model"]
    model_choice = st.selectbox("Select Model", models, index=models.index(st.session_state['selected_model']))
    if model_choice != st.session_state['selected_model']:
        st.session_state['selected_model'] = model_choice

def display_chat_page():
    st.title("Chat with Prompt Agent")
    prompt = st.session_state.get('current_prompt', None)
    
    if not prompt:
        st.warning("Please load a prompt first.")
        return

    # Chat Interface
    user_input = st.text_input("Your Question:")
    if user_input:
        # Call the appropriate model based on selection
        response = get_model_response(user_input)

        # Add to conversation history
        st.session_state['conversation_history'].append(('User', user_input))
        st.session_state['conversation_history'].append(('Agent', response))

        # Display conversation
        for speaker, text in st.session_state['conversation_history']:
            st.write(f"**{speaker}:** {text}")

        # Save the conversation
        save_conversation(st.session_state['conversation_history'])

def get_model_response(user_input):
    """Fetch response from the selected model."""
    if st.session_state['selected_model'] == "Local Model":
        model = LocalModel(settings)
    elif st.session_state['selected_model'] == "Litellm Model":
        model = LitellmModel(settings)
    
    return model.get_response(user_input)

def display_settings_page():
    st.title("Model Settings")

    # Input fields for model-specific settings
    model_type = st.selectbox("Select Model", ["Local Model", "Litellm Model"], index=["Local Model", "Litellm Model"].index(settings.get("selected_model", "Local Model")))
    temperature = st.slider("Set Temperature", min_value=0.0, max_value=1.0, value=settings.get("temperature", 0.7))
    api_key = st.text_input("API Key", value=settings.get("api_key", ""))

    if st.button("Save Settings"):
        # Save the settings to YAML file
        update_setting("selected_model", model_type)
        update_setting("temperature", temperature)
        update_setting("api_key", api_key)
        st.success("Settings saved!")

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Select Page", ["Home", "Chat", "Model Settings"])
    
    if app_mode == "Home":
        display_prompt_page()
    elif app_mode == "Chat":
        display_chat_page()
    elif app_mode == "Model Settings":
        display_settings_page()

if __name__ == '__main__':
    main()
