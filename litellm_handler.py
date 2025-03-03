import litellm
import yaml

# Load configuration from YAML
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

CONFIG = load_config()

# Simulated AI responses for testing UI
SAMPLE_RESPONSES = {
    "Hello": "Hi there! How can I assist you today?",
    "What is AI?": "AI stands for Artificial Intelligence, which simulates human intelligence in machines.",
    "Tell me a joke": "Why don’t robots get tired? Because they recharge their batteries!"
}

def generate_response(prompt):
    selected_model = CONFIG["models"]["default"]

    # Return sample response if available, otherwise use LiteLLM
    if prompt in SAMPLE_RESPONSES:
        return SAMPLE_RESPONSES[prompt]

    response = litellm.completion(
        model=selected_model,
        messages=[{"role": "user", "content": prompt}],
        api_key=CONFIG["api_keys"].get("openai")  
    )
    
    return response["choices"][0]["message"]["content"]
