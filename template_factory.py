import streamlit as st
import requests
from PIL import Image
import io
import os

# GitHub templates along with their corresponding URLs and images.
template_info = {
    "Simple Streamlit Authentication": {
        "url": "https://github.com/SourceBox-LLC/simple-streamlit-authentication.git",
        "image": "images/streamlit login template.PNG",
        "details": "A streamlined authentication system for Streamlit apps that includes user registration, login, and session management using local storage for credentials.",
        "stack": "Streamlit, Python"
    },

    "AWS Lambda Auth": {
        "url": "https://github.com/SourceBox-LLC/streamlit-login-template.git",
        "image": "images/streamlit login template.PNG",
        "details": "Secure authentication framework for Streamlit applications using AWS Lambda for serverless credential verification and user management in the cloud.",
        "stack": "Streamlit, AWS Lambda, Python"
    },

    "Chatbot": {
        "url": "https://github.com/SourceBox-LLC/streamlit-basic-langchain-chatbot.git",
        "image": "images/streamlit chatbot anthropic template.png",
        "details": "Interactive conversational interface powered by Anthropic's Claude 3.5 Sonnet model, featuring message history, customizable prompts, and a responsive UI.",
        "stack": "Streamlit, LangChain, Python"
    },

    "RAG Chatbot ()": {
        "url": "https://github.com/SourceBox-LLC/streamlit-basic-RAG-langchain-chatbot.git",
        "image": "images/streamlit rag chatbot template.png",
        "details": "Retrieval-Augmented Generation chatbot that combines document search with AI responses, allowing users to query their own data with Claude 3.5 Sonnet.",
        "stack": "LangChain, Anthropic, Streamlit, Python"
    },

    "Image Generator Multi-Modal": {
        "url": "https://github.com/SourceBox-LLC/image-generator-multi-select-template.git",
        "image": "images/image chatbot.png",
        "details": "Versatile image generation interface featuring multiple AI models from Hugging Face, with customizable parameters and a gallery view for comparing outputs.",
        "stack": "Hugging Face, Streamlit, Python"
    },

    "Ace Editor": {
        "url": "https://github.com/SourceBox-LLC/streamlit-ace-editor.git",
        "image": "images/ace_editor_img.PNG",
        "details": "Advanced code editing environment with syntax highlighting, multiple themes, and keyboard shortcuts, perfect for creating in-app code editors or IDEs.",
        "stack": "Streamlit, Ace Editor, Python"
    }
}


def convert_to_raw(url):
    """
    Convert a GitHub URL to its raw file URL.
    Example:
      https://github.com/user/repo/blob/branch/path/to/file.py
      becomes:
      https://raw.githubusercontent.com/user/repo/branch/path/to/file.py
    """
    if "github.com" in url and "/blob/" in url:
        return url.replace("github.com", "raw.githubusercontent.com").replace("/blob", "")
    return url

# -----------------------------------------------------------------------------
# Modal Dialog Function using st.dialog with width set to "large"
# This modal shows the main template file at the top,
# followed by the rest of the files in expandable accordions.
# A "Select Template" button is added at the bottom to save everything
# to st.session_state.
# -----------------------------------------------------------------------------
@st.dialog("Template Preview", width="large")
def show_template_modal(main_file, main_file_content, other_files):
    st.markdown(f"## 📄 Main Template File: `{main_file}`")
    st.code(main_file_content, language="python")
    if other_files:
        st.markdown("## 📁 Other Files")
        for file_path, content in other_files.items():
            with st.expander(f"📝 {file_path}"):
                st.code(content, language="python")
                
    # Button to select the template and store its data to session
    if st.button("✅ Select Template", type="primary"):
        st.session_state["selected_template"] = {
            "main_file": main_file,
            "main_file_content": main_file_content,
            "other_files": other_files,
            "details": st.session_state.get("selected_template_details", "No details provided."),
            "stack": st.session_state.get("selected_template_stack", "No stack information."),
        }
        st.success("✨ Template saved to session!")
        st.rerun()

def open_repo_template_modal(url):
    """
    Process a repository URL (ending in .git) by:
      - Determining the default branch via the GitHub API.
      - Fetching the repository tree.
      - Selecting a main file (preferring app.py or main.py).
      - Fetching the content of the main file and all other files.
      - Calling the modal dialog to show these files.
    """
    # Remove trailing '.git' if present and parse repository details
    base_url = url[:-4] if url.endswith('.git') else url
    parts = base_url.split('/')
    if len(parts) < 5:
        st.error("Invalid repository URL format.")
        return

    owner = parts[3]
    repo = parts[4]

    # Get repository info to determine the default branch
    repo_info_url = f"https://api.github.com/repos/{owner}/{repo}"
    st.write(f"Fetching repository info from: {repo_info_url}")
    try:
        repo_info_response = requests.get(repo_info_url)
        repo_info_response.raise_for_status()
        repo_info = repo_info_response.json()
        branch = repo_info.get("default_branch", "main")  # Fallback to "main" if not found
        st.write(f"Default branch: {branch}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching repository info: {e}")
        return

    # Build the GitHub API URL for the tree (recursive)
    tree_api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    st.write(f"Fetching repository tree from: {tree_api_url}")
    try:
        tree_response = requests.get(tree_api_url)
        tree_response.raise_for_status()
        tree_data = tree_response.json()
        
        # Get list of files (filtering items with type 'blob')
        files = [item['path'] for item in tree_data.get('tree', []) if item.get("type") == "blob"]
        if not files:
            st.warning("No files found in the repository.")
            return
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching repository tree: {e}")
        return

    # Determine the main file:
    main_file = None
    if "app.py" in files:
        main_file = "app.py"
    elif "main.py" in files:
        main_file = "main.py"
    else:
        # If none match, choose the first file that ends with .py, otherwise the first file overall.
        py_files = [f for f in files if f.endswith('.py')]
        if py_files:
            main_file = sorted(py_files)[0]
        else:
            main_file = sorted(files)[0]

    # Fetch content for the main file
    raw_main_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{main_file}"
    st.write(f"Fetching main file from: {raw_main_url}")
    try:
        main_file_response = requests.get(raw_main_url)
        main_file_response.raise_for_status()
        main_file_content = main_file_response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching main file: {e}")
        return

    # Fetch content for the rest of the files (exclude the main file)
    other_files = {}
    for file in files:
        if file == main_file:
            continue
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file}"
        try:
            response = requests.get(raw_url)
            response.raise_for_status()
            other_files[file] = response.text
        except requests.exceptions.RequestException as e:
            other_files[file] = f"Error fetching file: {e}"

    # Show the modal dialog with the template details
    show_template_modal(main_file, main_file_content, other_files)

@st.dialog("Generated Template Preview", width="large")
def open_generated_template_modal():
    """
    Show a modal dialog with the generated template.
    """
    # Retrieve the generated template from the session_state.
    generated_template = st.session_state.get("generated_template", {})
    
    if isinstance(generated_template, dict):
        main_file = generated_template.get("main_file", "main.py")
        main_file_content = generated_template.get("main_file_content", "")
        other_files = generated_template.get("other_files", {})
        
        # Display the main file.
        st.markdown(f"## 📄 Main Template File: `{main_file}`")
        st.code(main_file_content, language="python")
        
        # Display other files if any.
        if other_files:
            st.markdown("## 📁 Other Files")
            for file_path, content in other_files.items():
                with st.expander(f"📝 {file_path}"):
                    st.code(content, language="python")
        
        # Button to select the template.
        if st.button("✅ Select Template", type="primary"):
            st.session_state["selected_template"] = generated_template
            st.success("✨ Generated template saved to session!")
            st.rerun()
    else:
        # If it's a string or other type, just display it as is.
        st.markdown("## Generated Template")
        st.write(generated_template)
        
        # Button to save the template as a string.
        if st.button("✅ Select Template", type="primary"):
            st.session_state["selected_template"] = {
                "main_file": "generated_template.txt",
                "main_file_content": str(generated_template),
                "other_files": {},
            }
            st.success("✨ Generated template saved to session!")
            st.rerun()

# Add this function to resize images to a standard size
def resize_image_to_standard(image_path, width=300, height=200):
    """
    Resize an image to a standard size using PIL
    """
    try:
        img = Image.open(image_path)
        img = img.resize((width, height), Image.LANCZOS)
        
        # Create a BytesIO object to hold the image data
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format if img.format else 'PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr
    except Exception as e:
        st.error(f"Error resizing image: {e}")
        return None

def display_templates_component():
    """
    Component to display a grid of template cards.
    Each card shows:
    - Template name as a header
    - Image (if available)
    - A short description
    - Selection button
    """
    # Convert dict to list for easier processing in batches
    all_templates = list(template_info.items())
    
    # Process templates in rows of 2 (instead of 3)
    for i in range(0, len(all_templates), 2):
        # Create a fresh row for each group of 2 templates
        row = st.columns(2, gap="large")
        
        # Process up to 2 templates in this row
        for j in range(2):
            col_index = j
            template_index = i + j
            
            # Check if we still have templates to display
            if template_index < len(all_templates):
                template_name, info = all_templates[template_index]
                
                # Display template in this column
                with row[col_index]:
                    # Create a styled card for the template
                    st.markdown(f"""
                        <div class="template-card">
                            <h3 style="margin-top: 0;">{template_name}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the template image if available
                    if "image" in info and info["image"]:
                        # Resize the image to standard dimensions
                        image_path = info["image"]
                        if os.path.exists(image_path):
                            resized_img = resize_image_to_standard(image_path, width=300, height=200)
                            if resized_img:
                                st.image(resized_img, caption=template_name, width=300)
                            else:
                                st.image(image_path, caption=template_name, width=300)
                        else:
                            st.warning(f"Image not found: {image_path}")
                    
                    # Display template details
                    if "details" in info and info["details"]:
                        st.markdown(f"**Description**: {info['details']}")
                        
                    # Display tech stack as badges
                    if "stack" in info and info["stack"]:
                        stack_items = info["stack"].split(", ")
                        badges_html = "<div style='margin: 10px 0;'>"
                        for item in stack_items:
                            badges_html += f'<span style="background-color: #FF4B4B; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 5px; font-weight: 500;">{item}</span>'
                        badges_html += "</div>"
                        st.markdown(badges_html, unsafe_allow_html=True)
                    
                    # Create a select button for the template
                    if st.button(f"📥 Select {template_name}", key=f"select_{template_name}", use_container_width=True):
                        # Store necessary information in session_state before opening the modal
                        st.session_state["selected_template_name"] = template_name
                        st.session_state["selected_template_image"] = info.get("image", None)
                        st.session_state["selected_template_details"] = info.get("details", "")
                        st.session_state["selected_template_stack"] = info.get("stack", "")
                        
                        # Call open_repo_template_modal with the template URL
                        open_repo_template_modal(info["url"])
        
        # Add a spacer between rows
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Optional: For testing this module independently
if __name__ == "__main__":
    display_templates_component()