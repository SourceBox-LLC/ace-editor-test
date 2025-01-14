import streamlit as st
from template_factory import generate_template  # Assuming you have a separate template_factory.py
from streamlit_ace import st_ace
import subprocess
import tempfile
import sys
import os
from git_factory import open_github_new_project, push_template_to_github

def main():
    # --- Session State Setup ---
    if 'code' not in st.session_state:
        st.session_state.code = ""
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    if 'run_output' not in st.session_state:
        st.session_state.run_output = ""

    # --- Page Configuration ---
    # NOTE: If you see a warning about set_page_config, move this to app.py or
    #       the top of your script before other Streamlit calls.
    st.set_page_config(page_title="Streamlit App with Sidebar", layout="wide")
    st.title("Streamlit Demo with Sidebar")

    # --- Quickstart Template Selection ---
    quickstart = st.selectbox("Quickstart Template", ["None", "Hello World", "Authentication"])

    # --- Load Template Button ---
    if st.button("Load Template"):
        if quickstart == "Hello World":
            prompt = "generate hello world python script"
            template = generate_template(prompt)
            if template:
                st.session_state.code = template
                st.success("Quickstart template loaded.")
                st.session_state.edit_mode = False
                st.session_state.run_output = ""
            else:
                st.error("Failed to generate Quickstart template. Please try again.")

        elif quickstart == "Authentication":
            prompt = "generate a quickstart streamlit app template with authentication"
            template = generate_template(prompt)
            if template:
                st.session_state.code = template
                st.success("Authentication template loaded.")
                st.session_state.edit_mode = False
                st.session_state.run_output = ""
            else:
                st.error("Failed to generate Authentication template. Please try again.")

        elif quickstart == "None":
            st.session_state.code = ""
            st.warning("Editor cleared.")
            st.session_state.edit_mode = False
            st.session_state.run_output = ""

    # --- Sidebar Settings ---
    with st.sidebar:
        st.header("Editor Settings")

        # Language selection
        language = st.selectbox("Language", ["python", "javascript", "html", "markdown"], key='language_select')

        # Theme selection
        theme = st.selectbox(
            "Theme",
            ["monokai", "github", "solarized_dark", "solarized_light", "terminal"],
            key='theme_select'
        )

        # Keybinding selection
        keybinding = st.selectbox(
            "Keybinding",
            ["sublime", "vscode", "atom", "vim", "emacs"],
            index=0,  # Default to 'sublime'
            key='keybinding_select'
        )

        # Auto-update checkbox
        auto_update = st.checkbox("Auto Update (run on every keystroke)", value=False, key='auto_update_checkbox')

    # --- Main Editor Area ---
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
                st.session_state.edit_mode = False
                st.session_state.run_output = ""
            else:
                st.error("Cannot save empty code.")

        # Run Button
        if st.button("Run"):
            if edited_code:
                try:
                    # Create a temporary Python file
                    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
                        tmp_file.write(edited_code)
                        tmp_file_path = tmp_file.name

                    # Execute the temporary Python script
                    result = subprocess.run(
                        [sys.executable, tmp_file_path],
                        capture_output=True,
                        text=True,
                        timeout=30
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
                    if os.path.exists(tmp_file_path):
                        os.remove(tmp_file_path)

                st.info("Script execution completed.")

            else:
                st.error("No code available to run.")

        # Create Github Repository Button
        if st.button("Create Github Repository"):
            open_github_new_project()
            st.session_state.edit_mode = False

        # GitHub Repository URL Input
        repo_url = st.text_input("Enter the GitHub repository URL")

        # Upload Button
        if st.button("Upload"):
            if repo_url and edited_code:
                try:
                    push_template_to_github(repo_url, edited_code)
                    st.success("Code pushed to GitHub successfully.")
                except Exception as e:
                    st.error(f"Failed to push code to GitHub: {str(e)}")
            else:
                st.error("Please enter a valid GitHub URL and ensure code is available.")

        # Display any run output
        if st.session_state.run_output:
            st.markdown("---")
            st.header("Run Output")
            st.markdown(st.session_state.run_output)

    else:
        # If not in edit mode but we have code, show the generated code
        if st.session_state.code:
            st.header("Generated Template")
            st.code(st.session_state.code, language=language)

            # Button to switch into edit mode
            if st.button("Edit Template"):
                st.session_state.edit_mode = True
        else:
            st.info("Select a Quickstart Template from the sidebar and click 'Load Template' to see the generated code here.")

    # --- Go Back to Home (app.py) ---
    st.markdown("---")
    if st.button("Go Back"):
        st.session_state["page"] = "home"
        st.rerun()
