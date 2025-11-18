# Quick Start Guide - Google Sheets Integration

## What You Need

1. **Google Sheet ID** - Get it from your sheet URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit#gid=0
   ```

2. **credentials.json** - Service account credentials from Google Cloud Console

3. **Share your sheet** - With the service account email from credentials.json

## Quick Setup (5 Steps)

### 1. Get Service Account Credentials
- Go to: https://console.cloud.google.com/
- Enable Google Sheets API
- Create Service Account → Download JSON → Rename to `credentials.json`
- Place in: `C:\Users\xMonks\Downloads\Marketing-Dashboard-main\Marketing-Dashboard-main\`

### 2. Update .env File
```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=paste_your_sheet_id_here
GOOGLE_SHEET_GID=0
```

### 3. Share Your Google Sheet
- Open your Google Sheet
- Click "Share"
- Add the email from `credentials.json` (field: `client_email`)
- Give "Viewer" permission

### 4. Run Dashboard
```powershell
C:/Users/xMonks/Downloads/Marketing-Dashboard-main/Marketing-Dashboard-main/.venv/Scripts/streamlit.exe run full_dashboard.py
```

### 5. Access Dashboard
- Open: http://localhost:8501
 - Click "Frejun Dashboard" tab
- Click "Load Sheet Data"

## Dashboard Features

### Two Tabs:
1. **🔍 CRM Leads Dashboard** - Your existing Zoho CRM (unchanged)
2. **📊 Frejun Dashboard** - New Google Sheets visualization

### Sheets Dashboard Features:
- ✅ Automatic data loading from Google Sheets
- ✅ Interactive data table
- ✅ Column-based filtering
- ✅ Auto-generated visualizations:
  - Bar charts
  - Pie charts
  - Line charts (trends)
- ✅ Summary statistics
- ✅ CSV export

## Example Sheet Structure

Your Google Sheet can have any structure. The dashboard will:
- Auto-detect numeric vs text columns
- Create appropriate visualizations
- Allow filtering on any column

Example:
| Month | Sales | Region | Product |
|-------|-------|--------|---------|
| Jan   | 5000  | North  | Widget  |
| Feb   | 6200  | South  | Gadget  |

## Troubleshooting

**"Credentials file not found"**
→ Check `credentials.json` is in the project root

**"No data found"**
→ Verify Sheet ID and that sheet is shared

**"Permission denied"**
→ Share the sheet with service account email

## Security

🔒 **Never commit these files to Git:**
- credentials.json (already in .gitignore)
- .env (already in .gitignore)

## Need Help?

See detailed guide: `GOOGLE_SHEETS_SETUP.md`
