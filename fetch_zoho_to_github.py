import os
import requests
from git import Repo
from datetime import datetime

# Configuration from environment variables
CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token must be stored securely
GITHUB_USER = "Sasi-Git-Creator"
REPO_NAME = "Zoho-CRM"
REPO_PATH = "zoho_backup"
BRANCH_NAME = "main"

# Construct GitHub repo URL using the token
GITHUB_REPO = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

def get_access_token():
    """Fetch Zoho OAuth access token using refresh token."""
    url = "https://accounts.zoho.in/oauth/v2/token"
    data = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_zoho_functions(access_token):
    """
    Placeholder: Zoho CRM does not offer a public API to fetch custom functions directly.
    This function should be replaced with a supported workaround if possible.
    """
    print("⚠️ Warning: Zoho CRM does not support fetching custom functions via API.")
    return []

def backup_to_github():
    try:
        access_token = get_access_token()
        functions = fetch_zoho_functions(access_token)

        if not functions:
            print("ℹ️ No functions found to back up.")
            return

        # Clone the repo
        repo = Repo.clone_from(GITHUB_REPO, REPO_PATH, branch=BRANCH_NAME)

        # Write each function into a .deluge file
        for func in functions:
            file_path = os.path.join(REPO_PATH, f"{func['name']}.deluge")
            with open(file_path, "w") as f:
                f.write(func["script"])

        # Stage, commit, and push changes
        repo.git.add(A=True)
        repo.index.commit(f"Auto-backup: {datetime.now().isoformat()}")
        origin = repo.remote(name="origin")
        origin.push()

        print("✅ Backup pushed to GitHub successfully.")

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.text}")
    except Exception as e:
        print(f"❌ Error during backup: {e}")

if __name__ == "__main__":
    backup_to_github()
