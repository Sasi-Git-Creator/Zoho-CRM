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

def fetch_zoho_functions(access_token):
    url = "https://www.zohoapis.com/crm/v2/functions"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("data", [])

def backup_to_github():
    access_token = get_access_token()
    functions = fetch_zoho_functions(access_token)
    
    repo = Repo.clone_from(GITHUB_REPO, REPO_PATH, branch="main")
    
    for func in functions:
        with open(f"{REPO_PATH}/{func['name']}.deluge", "w") as f:
            f.write(func["script"])
    
    repo.git.add(A=True)
    repo.index.commit(f"Auto-update: {datetime.now()}")
    origin = repo.remote(name="origin")
    origin.push()

if __name__ == "__main__":
    backup_to_github()
