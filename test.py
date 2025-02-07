import streamlit as st
from template_factory import display_templates_component

st.header("Templates")
st.subheader("quickly download templates")

# Define options for the selectbox
options = ["None", "Select Existing Templates", "Generate New Template"]


# Create a selectbox in Streamlit
selected_option = st.selectbox("Choose an option:", options)

# Display the selected option
st.write(f"You selected: {selected_option}")

if selected_option == "Select Existing Templates":
    display_templates_component()

if selected_option == "Generate New Template":
    st.write("Generate New Template")


