# 🎉 Google Sheets Integration - READY TO USE!

## ✅ What's Been Configured

Your dashboard now supports **7 team members** with individual Google Sheet tabs:

| Team Member | GID         | Status |
|-------------|-------------|---------|
| Rejna       | 1751742792  | ✅ Configured |
| Saurav      | 454155290   | ✅ Configured |
| Aakib       | 1998718961  | ✅ Configured |
| Ankisha     | 1664806045  | ✅ Configured |
| Priyanka    | 828536614   | ✅ Configured |
| Ankita      | 768744776   | ✅ Configured |
| Sujal       | 507391559   | ✅ Configured |

**Google Sheet URL:** https://docs.google.com/spreadsheets/d/1jS9itYg7DccpssVn0vaabiP7LJyjoVoic_i1dqNIdXE/edit?usp=sharing

## 🚀 ONE THING LEFT: Get Your Credentials

You need to create a Google Service Account and download `credentials.json`:

### Quick Steps:

1. **Go to:** https://console.cloud.google.com/
2. **Create project** (or use existing)
3. **Enable** "Google Sheets API"
4. **Create Service Account:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name it "Marketing Dashboard"
   - Download the JSON key file
5. **Rename file** to `credentials.json`
6. **Save it here:**
   ```
   C:\Users\xMonks\Downloads\Marketing-Dashboard-main\Marketing-Dashboard-main\credentials.json
   ```

7. **Share your Google Sheet:**
   - Open your sheet
   - Click "Share"
   - Add the email from credentials.json (the `client_email` field)
   - Give it "Viewer" access

## 🎯 Then Run the Dashboard:

```powershell
C:/Users/xMonks/Downloads/Marketing-Dashboard-main/Marketing-Dashboard-main/.venv/Scripts/streamlit.exe run full_dashboard.py
```

Open: **http://localhost:8501**

## 📊 How to Use:

1. Click "📊 Frejun Dashboard" tab
2. Select a team member from dropdown (e.g., "Rejna")
3. Click "🔄 Load Sheet Data"
4. View their data, charts, and analytics!

## 🎨 Features Available:

- ✅ **Team Member Selector** - Choose any of the 7 team members
- ✅ **Auto-Load Data** - Pulls data from their specific sheet tab
- ✅ **Interactive Filtering** - Filter by any column
- ✅ **Auto Visualizations** - Bar, Pie, and Line charts
- ✅ **Summary Stats** - Descriptive statistics
- ✅ **CSV Export** - Download data with team member name
- ✅ **Seamless Switching** - Switch between team members instantly

## 📁 Files Created/Updated:

- ✅ `.env` - Google Sheet ID and team GIDs configured
- ✅ `sheets_integration.py` - Multi-tab support added
- ✅ `full_dashboard.py` - Team member selector integrated
- ✅ `requirements.txt` - Google API packages added
- ✅ `TEAM_SHEETS_CONFIG.md` - Team setup reference
- ✅ `GOOGLE_SHEETS_SETUP.md` - Detailed setup guide
- ✅ `QUICKSTART_SHEETS.md` - Quick reference

## 🔐 Security:

Your `credentials.json` file is protected:
- ✅ Added to `.gitignore`
- ✅ Will NOT be committed to Git
- ✅ Keep it secure and local

## 💡 Pro Tips:

1. **Test with one team member first** (e.g., Rejna)
2. **Make sure sheet tabs have data** before loading
3. **Use the same sheet structure** for all team members for best results
4. **Export CSV** to backup team member data regularly

## 🆘 Need Help?

See these guides:
- `TEAM_SHEETS_CONFIG.md` - Team-specific setup
- `GOOGLE_SHEETS_SETUP.md` - Detailed Google Cloud setup
- `QUICKSTART_SHEETS.md` - Quick reference guide

## ✨ You're Almost Ready!

Just get your `credentials.json` file and you're good to go! 🚀
