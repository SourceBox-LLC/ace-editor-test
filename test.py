import streamlit as st
from template_factory import display_templates_component, open_generated_template_modal
from bedrock import generate_template

st.header("Templates")
st.subheader("Quickly download templates")

# Define options for the selectbox
options = ["None", "Select Existing Templates", "Generate New Template"]

# Create a selectbox in Streamlit
selected_option = st.selectbox("Choose an option:", options)
st.write(f"You selected: {selected_option}")

if selected_option == "Select Existing Templates":
    display_templates_component()

if selected_option == "Generate New Template":
    st.write("Generate New Template")
    prompt = st.text_area("Enter a prompt for the new template:")
    
    if st.button("Generate Template"):
        st.write(f"Generating template for: {prompt}")
        # Assume generate_template returns a dict or a string template.
        template = generate_template(prompt)
        # Save the generated result to a temporary session variable.
        st.session_state["generated_template"] = template
        st.success("New template generated! Preview it below.")
    
    # If a generated template exists, show a preview button (which opens the modal)
    if st.session_state.get("generated_template"):
        if st.button("Preview Generated Template"):
            open_generated_template_modal()


