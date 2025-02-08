import streamlit as st
from streamlit_ace import st_ace


def ace_editor(content):
    """
    This function creates a Streamlit app with an Ace editor widget.
    It allows users to customize the editor's theme, language, height, font size, tab size, and word wrap.
    The editor's content is displayed below the widget, and the user can toggle the display of line numbers and a print margin.
    """
    # Configure the page to use the full width and set a title

    st.set_page_config(page_title="Big Ace Editor Example", layout="wide")
    # ========================
    # Sidebar - Editor Controls
    # ========================
    st.sidebar.title("Editor Controls")

    # Theme selector for the Ace editor
    theme = st.sidebar.selectbox(
        "Choose Theme",
        options=["monokai", "github", "tomorrow", "kuroir", "twilight", "xcode", "textmate", "terminal"],
        index=0,
    )
    # Language selector
    language = st.sidebar.selectbox(
        "Select Language",
        options=["python", "javascript", "html", "css", "java", "c++", "ruby"],
        index=0,
    )
    # Editor height in pixels
    height = st.sidebar.slider("Editor Height (px)", min_value=300, max_value=1000, value=600)
    # Font size selector
    font_size = st.sidebar.slider("Font Size", min_value=8, max_value=24, value=14)
    # Tab size selector
    tab_size = st.sidebar.slider("Tab Size", min_value=2, max_value=8, value=4)
    # Toggle for enabling word-wrap
    wrap_enabled = st.sidebar.checkbox("Enable Wrap", value=True)
    # Toggle to show line numbers (gutter on the left)
    show_gutter = st.sidebar.checkbox("Show Gutter", value=True)
    # Toggle for print margin
    show_print_margin = st.sidebar.checkbox("Show Print Margin", value=False)
    # Keybinding selection for the editor
    keybinding = st.sidebar.selectbox(
        "Keybinding Mode",
        options=["ace", "vscode", "sublime", "emacs"],
        index=1,
    )
    # Option to update editor content automatically
    auto_update = st.sidebar.checkbox("Auto-update Editor", value=True)
    # ========================
    # Main Content - The Big Editor
    # ========================
    st.title("Big Ace Editor")
    # Default content displayed in the editor
    default_content = content
    # Create the Ace editor widget

    editor_content = st_ace(
        value=default_content,
        language=language,
        theme=theme,
        height=height,
        font_size=font_size,
        tab_size=tab_size,
        wrap=wrap_enabled,
        show_gutter=show_gutter,
        keybinding=keybinding,
        auto_update=auto_update,
    )
    # Display the content from the editor below the widget
    st.subheader("Editor Output:")
    st.code(editor_content, language=language)

    return editor_content




if __name__ == "__main__":

    content = """
    # Welcome to the Ace Editor
    def main():
        print("Hello, Streamlit Ace!")

    if __name__ == "__main__":
        main()
    """
    ace_editor(content)

