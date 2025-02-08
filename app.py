import streamlit as st
from template_factory import display_templates_component, open_generated_template_modal
from bedrock import generate_template

# -------------------------------------------------------------------
# Initialize session state keys if they don't exist yet.
if "selected_template" not in st.session_state:
    st.session_state["selected_template"] = None
if "generated_template" not in st.session_state:
    st.session_state["generated_template"] = None

# -------------------------------------------------------------------
# If a template has already been selected, show its details automatically.
if st.session_state["selected_template"] is not None:
    selected_template = st.session_state["selected_template"]

    st.header("Selected Template Details")
    
    # (Optional) Insert a template image here if available:
    st.write("Insert template image here!")
    
    # Display the main file (the main app file) normally.
    st.subheader(f"Main File: {selected_template['main_file']}")
    st.code(selected_template["main_file_content"], language="python")
    
    # Display other files in an accordion.
    other_files = selected_template.get("other_files", {})
    if other_files:
        st.subheader("Other Files")
        for file_name, content in other_files.items():
            with st.expander(file_name):
                st.code(content, language="python")
    
    # Sidebar information for the selected template.
    with st.sidebar:
        st.header(f"{selected_template.get('main_file', 'Template')} Template")
        st.subheader("One Sentence Explanation")
        st.markdown("---")
        st.subheader("Details")
        st.write("Longer in-depth explanation")
        st.markdown("---")
        st.subheader("Stack")
        st.write("Stack details list here")
        st.markdown("---")
        st.subheader("Use Case")
        st.write("Explanation of use cases")
    
    #edit template via ace editor
    if st.button("Edit Template"):
        pass

    # Option to clear the selection and return to the selection UI.
    if st.button("Select Another Template"):
        st.session_state["selected_template"] = None
        st.rerun()  # Force a rerun to show the selection UI.
    
    st.stop()  # Stop further execution so the selection UI is not rendered.

# -------------------------------------------------------------------
# Template Selection / Generation UI (shown only if no template is selected)
st.header("Templates")
st.subheader("Quickly download templates")

# Define options for the selectbox.
options = ["None", "Select Existing Templates", "Generate New Template"]

# Create a selectbox in Streamlit.
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
        # Save the generated result to session state.
        st.session_state["generated_template"] = template
        st.success("New template generated! Preview it below.")
    
    # If a generated template exists, show a preview button (which opens the modal).
    if st.session_state.get("generated_template"):
        if st.button("Preview Generated Template"):
            open_generated_template_modal()
