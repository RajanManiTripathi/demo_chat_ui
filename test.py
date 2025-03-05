from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import yaml
from litellm import completion,model_cost
from datetime import datetime
from typing import Dict, List

os.environ['GEMINI_API_KEY'] = "AIzaSyBwrlc9Ga3YAdW5OyxGpZ6IZIY0gBOWaJo"  # Replace with actual key if necessary

# FastAPI app instance
app = FastAPI()

# Sample in-memory storage for conversation history
conversation_history: Dict[str, List[Dict[str, str]]] = {}

# Pydantic model to handle user inputs
class ChatRequest(BaseModel):
    user_input: str  # User's message to the assistant
    session_id: str  # Session identifier
    persona_prompt: str  # Prompt/Persona for the model
    model_name: str  # Model name to be used for the conversation
# Helper function to calculate cost and tokens
def calculate_cost_and_tokens(response, cost_per_token: float):
    # Assuming token usage is available in the `response.usage` or another attribute
    tokens_used = response.usage.get("total_tokens", 0)  # Adjust if necessary
    cost = tokens_used * cost_per_token  # Calculate cost
    return tokens_used, cost

# Function to log the conversation to a text file
def log_conversation(user_input: str, assistant_response: str, tokens_used: int, cost: float):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("conversation_log.txt", "a") as log_file:
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"User: {user_input}\n")
        log_file.write(f"Assistant: {assistant_response}\n")
        log_file.write(f"Tokens Used: {tokens_used}, Cost: ${cost}\n")
        log_file.write("-" * 50 + "\n")

def get_price_per_token(model_name: str, is_input: bool ) -> float:
    """
    Retrieves the price per token for a given model from litellm's model cost data.

    Args:
        model_name: The name of the model (e.g., "gpt-3.5-turbo", "claude-2").
        is_input: True if retrieving the input token price, False for output token price.

    Returns:
        The price per token in USD, or None if the model is not found or cost data is unavailable.
    """
    try:
        if model_name in model_cost:
            cost_data = model_cost[model_name]
            if is_input:
                return cost_data.get("input_cost_per_token")
            else:
                return cost_data.get("output_cost_per_token")
        else:
            return None  # Model not found in cost data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@app.post("/chat/")
async def chat_with_assistant(request: ChatRequest):
    try:
        # Extract request data
        model_name = request.model_name
        prompt = request.persona_prompt
        cost_per_token = get_price_per_token(model_name, True)  # Get input token cost
        print('cost_per_token : ',cost_per_token)
        # Get the session history if available, or start a new conversation
        if request.session_id not in conversation_history:
            conversation_history[request.session_id] = [{"role": "system", "content": prompt}]
        
        # Append the user's input to the conversation history
        conversation_history[request.session_id].append({"role": "user", "content": request.user_input})
        
        # Call Litellm to get the response, pass the entire conversation history
        response = completion(
            model=model_name,
            messages=conversation_history[request.session_id]
        )

        # Check for the usage information in the response (adjust based on actual Litellm structure)
        assistant_response = response.choices[0].message.content
        tokens_used, cost = calculate_cost_and_tokens(response, cost_per_token)

        # Append the assistant's response to the conversation history
        conversation_history[request.session_id].append({"role": "assistant", "content": assistant_response})

        # Log the conversation to the file
        log_conversation(request.user_input, assistant_response, tokens_used, cost)

        # Return the assistant's response, tokens used, and calculated cost
        return {
            "response": assistant_response,
            "tokens_used": tokens_used,
            "cost": cost
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Litellm-powered assistant API!"}
