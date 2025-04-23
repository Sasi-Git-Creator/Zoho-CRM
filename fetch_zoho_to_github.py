import requests
import os
from git import Repo
from datetime import datetime

# Configuration
CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
REPO_PATH = "zoho_backup"
GITHUB_REPO = "https://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@github.com/Sasi-Git-Creator/Zoho-CRM"

# Function to get the access token using the refresh token
def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"
    data = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    return response.json()["access_token"]

# Function to fetch Zoho CRM data (Leads in this case)
def fetch_zoho_data(access_token):
    url = "https://www.zohoapis.com/crm/v2/Leads"  # You can change this to any module like Deals, Contacts, etc.
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("data", [])

# Function to backup data to GitHub repository
def backup_to_github():
    access_token = get_access_token()  # Get access token
    data = fetch_zoho_data(access_token)  # Fetch Zoho CRM data (Leads)
    
    # Clone the GitHub repository (backup folder)
    repo = Repo.clone_from(GITHUB_REPO, REPO_PATH, branch="main")
    
    # Loop through the fetched records and save them as JSON files in the repo
    for record in data:
        with open(f"{REPO_PATH}/{record['id']}.json", "w") as f:
            f.write(str(record))
    
    # Add all the changes and commit
    repo.git.add(A=True)
    repo.index.commit(f"Auto-update: {datetime.now()}")
    
    # Push changes to GitHub
    origin = repo.remote(name="origin")
    origin.push()

# Main entry point to run the backup
if __name__ == "__main__":
    backup_to_github()
