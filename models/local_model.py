class LocalModel:
    def __init__(self, settings):
        self.name = "Local Model"
        self.temperature = settings.get("temperature", 0.7)
    
    def get_response(self, user_input):
        # Placeholder logic for a local model that takes temperature into account
        return f"Local Model response (Temp: {self.temperature}): {user_input}"
