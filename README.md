# Zoho CRM Code Sync

This repository automatically syncs custom scripts/functions from Zoho CRM to GitHub using GitHub Actions.

## 📌 Purpose
- **Backup**: Securely store Zoho CRM Deluge scripts.
- **Version Control**: Track changes over time.
- **Disaster Recovery**: Restore scripts if Zoho data is lost.

## ⚙️ Setup
1. **Zoho OAuth**: Configured with `ZohoCRM.settings.ALL` scope.
2. **GitHub Secrets**:
   - `ZOHO_CLIENT_ID`
   - `ZOHO_CLIENT_SECRET` 
   - `ZOHO_REFRESH_TOKEN`
3. **Automation**: Runs daily via [GitHub Actions](.github/workflows/sync_zoho.yml).

## 📂 File Structure
- `scripts/`: Stores exported `.deluge` files.
- `logs/`: Sync history (optional).

## 🔄 Manual Trigger
Go to **Actions → Sync Zoho to GitHub → Run workflow**.

---

> **Note**: This README will initialize your `main` branch, fixing the "invalid ref" error.
