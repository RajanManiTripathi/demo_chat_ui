import streamlit as st
import yaml

# Load YAML Configuration
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

CONFIG = load_config()

st.set_page_config(page_title="Settings", layout="wide")
st.title("⚙️ AI Settings")

# Model Selection
st.subheader("🤖 AI Model Selection")
new_model = st.selectbox("Choose an AI Model:", CONFIG["models"]["available_models"], index=0)

# Token Pricing
st.subheader("💰 Pricing & Limits")
token_limit = st.slider("Max Token Limit:", min_value=1000, max_value=10000, value=CONFIG["pricing"]["token_limit"])
cost_per_token = st.number_input("Cost Per Token ($):", value=CONFIG["pricing"]["cost_per_token"], step=0.001)

# Storage Management
st.subheader("🗄️ Storage Settings")
storage_usage = st.slider("Storage Usage (%)", min_value=0, max_value=100, value=CONFIG["storage"]["usage_percentage"])

# Save Settings Button
if st.button("Save Settings"):
    CONFIG["models"]["default"] = new_model
    CONFIG["pricing"]["token_limit"] = token_limit
    CONFIG["pricing"]["cost_per_token"] = cost_per_token
    CONFIG["storage"]["usage_percentage"] = storage_usage

    with open("config.yaml", "w") as file:
        yaml.dump(CONFIG, file)
    
    st.success("✅ Settings updated successfully!")
