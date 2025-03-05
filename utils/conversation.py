import yaml

CONVERSATION_FILE = "conversation_history.yaml"

# Save conversation history to a file
def save_conversation(conversation_history):
    with open(CONVERSATION_FILE, 'w') as file:
        yaml.dump(conversation_history, file)

# Load saved conversation history
def load_conversation():
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, 'r') as file:
            return yaml.safe_load(file)
    return []
