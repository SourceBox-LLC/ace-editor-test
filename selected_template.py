import streamlit as st

# Initialize the key if it doesn't exist yet.
if "selected_template" not in st.session_state:
    st.session_state["selected_template"] = None


