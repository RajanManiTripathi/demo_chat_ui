import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(
    page_title="Rooms | AI Chat Assistant",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for animations and styling
st.markdown("""
<style>
    /* Card animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Room card styling */
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid rgba(49, 51, 63, 0.2)"] {
        animation: fadeInUp 0.5s ease-out;
        border: none !important;
        background: white;
        border-radius: 0.75rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s, box-shadow 0.2s;
        overflow: hidden;
    }
    
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid rgba(49, 51, 63, 0.2)"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Room card header */
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid rgba(49, 51, 63, 0.2)"] > div:first-child {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        margin: -1rem -1rem 1rem -1rem;
        padding: 1rem;
    }
    
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid rgba(49, 51, 63, 0.2)"] > div:first-child > div > div > p {
        color: white !important;
        font-weight: bold;
    }
    
    /* Room card caption */
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid rgba(49, 51, 63, 0.2)"] > div:nth-child(2) > div > div > p {
        color: #6b7280 !important;
    }
    
    /* Info box styling */
    div[role="alert"] {
        border: none !important;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background-color: #f3f4f6;
        padding: 0.75rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
    
    /* Form styling */
    [data-testid="stForm"] {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Template card styling */
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid rgba(49, 51, 63, 0.2)"] {
        height: 100%;
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
    
    if st.button("💬 Chat"):
        switch_page("Chat")
    
    if st.button("🚪 Rooms", disabled=True):
        pass
    
    if st.button("⚙️ Settings"):
        switch_page("Settings")
    
    if st.button("🧠 Personas"):
        switch_page("Personas")
    
    if st.button("📝 Prompts"):
        switch_page("Prompts")
    
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

# Main content with enhanced styling
st.title("Chat Rooms")

# Hero section with animation
st.markdown("""
<div style="animation: fadeInUp 0.5s ease-out;">
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 2rem; 
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
        <h2 style="color: white; margin-bottom: 0.5rem; font-size: 1.5rem;">
            Organize Your AI Conversations
        </h2>
        <p style="color: white; opacity: 0.9;">
            Create specialized chat rooms for different topics, each with its own AI model, persona, and conversation history.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Display existing rooms with enhanced styling
st.subheader("Available Rooms")

# Create columns for room cards
cols = st.columns(2)

# Room icons based on name
room_icons = {
    "General Chat": "💬",
    "HR Assistant": "👔",
    "Creative Writing": "✍️",
    "Tech Support": "💻",
    "Customer Support": "🎧",
    "Code Assistant": "👨‍💻",
    "Content Creation": "📝"
}

# Default icon for other rooms
default_icon = "🚪"

# Add animation delay for staggered appearance
for i, (room_name, room_data) in enumerate(st.session_state.rooms.items()):
    with cols[i % 2]:
        # Get room icon
        room_icon = room_icons.get(room_name, default_icon)
        
        # Get model and persona info
        model_name = st.session_state.config["models"][room_data["model"]]["name"]
        persona_key = room_data.get("persona", "general")
        persona_name = st.session_state.personas[persona_key]["name"] if persona_key in st.session_state.personas else "General Assistant"
        
        # Message count
        message_count = len(room_data.get("messages", []))
        
        # Custom styling for each room card
        st.markdown(f"""
        <div style="animation: fadeInUp 0.5s ease-out; animation-delay: {i * 0.1}s; opacity: 0; animation-fill-mode: forwards;
                    background: white; border-radius: 0.75rem; overflow: hidden; margin-bottom: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    transition: transform 0.2s, box-shadow 0.2s;">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 1.5rem; display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">{room_icon}</div>
                <div>
                    <div style="color: white; font-weight: bold; font-size: 1.2rem;">{room_name}</div>
                    <div style="color: white; opacity: 0.9; font-size: 0.9rem;">{room_data["description"]}</div>
                </div>
            </div>
            
            <div style="padding: 1.5rem;">
                <div style="display: flex; margin-bottom: 1rem;">
                    <div style="flex: 1; background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.5rem; margin-right: 0.5rem;">
                        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">MODEL</div>
                        <div style="font-weight: bold;">{model_name}</div>
                    </div>
                    <div style="flex: 1; background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.5rem;">
                        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">PERSONA</div>
                        <div style="font-weight: bold;">{persona_name}</div>
                    </div>
                </div>
                
                <div style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 1rem; text-align: center;">
                    <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">MESSAGES</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #1e3a8a;">{message_count}</div>
                </div>
                
                <div style="display: flex; gap: 0.5rem;">
                    <button onclick="enterRoom('{room_name}')" style="flex: 1; padding: 0.75rem; border: none; border-radius: 0.5rem; 
                                                                      background-color: #3b82f6; color: white; font-weight: 600;
                                                                      cursor: pointer; transition: all 0.2s;">
                        Enter Room
                    </button>
                    <button onclick="deleteRoom('{room_name}')" 
                            style="flex: 1; padding: 0.75rem; border: none; border-radius: 0.5rem; 
                                   background-color: {('#ef4444' if room_name not in ['General Chat', 'HR Assistant', 'Creative Writing', 'Tech Support'] else '#9ca3af')}; 
                                   color: white; font-weight: 600; cursor: pointer; transition: all 0.2s;
                                   {('opacity: 0.5; cursor: not-allowed;' if room_name in ['General Chat', 'HR Assistant', 'Creative Writing', 'Tech Support'] else '')}">
                        Delete Room
                    </button>
                </div>
            </div>
        </div>
        
        <script>
            function enterRoom(roomName) {{
                // Submit a form to enter the room
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'enter_room';
                input.value = roomName;
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }}
            
            function deleteRoom(roomName) {{
                // Check if room is a default room
                if (['General Chat', 'HR Assistant', 'Creative Writing', 'Tech Support'].includes(roomName)) {{
                    return;
                }}
                
                // Submit a form to delete the room
                if (confirm('Are you sure you want to delete this room? This action cannot be undone.')) {{
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = '';
                    
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'delete_room';
                    input.value = roomName;
                    
                    form.appendChild(input);
                    document.body.appendChild(form);
                    form.submit();
                }}
            }}
        </script>
        """, unsafe_allow_html=True)
        
        # Handle room actions with hidden buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Enter {room_name}", key=f"enter_{room_name}", use_container_width=True):
                st.session_state.current_room = room_name
                switch_page("Chat")
        
        with col2:
            if st.button(f"Delete {room_name}", key=f"delete_{room_name}", use_container_width=True, disabled=room_name in ["General Chat", "HR Assistant", "Creative Writing", "Tech Support"]):
                if room_name == st.session_state.current_room:
                    st.session_state.current_room = "General Chat"
                del st.session_state.rooms[room_name]
                st.success(f"Room '{room_name}' deleted!")
                st.experimental_rerun()

# Create new room with enhanced styling
st.divider()
st.subheader("Create New Room")

with st.form("new_room_form"):
    st.markdown("""
    <div style="margin-bottom: 1rem; padding: 1rem; background-color: #f3f4f6; border-radius: 0.5rem;">
        <div style="font-weight: bold; margin-bottom: 0.5rem;">Create a New Chat Room</div>
        <div style="color: #6b7280; font-size: 0.9rem;">
            Each room maintains its own conversation history and can use different AI models and personas.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    new_room_name = st.text_input("Room Name")
    new_room_description = st.text_input("Description")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
        
        new_room_model = st.selectbox(
            "Default AI Model",
            model_options,
            format_func=format_model
        )
    
    with col2:
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
        
        new_room_persona = st.selectbox(
            "Default AI Persona",
            persona_options,
            format_func=format_persona
        )
    
    submit_button = st.form_submit_button("Create Room")
    
    if submit_button and new_room_name and new_room_name not in st.session_state.rooms:
        st.session_state.rooms[new_room_name] = {
            "description": new_room_description,
            "model": new_room_model,
            "persona": new_room_persona,
            "messages": []
        }
        st.success(f"Room '{new_room_name}' created!")
        st.experimental_rerun()

# Room templates with enhanced styling
st.divider()
st.subheader("Room Templates")

st.markdown("""
<div style="margin-bottom: 1.5rem; padding: 1rem; background-color: #f3f4f6; border-radius: 0.5rem;">
    <div style="font-weight: bold; margin-bottom: 0.5rem;">Quick-Start Templates</div>
    <div style="color: #6b7280; font-size: 0.9rem;">
        Get started quickly with pre-configured room templates for specific use cases.
    </div>
</div>
""", unsafe_allow_html=True)

# Create columns for template cards
template_cols = st.columns(3)

templates = [
    {
        "name": "Customer Support",
        "description": "Handle customer inquiries and support requests",
        "model": "gpt-3.5-turbo",
        "persona": "general",
        "icon": "🎧",
        "color": "emerald"
    },
    {
        "name": "Code Assistant",
        "description": "Help with programming and technical questions",
        "model": "gpt-4",
        "persona": "tech_expert",
        "icon": "👨‍💻",
        "color": "blue"
    },
    {
        "name": "Content Creation",
        "description": "Generate creative content and marketing copy",
        "model": "claude-2",
        "persona": "creative_writer",
        "icon": "📝",
        "color": "purple"
    }
]

# Color gradients for templates
color_gradients = {
    "emerald": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
    "blue": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
    "purple": "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)"
}

for i, template in enumerate(templates):
    with template_cols[i % 3]:
        # Get model and persona info
        model_name = st.session_state.config["models"][template["model"]]["name"]
        persona_name = st.session_state.personas[template["persona"]]["name"]
        
        # Custom styling for each template card
        st.markdown(f"""
        <div style="animation: fadeInUp 0.5s ease-out; animation-delay: {i * 0.1 + 0.3}s; opacity: 0; animation-fill-mode: forwards;
                    background: white; border-radius: 0.75rem; overflow: hidden; height: 100%;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    transition: transform 0.2s, box-shadow 0.2s;">
            <div style="background: {color_gradients[template['color']]}; padding: 1.5rem; display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">{template["icon"]}</div>
                <div>
                    <div style="color: white; font-weight: bold; font-size: 1.2rem;">{template["name"]}</div>
                    <div style="color: white; opacity: 0.9; font-size: 0.9rem;">{template["description"]}</div>
                </div>
            </div>
            
            <div style="padding: 1.5rem;">
                <div style="display: flex; margin-bottom: 1rem;">
                    <div style="flex: 1; background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.5rem; margin-right: 0.5rem;">
                        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">MODEL</div>
                        <div style="font-weight: bold;">{model_name}</div>
                    </div>
                    <div style="flex: 1; background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.5rem;">
                        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">PERSONA</div>
                        <div style="font-weight: bold;">{persona_name}</div>
                    </div>
                </div>
                
                <button onclick="createTemplate('{template['name']}', '{template['description']}', '{template['model']}', '{template['persona']}')" 
                        style="width: 100%; padding: 0.75rem; border: none; border-radius: 0.5rem; 
                               background-color: #3b82f6; color: white; font-weight: 600;
                               cursor: pointer; transition: all 0.2s;">
                    Create Room
                </button>
            </div>
        </div>
        
        <script>
            function createTemplate(name, description, model, persona) {{
                // Submit a form to create the room from template
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '';
                
                const nameInput = document.createElement('input');
                nameInput.type = 'hidden';
                nameInput.name = 'template_name';
                nameInput.value = name;
                
                const descInput = document.createElement('input');
                descInput.type = 'hidden';
                descInput.name = 'template_description';
                descInput.value = description;
                
                const modelInput = document.createElement('input');
                modelInput.type = 'hidden';
                modelInput.name = 'template_model';
                modelInput.value = model;
                
                const personaInput = document.createElement('input');
                personaInput.type = 'hidden';
                personaInput.name = 'template_persona';
                personaInput.value = persona;
                
                form.appendChild(nameInput);
                form.appendChild(descInput);
                form.appendChild(modelInput);
                form.appendChild(personaInput);
                document.body.appendChild(form);
                form.submit();
            }}
        </script>
        """, unsafe_allow_html=True)
        
        # Button to create from template (hidden, used by JavaScript)
        if st.button(f"Create {template['name']} Room", key=f"template_{i}", use_container_width=True):
            # Check if room already exists
            new_name = template["name"]
            counter = 1
            while new_name in st.session_state.rooms:
                new_name = f"{template['name']} {counter}"
                counter += 1
            
            # Create the room
            st.session_state.rooms[new_name] = {
                "description": template["description"],
                "model": template["model"],
                "persona": template["persona"],
                "messages": []
            }
            st.success(f"Room '{new_name}' created from template!")
            st.experimental_rerun()