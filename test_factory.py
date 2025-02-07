import streamlit as st
import requests

# GitHub templates with their respective GitHub URLs
template_urls = {
    "AWS Lambda Auth - Streamlit": "https://github.com/SourceBox-LLC/streamlit-login-template/blob/master/main.py",
    "Streamlit Chatbot": "https://github.com/your-org/streamlit-chatbot-template/blob/master/main.py"  # update with actual URL
}

st.write("Displaying templates here")

# Define options for the selectbox
options = ["None", "AWS Lambda Auth - Streamlit", "Generate New Template"]

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

# Process the selected option
if selected_option == "None":
    st.info("No template selected.")
elif selected_option == "Generate New Template":
    st.info("Generate New Template functionality is not implemented yet.")
elif selected_option in template_urls:
    # Get the corresponding URL for the selected template
    url = template_urls[selected_option]
    raw_url = convert_to_raw(url)
    
    st.write(f"Fetching the template from: {raw_url}")
    
    try:
        response = requests.get(raw_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        
        template_content = response.text
        
        # Display the downloaded code using st.code (with Python syntax highlighting)
        st.code(template_content, language="python")
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading the template: {e}")
else:
    st.warning("Unknown selection.")
