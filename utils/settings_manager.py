import yaml
import os

SETTINGS_FILE = "config/settings.yaml"

# Load settings from YAML file
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            return yaml.safe_load(file)
    return {}  # Return an empty dictionary if no settings file exists

# Save settings to YAML file
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        yaml.dump(settings, file, default_flow_style=False)

# Update specific setting
def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
