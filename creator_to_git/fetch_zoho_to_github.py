import requests
import os
from git import Repo
from datetime import datetime

# === 🔧 CONFIGURATION ===
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")
OWNER_NAME = "Sasi-Git-Creator"  # Your GitHub username
APP_NAME = "crm-function-backup"
REPORT_LINK_NAME = "All_Function_Backups"

GITHUB_TOKEN = os.getenv("GTB_TOKEN")
GITHUB_REPO = "Zoho-CRM"
LOCAL_CLONE_PATH = "/tmp/deluge_sync"

# === 📡 FETCH DATA FROM CREATOR ===
def fetch_deluge_functions():
    print("📡 Fetching Deluge functions from Zoho Creator...")
    url = f"https://creator.zoho.in/api/v2/excell/crm-function-backup/report/All_Function_Backups"
    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("data", [])

# === 📝 SAVE EACH FUNCTION TO FILE ===
def write_functions_to_files(data):
    os.makedirs(LOCAL_CLONE_PATH, exist_ok=True)
    for record in data:
        name = record["Function_Name"].strip().replace(" ", "_")
        code = record["Function_Code"]
        file_path = os.path.join(LOCAL_CLONE_PATH, f"{name}.deluge")
        with open(file_path, "w") as file:
            file.write(code)
    print("✅ Saved all functions locally in:", LOCAL_CLONE_PATH)

# === 🧬 GIT COMMIT AND PUSH ===
def push_to_github():
    repo_url = f"https://{GITHUB_TOKEN}@github.com/{OWNER_NAME}/{GITHUB_REPO}.git"
    if os.path.exists(os.path.join(LOCAL_CLONE_PATH, ".git")):
        repo = Repo(LOCAL_CLONE_PATH)
    else:
        print("📥 Cloning fresh repo...")
        repo = Repo.clone_from(repo_url, LOCAL_CLONE_PATH)

    repo.git.add(A=True)
    repo.index.commit(f"Backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    repo.remote().push()
    print("🚀 Pushed changes to GitHub!")

# === 🚀 RUN EVERYTHING ===
if __name__ == "__main__":
    data = fetch_deluge_functions()
    write_functions_to_files(data)
    push_to_github()
