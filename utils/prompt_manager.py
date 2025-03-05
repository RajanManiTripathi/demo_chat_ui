import yaml

# Load a YAML prompt from file
def load_prompt(file):
    try:
        prompt = yaml.safe_load(file)
        return prompt
    except yaml.YAMLError as e:
        print(f"Error loading YAML: {e}")
        return {}

# Save current prompt to a local YAML file
def save_prompt(prompt):
    with open('prompt.yaml', 'w') as file:
        yaml.dump(prompt, file)
