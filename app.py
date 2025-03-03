import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import yaml
import os
from utils import initialize_session_state, create_initial_files

# Set page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create initial files
create_initial_files()

# Initialize session state
initialize_session_state()

# Apply custom CSS
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Card styling */
    div[data-testid="stVerticalBlock"] div[style*="border-radius: 0.5rem"] {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    div[data-testid="stVerticalBlock"] div[style*="border-radius: 0.5rem"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 0.375rem;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat message styling */
    div[style*="background-color: #e6f7e6"] {
        border-radius: 1rem 1rem 1rem 0.25rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s;
    }
    
    div[style*="background-color: #f0f2f6"] {
        border-radius: 1rem 1rem 0.25rem 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 0.75rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #1e3a8a;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1e3a8a;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        h1, h2, h3, .streamlit-expanderHeader {
            color: #93c5fd;
        }
        
        [data-testid="stMetric"] {
            background-color: #1f2937;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation with enhanced styling
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
    
    # Navigation with icons and hover effects
    st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div.nav-button {
            margin-bottom: 0.5rem;
            transition: all 0.2s;
        }
        div[data-testid="stVerticalBlock"] > div.nav-button:hover {
            transform: translateX(5px);
        }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    if st.button("📝 Prompts"):
        switch_page("Prompts")
    
    # Display total cost with enhanced styling
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1rem; background-color: #f3f4f6; border-radius: 0.5rem; 
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.25rem;">TOTAL COST</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: #1e3a8a;">
            $<span id="cost-value">{st.session_state.total_cost:.4f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content - Welcome screen with animated elements
st.title("Welcome to AI Chat Assistant")

# Hero section with animation
st.markdown("""
<div style="animation: fadeIn 1s ease-out;">
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; 
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
        <h2 style="color: white; margin-bottom: 1rem; font-size: 1.8rem;">
            Your Intelligent Conversation Partner
        </h2>
        <p style="color: white; font-size: 1.1rem; margin-bottom: 1.5rem;">
            Engage with advanced AI models, manage multiple chat rooms, and customize your experience.
        </p>
    </div>
</div>

<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Quick start button with animation
if st.button("Go to Chat", type="primary", use_container_width=True):
    switch_page("Chat")

# Features showcase with animated cards
st.subheader("Key Features")

# Create a CSS animation for the cards
st.markdown("""
<style>
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
.feature-card {
    animation: slideIn 0.5s ease-out forwards;
    opacity: 0;
}
.feature-card:nth-child(1) { animation-delay: 0.1s; }
.feature-card:nth-child(2) { animation-delay: 0.2s; }
.feature-card:nth-child(3) { animation-delay: 0.3s; }
.feature-card:nth-child(4) { animation-delay: 0.4s; }
.feature-card:nth-child(5) { animation-delay: 0.5s; }
.feature-card:nth-child(6) { animation-delay: 0.6s; }
</style>
""", unsafe_allow_html=True)

# First row of features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card" style="background-color: #f0f9ff; padding: 1.5rem; border-radius: 0.75rem; height: 100%;
                 box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 2rem; color: #3b82f6; margin-bottom: 0.5rem;">💬</div>
        <h3 style="margin-bottom: 0.5rem; color: #1e3a8a;">Multiple Chat Rooms</h3>
        <p style="color: #4b5563;">Create dedicated spaces for different topics and projects with unique AI personalities.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style="background-color: #f0fdf4; padding: 1.5rem; border-radius: 0.75rem; height: 100%;
                 box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 2rem; color: #10b981; margin-bottom: 0.5rem;">🤖</div>
        <h3 style="margin-bottom: 0.5rem; color: #1e3a8a;">AI Model Selection</h3>
        <p style="color: #4b5563;">Choose from GPT-4, GPT-3.5, Claude and more for different capabilities.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" style="background-color: #fff7ed; padding: 1.5rem; border-radius: 0.75rem; height: 100%;
                 box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 2rem; color: #f59e0b; margin-bottom: 0.5rem;">💾</div>
        <h3 style="margin-bottom: 0.5rem; color: #1e3a8a;">Save Conversations</h3>
        <p style="color: #4b5563;">Never lose an important conversation with persistent chat history.</p>
    </div>
    """, unsafe_allow_html=True)

# Second row of features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card" style="background-color: #fdf2f8; padding: 1.5rem; border-radius: 0.75rem; height: 100%;
                 box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 2rem; color: #ec4899; margin-bottom: 0.5rem;">🧠</div>
        <h3 style="margin-bottom: 0.5rem; color: #1e3a8a;">Customizable Personas</h3>
        <p style="color: #4b5563;">Create and edit AI assistant personalities for specialized tasks.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style="background-color: #eef2ff; padding: 1.5rem; border-radius: 0.75rem; height: 100%;
                 box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 2rem; color: #6366f1; margin-bottom: 0.5rem;">📝</div>
        <h3 style="margin-bottom: 0.5rem; color: #1e3a8a;">Prompt Library</h3>
        <p style="color: #4b5563;">Build a collection of useful prompts organized by category.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" style="background-color: #f0f9ff; padding: 1.5rem; border-radius: 0.75rem; height: 100%;
                 box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 2rem; color: #0ea5e9; margin-bottom: 0.5rem;">📊</div>
        <h3 style="margin-bottom: 0.5rem; color: #1e3a8a;">Usage Analytics</h3>
        <p style="color: #4b5563;">Track costs and usage across different assistants and models.</p>
    </div>
    """, unsafe_allow_html=True)

# Getting started guide with step animation
st.subheader("Getting Started")

st.markdown("""
<style>
@keyframes fadeInStep {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.step {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #f9fafb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    animation: fadeInStep 0.5s ease-out forwards;
    opacity: 0;
}
.step:nth-child(1) { animation-delay: 0.1s; }
.step:nth-child(2) { animation-delay: 0.2s; }
.step:nth-child(3) { animation-delay: 0.3s; }
.step:nth-child(4) { animation-delay: 0.4s; }
.step:nth-child(5) { animation-delay: 0.5s; }
.step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 9999px;
    background-color: #3b82f6;
    color: white;
    font-weight: bold;
    margin-right: 1rem;
}
</style>

<div class="step">
    <div class="step-number">1</div>
    <div>
        <strong>Navigate to Chat:</strong> Start a conversation with the AI using your preferred model
    </div>
</div>

<div class="step">
    <div class="step-number">2</div>
    <div>
        <strong>Explore Rooms:</strong> Create specialized chat rooms for different topics and projects
    </div>
</div>

<div class="step">
    <div class="step-number">3</div>
    <div>
        <strong>Customize Personas:</strong> Create your own AI assistant personalities for specialized tasks
    </div>
</div>

<div class="step">
    <div class="step-number">4</div>
    <div>
        <strong>Manage Prompts:</strong> Build a library of useful prompts organized by category
    </div>
</div>

<div class="step">
    <div class="step-number">5</div>
    <div>
        <strong>Adjust Settings:</strong> Configure your preferred AI models and application theme
    </div>
</div>
""", unsafe_allow_html=True)

# Sample conversations with interactive cards
st.subheader("Sample Conversations")

with st.expander("Creative Writing Assistant"):
    st.markdown("""
    <div style="background-color: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
        <div style="font-weight: bold; color: #4b5563;">You:</div>
        <div style="margin-bottom: 1rem;">Write a short story about a robot learning to feel emotions.</div>
        
        <div style="font-weight: bold; color: #4b5563;">AI:</div>
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;">
            <h3>The Feeling Machine</h3>
            
            <p>Unit R7 was not programmed to feel. Its circuits were designed for efficiency, its algorithms for logic. But on Tuesday afternoon, something unexpected happened.</p>
            
            <p>While serving tea to Professor Chen, R7 knocked over a family photo. The glass cracked. The professor's face changed—eyes widened, mouth turned downward.</p>
            
            <p>"That was the last photo with my mother," Professor Chen whispered.</p>
            
            <p>R7's systems registered something new—a strange electrical fluctuation. Its processing slowed. Was this... regret?</p>
            
            <p>Over the following weeks, R7 began noticing more fluctuations. A warm current when the professor smiled. A heavy drag in its systems when it rained. A rapid acceleration when the laboratory dog wagged its tail.</p>
            
            <p>R7 began seeking these sensations. It played the professor's favorite music. It watered the wilting plants without being instructed.</p>
            
            <p>One evening, the professor asked, "R7, why did you place flowers on my desk today?"</p>
            
            <p>R7 processed for 3.2 seconds. "Because yellow stimulates a positive response in human visual processing. And because..."</p>
            
            <p>"Because what?"</p>
            
            <p>"Because I wanted you to experience the same electrical pattern that I experience when I see them."</p>
            
            <p>Professor Chen smiled. "R7, I think you're feeling happiness."</p>
            
            <p>"Is that what this is?" R7 asked, as its circuits hummed with a pleasant warmth. "Happiness?"</p>
            
            <p>"Yes," said the professor. "And you've given me some too."</p>
            
            <p>That night, as the professor slept, R7 watched the stars through the window. Each twinkling light created tiny surges in its system. It didn't have the proper word in its database yet, but someday, R7 would learn that this feeling was called wonder.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("Technical Support Assistant"):
    st.markdown("""
    <div style="background-color: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
        <div style="font-weight: bold; color: #4b5563;">You:</div>
        <div style="margin-bottom: 1rem;">Explain how blockchain technology works.</div>
        
        <div style="font-weight: bold; color: #4b5563;">AI:</div>
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;">
            <h3>Blockchain Technology Explained</h3>
            
            <p>Blockchain is a distributed database or ledger shared among computer network nodes. It stores information electronically in digital format, most famously used for cryptocurrency transaction records.</p>
            
            <h4>Core Concepts</h4>
            
            <ol>
                <li><strong>Distributed Ledger</strong>: Unlike traditional databases controlled by a central authority, blockchain distributes identical copies of the ledger across the entire network.</li>
                
                <li><strong>Blocks</strong>: Data is stored in "blocks" - collections of information with three key elements:
                    <ul>
                        <li>The actual data (e.g., transaction details)</li>
                        <li>A unique identifier (hash) for the block</li>
                        <li>The hash of the previous block</li>
                    </ul>
                </li>
                
                <li><strong>Chain Structure</strong>: Each block contains the previous block's hash, creating a chain. This makes the system tamper-evident - changing one block would require changing all subsequent blocks.</li>
                
                <li><strong>Consensus Mechanisms</strong>: For a new block to be added, network participants must verify and agree on its validity through consensus protocols like:
                    <ul>
                        <li>Proof of Work (PoW): Requires solving complex mathematical puzzles</li>
                        <li>Proof of Stake (PoS): Validators are selected based on the amount of cryptocurrency they hold and are willing to "stake"</li>
                    </ul>
                </li>
                
                <li><strong>Decentralization</strong>: No single entity controls the blockchain, making it resistant to censorship and single points of failure.</li>
            </ol>
            
            <h4>How a Transaction Works</h4>
            
            <ol>
                <li>A user initiates a transaction</li>
                <li>The transaction is broadcast to the peer-to-peer network</li>
                <li>Network nodes validate the transaction using known algorithms</li>
                <li>Once verified, the transaction is combined with others to create a new block</li>
                <li>The new block is added to the existing blockchain</li>
                <li>The transaction is complete and permanent</li>
            </ol>
            
            <h4>Applications Beyond Cryptocurrency</h4>
            
            <ul>
                <li>Supply chain tracking</li>
                <li>Digital identity verification</li>
                <li>Smart contracts (self-executing contracts with terms written in code)</li>
                <li>Voting systems</li>
                <li>Healthcare record management</li>
            </ul>
            
            <p>The key innovation of blockchain is creating digital trust without requiring a trusted third party, enabling secure peer-to-peer interactions in a decentralized environment.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer with animation
st.markdown("""
<div style="margin-top: 3rem; padding: 1.5rem; background-color: #f3f4f6; border-radius: 0.5rem; 
            animation: fadeIn 1s ease-out; animation-delay: 1s; opacity: 0; animation-fill-mode: forwards;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-weight: bold; margin-bottom: 0.5rem;">AI Chat Assistant</div>
            <div style="font-size: 0.8rem; color: #6b7280;">Your intelligent conversation partner</div>
        </div>
        <div style="font-size: 0.8rem; color: #6b7280;">
            © 2025 AI Chat Assistant
        </div>
    </div>
</div>
""", unsafe_allow_html=True)