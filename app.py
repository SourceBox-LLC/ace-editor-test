import streamlit as st
from template_factory import display_templates_component, open_generated_template_modal
from bedrock import generate_template
import io
import zipfile
import os
import base64

# Set page configuration
st.set_page_config(
    page_title="Template Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
def load_css():
    with open(".streamlit/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except:
    pass

# -------------------------------------------------------------------
# Initialize session state keys if they don't exist yet.
if "selected_template" not in st.session_state:
    st.session_state["selected_template"] = None
if "generated_template" not in st.session_state:
    st.session_state["generated_template"] = None

# -------------------------------------------------------------------
def create_template_zip(template):
    """
    Given a template dict with keys 'main_file', 'main_file_content', and optionally 'other_files',
    create an in-memory ZIP file containing all of the template files.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Write the main file.
        main_file_name = template.get("main_file", "template.txt")
        main_content = template.get("main_file_content", "")
        zip_file.writestr(main_file_name, main_content)
        
        # Write any other files.
        for file_name, content in template.get("other_files", {}).items():
            zip_file.writestr(file_name, content)
    buffer.seek(0)  # Rewind the buffer to the beginning so it can be read.
    return buffer

# -------------------------------------------------------------------
# Function to add rounded borders to images
def add_image_styling(image_path, caption=None, width=None):
    img_html = f'<img src="data:image/png;base64,{get_base64_of_image(image_path)}" class="template-image"'
    
    if width:
        img_html += f' width="{width}"'
    
    img_html += '>'
    
    if caption:
        img_html += f'<p style="text-align: center; font-style: italic;">{caption}</p>'
    
    return img_html

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# -------------------------------------------------------------------
# Check if we are in "edit mode". If so, show the Ace editor.
if st.session_state.get("edit_mode"):
    from ace_editor import ace_editor
    
    st.markdown("<h1 style='text-align:center;'>Template Editor</h1>", unsafe_allow_html=True)
    
    # Retrieve the current template code from the session.
    template_code = st.session_state.get("selected_template", {}).get("main_file_content", "")
    # Run the Ace editor and capture the (possibly edited) content.
    edited_code = ace_editor(template_code)
    
    # Create two columns for the Save and Back buttons.
    col1, col2 = st.columns(2)
    
    if col1.button("💾 Save Changes", use_container_width=True):
        # Save the updated code into st.session_state.
        st.session_state["selected_template"]["main_file_content"] = edited_code
        st.success("✅ Changes saved successfully!")
        st.session_state["edit_mode"] = False
        st.rerun()
    
    if col2.button("⬅️ Back to Template Details", use_container_width=True):
        st.session_state["edit_mode"] = False
        st.rerun()
    
    st.stop()

# -------------------------------------------------------------------
# If a template has already been selected, show its details automatically.
if st.session_state["selected_template"] is not None:
    selected_template = st.session_state["selected_template"]

    # Create a container for the template details
    template_container = st.container()
    
    with template_container:
        st.markdown("<h1 style='text-align:center;'>Selected Template Details</h1>", unsafe_allow_html=True)
        
        # Create columns for image and information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Look for an image stored in session state OR use the image from the template details (if available)
            template_image = st.session_state.get("selected_template_image", selected_template.get("image"))
            template_caption = st.session_state.get("selected_template_name", selected_template.get("name", "Template Preview"))

            if template_image:
                # If the image path is not absolute, construct an absolute path based on the current working directory.
                if not os.path.isabs(template_image):
                    image_path = os.path.join(os.getcwd(), template_image)
                else:
                    image_path = template_image

                # Optionally, verify if the file exists. If not, display an error message.
                if os.path.exists(image_path):
                    st.markdown(add_image_styling(image_path, template_caption), unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ Image file not found at: {image_path}")
            else:
                st.warning("⚠️ Template image not available")
            
            # Display the main file in a nicely styled code block
            st.markdown(f"### 📄 Main File: `{selected_template['main_file']}`")
            st.code(selected_template["main_file_content"], language="python")
            
            # Display other files in a clean accordion
            other_files = selected_template.get("other_files", {})
            if other_files:
                st.markdown("### 📁 Additional Files")
                for file_name, content in other_files.items():
                    with st.expander(f"📝 {file_name}"):
                        st.code(content, language="python")
        
        with col2:
            # Create a styled sidebar card
            st.markdown('<div class="template-card">', unsafe_allow_html=True)
            st.markdown(f"### 🧰 {selected_template.get('main_file', 'Template')} Template")
            
            # Details section
            st.markdown("#### 📋 Details")
            st.markdown(selected_template.get("details", "No details provided."))
            
            # Stack section
            st.markdown("#### 🔧 Tech Stack")
            stack_info = selected_template.get("stack", "No stack information.")
            # Create badges for each technology in the stack
            if stack_info:
                stack_items = stack_info.split(", ")
                badges_html = ""
                for item in stack_items:
                    badges_html += f'<span style="background-color: #FF4B4B; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 5px; font-weight: 500;">{item}</span>'
                st.markdown(badges_html, unsafe_allow_html=True)
            
            # Create the ZIP archive from the template
            template_zip = create_template_zip(selected_template)
            
            # Add some space
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Provide action buttons
            st.download_button(
                label="📥 Download Template",
                data=template_zip,
                file_name="template.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            st.link_button("🏗️ Create New Repository", 
                          url="https://github.com/new",
                          use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
    # Action buttons at the bottom
    col1, col2 = st.columns(2)
    
    # Button to switch to edit mode with the current template code loaded in the Ace editor
    if col1.button("✏️ Edit Template", use_container_width=True):
        st.session_state["edit_mode"] = True
        st.rerun()

    # Button to clear the current template if needed
    if col2.button("🔄 Select Another Template", use_container_width=True):
        st.session_state["selected_template"] = None
        st.rerun()
    
    st.stop()  # Stop further execution so the selection UI is not rendered.

# -------------------------------------------------------------------
# Template Selection / Generation UI (shown only if no template is selected)
# Creating a modern hero section
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">Template Lab</h1>
        <p style="font-size: 1.5rem; color: #cccccc; margin-bottom: 2rem;">
            Accelerate Your Development Workflow
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Center the logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/app logo.webp", width=350)

# Add a descriptive section
st.markdown(
    """
    <div style="background-color: rgba(30, 33, 41, 0.5); border-radius: 10px; padding: 1.5rem; margin: 2rem 0;">
        <h2 style="margin-top: 0;">Why Use Template Lab?</h2>
        <div style="display: flex; align-items: start; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-right: 1rem;">⚡</div>
            <div>
                <h3 style="margin: 0;">Accelerate Development</h3>
                <p>Skip the boilerplate setup and get straight to building what matters.</p>
            </div>
        </div>
        <div style="display: flex; align-items: start; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-right: 1rem;">🔧</div>
            <div>
                <h3 style="margin: 0;">Best Practices Built-in</h3>
                <p>All templates follow industry standards and best practices for clean, maintainable code.</p>
            </div>
        </div>
        <div style="display: flex; align-items: start;">
            <div style="font-size: 2rem; margin-right: 1rem;">🤖</div>
            <div>
                <h3 style="margin: 0;">AI-Powered Customization</h3>
                <p>Generate custom templates with our AI assistant or modify existing ones to fit your needs.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Add sidebar guide content
with st.sidebar:
    st.markdown(
        """
        <h2 style="margin-top: 0;">🧭 Guide</h2>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="template-card">
            <h3 style="margin-top: 0;">📋 Getting Started</h3>
            <ol>
                <li><strong>Browse</strong> - Select from our curated template collection</li>
                <li><strong>Generate</strong> - Create custom templates with AI</li>
                <li><strong>Customize</strong> - Edit templates to match your requirements</li>
                <li><strong>Download</strong> - Get your template and start building</li>
            </ol>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="template-card">
            <h3 style="margin-top: 0;">⚙️ Template Types</h3>
            <ul>
                <li><strong>Web Applications</strong> - Streamlit, Flask, Django</li>
                <li><strong>AI/ML Projects</strong> - LangChain, Hugging Face</li>
                <li><strong>Authentication</strong> - Local or Cloud-based</li>
                <li><strong>Custom Solutions</strong> - Generated based on your needs</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Define options for the selectbox with better styling
st.markdown("### 🚀 Get Started")
options = ["Select an option", "Browse Existing Templates", "Generate Custom Template"]

# Create a styled selectbox
selected_option = st.selectbox("Choose how you want to proceed:", options)

# Based on selection, show appropriate content
if selected_option == "Browse Existing Templates":
    st.markdown("## 📚 Template Collection")
    display_templates_component()

elif selected_option == "Generate Custom Template":
    st.markdown(
        """
        <div class="template-card">
            <h2 style="margin-top: 0;">🤖 AI Template Generator</h2>
            <p>Describe the template you need, and our AI will create it for you.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    prompt = st.text_area(
        "Describe your ideal template:",
        placeholder="Example: A Flask API with MongoDB integration and JWT authentication...",
        height=150
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🔮 Generate Template", use_container_width=True):
            with st.spinner("🧙‍♂️ Our AI is crafting your template..."):
                template = generate_template(prompt)
                # Save the generated result to session state.
                st.session_state["generated_template"] = template
                st.success("✅ New template generated! Preview it below.")
    
    # If a generated template exists, show a preview button (which opens the modal).
    if st.session_state.get("generated_template"):
        with col2:
            if st.button("👁️ Preview Template", use_container_width=True):
                open_generated_template_modal()
