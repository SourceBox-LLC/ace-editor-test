import streamlit as st
from streamlit_ace import st_ace
from bedrock import auto_edit_template

def ace_editor(content):
    """
    Displays the Ace editor with manual editing and an AI-edit option.
    Both the Ace editor and the output below are updated when new AI-edited
    code is returned.
    """
    # Initialize session state variables if not already set.
    if "editor_content" not in st.session_state:
        st.session_state["editor_content"] = content
    if "ace_version" not in st.session_state:
        st.session_state["ace_version"] = 0  # Used to force reinitialization of the Ace widget

    # ------------------------------
    # Sidebar - Editor Configuration
    # ------------------------------
    st.sidebar.title("Editor Controls")
    theme = st.sidebar.selectbox(
        "Choose Theme",
        options=["monokai", "github", "tomorrow", "kuroir", "twilight", "xcode", "textmate", "terminal"],
        index=0,
    )
    language = st.sidebar.selectbox(
        "Select Language",
        options=["python", "javascript", "html", "css", "java", "c++", "ruby"],
        index=0,
    )
    height = st.sidebar.slider("Editor Height (px)", min_value=300, max_value=1000, value=600)
    font_size = st.sidebar.slider("Font Size", min_value=8, max_value=24, value=14)
    tab_size = st.sidebar.slider("Tab Size", min_value=2, max_value=8, value=4)
    wrap_enabled = st.sidebar.checkbox("Enable Wrap", value=True)
    show_gutter = st.sidebar.checkbox("Show Gutter", value=True)
    show_print_margin = st.sidebar.checkbox("Show Print Margin", value=False)
    keybinding = st.sidebar.selectbox(
        "Keybinding Mode",
        options=["ace", "vscode", "sublime", "emacs"],
        index=1,
    )
    auto_update = st.sidebar.checkbox("Auto-update Editor", value=True)

    # ------------------------------
    # Main Content - The Ace Editor
    # ------------------------------
    st.title("Template Editor")
    # Use a dynamic key based on the version counter so that when the version increments,
    # the Ace widget is forced to reinitialize with the new content.
    editor_content = st_ace(
        value=st.session_state["editor_content"],
        language=language,
        theme=theme,
        height=height,
        font_size=font_size,
        tab_size=tab_size,
        wrap=wrap_enabled,
        show_gutter=show_gutter,
        keybinding=keybinding,
        auto_update=auto_update,
        key=f"ace_editor_{st.session_state['ace_version']}"
    )

    # Update the session state with the current editor content.
    st.session_state["editor_content"] = editor_content

    # ------------------------------
    # AI Edit Section
    # ------------------------------
    st.subheader("AI Prompt Edit (Optional)")
    prompt_edit = st.text_area("Enter your AI prompt to edit the template automatically:")

    if st.button("Submit AI Edit"):
        # Pass both the current prompt and the current editor content to your AI editor function.
        new_code = auto_edit_template(prompt=prompt_edit, code=editor_content)
        if new_code:
            # Update session state with the AI-edited code.
            st.session_state["editor_content"] = new_code
            # Increment the version to force the Ace editor widget to reinitialize.
            st.session_state["ace_version"] += 1
            st.success("Editor updated with AI edits!")
            st.rerun()
        else:
            st.error("AI did not return any new code. Please try again.")

    # ------------------------------
    # Display the Updated Code Below
    # ------------------------------
    st.subheader("Editor Output:")
    st.code(editor_content, language=language)

    return editor_content


if __name__ == "__main__":
    sample_content = """
# Welcome to the Ace Editor
def main():
    print("Hello, Streamlit Ace!")

if __name__ == "__main__":
    main()
"""
    ace_editor(sample_content)
