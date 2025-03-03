import streamlit as st

st.set_page_config(layout="wide", page_title="Assistants Room")

st.title("🗂 Assistants Gallery")

# Room Tabs
tab1, tab2 = st.tabs(["Public Room", "HR Room"])

with tab1:
    st.subheader("Public Room")
    st.button("Translation Assistant")
    st.button("Catalog Writing Assistant")
    st.button("Email Drafting Assistant")

with tab2:
    st.subheader("HR Room")
    st.button("Interview Summary Assistant")
    st.button("Candidate Filtering Assistant")

# Navigation
st.sidebar.page_link("Home.py", label="💬 Chat")
st.sidebar.page_link("settings.py", label="⚙️ Settings")
