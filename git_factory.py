import webbrowser
import os
import git
import tempfile
import shutil

def open_github_new_project():
    # URL for creating a new repository on GitHub
    github_new_repo_url = "https://github.com/new"
    
    # Open the URL in the default web browser
    webbrowser.open(github_new_repo_url)

# Call the function to open the page
#open_github_new_project()



def push_template_to_github(repo_url, template_code, commit_message="Update template"):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as repo_dir:
        # Clone the repository to the temporary directory
        repo = git.Repo.clone_from(repo_url, repo_dir)

        # Write the template code to a file in the repository
        template_file_path = os.path.join(repo_dir, "template.py")  # Adjust the file path as needed
        with open(template_file_path, "w") as f:
            f.write(template_code)

        # Add the changes to the staging area
        repo.git.add(template_file_path)

        # Commit the changes
        repo.git.commit("-m", commit_message)

        # Push the changes to the remote repository
        repo.git.push()

'''
# Example usage
repo_url = "https://github.com/yourusername/yourrepo.git"
template_code = """
# Your template code here
print("Hello, GitHub!")
"""
push_template_to_github(repo_url, template_code)
'''
