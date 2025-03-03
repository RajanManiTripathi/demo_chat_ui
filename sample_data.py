"""
sample_data.py
This file holds predefined data for chat history, rooms, assistants, and pricing.
"""

sample_chat_history = [
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
    {"role": "user", "content": "Can you summarize this document?"},
    {"role": "assistant", "content": "Sure! Please upload the document."},
    {"role": "user", "content": "I need a product description for a new skincare line."},
    {"role": "assistant", "content": "Here's a sample description..."}
]

sample_rooms = {
    "Public Room": ["Translation Assistant", "Catalog Writing Assistant", "Email Drafting Assistant"],
    "HR Room": ["Interview Summary Assistant", "Candidate Filtering and Scoring"]
}

sample_pricing = {
    "credits_used": "$10.21",
    "monthly_cost": "$1.23 This Month"
}
