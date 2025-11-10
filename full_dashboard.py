import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# -----------------------------
# Zoho CRM API details
# -----------------------------
ZOHO_CLIENT_ID = "1000.JY4N7CSGP5S31JKJFEMJTSBZGJL2EJ"
ZOHO_CLIENT_SECRET = "60ab68b202ff2d73e9113cadeaf6f17218c8e3febb"
ZOHO_REFRESH_TOKEN = "1000.985a431241ab09913d864dfa4e3d66fd.1658f0fc3616853d44d9dcac4ef42104"

class ZohoCRM:
    def __init__(self):
        self.base_url = "https://www.zohoapis.com/crm/v2"
        self.access_token = None
        
    def get_access_token(self):
        """Get access token using refresh token"""
        url = "https://accounts.zoho.com/oauth/v2/token"
        
        data = {
            'refresh_token': ZOHO_REFRESH_TOKEN,
            'client_id': ZOHO_CLIENT_ID,
            'client_secret': ZOHO_CLIENT_SECRET,
            'grant_type': 'refresh_token'
        }
        
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            return True
        except Exception as e:
            st.error(f"Failed to get access token: {e}")
            return False
    
    def get_leads(self, count=5000):
        """Get leads from CRM with pagination support"""
        if not self.access_token:
            return None
            
        url = f"{self.base_url}/Leads"
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        all_leads = []
        page = 1
        per_page = 200  # Zoho's maximum per page
        
        try:
            while len(all_leads) < count:
                params = {
                    'sort_by': 'Created_Time',
                    'sort_order': 'desc',
                    'per_page': per_page,
                    'page': page
                }
                
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                leads_data = response.json()
                
                page_leads = leads_data.get('data', [])
                if not page_leads:
                    break
                    
                all_leads.extend(page_leads)
                
                # Check if there are more records
                info = leads_data.get('info', {})
                if not info.get('more_records', False):
                    break
                    
                page += 1
                
                # Safety check to prevent infinite loop
                if page > 50:  # Max 50 pages = 10,000 leads
                    break
            
            # Return only the requested count
            return all_leads[:count]
            
        except Exception as e:
            st.error(f"Failed to fetch leads: {e}")
            return None
    
    def get_lead_owners(self, leads):
        """Get lead owners from CRM data and filter to show only the 5 specific email addresses"""
        # The 5 specific email addresses we want to show
        target_emails = [
            'aakib.posharkar@xmonks.com',
            'ankita.vinayak@xmonks.com', 
            'preeti@erickson.co.in',
            'rejna.balan@xmonks.com',
            'saurav.tiwari@xmonks.com'
        ]
        
        # Get actual owners from CRM data
        actual_owners = set()
        owner_email_map = {}  # Map display name to email
        
        for lead in leads:
            owner_data = lead.get('Owner', {})
            owner_name = owner_data.get('name')
            owner_email = owner_data.get('email')
            
            if owner_name and owner_email:
                actual_owners.add(owner_name)
                owner_email_map[owner_name] = owner_email
        
        # Filter to only show owners whose emails are in our target list
        filtered_owners = []
        for owner_name in actual_owners:
            owner_email = owner_email_map.get(owner_name)
            if owner_email and owner_email in target_emails:
                filtered_owners.append(owner_name)
        
        return sorted(filtered_owners)
    
    def get_lead_statuses(self, leads):
        """Get unique lead statuses from CRM data, including 'Not Set' for leads without status"""
        statuses = set()
        has_empty_status = False
        
        for lead in leads:
            status = lead.get('Lead_Status')
            if status:
                statuses.add(status)
            else:
                has_empty_status = True
        
        # Add "Not Set" if there are leads without status
        if has_empty_status:
            statuses.add('Not Set')
            
        return sorted(list(statuses))

def filter_leads(leads, lead_sources=None, lead_owner=None, lead_status=None, start_date=None, end_date=None):
    """Filter leads based on criteria"""
    if not leads:
        return []
    
    filtered = leads.copy()
    
    # Filter by lead sources
    if lead_sources:
        filtered = [lead for lead in filtered if lead.get('Lead_Source') in lead_sources]
    
    # Filter by lead owner
    if lead_owner and lead_owner != "All":
        filtered = [lead for lead in filtered if lead.get('Owner', {}).get('name') == lead_owner]
    
    # Filter by lead status
    if lead_status and lead_status != "All":
        if lead_status == "Not Set":
            # Filter for leads with no status or empty status
            filtered = [lead for lead in filtered if not lead.get('Lead_Status')]
        else:
            # Filter for leads with the specific status
            filtered = [lead for lead in filtered if lead.get('Lead_Status') == lead_status]
    
    # Filter by date range
    if start_date or end_date:
        date_filtered = []
        for lead in filtered:
            created_time = lead.get('Created_Time')
            if created_time:
                try:
                    dt = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                    lead_date = dt.date()
                    
                    if start_date and end_date:
                        if start_date <= lead_date <= end_date:
                            date_filtered.append(lead)
                    elif start_date:
                        if lead_date >= start_date:
                            date_filtered.append(lead)
                    elif end_date:
                        if lead_date <= end_date:
                            date_filtered.append(lead)
                except:
                    continue
        filtered = date_filtered
    
    return filtered

def create_scoreboard(leads):
    """Create comprehensive metric cards for both sources and status"""
    total_leads = len(leads)
    
    # Lead Sources metrics
    google_ads = len([l for l in leads if l.get('Lead_Source') == 'Google Ads 2025'])
    whatsapp = len([l for l in leads if l.get('Lead_Source') == 'Whatsapp Marketing'])
    form_submission = len([l for l in leads if l.get('Lead_Source') == 'Form Submission'])
    self_created = len([l for l in leads if l.get('Lead_Source') == 'Self Created'])
    
    # Lead Status metrics - include ALL leads (including those with no status)
    status_counts = {}
    for lead in leads:
        status = lead.get('Lead_Status')
        if status:
            status_counts[status] = status_counts.get(status, 0) + 1
        else:
            # Count leads with no status as "Not Set" or "Pending"
            status_counts['Not Set'] = status_counts.get('Not Set', 0) + 1
    
    # Sort by count and get top statuses
    sorted_statuses = sorted(status_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Lead Sources Row
    st.subheader("📂 Lead Sources Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🎯 Total Leads", total_leads)
    
    with col2:
        st.metric("🔍 Google Ads", google_ads)
    
    with col3:
        st.metric("💬 WhatsApp", whatsapp)
    
    with col4:
        st.metric("📝 Form Submissions", form_submission)
    
    with col5:
        st.metric("✏️ Self Created", self_created)
    
    # Add some spacing
    st.markdown("---")
    
    # Lead Status Row
    st.subheader("📊 Lead Status Overview")
    
    if sorted_statuses:
        # Create columns based on number of statuses (max 5)
        num_statuses = min(len(sorted_statuses), 5)
        status_cols = st.columns(num_statuses)
        
        # Status icons mapping
        status_icons = {
            'New': '🆕',
            'Contacted': '📞',
            'Qualified': '✅',
            'Unqualified': '❌',
            'Converted': '🎉',
            'Lost': '💔',
            'Not Contacted': '📋',
            'Attempting to Contact': '🔄',
            'Contact in Future': '📅',
            'Pre-Qualified': '⭐',
            'Not Qualified': '🚫',
            'Junk Lead': '🗑️',
            'Not Set': '❓'
        }
        
        for i, (status, count) in enumerate(sorted_statuses[:num_statuses]):
            with status_cols[i]:
                # Get appropriate icon or use default
                icon = status_icons.get(status, '📈')
                st.metric(f"{icon} {status}", count)
    else:
        st.info("No status data available")

def create_charts(leads):
    """Create visualization charts"""
    if not leads:
        st.warning("No data available for charts")
        return
    
    # Prepare data
    df = pd.DataFrame(leads)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for lead sources
        if 'Lead_Source' in df.columns:
            source_counts = df['Lead_Source'].value_counts()
            fig_pie = px.pie(
                values=source_counts.values, 
                names=source_counts.index,
                title="Lead Distribution by Source",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No source data available")
    
    with col2:
        # Daily trend chart
        if 'Created_Time' in df.columns:
            df['Date'] = pd.to_datetime(df['Created_Time']).dt.date
            daily_counts = df.groupby(['Date', 'Lead_Source']).size().unstack(fill_value=0)
            
            fig_line = go.Figure()
            colors = {
                'Google Ads 2025': '#FF6B6B', 
                'Whatsapp Marketing': '#4ECDC4', 
                'Form Submission': '#45B7D1',
                'Self Created': '#FECA57'
            }
            
            for source in daily_counts.columns:
                fig_line.add_trace(go.Scatter(
                    x=daily_counts.index,
                    y=daily_counts[source],
                    mode='lines+markers',
                    name=source,
                    line=dict(color=colors.get(source, '#888888'), width=3)
                ))
            
            fig_line.update_layout(
                title="Daily Leads Trend",
                xaxis_title="Date",
                yaxis_title="Number of Leads",
                height=400
            )
            
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No date data available")

def create_leads_table(leads):
    """Create leads data table"""
    if not leads:
        st.warning("No leads data available")
        return
    
    # Prepare table data
    table_data = []
    for lead in leads:
        table_data.append({
            'Name': f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip(),
            'Email': lead.get('Email', 'N/A'),
            'Phone': lead.get('Phone', 'N/A'),
            'Company': lead.get('Company', 'N/A'),
            'Source': lead.get('Lead_Source', 'N/A'),
            'Status': lead.get('Lead_Status', 'N/A'),
            'Owner': lead.get('Owner', {}).get('name', 'N/A'),
            'Created': lead.get('Created_Time', 'N/A')
        })
    
    df = pd.DataFrame(table_data)
    
    # Format created date
    if 'Created' in df.columns:
        try:
            df['Created'] = pd.to_datetime(df['Created']).dt.strftime('%Y-%m-%d %H:%M')
        except:
            pass
    
    st.dataframe(df, use_container_width=True, height=400)

def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="Marketing Leads Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    # Header
    st.title("📊 Marketing Leads Dashboard")
    st.markdown("Real-time insights from Zoho CRM with advanced filtering")
    
    # Initialize CRM
    if 'crm' not in st.session_state:
        st.session_state.crm = ZohoCRM()
    
    # Sidebar for filters
    st.sidebar.header("🔧 Filters & Controls")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        with st.spinner("Connecting to Zoho CRM..."):
            if st.session_state.crm.get_access_token():
                st.session_state.leads = st.session_state.crm.get_leads()
                st.sidebar.success("✅ Data refreshed!")
                time.sleep(1)  # Brief pause to show success message
            else:
                st.sidebar.error("❌ Connection failed!")
                st.session_state.leads = []
    
    # Load data if not exists
    if 'leads' not in st.session_state:
        with st.spinner("Loading initial data..."):
            if st.session_state.crm.get_access_token():
                st.session_state.leads = st.session_state.crm.get_leads()
            else:
                st.session_state.leads = []
    
    # Get all leads
    all_leads = st.session_state.get('leads', [])
    
    if not all_leads:
        st.error("❌ No data available. Please check your connection and refresh.")
        st.sidebar.info("Click 'Refresh Data' to load leads from Zoho CRM")
        return
    
    # Target marketing sources
    target_sources = ['Google Ads 2025', 'Whatsapp Marketing', 'Form Submission', 'Self Created']
    
    # Debug: Show sample owner data structure
    if all_leads:
        st.sidebar.subheader("🔍 Debug Info")
        with st.sidebar.expander("Owner Data Structure"):
            sample_owners = []
            for lead in all_leads[:5]:  # Check first 5 leads
                owner_data = lead.get('Owner', {})
                if owner_data:
                    sample_owners.append({
                        'name': owner_data.get('name'),
                        'email': owner_data.get('email'),
                        'id': owner_data.get('id')
                    })
            
            for i, owner in enumerate(sample_owners):
                st.write(f"Lead {i+1} Owner:")
                st.json(owner)
    
    # Sidebar filters
    st.sidebar.subheader("📂 Lead Sources")
    selected_sources = st.sidebar.multiselect(
        "Select sources to display:",
        target_sources,
        default=target_sources,
        help="Choose which lead sources to include in the dashboard"
    )
    
    # Lead owner filter
    st.sidebar.subheader("👤 Lead Owner")
    owners = st.session_state.crm.get_lead_owners(all_leads)
    selected_owner = st.sidebar.selectbox(
        "Filter by owner:",
        ["All"] + owners,
        help="Select a specific lead owner or 'All' to show leads from all owners"
    )
    
    # Lead status filter
    st.sidebar.subheader("📊 Lead Status")
    statuses = st.session_state.crm.get_lead_statuses(all_leads)
    selected_status = st.sidebar.selectbox(
        "Filter by status:",
        ["All"] + statuses,
        help="Select a specific lead status or 'All' to show leads with any status"
    )
    
    # Date filters
    st.sidebar.subheader("📅 Date Range Filter")
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    quarter_ago = today - timedelta(days=90)
    
    # Enhanced date range presets
    date_preset = st.sidebar.selectbox(
        "Quick date ranges:",
        ["Custom Range", "Today", "Yesterday", "Last 7 days", "Last 30 days", "Last 90 days", "This Month", "Last Month", "All time"],
        help="Select a predefined time range or choose 'Custom Range' for specific dates"
    )
    
    # Calculate date ranges based on selection
    if date_preset == "Today":
        start_date = end_date = today
    elif date_preset == "Yesterday":
        yesterday = today - timedelta(days=1)
        start_date = end_date = yesterday
    elif date_preset == "Last 7 days":
        start_date = week_ago
        end_date = today
    elif date_preset == "Last 30 days":
        start_date = month_ago
        end_date = today
    elif date_preset == "Last 90 days":
        start_date = quarter_ago
        end_date = today
    elif date_preset == "This Month":
        start_date = today.replace(day=1)
        end_date = today
    elif date_preset == "Last Month":
        # First day of last month
        first_day_this_month = today.replace(day=1)
        last_month = first_day_this_month - timedelta(days=1)
        start_date = last_month.replace(day=1)
        end_date = last_month
    elif date_preset == "All time":
        start_date = end_date = None
    else:  # Custom Range
        st.sidebar.markdown("**📅 Select Custom Date Range:**")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(
                "From Date", 
                value=week_ago,
                max_value=today,
                help="Select the start date for filtering"
            )
        with col2:
            end_date = st.date_input(
                "To Date", 
                value=today,
                max_value=today,
                help="Select the end date for filtering"
            )
        
        # Validate date range
        if start_date > end_date:
            st.sidebar.error("⚠️ Start date cannot be after end date!")
            start_date = end_date
    
    # Show selected date range
    if start_date and end_date:
        if start_date == end_date:
            st.sidebar.info(f"📅 Filtering for: **{start_date.strftime('%B %d, %Y')}**")
        else:
            st.sidebar.info(f"📅 Filtering from: **{start_date.strftime('%B %d, %Y')}** to **{end_date.strftime('%B %d, %Y')}**")
    elif start_date is None and end_date is None:
        st.sidebar.info("📅 Showing all dates")
    
    st.sidebar.markdown("---")
    
    # Apply filters
    filtered_leads = filter_leads(
        all_leads,
        lead_sources=selected_sources,
        lead_owner=selected_owner,
        lead_status=selected_status,
        start_date=start_date,
        end_date=end_date
    )
    
    # Show filter summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Filter Summary:**")
    st.sidebar.markdown(f"• **Total leads found:** {len(filtered_leads)}")
    st.sidebar.markdown(f"• **Date range:** {start_date} to {end_date}" if start_date and end_date else "• **Date range:** All time")
    st.sidebar.markdown(f"• **Lead owner:** {selected_owner}")
    st.sidebar.markdown(f"• **Lead status:** {selected_status}")
    st.sidebar.markdown(f"• **Sources:** {len(selected_sources)} selected")
    
    # Display metrics
    st.header("📈 Key Metrics")
    create_scoreboard(filtered_leads)
    
    # Display charts
    st.header("📊 Analytics")
    create_charts(filtered_leads)
    
    # Display table
    st.header("📋 Leads Details")
    
    # Show export option
    if filtered_leads:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Showing {len(filtered_leads)} leads")
        with col2:
            if st.button("📥 Export CSV"):
                # Prepare CSV data
                csv_data = []
                for lead in filtered_leads:
                    csv_data.append({
                        'Name': f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip(),
                        'Email': lead.get('Email', ''),
                        'Phone': lead.get('Phone', ''),
                        'Company': lead.get('Company', ''),
                        'Source': lead.get('Lead_Source', ''),
                        'Status': lead.get('Lead_Status', ''),
                        'Owner': lead.get('Owner', {}).get('name', ''),
                        'Created': lead.get('Created_Time', '')
                    })
                
                csv_df = pd.DataFrame(csv_data)
                csv = csv_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"leads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    create_leads_table(filtered_leads)
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tips:**")
    st.markdown("• Use the sidebar filters to customize your view")
    st.markdown("• Select date ranges to analyze trends over time") 
    st.markdown("• Export filtered data as CSV for further analysis")
    st.markdown(f"• Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()