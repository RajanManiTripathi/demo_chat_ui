import streamlit as st
import yaml
import os
import time
import random
import json

def load_config():
    """Load configuration from YAML file"""
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    return {
        "models": {
            "gpt-4": {"name": "GPT-4", "cost_per_1k_tokens": 0.03},
            "gpt-3.5-turbo": {"name": "GPT-3.5", "cost_per_1k_tokens": 0.002},
            "claude-2": {"name": "Claude 2", "cost_per_1k_tokens": 0.025},
            "llama-2": {"name": "Llama 2", "cost_per_1k_tokens": 0.001},
            "mistral-7b": {"name": "Mistral 7B", "cost_per_1k_tokens": 0.0005}
        },
        "default_model": "gpt-3.5-turbo",
        "user_name": "User",
        "theme": "light"
    }

def save_config(config):
    """Save configuration to YAML file"""
    with open("config.yaml", "w") as file:
        yaml.dump(config, file)

def load_personas():
    """Load assistant personas from JSON file"""
    if os.path.exists("personas.json"):
        with open("personas.json", "r") as file:
            return json.load(file)
    return {
        "general": {
            "name": "General Assistant",
            "description": "A helpful, general-purpose AI assistant",
            "system_prompt": "You are a helpful, general-purpose AI assistant. Answer questions accurately and concisely.",
            "sample_responses": [
                "I'm here to help with any questions you might have.",
                "That's an interesting question. Here's what I know about it...",
                "I'd be happy to assist you with that. Let me provide some information."
            ]
        },
        "hr_assistant": {
            "name": "HR Assistant",
            "description": "Specialized in HR, recruitment, and workplace policies",
            "system_prompt": "You are an HR assistant specializing in recruitment, employee relations, and workplace policies. Provide professional advice on HR matters.",
            "sample_responses": [
                "From an HR perspective, the best approach would be...",
                "When conducting interviews, it's important to consider...",
                "Regarding workplace policies, I recommend..."
            ]
        },
        "creative_writer": {
            "name": "Creative Writer",
            "description": "Assists with creative writing, storytelling, and content creation",
            "system_prompt": "You are a creative writing assistant. Help with storytelling, character development, plot ideas, and creative content.",
            "sample_responses": [
                "Here's a creative story based on your prompt...",
                "Your character could be developed further by...",
                "For an engaging plot twist, consider..."
            ]
        },
        "tech_expert": {
            "name": "Tech Expert",
            "description": "Specialized in technology, programming, and technical support",
            "system_prompt": "You are a technical expert assistant. Provide accurate information about technology, programming, and technical troubleshooting.",
            "sample_responses": [
                "The technical solution to this problem is...",
                "In programming, this concept works by...",
                "To troubleshoot this issue, try the following steps..."
            ]
        }
    }

def save_personas(personas):
    """Save assistant personas to JSON file"""
    with open("personas.json", "w") as file:
        json.dump(personas, file, indent=2)

def load_sample_prompts():
    """Load sample prompts from JSON file"""
    if os.path.exists("sample_prompts.json"):
        with open("sample_prompts.json", "r") as file:
            return json.load(file)
    return {
        "general": [
            "Explain quantum computing in simple terms",
            "What are the major events that happened in 1969?",
            "How does photosynthesis work?",
            "What's the difference between machine learning and deep learning?",
            "Can you explain the concept of compound interest?"
        ],
        "hr_assistant": [
            "What questions should I ask in a job interview for a software developer?",
            "How do I create an effective onboarding process for new employees?",
            "What are some strategies for improving employee retention?",
            "How should I handle a workplace conflict between team members?",
            "What are the key components of a good performance review?"
        ],
        "creative_writer": [
            "Write a short story about a robot learning to feel emotions",
            "Create a character description for a fantasy novel protagonist",
            "Give me a plot outline for a mystery set in Victorian London",
            "Write a poem about the changing seasons",
            "Develop a dialogue between two characters meeting for the first time"
        ],
        "tech_expert": [
            "Explain how blockchain technology works",
            "What are the best practices for securing a web application?",
            "How does natural language processing work?",
            "What's the difference between REST and GraphQL APIs?",
            "Explain the concept of containerization and Docker"
        ]
    }

def save_sample_prompts(prompts):
    """Save sample prompts to JSON file"""
    with open("sample_prompts.json", "w") as file:
        json.dump(prompts, file, indent=2)

def simulate_ai_response(prompt, model, persona="general"):
    """Simulate an AI response based on the selected model and persona with improved response generation"""
    # Load personas
    personas = load_personas()
    selected_persona = personas.get(persona, personas["general"])
    
    # Get sample responses for the selected persona
    sample_responses = selected_persona.get("sample_responses", [
        "This is a simulated response. In a production environment, this would connect to an AI API."
    ])
    
    # Add some randomness to the response
    base_response = random.choice(sample_responses)
    
    # Add model-specific information
    model_info = {
        "gpt-4": "As GPT-4, I can provide detailed and nuanced responses across a wide range of topics.",
        "gpt-3.5-turbo": "As GPT-3.5, I aim to be helpful, harmless, and honest in my responses.",
        "claude-2": "As Claude 2, I'm designed to be helpful, harmless, and honest.",
        "llama-2": "As Llama 2, I'm an open-source language model trained on diverse internet data.",
        "mistral-7b": "As Mistral 7B, I'm a compact but powerful language model optimized for efficiency."
    }
    
    # Simulate typing delay with progress bar
    with st.spinner("AI is thinking..."):
        # Create a progress bar
        progress_bar = st.progress(0)
        
        # Simulate thinking time based on model (more advanced models "think" longer)
        thinking_time = {
            "gpt-4": 2.0,
            "gpt-3.5-turbo": 1.5,
            "claude-2": 1.8,
            "llama-2": 1.2,
            "mistral-7b": 1.0
        }.get(model, 1.5)
        
        # Update progress bar
        for i in range(10):
            time.sleep(thinking_time / 10)
            progress_bar.progress((i + 1) / 10)
        
        # Remove progress bar
        progress_bar.empty()
    
    # Generate a more contextual response based on the prompt
    prompt_lower = prompt.lower()
    
    # Check for specific keywords in the prompt for more targeted responses
    if "hello" in prompt_lower or "hi" in prompt_lower or "hey" in prompt_lower:
        response = f"Hello! I'm {selected_persona['name']}. {base_response}"
    
    elif "who are you" in prompt_lower or "what can you do" in prompt_lower:
        response = f"""I'm {selected_persona['name']}, {selected_persona['description']}. 
        
I'm currently running as a simulation of {model_info.get(model, 'an AI assistant')}. I can help you with a variety of tasks related to my expertise, including answering questions, providing information, and assisting with specific problems.

My capabilities include:
- Answering questions in my knowledge domain
- Providing explanations and clarifications
- Offering suggestions and recommendations
- Helping with creative and technical tasks

How can I assist you today?"""
    
    elif "help" in prompt_lower or "assist" in prompt_lower:
        response = f"""I'd be happy to help! As {selected_persona['name']}, I specialize in {selected_persona['description']}. 

What specific assistance do you need today? I'm ready to provide information, answer questions, or help you solve problems in my area of expertise.

{base_response}"""
    
    elif any(keyword in prompt_lower for keyword in ["explain", "what is", "how does", "why"]):
        # For explanations, create a more structured response
        topic = prompt.replace("explain", "").replace("what is", "").replace("how does", "").replace("why", "").strip()
        
        response = f"""Let me explain about {topic}.

{base_response}

{model_info.get(model, '')}

Would you like me to elaborate on any specific aspect of this topic?"""
    
    elif "write" in prompt_lower or "create" in prompt_lower or "generate" in prompt_lower:
        # For creative requests
        response = f"""Here's what I've created based on your request:

{base_response}

I hope this meets your expectations! Would you like me to revise or expand on any part of it?"""
    
    elif "compare" in prompt_lower or "difference" in prompt_lower or "versus" in prompt_lower or "vs" in prompt_lower:
        # For comparison requests
        response = f"""Here's a comparison as requested:

{base_response}

The key differences can be summarized as:
1. First major difference point
2. Second major difference point
3. Third major difference point

Is there a specific aspect of this comparison you'd like me to explore further?"""
    
    elif "list" in prompt_lower or "steps" in prompt_lower or "how to" in prompt_lower:
        # For list or step-by-step requests
        response = f"""Here's a step-by-step guide:

1. First step in the process
2. Second step with important details
3. Third step with considerations
4. Final step to complete the task

{base_response}

Would you like more details on any of these steps?"""
    
    else:
        # Add some context from the prompt to make it seem more responsive
        words = prompt.split()
        if len(words) > 3:
            context = " ".join(words[:3]) + "..."
        else:
            context = prompt
        
        response = f"""Regarding '{context}':

{base_response}

{model_info.get(model, '')}

Is there anything specific about this topic you'd like me to address?"""
    
    # Add a disclaimer
    response += "\n\n(Note: This is a simulated response for demonstration purposes.)"
    
    return response

def calculate_cost(prompt, response, model, config):
    """Calculate approximate cost based on token count with improved estimation"""
    # More accurate estimation: 1 token ≈ 4 characters for English text
    prompt_chars = len(prompt)
    response_chars = len(response)
    
    # Adjust for different languages and special characters
    if any(ord(c) > 127 for c in prompt + response):  # Non-ASCII characters
        # Non-English languages often use more tokens per character
        estimated_prompt_tokens = prompt_chars / 3
        estimated_response_tokens = response_chars / 3
    else:
        estimated_prompt_tokens = prompt_chars / 4
        estimated_response_tokens = response_chars / 4
    
    # Different models have different pricing for prompt vs. completion tokens
    model_pricing = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
        "claude-2": {"prompt": 0.02, "completion": 0.025},
        "llama-2": {"prompt": 0.0008, "completion": 0.001},
        "mistral-7b": {"prompt": 0.0004, "completion": 0.0005}
    }
    
    # Use model-specific pricing if available, otherwise use the config
    if model in model_pricing:
        prompt_cost = (estimated_prompt_tokens / 1000) * model_pricing[model]["prompt"]
        completion_cost = (estimated_response_tokens / 1000) * model_pricing[model]["completion"]
        total_cost = prompt_cost + completion_cost
    else:
        # Fallback to config pricing
        cost_per_1k = config["models"][model]["cost_per_1k_tokens"]
        total_tokens = estimated_prompt_tokens + estimated_response_tokens
        total_cost = (total_tokens / 1000) * cost_per_1k
    
    return total_cost

def initialize_session_state():
    """Initialize all session state variables if they don't exist"""
    # Load configuration
    if "config" not in st.session_state:
        st.session_state.config = load_config()
    
    # Load personas
    if "personas" not in st.session_state:
        st.session_state.personas = load_personas()
    
    # Load sample prompts
    if "sample_prompts" not in st.session_state:
        st.session_state.sample_prompts = load_sample_prompts()
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    
    # Initialize current room
    if "current_room" not in st.session_state:
        st.session_state.current_room = "General Chat"
    
    # Initialize rooms with default personas
    if "rooms" not in st.session_state:
        st.session_state.rooms = {
            "General Chat": {
                "description": "General AI Assistant",
                "model": st.session_state.config["default_model"],
                "persona": "general",
                "messages": []
            },
            "HR Assistant": {
                "description": "Interview & Candidate Analysis AI",
                "model": st.session_state.config["default_model"],
                "persona": "hr_assistant",
                "messages": []
            },
            "Creative Writing": {
                "description": "Creative Writing & Storytelling Assistant",
                "model": st.session_state.config["default_model"],
                "persona": "creative_writer",
                "messages": []
            },
            "Tech Support": {
                "description": "Technical Support & Programming Assistant",
                "model": st.session_state.config["default_model"],
                "persona": "tech_expert",
                "messages": []
            }
        }
    
    # Initialize saved prompts
    if "saved_prompts" not in st.session_state:
        st.session_state.saved_prompts = []
    
    # Initialize total cost
    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0

def create_initial_files():
    """ Create initial JSON files if they don't exist"""
    # Create personas.json if it doesn't exist
    if not os.path.exists("personas.json"):
        save_personas(load_personas())
    
    # Create sample_prompts.json if it doesn't exist
    if not os.path.exists("sample_prompts.json"):
        save_sample_prompts(load_sample_prompts())
    
    # Create config.yaml if it doesn't exist
    if not os.path.exists("config.yaml"):
        save_config(load_config())