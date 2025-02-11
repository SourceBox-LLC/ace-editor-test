import streamlit as st
import requests

# GitHub templates along with their corresponding URLs and images.
template_info = {
    "Simple Streamlit Authentication (Streamlit + Python)": {
        "url": "https://github.com/SourceBox-LLC/simple-streamlit-authentication.git",
        "image": "images/streamlit login template.PNG",
        "details": "",
        "stack": ""
    },

    "AWS Lambda Auth (Streamlit + AWS Lambda + Python)": {
        "url": "https://github.com/SourceBox-LLC/streamlit-login-template.git",
        "image": "images/streamlit login template.PNG",
        "details": "",
        "stack": ""
    },

    "Chatbot (LangChain + Anthropic + Streamlit + Python)": {
        "url": "https://github.com/SourceBox-LLC/streamlit-basic-langchain-chatbot.git",
        "image": "images/streamlit chatbot anthropic template.png",
        "details": "",
        "stack": ""
    },

    "RAG Chatbot (LangChain + Anthropic + Streamlit + Python)": {
        "url": "https://github.com/SourceBox-LLC/streamlit-basic-RAG-langchain-chatbot.git",
        "image": "images/streamlit rag chatbot template.png",
        "details": "",
        "stack": ""
    },

    "Image Generator Multi-Modal (Hugging Face + Streamlit + Python)": {
        "url": "https://github.com/SourceBox-LLC/image-generator-multi-select-template.git",
        "image": "images/image chatbot.png",
        "details": "",
        "stack": ""
    },

    "Ace Editor (Streamlit + Ace Editor + Python)": {
        "url": "https://github.com/SourceBox-LLC/streamlit-ace-editor.git",
        "image": "images/ace_editor_img.PNG",
        "details": "",
        "stack": ""
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
    st.markdown(f"## Main Template File: `{main_file}`")
    st.code(main_file_content, language="python")
    if other_files:
        st.markdown("## Other Files")
        for file_path, content in other_files.items():
            with st.expander(file_path):
                st.code(content, language="python")
                
    # Button to select the template and store its data to session
    if st.button("Select Template"):
        st.session_state["selected_template"] = {
            "main_file": main_file,
            "main_file_content": main_file_content,
            "other_files": other_files,
        }
        st.success("Template saved to session!")
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

def open_generated_template_modal():
    """
    Opens the modal dialog for a generated new template.
    Expects st.session_state["generated_template"] to contain either:
     - a dictionary with keys "main_file", "main_file_content", and "other_files", or
     - a plain string representing a single-file template.
    """
    generated = st.session_state.get("generated_template")
    if not generated:
        st.error("No generated template available.")
        return
    
    # If generated is a string, assume that it's the main file content and wrap it in a dict.
    if isinstance(generated, str):
        generated = {
            "main_file": "main.py",
            "main_file_content": generated,
            "other_files": {}
        }
    
    main_file = generated.get("main_file")
    main_file_content = generated.get("main_file_content")
    other_files = generated.get("other_files", {})
    show_template_modal(main_file, main_file_content, other_files)

def display_templates_component():
    """
    Renders the templates component.
    Use this function in your app.py to display the templates.
    """
    st.markdown("## Available Templates")
    
    # Create a stacked list; each template is rendered as its own form ("card")
    for idx, (template_name, data) in enumerate(template_info.items()):
        url = data["url"]
        image = data["image"]
    
        with st.form(key=f"template_form_{idx}"):
            st.markdown(f"### {template_name}")
            st.image(image, caption=template_name)
            st.write("This template is perfect for your project. Click below to select it!")
    
            # The submit button inside the form
            submitted = st.form_submit_button(f"Select {template_name}")
    
            if submitted:
                st.success(f"You selected the {template_name} template!")
    
                # Process based on the URL type:
                if url.endswith('.git'):
                    open_repo_template_modal(url)
                else:
                    raw_url = convert_to_raw(url)
                    st.write(f"Fetching the template from: {raw_url}")
                    try:
                        response = requests.get(raw_url)
                        response.raise_for_status()
                        template_content = response.text
                        st.code(template_content, language="python")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error downloading the template: {e}")
    
    # NEW: If a generated new template exists, add a preview button.
    if st.session_state.get("generated_template"):
        st.markdown("## Generated New Template")
        if st.button("Preview Generated Template"):
            open_generated_template_modal()

# Optional: For testing this module independently
if __name__ == "__main__":
    display_templates_component()