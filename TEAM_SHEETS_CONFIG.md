# Team Member Sheets - Quick Setup

## ✅ Configuration Complete!

Your Google Sheet has been configured with all 7 team member tabs:

### Team Members & Sheet IDs:
1. **Rejna** - GID: 1751742792
2. **Saurav** - GID: 454155290  
3. **Aakib** - GID: 1998718961
4. **Ankisha** - GID: 1664806045
5. **Priyanka** - GID: 828536614
6. **Ankita** - GID: 768744776
7. **Sujal** - GID: 507391559

### Google Sheet ID:
`1jS9itYg7DccpssVn0vaabiP7LJyjoVoic_i1dqNIdXE`

## 🚀 Next Steps to Get Started:

### 1. Create Google Service Account
Follow the detailed guide in `GOOGLE_SHEETS_SETUP.md` to:
- Create a Google Cloud project
- Enable Google Sheets API
- Create a service account
- Download `credentials.json`

### 2. Place credentials.json
Save the downloaded file as:
```
C:\Users\xMonks\Downloads\Marketing-Dashboard-main\Marketing-Dashboard-main\credentials.json
```

### 3. Share Your Google Sheet
**IMPORTANT:** Share your Google Sheet with the service account email:
- Open: https://docs.google.com/spreadsheets/d/1jS9itYg7DccpssVn0vaabiP7LJyjoVoic_i1dqNIdXE/edit
- Click "Share" button
- Add the email from `credentials.json` → look for `client_email` field
- Give "Viewer" permission
- Click "Send"

### 4. Run the Dashboard
```powershell
C:/Users/xMonks/Downloads/Marketing-Dashboard-main/Marketing-Dashboard-main/.venv/Scripts/streamlit.exe run full_dashboard.py
```

### 5. Use the Dashboard
1. Open: http://localhost:8501
2. Click the "📊 Frejun Dashboard" tab
3. Select a team member from the dropdown
4. Click "🔄 Load Sheet Data"
5. View their performance data!

## 📊 Dashboard Features

### Team Member Selection
- **Dropdown menu** in sidebar to select any team member
- **Auto-loads** data for the selected team member
- **Switches seamlessly** between team members

### For Each Team Member You Can:
- ✅ View their complete data table
- ✅ Filter by any column
- ✅ Generate automatic visualizations (bar, pie, line charts)
- ✅ View summary statistics
- ✅ Export their data as CSV
- ✅ Track performance metrics

## 🔍 How It Works

Each team member has their own sheet tab in your Google Spreadsheet:
- The dashboard reads the specific GID for each person
- When you select a team member, it loads their sheet
- All visualizations and analytics are specific to that person
- Data is kept separate and organized

## 📝 Example Usage Flow

1. Select "Rejna" from dropdown
2. Click "Load Sheet Data"
3. View Rejna's performance metrics
4. Generate charts to analyze trends
5. Switch to "Saurav" to view his data
6. Compare performance across team members

## ⚙️ Current Configuration in .env

```env
GOOGLE_SHEET_ID=1jS9itYg7DccpssVn0vaabiP7LJyjoVoic_i1dqNIdXE

SHEET_REJNA=1751742792
SHEET_SAURAV=454155290
SHEET_AAKIB=1998718961
SHEET_ANKISHA=1664806045
SHEET_PRIYANKA=828536614
SHEET_ANKITA=768744776
SHEET_SUJAL=507391559
```

## 🎯 What's Already Done

✅ Google Sheet ID configured  
✅ All 7 team member GIDs configured  
✅ Dashboard updated with team member selector  
✅ Multi-tab support implemented  
✅ Export functionality personalized per team member  

## ⏭️ What You Need to Do

⬜ Create Google Cloud service account  
⬜ Download and save credentials.json  
⬜ Share Google Sheet with service account email  
⬜ Run the dashboard  

## 🆘 Troubleshooting

**"Credentials file not found"**
→ Make sure `credentials.json` is in the project root directory

**"Permission denied"**
→ Share the Google Sheet with the service account email from credentials.json

**"No data found for [Team Member]"**
→ Check that the team member's sheet tab exists and has data

**"Sheet with GID not found"**
→ Verify the GID matches the actual sheet tab in Google Sheets

## 📞 Support

For detailed setup instructions, see:
- `GOOGLE_SHEETS_SETUP.md` - Complete setup guide
- `QUICKSTART_SHEETS.md` - Quick reference

Your Google Sheet URL:
https://docs.google.com/spreadsheets/d/1jS9itYg7DccpssVn0vaabiP7LJyjoVoic_i1dqNIdXE/edit?usp=sharing
