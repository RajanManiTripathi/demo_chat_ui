import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
from utils import simulate_ai_response, calculate_cost

# Set page configuration
st.set_page_config(
    page_title="Chat | AI Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for animations and styling
st.markdown("""
<style>
    /* Chat message animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* User message styling */
    div[style*="background-color: #e6f7e6"] {
        animation: slideInRight 0.3s ease-out;
        background: linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%) !important;
        border-radius: 1rem 1rem 0.25rem 1rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 4px solid #10b981;
    }
    
    /* AI message styling */
    div[style*="background-color: #f0f2f6"] {
        animation: slideInLeft 0.3s ease-out;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        border-radius: 1rem 1rem 1rem 0.25rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 4px solid #3b82f6;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        border-radius: 0.75rem;
        border: 2px solid #e5e7eb;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.2s;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Form submit button styling */
    button[kind="primaryFormSubmit"] {
        background-color: #3b82f6 !important;
    }
    
    button[kind="secondaryFormSubmit"] {
        background-color: #6b7280 !important;
        color: white !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1e3a8a;
        background-color: #f3f4f6;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 0.5rem;
    }
    
    /* Room info styling */
    .stCaption {
        background-color: #f3f4f6;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.title("AI Chat Assistant")
    
    # User profile section with avatar
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #3b82f6; 
                    display: flex; align-items: center; justify-content: center; margin-right: 10px;">
            <span style="color: white; font-weight: bold; font-size: 1.2rem;">
                {st.session_state.config['user_name'][0].upper()}
            </span>
        </div>
        <div>
            <div style="font-weight: bold; font-size: 1.1rem;">{st.session_state.config['user_name']}</div>
            <div style="font-size: 0.8rem; color: #6b7280;">Active User</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.subheader("Navigation")
    
    if st.button("🏠 Home"):
        switch_page("Home")
    
    if st.button("💬 Chat", disabled=True):
        pass
    
    if st.button("🚪 Rooms"):
        switch_page("Rooms")
    
    if st.button("⚙️ Settings"):
        switch_page("Settings")
    
    if st.button("🧠 Personas"):
        switch_page("Personas")
    
    if st.button("📝 Prompts"):
        switch_page("Prompts")
    
    # Room selection with enhanced UI
    st.subheader("Current Room")
    
    # Room selection with custom styling
    st.markdown("""
    <style>
        div[data-testid="stSelectbox"] > div:first-child {
            background-color: #f3f4f6;
            border-radius: 0.5rem;
            padding: 0.25rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    room_options = list(st.session_state.rooms.keys())
    selected_room = st.selectbox(
        "Select Room",
        room_options,
        index=room_options.index(st.session_state.current_room)
    )
    
    if selected_room != st.session_state.current_room:
        st.session_state.current_room = selected_room
        st.experimental_rerun()
    
    # Model selection for current room with icons
    current_model = st.session_state.rooms[st.session_state.current_room]["model"]
    model_options = list(st.session_state.config["models"].keys())
    
    # Model icons
    model_icons = {
        "gpt-4": "🧠",
        "gpt-3.5-turbo": "💬",
        "claude-2": "🤖",
        "llama-2": "🦙",
        "mistral-7b": "✨"
    }
    
    # Format function with icons
    def format_model(model_id):
        icon = model_icons.get(model_id, "🤖")
        return f"{icon} {st.session_state.config['models'][model_id]['name']}"
    
    selected_model = st.selectbox(
        "AI Model",
        model_options,
        index=model_options.index(current_model),
        format_func=format_model
    )
    
    if selected_model != current_model:
        st.session_state.rooms[st.session_state.current_room]["model"] = selected_model
    
    # Persona selection for current room with icons
    current_persona = st.session_state.rooms[st.session_state.current_room].get("persona", "general")
    persona_options = list(st.session_state.personas.keys())
    
    # Persona icons
    persona_icons = {
        "general": "🤖",
        "hr_assistant": "👔",
        "creative_writer": "✍️",
        "tech_expert": "💻"
    }
    
    # Add icons for other personas
    for persona in persona_options:
        if persona not in persona_icons:
            persona_icons[persona] = "🧠"
    
    # Format function with icons
    def format_persona(persona_id):
        icon = persona_icons.get(persona_id, "🧠")
        return f"{icon} {st.session_state.personas[persona_id]['name']}"
    
    selected_persona = st.selectbox(
        "AI Persona",
        persona_options,
        index=persona_options.index(current_persona) if current_persona in persona_options else 0,
        format_func=format_persona
    )
    
    if selected_persona != current_persona:
        st.session_state.rooms[st.session_state.current_room]["persona"] = selected_persona
    
    # Saved prompts with enhanced UI
    st.subheader("Saved Prompts")
    
    # Get prompts for the current persona
    current_persona = st.session_state.rooms[st.session_state.current_room].get("persona", "general")
    persona_prompts = st.session_state.sample_prompts.get(current_persona, [])
    user_saved_prompts = st.session_state.saved_prompts
    
    # Combine sample prompts and user saved prompts
    all_prompts = [""] + persona_prompts + user_saved_prompts
    
    saved_prompt = st.selectbox(
        "Select a prompt",
        all_prompts,
        format_func=lambda x: f"{x[:50]}..." if len(x) > 50 else x
    )
    
    if saved_prompt and st.button("Use Prompt", use_container_width=True):
        st.session_state.current_prompt = saved_prompt
        st.experimental_rerun()
    
    # Display total cost with enhanced styling
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1rem; background-color: #f3f4f6; border-radius: 0.5rem; 
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">TOTAL COST</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: #1e3a8a;">
            $<span id="cost-value">{:.4f}</span>
        </div>
    </div>
    """.format(st.session_state.total_cost), unsafe_allow_html=True)

# Main chat interface with enhanced styling
st.title(f"Chat: {st.session_state.current_room}")

# Get current room info
current_room_data = st.session_state.rooms[st.session_state.current_room]
current_persona = current_room_data.get("persona", "general")
persona_data = st.session_state.personas.get(current_persona, {"name": "Assistant", "description": "AI Assistant"})

# Display room description with persona info and enhanced styling
st.markdown(f"""
<div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
            padding: 1rem; border-radius: 0.75rem; margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <div style="display: flex; align-items: center;">
        <div style="font-size: 1.5rem; margin-right: 0.5rem;">{persona_icons.get(current_persona, "🧠")}</div>
        <div>
            <div style="font-weight: bold; font-size: 1.1rem;">{current_room_data['description']}</div>
            <div style="font-size: 0.9rem;">Using <span style="color: #1e3a8a; font-weight: 600;">{persona_data['name']}</span> persona</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Show persona information with enhanced styling
with st.expander(f"About {persona_data['name']}"):
    st.markdown(f"""
    <div style="background-color: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
        <div style="font-weight: bold; margin-bottom: 0.5rem;">Description:</div>
        <div>{persona_data['description']}</div>
    </div>
    
    <div style="background-color: #f9fafb; padding: 1rem; border-radius: 0.5rem;">
        <div style="font-weight: bold; margin-bottom: 0.5rem;">System Prompt:</div>
        <div style="font-family: monospace; background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; border-left: 3px solid #3b82f6;">
            {persona_data.get('system_prompt', 'No system prompt defined.')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialize current room's message history if empty
if not current_room_data.get("messages"):
    current_room_data["messages"] = []

# Display chat messages with enhanced styling
chat_container = st.container()

with chat_container:
    if not current_room_data["messages"]:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem; color: #6b7280; background-color: #f9fafb; 
                    border-radius: 0.75rem; margin: 2rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">No messages yet</div>
            <div>Start a conversation by typing a message below</div>
        </div>
        """, unsafe_allow_html=True)
    
    for i, message in enumerate(current_room_data["messages"]):
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; margin-bottom: 1.5rem; justify-content: flex-end;">
                <div style="max-width: 80%; background-color: #e6f7e6; padding: 1rem; border-radius: 1rem 1rem 0.25rem 1rem;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); animation-delay: {i * 0.1}s;">
                    <div style="font-weight: bold; margin-bottom: 0.5rem; display: flex; align-items: center;">
                        <div style="width: 24px; height: 24px; border-radius: 50%; background-color: #10b981; 
                                    display: flex; align-items: center; justify-content: center; margin-right: 8px;">
                            <span style="color: white; font-size: 0.8rem;">
                                {st.session_state.config['user_name'][0].upper()}
                            </span>
                        </div>
                        <span>You</span>
                    </div>
                    <div style="white-space: pre-wrap;">{message["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            model_name = st.session_state.config["models"][message.get("model", "gpt-3.5-turbo")]["name"]
            model_icon = model_icons.get(message.get("model", "gpt-3.5-turbo"), "🤖")
            persona_name = persona_data['name']
            persona_icon = persona_icons.get(current_persona, "🧠")
            
            st.markdown(f"""
            <div style="display: flex; margin-bottom: 1.5rem;">
                <div style="max-width: 80%; background-color: #f0f2f6; padding: 1rem; border-radius: 1rem 1rem 1rem 0.25rem;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); animation-delay: {i * 0.1}s;">
                    <div style="font-weight: bold; margin-bottom: 0.5rem; display: flex; align-items: center;">
                        <div style="width: 24px; height: 24px; border-radius: 50%; background-color: #3b82f6; 
                                    display: flex; align-items: center; justify-content: center; margin-right: 8px;">
                            <span style="color: white; font-size: 0.8rem;">
                                {persona_icon}
                            </span>
                        </div>
                        <span>{persona_name}</span>
                    </div>
                    <div style="white-space: pre-wrap;">{message["content"]}</div>
                    <div style="font-size: 0.8em; color: #6b7280; text-align: right; margin-top: 0.5rem;">
                        {model_icon} {model_name} | 
                        💰 ${message.get("cost", 0):.4f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Chat input with enhanced styling
st.divider()

# Use saved prompt if available
initial_prompt = ""
if "current_prompt" in st.session_state:
    initial_prompt = st.session_state.current_prompt
    del st.session_state.current_prompt

# Input form with enhanced styling
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Your message:", value=initial_prompt, height=100)
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        submit_button = st.form_submit_button("Send", use_container_width=True)
    
    with col2:
        save_prompt = st.form_submit_button("Save as Prompt", use_container_width=True)
    
    with col3:
        st.markdown("")  # Empty space for alignment

# Handle save prompt with toast notification
if save_prompt and user_input and user_input not in st.session_state.saved_prompts:
    st.session_state.saved_prompts.append(user_input)
    
    # Success message with enhanced styling
    st.markdown(f"""
    <div style="position: fixed; bottom: 20px; right: 20px; background-color: #10b981; color: white;
                padding: 1rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                animation: slideInRight 0.3s ease-out; z-index: 9999;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 1.2rem; margin-right: 0.5rem;">✅</div>
            <div>
                <div style="font-weight: bold;">Prompt Saved</div>
                <div style="font-size: 0.8rem;">{user_input[:30]}...</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)
    st.experimental_rerun()

# Handle chat submission with typing animation
if submit_button and user_input:
    # Add user message to chat
    current_room_data["messages"].append({
        "role": "user",
        "content": user_input
    })
    
    # Get current model and persona
    current_model = current_room_data["model"]
    current_persona = current_room_data.get("persona", "general")
    
    # Show typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown(f"""
    <div style="display: flex; margin-bottom: 1.5rem;">
        <div style="max-width: 80%; background-color: #f0f2f6; padding: 1rem; border-radius: 1rem 1rem 1rem 0.25rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="font-weight: bold; margin-bottom: 0.5rem; display: flex; align-items: center;">
                <div style="width: 24px; height: 24px; border-radius: 50%; background-color: #3b82f6; 
                            display: flex; align-items: center; justify-content: center; margin-right: 8px;">
                    <span style="color: white; font-size: 0.8rem;">
                        {persona_icons.get(current_persona, "🧠")}
                    </span>
                </div>
                <span>{st.session_state.personas[current_persona]['name']}</span>
            </div>
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    
    <style>
    .typing-indicator {
        display: flex;
        align-items: center;
    }
    .typing-indicator span {
        height: 10px;
        width: 10px;
        margin: 0 2px;
        background-color: #3b82f6;
        border-radius: 50%;
        display: inline-block;
        opacity: 0.4;
        animation: typing 1s infinite;
    }
    .typing-indicator span:nth-child(1) { animation-delay: 0s; }
    .typing- ing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        0% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2 ); }
        100% { opacity: 0.4; transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Generate AI response
    ai_response = simulate_ai_response(user_input, current_model, current_persona)
    
    # Calculate cost
    message_cost = calculate_cost(user_input, ai_response, current_model, st.session_state.config)
    st.session_state.total_cost += message_cost
    
    # Remove typing indicator
    typing_placeholder.empty()
    
    # Add AI response to chat
    current_room_data["messages"].append({
        "role": "assistant",
        "content": ai_response,
        "model": current_model,
        "persona": current_persona,
        "cost": message_cost
    })
    
    # Rerun to update the UI
    st.experimental_rerun()

# Chat controls with enhanced styling
col1, col2 = st.columns(2)

with col1:
    if st.button("Clear Chat", use_container_width=True):
        # Confirmation dialog using HTML/CSS
        st.markdown("""
        <div id="confirmation-dialog" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                    background-color: rgba(0,0,0,0.5); z-index: 9999; justify-content: center; align-items: center;">
            <div style="background-color: white; padding: 2rem; border-radius: 0.5rem; max-width: 400px; text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 1rem;">⚠️</div>
                <div style="font-weight: bold; font-size: 1.2rem; margin-bottom: 1rem;">Clear Chat History?</div>
                <div style="margin-bottom: 1.5rem;">This will delete all messages in this room. This action cannot be undone.</div>
                <div style="display: flex; justify-content: space-between;">
                    <button id="cancel-clear" style="padding: 0.5rem 1rem; border-radius: 0.25rem; border: 1px solid #e5e7eb; 
                                                    background-color: white; cursor: pointer;">
                        Cancel
                    </button>
                    <button id="confirm-clear" style="padding: 0.5rem 1rem; border-radius: 0.25rem; border: none; 
                                                     background-color: #ef4444; color: white; cursor: pointer;">
                        Clear Chat
                    </button>
                </div>
            </div>
        </div>
        
        <script>
            // Show confirmation dialog
            document.getElementById('confirmation-dialog').style.display = 'flex';
            
            // Handle cancel button
            document.getElementById('cancel-clear').addEventListener('click', function() {
                document.getElementById('confirmation-dialog').style.display = 'none';
            });
            
            // Handle confirm button
            document.getElementById('confirm-clear').addEventListener('click', function() {
                // Submit a form to clear the chat
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'clear_chat';
                input.value = 'true';
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            });
        </script>
        """, unsafe_allow_html=True)
        
        current_room_data["messages"] = []
        st.experimental_rerun()

with col2:
    if st.button("Export Conversation", use_container_width=True):
        # In a real app, this would generate a downloadable file
        st.info("In a production app, this would export the current conversation to a file.")
        
        # Show export options dialog
        st.markdown("""
        <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
            <div style="font-weight: bold; margin-bottom: 0.5rem;">Export Options</div>
            <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                <button style="padding: 0.5rem 1rem; border-radius: 0.25rem; border: none; 
                               background-color: #3b82f6; color: white; cursor: pointer; flex: 1;">
                    Export as PDF
                </button>
                <button style="padding: 0.5rem 1rem; border-radius: 0.25rem; border: none; 
                               background-color: #3b82f6; color: white; cursor: pointer; flex: 1;">
                    Export as Markdown
                </button>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <button style="padding: 0.5rem 1rem; border-radius: 0.25rem; border: none; 
                               background-color: #3b82f6; color: white; cursor: pointer; flex: 1;">
                    Export as JSON
                </button>
                <button style="padding: 0.5rem 1rem; border-radius: 0.25rem; border: none; 
                               background-color: #3b82f6; color: white; cursor: pointer; flex: 1;">
                    Export as Text
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)