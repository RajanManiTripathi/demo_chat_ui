import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
from utils import save_personas

# Set page configuration
st.set_page_config(
    page_title="Personas | AI Chat Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation
with st.sidebar:
    st.title("AI Chat Assistant")
    
    # User profile section
    st.subheader(f"Profile: {st.session_state.config['user_name']}")
    
    # Navigation
    st.subheader("Navigation")
    
    if st.button("🏠 Home"):
        switch_page("Home")
    
    if st.button("💬 Chat"):
        switch_page("Chat")
    
    if st.button("🚪 Rooms"):
        switch_page("Rooms")
    
    if st.button("⚙️ Settings"):
        switch_page("Settings")
    
    if st.button("🧠 Personas", disabled=True):
        pass
    
    if st.button("📝 Prompts"):
        switch_page("Prompts")
    
    # Display total cost
    st.sidebar.metric("Total Cost", f"${st.session_state.total_cost:.4f}")

# Main content
st.title("AI Assistant Personas")
st.markdown("""
Create and manage different AI assistant personalities. Each persona has its own characteristics, 
system prompt, and sample responses that define how the AI will interact with you.
""")

# Display existing personas
st.subheader("Available Personas")

# Create tabs for viewing and editing personas
persona_tabs = st.tabs(["View Personas", "Edit Personas", "Create New Persona"])

with persona_tabs[0]:  # View Personas
    # Create columns for persona cards
    cols = st.columns(2)
    
    for i, (persona_id, persona_data) in enumerate(st.session_state.personas.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(persona_data["name"])
                st.caption(persona_data["description"])
                
                # System prompt
                with st.expander("System Prompt"):
                    st.markdown(persona_data.get("system_prompt", "No system prompt defined."))
                
                # Sample responses
                with st.expander("Sample Responses"):
                    for j, response in enumerate(persona_data.get("sample_responses", [])):
                        st.markdown(f"{j+1}. {response}")
                
                # Show which rooms use this persona
                rooms_using_persona = []
                for room_name, room_data in st.session_state.rooms.items():
                    if room_data.get("persona") == persona_id:
                        rooms_using_persona.append(room_name)
                
                if rooms_using_persona:
                    st.markdown("**Used in rooms:**")
                    for room in rooms_using_persona:
                        st.markdown(f"- {room}")
                else:
                    st.markdown("**Not currently used in any room**")

with persona_tabs[1]:  # Edit Personas
    # Select persona to edit
    persona_options = list(st.session_state.personas.keys())
    selected_persona_id = st.selectbox(
        "Select Persona to Edit",
        persona_options,
        format_func=lambda x: st.session_state.personas[x]["name"]
    )
    
    selected_persona = st.session_state.personas[selected_persona_id]
    
    # Edit form
    with st.form("edit_persona_form"):
        edited_name = st.text_input("Persona Name", value=selected_persona["name"])
        edited_description = st.text_area("Description", value=selected_persona["description"])
        edited_system_prompt = st.text_area("System Prompt", value=selected_persona.get("system_prompt", ""))
        
        # Sample responses
        st.subheader("Sample Responses")
        st.markdown("Enter one response per line. These will be used to simulate AI responses.")
        
        sample_responses_text = "\n".join(selected_persona.get("sample_responses", []))
        edited_sample_responses = st.text_area("Sample Responses", value=sample_responses_text, height=200)
        
        # Process sample responses into a list
        sample_responses_list = [resp.strip() for resp in edited_sample_responses.split("\n") if resp.strip()]
        
        # Submit button
        submit_button = st.form_submit_button("Save Changes")
        
        if submit_button:
            # Update persona data
            st.session_state.personas[selected_persona_id] = {
                "name": edited_name,
                "description": edited_description,
                "system_prompt": edited_system_prompt,
                "sample_responses": sample_responses_list
            }
            
            # Save to file
            save_personas(st.session_state.personas)
            
            st.success(f"Persona '{edited_name}' updated successfully!")
    
    # Delete persona button (outside the form)
    if st.button("Delete Persona", disabled=selected_persona_id in ["general", "hr_assistant", "creative_writer", "tech_expert"]):
        # Check if persona is in use
        in_use = False
        for room_data in st.session_state.rooms.values():
            if room_data.get("persona") == selected_persona_id:
                in_use = True
                break
        
        if in_use:
            st.error("Cannot delete this persona because it is currently in use by one or more rooms.")
        else:
            # Delete the persona
            del st.session_state.personas[selected_persona_id]
            
            # Save to file
            save_personas(st.session_state.personas)
            
            st.success(f"Persona '{selected_persona['name']}' deleted successfully!")
            st.experimental_rerun()

with persona_tabs[2]:  # Create New Persona
    with st.form("new_persona_form"):
        st.subheader("Create New Persona")
        
        new_persona_id = st.text_input("Persona ID (lowercase, no spaces)", 
                                       help="This is used internally. Use lowercase letters, numbers, and underscores only.")
        new_persona_name = st.text_input("Persona Name", 
                                         help="Display name for the persona")
        new_persona_description = st.text_area("Description", 
                                              help="Brief description of the persona's capabilities and personality")
        new_persona_system_prompt = st.text_area("System Prompt", 
                                                help="Instructions that define how the AI should behave")
        
        # Sample responses
        st.subheader("Sample Responses")
        st.markdown("Enter one response per line. These will be used to simulate AI responses.")
        new_sample_responses = st.text_area("Sample Responses", height=200)
        
        # Process sample responses into a list
        sample_responses_list = [resp.strip() for resp in new_sample_responses.split("\n") if resp.strip()]
        
        # Submit button
        submit_button = st.form_submit_button("Create Persona")
        
        if submit_button:
            if not new_persona_id or not new_persona_name:
                st.error("Persona ID and Name are required!")
            elif new_persona_id in st.session_state.personas:
                st.error(f"Persona ID '{new_persona_id}' already exists!")
            else:
                # Create new persona
                st.session_state.personas[new_persona_id] = {
                    "name": new_persona_name,
                    "description": new_persona_description,
                    "system_prompt": new_persona_system_prompt,
                    "sample_responses": sample_responses_list
                }
                
                # Save to file
                save_personas(st.session_state.personas)
                
                st.success(f"Persona '{new_persona_name}' created successfully!")
                st.experimental_rerun()

# Persona templates
st.divider()
st.subheader("Persona Templates")
st.markdown("Quick-start with pre-configured persona templates for specific use cases.")

# Create columns for template cards
template_cols = st.columns(3)

templates = [
    {
        "id": "customer_support",
        "name": "Customer Support Agent",
        "description": "Helpful, patient assistant for customer service",
        "system_prompt": "You are a customer support agent. Be helpful, patient, and solution-oriented. Address customer concerns professionally and empathetically.",
        "sample_responses": [
            "I understand your concern. Let me help you resolve this issue.",
            "I apologize for the inconvenience. Here's what we can do to fix this situation.",
            "Thank you for bringing this to our attention. Let me check what options are available."
        ]
    },
    {
        "id": "data_analyst",
        "name": "Data Analyst",
        "description": "Analytical assistant for data interpretation",
        "system_prompt": "You are a data analyst assistant. Help interpret data, explain statistical concepts, and provide insights based on information provided.",
        "sample_responses": [
            "Based on this data, the key trends indicate...",
            "From a statistical perspective, these results suggest...",
            "When analyzing these numbers, it's important to consider..."
        ]
    },
    {
        "id": "language_tutor",
        "name": "Language Tutor",
        "description": "Educational assistant for language learning",
        "system_prompt": "You are a language tutor. Help users learn new languages, explain grammar rules, provide examples, and correct mistakes in a supportive way.",
        "sample_responses": [
            "That's almost correct! Here's a small correction and explanation...",
            "Here's how you would say that in the target language...",
            "This grammar rule works as follows, with these examples..."
        ]
    }
]

for i, template in enumerate(templates):
    with template_cols[i % 3]:
        with st.container(border=True):
            st.subheader(template["name"])
            st.caption(template["description"])
            
            with st.expander("System Prompt"):
                st.markdown(template["system_prompt"])
            
            # Button to create from template
            if st.button(f"Use Template", key=f"template_{i}", use_container_width=True):
                # Check if persona already exists
                template_id = template["id"]
                counter = 1
                while template_id in st.session_state.personas:
                    template_id = f"{template['id']}_{counter}"
                    counter += 1
                
                # Create the persona
                st.session_state.personas[template_id] = {
                    "name": template["name"],
                    "description": template["description"],
                    "system_prompt": template["system_prompt"],
                    "sample_responses": template["sample_responses"]
                }
                
                # Save to file
                save_personas(st.session_state.personas)
                
                st.success(f"Persona '{template['name']}' created from template!")
                st.experimental_rerun()