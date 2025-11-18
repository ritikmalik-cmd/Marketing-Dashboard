# Google Sheets Integration Setup Guide

## Overview
Your dashboard now has two tabs:
1. **CRM Leads Dashboard** - Your existing Zoho CRM integration (unchanged)
2. **Frejun Dashboard** - New Google Sheets integration for visualizing Excel data

## Prerequisites
- Google Cloud Platform account
- A Google Sheet you want to visualize
- Service account credentials

## Setup Instructions

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### Step 2: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `Marketing Dashboard Service`
   - Description: `Service account for marketing dashboard`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

### Step 3: Download Credentials

1. Find your newly created service account in the list
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose "JSON" format
6. Click "Create" - this will download a JSON file
7. **Rename the file to `credentials.json`**
8. **Move it to your project directory:**
   ```
   C:\Users\xMonks\Downloads\Marketing-Dashboard-main\Marketing-Dashboard-main\credentials.json
   ```

### Step 4: Share Your Google Sheet

1. Open your Google Sheet
2. Note the **Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit#gid=[GID]
   ```
3. Click the "Share" button
4. Add the service account email (found in credentials.json):
   - Look for the `client_email` field
   - Example: `marketing-dashboard@project-id.iam.gserviceaccount.com`
5. Give it "Viewer" permission
6. Click "Send"

### Step 5: Update .env File

Update your `.env` file with the following:

```env
# Google Sheets Integration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_actual_sheet_id_here
GOOGLE_SHEET_GID=0
```

Replace:
- `GOOGLE_SHEET_ID`: The ID from your Google Sheet URL
- `GOOGLE_SHEET_GID`: The specific sheet/tab to load (0 for first sheet, or specific GID from URL)

### Step 6: Run the Dashboard

```powershell
C:/Users/xMonks/Downloads/Marketing-Dashboard-main/Marketing-Dashboard-main/.venv/Scripts/streamlit.exe run full_dashboard.py
```

## Features

### Frejun Dashboard Capabilities:

1. **Automatic Data Loading**
   - Loads data from your Google Sheet
   - Shows data overview (rows, columns, numeric columns)

2. **Data Filtering**
   - Filter by any column values
   - Interactive column selection

3. **Visualizations**
   - Bar charts for categorical vs numeric data
   - Pie charts for distribution analysis
   - Line charts for trend analysis
   - Auto-detects numeric and categorical columns

4. **Data Export**
   - Export filtered data as CSV
   - Download with timestamp

5. **Summary Statistics**
   - Descriptive statistics for numeric columns
   - Count, mean, std, min, max, quartiles

## Troubleshooting

### "Credentials file not found"
- Ensure `credentials.json` is in the project root directory
- Check the file name is exactly `credentials.json`

### "No data found"
- Verify your Google Sheet ID is correct
- Check that you've shared the sheet with the service account email
- Ensure the sheet has data in it

### "Permission denied"
- Make sure you shared the Google Sheet with the service account email
- Verify the service account has at least "Viewer" permission

### "Sheet not found"
- Check if the GID is correct
- Try setting `GOOGLE_SHEET_GID=0` to use the first sheet

## Example .env Configuration

```env
# Zoho CRM API Credentials
ZOHO_CLIENT_ID=1000.JY4N7CSGP5S31JKJFEMJTSBZGJL2EJ
ZOHO_CLIENT_SECRET=60ab68b202ff2d73e9113cadeaf6f17218c8e3febb
ZOHO_REFRESH_TOKEN=1000.985a431241ab09913d864dfa4e3d66fd.1658f0fc3616853d44d9dcac4ef42104

# Google Sheets Integration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
GOOGLE_SHEET_GID=0
```

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit `credentials.json` to Git**
   - Add it to `.gitignore`
   
2. **Never share your credentials file**
   - Contains sensitive authentication data

3. **Limit service account permissions**
   - Only give "Viewer" access to sheets
   - Don't use owner or editor permissions unless needed

4. **Keep credentials.json secure**
   - Don't share or upload to public locations
   - Store securely on your local machine

## Advanced Usage

### Using Specific Sheet Tabs

If your spreadsheet has multiple tabs/sheets, you can specify which one to load:

1. Open your Google Sheet
2. Click on the tab you want to use
3. Look at the URL - it will show `gid=XXXXXXX`
4. Update `.env`: `GOOGLE_SHEET_GID=XXXXXXX`

### Multiple Sheets

To work with multiple sheets, you can:
1. Create separate dashboard instances with different GIDs
2. Or modify the code to add a sheet selector in the UI

## Support

For issues or questions:
- Check the troubleshooting section above
- Verify all setup steps are completed
- Ensure credentials are correctly configured
