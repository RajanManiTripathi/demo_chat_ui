import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
from utils import save_sample_prompts

# Set page configuration
st.set_page_config(
    page_title="Prompts | AI Chat Assistant",
    page_icon="📝",
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
    
    if st.button("🧠 Personas"):
        switch_page("Personas")
    
    if st.button("📝 Prompts", disabled=True):
        pass
    
    # Display total cost
    st.sidebar.metric("Total Cost", f"${st.session_state.total_cost:.4f}")

# Main content
st.title("Prompt Library")
st.markdown("""
Manage your collection of prompts organized by category. These prompts can be quickly accessed 
during chat sessions to help you get the most out of your AI assistant.
""")

# Create tabs for different prompt categories
prompt_categories = list(st.session_state.sample_prompts.keys())
prompt_tabs = st.tabs(prompt_categories + ["User Saved", "Add Category"])

# Display prompts by category
for i, category in enumerate(prompt_categories):
    with prompt_tabs[i]:
        st.subheader(f"{category.replace('_', ' ').title()} Prompts")
        
        # Get prompts for this category
        category_prompts = st.session_state.sample_prompts[category]
        
        # Display each prompt with options to use or edit
        for j, prompt in enumerate(category_prompts):
            with st.container(border=True):
                st.markdown(f"**Prompt {j+1}:**")
                st.markdown(prompt)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("Use in Chat", key=f"use_{category}_{j}", use_container_width=True):
                        st.session_state.current_prompt = prompt
                        switch_page("Chat")
                
                with col2:
                    if st.button("Edit", key=f"edit_{category}_{j}", use_container_width=True):
                        st.session_state.editing_prompt = {
                            "category": category,
                            "index": j,
                            "text": prompt
                        }
                        st.experimental_rerun()
                
                with col3:
                    if st.button("Delete", key=f"delete_{category}_{j}", use_container_width=True):
                        st.session_state.sample_prompts[category].pop(j)
                        save_sample_prompts(st.session_state.sample_prompts)
                        st.success(f"Prompt deleted from {category}!")
                        st.experimental_rerun()
        
        # Add new prompt to this category
        st.divider()
        st.subheader(f"Add New Prompt to {category.replace('_', ' ').title()}")
        
        with st.form(key=f"add_prompt_{category}"):
            new_prompt = st.text_area("Enter new prompt:", height=100)
            submit = st.form_submit_button("Add Prompt")
            
            if submit and new_prompt:
                st.session_state.sample_prompts[category].append(new_prompt)
                save_sample_prompts(st.session_state.sample_prompts)
                st.success(f"Prompt added to {category}!")
                st.experimental_rerun()
        
        # Edit prompt if in editing mode
        if hasattr(st.session_state, "editing_prompt") and st.session_state.editing_prompt["category"] == category:
            st.divider()
            st.subheader("Edit Prompt")
            
            with st.form(key=f"edit_prompt_{category}"):
                edited_prompt = st.text_area("Edit prompt:", value=st.session_state.editing_prompt["text"], height=100)
                col1, col2 = st.columns(2)
                
                with col1:
                    save_edit = st.form_submit_button("Save Changes")
                
                with col2:
                    cancel_edit = st.form_submit_button("Cancel")
                
                if save_edit and edited_prompt:
                    index = st.session_state.editing_prompt["index"]
                    st.session_state.sample_prompts[category][index] = edited_prompt
                    save_sample_prompts(st.session_state.sample_prompts)
                    del st.session_state.editing_prompt
                    st.success("Prompt updated!")
                    st.experimental_rerun()
                
                if cancel_edit:
                    del st.session_state.editing_prompt
                    st.experimental_rerun()

# User saved prompts tab
with prompt_tabs[len(prompt_categories)]:
    st.subheader("Your Saved Prompts")
    
    if not st.session_state.saved_prompts:
        st.info("You haven't saved any prompts yet. You can save prompts during chat by clicking 'Save as Prompt'.")
    
    # Display each saved prompt
    for j, prompt in enumerate(st.session_state.saved_prompts):
        with st.container(border=True):
            st.markdown(f"**Prompt {j+1}:**")
            st.markdown(prompt)
            
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if st.button("Use in Chat", key=f"use_saved_{j}", use_container_width=True):
                    st.session_state.current_prompt = prompt
                    switch_page("Chat")
            
            with col2:
                if st.button("Edit", key=f"edit_saved_{j}", use_container_width=True):
                    st.session_state.editing_saved_prompt = {
                        "index": j,
                        "text": prompt
                    }
                    st.experimental_rerun()
            
            with col3:
                # Add to category dropdown
                categories = list(st.session_state.sample_prompts.keys())
                selected_category = st.selectbox("", categories, key=f"cat_select_{j}")
            
            with col4:
                if st.button("Add to Category", key=f"add_to_cat_{j}", use_container_width=True):
                    st.session_state.sample_prompts[selected_category].append(prompt)
                    save_sample_prompts(st.session_state.sample_prompts)
                    st.success(f"Prompt added to {selected_category}!")
            
            # Delete button in a new row
            if st.button("Delete", key=f"delete_saved_{j}", use_container_width=True):
                st.session_state.saved_prompts.pop(j)
                st.success("Prompt deleted!")
                st.experimental_rerun()
    
    # Edit saved prompt if in editing mode
    if hasattr(st.session_state, "editing_saved_prompt"):
        st.divider()
        st.subheader("Edit Saved Prompt")
        
        with st.form(key="edit_saved_prompt"):
            edited_prompt = st.text_area("Edit prompt:", value=st.session_state.editing_saved_prompt["text"], height=100)
            col1, col2 = st.columns(2)
            
            with col1:
                save_edit = st.form_submit_button("Save Changes")
            
            with col2:
                cancel_edit = st.form_submit_button("Cancel")
            
            if save_edit and edited_prompt:
                index = st.session_state.editing_saved_prompt["index"]
                st.session_state.saved_prompts[index] = edited_prompt
                del st.session_state.editing_saved_prompt
                st.success("Prompt updated!")
                st.experimental_rerun()
            
            if cancel_edit:
                del st.session_state.editing_saved_prompt
                st.experimental_rerun()

# Add category tab
with prompt_tabs[len(prompt_categories) + 1]:
    st.subheader("Add New Prompt Category")
    
    with st.form(key="add_category"):
        new_category = st.text_input("Category Name (lowercase, no spaces):", 
                                    help="Use lowercase letters, numbers, and underscores only.")
        new_category_display = st.text_input("Display Name:", 
                                           help="How the category will be displayed in the UI.")
        
        # Initial prompts
        st.subheader("Initial Prompts")
        st.markdown("Enter one prompt per line. These will be the starting prompts for this category.")
        initial_prompts = st.text_area("Initial Prompts:", height=200)
        
        # Process prompts into a list
        prompts_list = [prompt.strip() for prompt in initial_prompts.split("\n") if prompt.strip()]
        
        submit = st.form_submit_button("Create Category")
        
        if submit:
            if not new_category or not new_category_display:
                st.error("Category ID and Display Name are required!")
            elif new_category in st.session_state.sample_prompts:
                st.error(f"Category '{new_category}' already exists!")
            else:
                # Create new category
                st.session_state.sample_prompts[new_category] = prompts_list
                save_sample_prompts(st.session_state.sample_prompts)
                st.success(f"Category '{new_category_display}' created successfully!")
                st.experimental_rerun()

# Prompt templates
st.divider()
st.subheader("Prompt Templates by Task")
st.markdown("Quick-access templates for common AI tasks.")

# Create columns for template categories
template_cols = st.columns(3)

template_categories = [
    {
        "name": "Content Creation",
        "prompts": [
            "Write a blog post about [topic] that is engaging and informative.",
            "Create a social media caption for a photo of [subject].",
            "Generate 5 creative headlines for an article about [topic]."
        ]
    },
    {
        "name": "Programming Help",
        "prompts": [
            "Explain how to implement [feature] in [programming language].",
            "Debug this code: [paste code here]",
            "Write a function that [describe functionality] in [programming language]."
        ]
    },
    {
        "name": "Learning & Education",
        "prompts": [
            "Explain [complex topic] in simple terms as if I'm 10 years old.",
            "Create a study guide for [subject] with key concepts and examples.",
            "What are the main arguments for and against [controversial topic]?"
        ]
    }
]

for i, category in enumerate(template_categories):
    with template_cols[i]:
        with st.container(border=True):
            st.subheader(category["name"])
            
            for prompt in category["prompts"]:
                st.markdown(f"- {prompt}")
            
            if st.button(f"Use {category['name']} Templates", key=f"use_template_{i}", use_container_width=True):
                # Check if category exists
                category_id = category["name"].lower().replace(" ", "_")
                
                if category_id not in st.session_state.sample_prompts:
                    st.session_state.sample_prompts[category_id] = category["prompts"]
                else:
                    # Add prompts that don't already exist
                    for prompt in category["prompts"]:
                        if prompt not in st.session_state.sample_prompts[category_id]:
                            st.session_state.sample_prompts[category_id].append(prompt)
                
                save_sample_prompts(st.session_state.sample_prompts)
                st.success(f"Added {category['name']} templates to your prompt library!")
                st.experimental_rerun()