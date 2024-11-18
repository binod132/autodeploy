import os
import requests
import subprocess

# GitLab details
GITLAB_URL = "http://192.168.130.129"  # Your GitLab server URL
GROUP_NAME = "hmis"  # Replace with your group's name
ACCESS_TOKEN = os.getenv("GITLAB_TOKEN")  # Replace with your GitLab PAT

# Directory to clone repositories into
CLONE_DIR = "./gitlab_repos"

# Headers for API authentication
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def get_repositories(group_name):
    """Fetch all repositories from a GitLab group."""
    repos = []
    page = 1
    while True:
        url = f"{GITLAB_URL}/api/v4/groups/{group_name}/projects?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repositories: {response.text}")
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def clone_repositories(repos, clone_dir):
    """Clone all repositories into the specified directory using HTTP."""
    os.makedirs(clone_dir, exist_ok=True)
    os.chdir(clone_dir)
    for repo in repos:
        repo_name = repo["name"]
        # Replace 'https' with 'http' for non-secure cloning
        repo_url = repo["http_url_to_repo"].replace("https://", "http://")
        
        # Skip if repository already exists
        if os.path.exists(repo_name):
            print(f"Repository '{repo_name}' already exists. Skipping...")
            continue
        
        print(f"Cloning repository: {repo_name}")
        subprocess.run(["git", "clone", repo_url])

if __name__ == "__main__":
    try:
        print("Fetching repositories...")
        repositories = get_repositories(GROUP_NAME)
        print(f"Found {len(repositories)} repositories.")
        clone_repositories(repositories, CLONE_DIR)
        print("All repositories cloned successfully.")
    except Exception as e:
        print(f"Error: {e}")
