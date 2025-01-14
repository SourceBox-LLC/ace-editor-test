import streamlit as st
from template_factory import generate_template
from streamlit_ace import st_ace
import subprocess
import tempfile
import sys
import os

# Initialize session state for 'code', 'edit_mode', and 'run_output' if not already present
if 'code' not in st.session_state:
    st.session_state.code = ""
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'run_output' not in st.session_state:
    st.session_state.run_output = ""

# Page configuration
st.set_page_config(page_title="Streamlit App with Sidebar", layout="wide")
st.title("Streamlit Demo with Sidebar")

quickstart = st.selectbox("Quickstart Template", ["None", "Hello World", "Authentication"])

# Button to load template to prevent accidental overwrite
if st.button("Load Template"):
    if quickstart == "Hello World":
        prompt = "generate hello world python script"
        template = generate_template(prompt)
        if template:
            st.session_state.code = template  # Update the code
            st.success("Quickstart template loaded.")
            st.session_state.edit_mode = False  # Exit edit mode if active
            st.session_state.run_output = ""  # Clear previous run output
        else:
            st.error("Failed to generate Quickstart template. Please try again.")
    elif quickstart == "Authentication":
        prompt = "generate a quickstart streamlit app template with authentication"
        template = generate_template(prompt)
        if template:
            st.session_state.code = template  # Update the code
            st.success("Authentication template loaded.")
            st.session_state.edit_mode = False  # Exit edit mode if active
            st.session_state.run_output = ""  # Clear previous run output
        else:
            st.error("Failed to generate Authentication template. Please try again.")
    elif quickstart == "None":
        st.session_state.code = ""
        st.warning("Editor cleared.")
        st.session_state.edit_mode = False  # Exit edit mode if active
        st.session_state.run_output = ""  # Clear previous run output

# 1. Sidebar settings
with st.sidebar:
    st.header("Editor Settings")

    # Language selection
    language = st.selectbox("Language", ["python", "javascript", "html", "markdown"], key='language_select')

    # Theme selection
    theme = st.selectbox(
        "Theme",
        [
            "monokai",
            "github",
            "solarized_dark",
            "solarized_light",
            "terminal"
        ],
        key='theme_select'
    )

    # Keybinding selection
    keybinding = st.selectbox(
        "Keybinding",
        [
            "sublime",
            "vscode",
            "atom",
            "vim",
            "emacs"
        ],
        index=0,  # Default to 'sublime'
        key='keybinding_select'
    )

    # Auto-update checkbox
    auto_update = st.checkbox("Auto Update (run on every keystroke)", value=False, key='auto_update_checkbox')

# 2. Main area
if st.session_state.edit_mode:
    st.header("Edit Template")

    # Display the Ace Editor with the current code
    edited_code = st_ace(
        value=st.session_state.code,
        language=language,
        theme=theme,
        keybinding=keybinding,
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=True,
        wrap=False,
        auto_update=auto_update,
        height=500,
        key='ace_editor'
    )

    # Save Changes Button
    if st.button("Save Changes"):
        if edited_code:
            st.session_state.code = edited_code
            st.success("Template updated successfully.")
            st.session_state.edit_mode = False  # Exit edit mode
            st.session_state.run_output = ""  # Clear previous run output
        else:
            st.error("Cannot save empty code.")

    # Run Button
    if st.button("Run"):
        if edited_code:
            try:
                # Create a temporary Python file with the edited code
                with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
                    tmp_file.write(edited_code)
                    tmp_file_path = tmp_file.name

                # Execute the temporary Python script
                result = subprocess.run(
                    [sys.executable, tmp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=30  # Prevent long-running scripts
                )

                # Capture stdout and stderr
                stdout = result.stdout
                stderr = result.stderr

                # Combine stdout and stderr for display
                combined_output = ""
                if stdout:
                    combined_output += f"**Output:**\n```\n{stdout}\n```\n"
                if stderr:
                    combined_output += f"**Errors:**\n```\n{stderr}\n```\n"

                if not combined_output:
                    combined_output = "No output was generated."

                st.session_state.run_output = combined_output

            except subprocess.TimeoutExpired:
                st.session_state.run_output = "**Error:** The script timed out after 30 seconds."
            except Exception as e:
                st.session_state.run_output = f"**Error:** {str(e)}"
            finally:
                # Clean up the temporary file
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)

            st.info("Script execution completed.")

        else:
            st.error("No code available to run.")

    # Create Github Repository Button (Functionality Still to be Implemented)
    if st.button("Create Github Repository"):
        # TODO: Implement the GitHub repository creation functionality
        st.info("GitHub Repository creation is not yet implemented.")
        st.session_state.edit_mode = False

    # Display the run output if available
    if st.session_state.run_output:
        st.markdown("---")
        st.header("Run Output")
        st.markdown(st.session_state.run_output)
else:
    if st.session_state.code:
        st.header("Generated Template")
        st.code(st.session_state.code, language=language)
        
        # Add the "Edit Template" button below the generated code
        if st.button("Edit Template"):
            st.session_state.edit_mode = True
    else:
        st.info("Select a Quickstart Template from the sidebar and click 'Load Template' to see the generated code here.")
