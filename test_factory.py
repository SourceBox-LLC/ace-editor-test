import streamlit as st
import requests

# GitHub templates with their respective GitHub URLs
template_urls = {
    # Using a repository URL (ends with .git) for the AWS Lambda Auth template
    "AWS Lambda Auth - Streamlit": "https://github.com/SourceBox-LLC/streamlit-login-template.git",
    # For demonstration, this one remains as a file URL (update with the actual URL if needed)
    "Streamlit Chatbot": "https://github.com/your-org/streamlit-chatbot-template/blob/master/main.py"
}

st.write("Displaying templates here")

# Define options for the selectbox
options = ["", "AWS Lambda Auth - Streamlit", "Generate New Template"]

# Create a selectbox in Streamlit
selected_option = st.selectbox("Choose an option:", options)
st.write(f"You selected: {selected_option}")

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

def process_repo_template(url):
    """
    Process a repository URL (ending in .git) by fetching its tree using the GitHub API.
    This function determines the repository's default branch before querying the tree, 
    then lets the user select a file to view its contents.
    """
    # Remove trailing '.git' if present and parse repository details
    base_url = url[:-4] if url.endswith('.git') else url
    parts = base_url.split('/')
    if len(parts) < 5:
        st.error("Invalid repository URL format.")
        return

    owner = parts[3]
    repo  = parts[4]

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
        response = requests.get(tree_api_url)
        response.raise_for_status()
        tree_data = response.json()
        
        # Get list of files (filtering items with type 'blob')
        files = [item['path'] for item in tree_data.get('tree', []) if item.get("type") == "blob"]
        if not files:
            st.warning("No files found in the repository.")
            return
        
        # Let the user select a file to view with an empty entry at the top
        selected_file = st.selectbox("Select a file to view", [""] + sorted(files))
        if selected_file:
            # Create a raw URL for the file using the determined default branch
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{selected_file}"
            st.write(f"Fetching file from: {raw_url}")
            
            file_response = requests.get(raw_url)
            file_response.raise_for_status()
            
            file_content = file_response.text
            # Display the file content; adjust the language based on the file extension if needed.
            st.code(file_content, language="python")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching repository data: {e}")

# Process the selected option
if selected_option == "None":
    st.info("No template selected.")
elif selected_option == "Generate New Template":
    st.info("Generate New Template functionality is not implemented yet.")
elif selected_option in template_urls:
    # Get the corresponding URL for the selected template
    url = template_urls[selected_option]
    # If the URL ends with '.git', treat it as an entire repository
    if url.endswith('.git'):
        process_repo_template(url)
    else:
        # Otherwise, assume it is a GitHub file URL and convert it to raw
        raw_url = convert_to_raw(url)
        st.write(f"Fetching the template from: {raw_url}")
        
        try:
            response = requests.get(raw_url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an error
            template_content = response.text
            st.code(template_content, language="python")
        except requests.exceptions.RequestException as e:
            st.error(f"Error downloading the template: {e}")
else:
    st.warning("Unknown selection.")
