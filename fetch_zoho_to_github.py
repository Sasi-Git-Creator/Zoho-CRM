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
    print("Access token response:", response.json())
    return response.json()["access_token"]

def fetch_zoho_functions(access_token):
    url = "https://www.zohoapis.com/crm/v2/functions"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    response = requests.get(url, headers=headers)
    print("Functions response:", response.json())
    return response.json().get("data", [])

def backup_to_github():
    try:
        access_token = get_access_token()
        functions = fetch_zoho_functions(access_token)

        if not functions:
            print("No functions found in Zoho CRM.")
            return

        repo = Repo.clone_from(GITHUB_REPO, REPO_PATH, branch="main")

        for func in functions:
            file_path = f"{REPO_PATH}/{func['name']}.deluge"
            print(f"Writing function to: {file_path}")
            with open(file_path, "w") as f:
                f.write(func["script"])

        print("Git status before commit:\n", repo.git.status())
        repo.git.add(A=True)
        repo.index.commit(f"Auto-update: {datetime.now()}")
        origin = repo.remote(name="origin")
        origin.push()
        print("Push to GitHub completed.")

    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    backup_to_github()
