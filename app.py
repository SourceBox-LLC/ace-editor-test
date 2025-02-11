import streamlit as st
from template_factory import display_templates_component, open_generated_template_modal
from bedrock import generate_template
import io
import zipfile

# -------------------------------------------------------------------
# Initialize session state keys if they don't exist yet.
if "selected_template" not in st.session_state:
    st.session_state["selected_template"] = None
if "generated_template" not in st.session_state:
    st.session_state["generated_template"] = None

# -------------------------------------------------------------------
def create_template_zip(template):
    """
    Given a template dict with keys 'main_file', 'main_file_content', and optionally 'other_files',
    create an in-memory ZIP file containing all of the template files.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Write the main file.
        main_file_name = template.get("main_file", "template.txt")
        main_content = template.get("main_file_content", "")
        zip_file.writestr(main_file_name, main_content)
        
        # Write any other files.
        for file_name, content in template.get("other_files", {}).items():
            zip_file.writestr(file_name, content)
    buffer.seek(0)  # Rewind the buffer to the beginning so it can be read.
    return buffer

# -------------------------------------------------------------------
# Check if we are in "edit mode". If so, show the Ace editor.
if st.session_state.get("edit_mode"):
    from ace_editor import ace_editor
    # Retrieve the current template code from the session.
    template_code = st.session_state.get("selected_template", {}).get("main_file_content", "")
    # Run the Ace editor and capture the (possibly edited) content.
    edited_code = ace_editor(template_code)
    
    # Create two columns for the Save and Back buttons.
    col1, col2 = st.columns(2)
    
    if col1.button("Save"):
        # Save the updated code into st.session_state.
        st.session_state["selected_template"]["main_file_content"] = edited_code
        st.success("Changes saved!")
        st.session_state["edit_mode"] = False
        st.rerun()
    
    if col2.button("Back to Template Details"):
        st.session_state["edit_mode"] = False
        st.rerun()
    
    st.stop()

# -------------------------------------------------------------------
# If a template has already been selected, show its details automatically.
if st.session_state["selected_template"] is not None:
    selected_template = st.session_state["selected_template"]

    st.header("Selected Template Details")
    
    # Display the template image if available; otherwise, show placeholder text.
    if "selected_template_image" in st.session_state:
        st.image(
            st.session_state["selected_template_image"],
            caption=st.session_state.get("selected_template_name", "Template Image")
        )
    else:
        st.write("Insert template image here!")
        st.write(selected_template)
    
    # Display the main file normally.
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
        st.markdown("---")
        st.subheader("Details")
        st.write("Longer in-depth explanation")
        st.markdown("---")
        st.subheader("Stack")
        st.write("Stack details list here")
        st.markdown("---")
        
        # Create the ZIP archive from the template.
        template_zip = create_template_zip(selected_template)
        
        # Provide a download button.
        st.download_button(
            label="Download Template",
            data=template_zip,
            file_name="template.zip",
            mime="application/zip"
        )
       
        st.link_button("Create New Repository", url="https://github.com/new")
        
    # Button to switch to edit mode with the current template code loaded in the Ace editor.
    if st.button("Edit Template"):
        st.session_state["edit_mode"] = True
        st.rerun()

    # Button to clear the current template if needed.
    if st.button("Select Another Template"):
        st.session_state["selected_template"] = None
        st.rerun()
    
    st.stop()  # Stop further execution so the selection UI is not rendered.

# -------------------------------------------------------------------
# Template Selection / Generation UI (shown only if no template is selected)
st.header("Templates")
st.subheader("Quickly download templates")

with st.sidebar:
    st.title("To Be Determined")

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
