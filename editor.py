import streamlit as st
from streamlit_ace import st_ace
import io
import contextlib

# Page configuration
st.set_page_config(page_title="Streamlit Ace App with Sidebar", layout="wide")
st.title("Streamlit Ace Demo with Sidebar")

# 1. Sidebar settings
with st.sidebar:
    st.header("Editor Settings")

    quickstart = st.selectbox("Quickstart Template", ["None","Streamlit Hello", "Streamlit Auth"])

    # Language selection
    language = st.selectbox("Language", ["python", "javascript", "html", "markdown"])

    # Theme selection
    theme = st.selectbox(
        "Theme",
        [
            "monokai",
            "github",
            "solarized_dark",
            "solarized_light",
            "terminal"
        ]
    )

    # Keybinding selection
    keybinding = st.selectbox("Keybinding", ["vscode", "vim", "emacs", "sublime"])

    # Auto-update checkbox
    auto_update = st.checkbox("Auto Update (run on every keystroke)", value=False)

# 2. Create the Ace editor in the main area
code = st_ace(
    value="print('Hello from Streamlit Ace!')",
    language=language,
    theme=theme,
    keybinding=keybinding,
    auto_update=auto_update,     # If True, updates the code on every keystroke
    font_size=14,
    show_gutter=True,
    show_print_margin=False,
    wrap=True,
    min_lines=15,
    max_lines=30,
    key="ace_editor"
)

# 3. Determine whether to execute code automatically or via button
execute_code = False
if auto_update:
    # Auto update: run whenever code changes
    execute_code = True
else:
    # Manual execution only with the "Run Code" button
    if st.button("Run Code"):
        execute_code = True

# 4. Execute and display the code output
if execute_code and code.strip():
    output_buffer = io.StringIO()
    with contextlib.redirect_stdout(output_buffer):
        try:
            exec(code, {})
        except Exception as e:
            # Print any errors to the output
            print(f"Error: {e}")
    st.subheader("Output:")
    st.code(output_buffer.getvalue(), language=language)
else:
    st.write("Click **Run Code** (or enable **Auto Update** in the sidebar) to execute the script.")
