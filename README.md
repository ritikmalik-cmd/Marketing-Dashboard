# Marketing Leads Dashboard

A comprehensive Streamlit dashboard for analyzing marketing leads from Zoho CRM with advanced filtering and analytics capabilities.

## Features

### 📊 **Comprehensive Analytics**
- **Real-time Lead Metrics** - Track total leads and breakdown by sources
- **Lead Status Overview** - Monitor pipeline status including "Not Set" leads
- **Interactive Charts** - Pie charts and trend analysis
- **Export Functionality** - Download filtered data as CSV

### 🔧 **Advanced Filtering**
- **Lead Sources** - Google Ads 2025, WhatsApp Marketing, Form Submission, Self Created
- **Lead Owners** - Filter by specific team members
- **Lead Status** - All statuses including unassigned leads
- **Date Range** - Multiple presets (Today, Last 7/30/90 days, Custom range)

### 📈 **Key Metrics Tracked**
- Total Leads Count
- Google Ads Performance
- WhatsApp Marketing Results
- Form Submission Leads
- Self Created Leads
- Lead Status Distribution (New, Contacted, Qualified, Not Set, etc.)

### 🎯 **Target Lead Sources**
- Google Ads 2025
- Whatsapp Marketing
- Form Submission
- Self Created

### 👥 **Filtered Lead Owners**
- aakib.posharkar@xmonks.com
- ankita.vinayak@xmonks.com
- preeti@erickson.co.in
- rejna.balan@xmonks.com
- saurav.tiwari@xmonks.com

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ritikmalik-cmd/Marketing-Dashboard.git
cd Marketing-Dashboard
```

2. **Install required packages:**
```bash
pip install streamlit requests pandas plotly
```

3. **Configure Zoho CRM credentials:**
Update the following variables in `full_dashboard.py`:
```python
ZOHO_CLIENT_ID = "your_client_id"
ZOHO_CLIENT_SECRET = "your_client_secret"
ZOHO_REFRESH_TOKEN = "your_refresh_token"
```

## Usage

1. **Run the dashboard:**
```bash
streamlit run full_dashboard.py
```

2. **Access the dashboard:**
Open your browser and go to `http://localhost:8501`

3. **Use the filters:**
- Use sidebar filters to customize your view
- Select date ranges for trend analysis
- Export filtered data for further analysis

## Dashboard Sections

### 🏠 **Overview**
- Lead Sources Overview (Total, Google Ads, WhatsApp, Form Submissions, Self Created)
- Lead Status Overview (Top 5 most common statuses with smart icons)

### 📊 **Analytics**
- Lead Distribution Pie Chart by Source
- Daily Leads Trend Line Chart

### 📋 **Leads Details**
- Comprehensive leads table with all lead information
- Export functionality for filtered results
- Real-time lead counts

## Features Highlights

- **Pagination Support** - Handles up to 5,000 leads with automatic pagination
- **Smart Status Tracking** - Includes "Not Set" for unassigned leads
- **Dynamic Filters** - Automatically adapts to your CRM data
- **Export Capabilities** - Download filtered results with timestamps
- **Real-time Updates** - Refresh data directly from Zoho CRM
- **Responsive Design** - Works on desktop and mobile devices

## Requirements

- Python 3.7+
- Streamlit
- Requests
- Pandas
- Plotly
- Valid Zoho CRM API credentials

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.

---

**Last Updated:** November 10, 2025
**Dashboard Version:** Enhanced with Lead Status Filtering