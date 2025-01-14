import streamlit as st
import editor  # Import our editor module

def home_page():
    """
    This is the 'home' page content.
    Centers the Quickstart and Edit Project boxes.
    """
    # Create a row with three columns: Spacer, Content, Spacer
    spacer1, content, spacer2 = st.columns([1, 2, 1])

    with content:
        # Within the content column, create two sub-columns for the boxes
        box1, box2 = st.columns(2)

        with box1:
            st.header("Quickstart")
            st.write("Get started on a new project fast")
        
            # Button that "navigates" to the editor
            if st.button("Get Started"):
                # Set session_state to "editor"
                st.session_state["page"] = "editor"
                st.rerun()  # Use rerun for better compatibility

        with box2:
            st.header("Edit Project")
            st.write("Get to work on an existing project")
        
            # Button to navigate to the editor or another desired page
            if st.button("Edit Project"):
                st.session_state["page"] = "editor"
                st.rerun()
                # Add similar logic here if you want to navigate somewhere else

def main():
    """
    Manages which page to show based on st.session_state.
    """
    # Initialize the page in session_state if it doesn't exist
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Show the correct page
    if st.session_state["page"] == "home":
        home_page()
    elif st.session_state["page"] == "editor":
        editor.main()   # Call the editor.py "main" function

if __name__ == "__main__":
    main()
